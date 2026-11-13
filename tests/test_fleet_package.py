import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / 'skills/engineering/fleet-architecture'
PRESET = ROOT / 'skills/engineering/fleet-preset'


def load_evaluator(path):
    spec = importlib.util.spec_from_file_location('readiness', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReadinessTests(unittest.TestCase):
    def test_scenarios(self):
        evaluator = load_evaluator(CORE / 'scripts/readiness.py')
        cases = json.loads((CORE / 'evals/readiness-cases.json').read_text())
        self.assertGreaterEqual(len(cases), 17)
        for case in cases:
            with self.subTest(case=case['name']):
                result = evaluator.evaluate(case['record'])
                self.assertEqual(result['status'], case['expected_status'])
                self.assertEqual(bool(result['reasons']), result['status'] != 'ready')

    def test_missing_policy_is_invalid(self):
        evaluator = load_evaluator(CORE / 'scripts/readiness.py')
        record = json.loads((CORE / 'assets/readiness.example.json').read_text())
        del record['policy']
        with self.assertRaises(evaluator.InvalidRecord):
            evaluator.evaluate(record)

    def test_malformed_records_fail_closed(self):
        evaluator = load_evaluator(CORE / 'scripts/readiness.py')
        for record in (None, [], {}, {'revision': 'x'}, {'revision': True, 'action': 'merge', 'target': 'x'}):
            with self.subTest(record=record), self.assertRaises(evaluator.InvalidRecord):
                evaluator.evaluate(record)

    def test_malformed_revision_binding_is_invalid(self):
        evaluator = load_evaluator(CORE / 'scripts/readiness.py')
        for value in ('true', 'false', 1, 0, None):
            record = json.loads((CORE / 'assets/readiness.example.json').read_text())
            record['authorization']['revision_bound'] = value
            record['authorization']['revision'] = 'stale'
            with self.subTest(value=value), self.assertRaises(evaluator.InvalidRecord):
                evaluator.evaluate(record)

    def test_cli_invalid_json_is_not_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.json'
            path.write_text('{')
            result = subprocess.run([sys.executable, str(CORE / 'scripts/readiness.py'), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stderr)['status'], 'invalid')


class PackagingTests(unittest.TestCase):
    def test_manifest_parity_and_discovery(self):
        manifests = [json.loads((ROOT / prefix / 'plugin.json').read_text()) for prefix in ('.claude-plugin', '.cursor-plugin')]
        self.assertEqual(manifests[0]['version'], manifests[1]['version'])
        self.assertEqual(manifests[0]['skills'], manifests[1]['skills'])
        self.assertEqual(len(manifests[0]['skills']), len(set(manifests[0]['skills'])))
        expected = {str(path.parent.relative_to(ROOT)) for path in (ROOT / 'skills').glob('*/*/SKILL.md')}
        self.assertEqual({x.removeprefix('./') for x in manifests[0]['skills']}, expected)
        for relative in manifests[0]['skills']:
            text = (ROOT / relative / 'SKILL.md').read_text()
            self.assertTrue(text.startswith('---\nname: '))
            self.assertIn('\ndescription: ', text)

    def test_readme_uses_official_skills_badge(self):
        readme = (ROOT / 'README.md').read_text()
        self.assertIn('[![skills.sh](https://skills.sh/b/mitchellknoth/skills)](https://skills.sh/mitchellknoth/skills)', readme)

    def test_generated_core_is_current(self):
        subprocess.run([sys.executable, str(ROOT / 'scripts/sync-fleet-core.py'), '--check'], check=True, capture_output=True)

    def test_modes_remain_distinct_and_dormant(self):
        template = json.loads((CORE / 'assets/installation.template.json').read_text())
        preset = json.loads((PRESET / 'assets/preset.template.json').read_text())
        self.assertEqual(template['roles'], [])
        self.assertTrue(all(value is None for value in template['policy'].values()))
        self.assertEqual(preset['policy']['review_round_limit'], 3)
        for config in (template, preset):
            self.assertFalse(config['automations']['enabled'])
            self.assertFalse(config['activation']['live_actions_enabled'])
            self.assertIsNone(config['policy']['authorization_source'])

    def test_each_skill_standalone_links_and_execution(self):
        for source in (CORE, PRESET):
            with self.subTest(skill=source.name), tempfile.TemporaryDirectory() as directory:
                isolated = Path(directory) / source.name
                shutil.copytree(source, isolated, ignore=shutil.ignore_patterns('__pycache__'))
                for file in isolated.rglob('*.md'):
                    for link in re.findall(r'\]\(([^)]+)\)', file.read_text()):
                        if '://' in link or link.startswith('#'):
                            continue
                        target = (file.parent / link.split('#')[0]).resolve()
                        self.assertTrue(target.is_relative_to(isolated), f'escaping link {file}: {link}')
                        self.assertTrue(target.exists(), f'missing link {file}: {link}')
                result = subprocess.run([sys.executable, str(isolated / 'scripts/readiness.py'), str(isolated / 'assets/readiness.example.json')], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)['status'], 'ready')
                evaluator = load_evaluator(isolated / 'scripts/readiness.py')
                for case in json.loads((isolated / 'evals/readiness-cases.json').read_text()):
                    self.assertEqual(evaluator.evaluate(case['record'])['status'], case['expected_status'])


if __name__ == '__main__':
    unittest.main()
