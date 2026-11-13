import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / 'skills/engineering/fleet-architecture'
PRESET = ROOT / 'skills/engineering/fleet-preset'


def evaluator(path):
    spec = importlib.util.spec_from_file_location('feedback', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FeedbackTests(unittest.TestCase):
    def test_synthetic_cases(self):
        model = evaluator(CORE / 'scripts/feedback.py')
        for case in json.loads((CORE / 'evals/feedback-cases.json').read_text()):
            with self.subTest(case=case['name']):
                result = model.classify(case['record'])
                self.assertEqual(result['status'], case['expected_status'])
                self.assertEqual(result['proposal_status'], case['expected_proposal'])
                self.assertEqual(len(result['followups']), case['expected_followups'])

    def test_idle_scoring_and_invented_effectiveness_invalid(self):
        model = evaluator(CORE / 'scripts/feedback.py')
        base = json.loads((CORE / 'assets/feedback.example.json').read_text())
        base['scores'] = [{'worked': False, 'grade': 'miss'}]
        with self.assertRaises(model.InvalidRecord):
            model.classify(base)
        base['scores'] = []
        base['advice'] = [{'id': 'A1', 'status': 'verified'}]
        with self.assertRaises(model.InvalidRecord):
            model.classify(base)

    def test_nonstring_evidence_references_are_invalid(self):
        model = evaluator(CORE / 'scripts/feedback.py')
        for value in (True, 1, 0, {}, [], '', '   '):
            for field in ('artifact', 'advice', 'proposal'):
                record = json.loads((CORE / 'assets/feedback.example.json').read_text())
                if field == 'artifact':
                    record['artifact']['reference'] = value
                elif field == 'advice':
                    record['advice'] = [{'id': 'A1', 'status': 'verified', 'outcome_evidence': value}]
                else:
                    record['proposal'] = {'confirmed': True, 'confirmation_source': value}
                with self.subTest(field=field, value=value), self.assertRaises(model.InvalidRecord):
                    model.classify(record)

    def test_template_configurable_preset_distinct(self):
        neutral = json.loads((CORE / 'assets/installation.template.json').read_text())
        preset = json.loads((PRESET / 'assets/preset.template.json').read_text())
        self.assertEqual(neutral['feedback']['loops'], [])
        self.assertIsNone(neutral['feedback']['confirmation_policy'])
        self.assertEqual(preset['feedback']['max_weekly_proposals'], 3)
        self.assertEqual(preset['feedback']['lesson_persistence_weeks'], 2)
        loops = {item['kind'] for item in preset['feedback']['loops']}
        self.assertTrue({'fleet_retro', 'coordinator_calibration', 'harness_hygiene', 'post_prune_regression'}.issubset(loops))
        self.assertFalse(preset['automations']['enabled'])

    def test_standalone_feedback(self):
        for source in (CORE, PRESET):
            with self.subTest(skill=source.name), tempfile.TemporaryDirectory() as directory:
                dest = Path(directory) / source.name
                shutil.copytree(source, dest, ignore=shutil.ignore_patterns('__pycache__'))
                result = subprocess.run([sys.executable, str(dest / 'scripts/feedback.py'), str(dest / 'assets/feedback.example.json')], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)['status'], 'recorded')


if __name__ == '__main__':
    unittest.main()
