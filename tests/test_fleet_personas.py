import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / 'skills/engineering/fleet-architecture'
PRESET = ROOT / 'skills/engineering/fleet-preset'


class PersonaPackagingTests(unittest.TestCase):
    def test_neutral_persona_does_not_select_preset_policy(self):
        record = json.loads((CORE / 'assets/persona.template.json').read_text())
        self.assertIsNone(record['purpose'])
        for field in ('decision_lens', 'boundaries', 'behavioral_lessons', 'skill_bindings', 'routine_bindings', 'source_records', 'unresolved_conflicts'):
            self.assertEqual(record[field], [])
        self.assertIsNone(record['private_context_ref'])

    def test_customer_discovery_starts_unknown_and_inactive(self):
        profile = json.loads((CORE / 'assets/customer-profile.template.json').read_text())
        self.assertEqual(profile['mode'], 'design')
        self.assertFalse(profile['activation']['enabled'])
        self.assertTrue(all(value == 'unknown' for value in profile['capabilities'].values()))
        self.assertIsNone(profile['policy']['authorization_source'])
        self.assertIsNone(profile['harness']['name'])
        self.assertEqual(profile['recommendations'], [])

    def test_catalog_has_provenance_and_real_role_files(self):
        catalog = json.loads((PRESET / 'assets/persona-catalog.json').read_text())
        ids = [item['id'] for item in catalog['personas']]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 15)
        for item in catalog['personas']:
            self.assertIn(item['status'], ('active', 'historical', 'installation-specific', 'ownership-folded-configuration-drift'))
            self.assertTrue((PRESET / item['path']).is_file())
            self.assertIn(item['coverage']['memory'], ('read', 'partial', 'not-inspected', 'self-reported'))
            self.assertIn(item['coverage']['skills'], ('read', 'partial', 'not-inspected', 'reported-inventory'))
            self.assertTrue(item['limitations'])
            if item['coverage']['memory'] == 'self-reported':
                self.assertTrue(any('report' in source or 'interview' in source for source in item['source_categories']))

if __name__ == '__main__':
    unittest.main()
