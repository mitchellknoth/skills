import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / 'skills/engineering/fleet-architecture'
PRESET = ROOT / 'skills/engineering/fleet-preset'
TARGETS = {'claude_code', 'codex', 'cursor', 'dot'}


class PrimitiveMapTests(unittest.TestCase):
    def setUp(self):
        self.map = json.loads((CORE / 'assets/primitive-bindings.json').read_text())

    def test_every_primitive_has_invariants_and_a_grok_binding(self):
        ids = [p['id'] for p in self.map['primitives']]
        self.assertEqual(len(ids), len(set(ids)))
        for primitive in self.map['primitives']:
            with self.subTest(primitive=primitive['id']):
                self.assertTrue(primitive['invariants'])
                self.assertTrue(primitive['guarantee_lost_if_emulated'])
                self.assertTrue(primitive['grok']['mechanism'])
                self.assertEqual(set(primitive['targets']), TARGETS)

    def test_unverified_targets_say_how_to_verify_and_invent_no_mapping(self):
        vocabulary = set(self.map['status_vocabulary'])
        for primitive in self.map['primitives']:
            for target, entry in primitive['targets'].items():
                with self.subTest(primitive=primitive['id'], target=target):
                    self.assertIn(entry['status'], vocabulary)
                    self.assertTrue(entry['todo'])
                    if entry['status'] == 'unknown':
                        self.assertIsNone(entry['mapping'])
                    else:
                        self.assertTrue(entry['evidence'])

    def test_functions_are_known_and_persona_catalog_binds_one_each(self):
        functions = set(self.map['functions'])
        for primitive in self.map['primitives']:
            self.assertTrue(set(primitive['used_by_functions']) <= functions | {'all'})
        catalog = json.loads((PRESET / 'assets/persona-catalog.json').read_text())
        for persona in catalog['personas']:
            self.assertIn(persona['function'], functions)

    def test_preset_bundles_identical_core_files(self):
        for name in ('functions.md', 'protocols.md', 'practices.md', 'field-evidence.md', 'primitives.md'):
            self.assertEqual((CORE / 'references' / name).read_bytes().replace(b'](../assets/', b'](../../assets/'),
                             (PRESET / 'references/core' / name).read_bytes())

    def test_core_functions_and_protocols_name_no_provider(self):
        for name in ('functions.md', 'protocols.md', 'practices.md'):
            text = (CORE / 'references' / name).read_text().lower()
            for provider in ('grok', 'claude', 'codex', 'cursor'):
                self.assertNotIn(provider, text, f'{name} names {provider}')


if __name__ == '__main__':
    unittest.main()
