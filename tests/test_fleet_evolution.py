"""Package-contract checks only; these do not test live agent learning."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills/engineering'


class EvolutionContractTests(unittest.TestCase):
    def test_improvement_template_is_inert_in_both_packages(self):
        for name in ('fleet-architecture', 'fleet-preset'):
            with self.subTest(skill=name):
                record = json.loads((SKILLS / name / 'assets/improvement.template.json').read_text())
                self.assertEqual(record['status'], 'draft')
                self.assertEqual(record['trial']['status'], 'not_started')
                self.assertIsNone(record['trial']['authorization_reference'])
                self.assertIsNone(record['trial']['policy_check_reference'])
                self.assertEqual(record['outcome']['classification'], 'inconclusive')
                self.assertEqual(record['outcome']['sample_count'], 0)
                self.assertEqual(record['disposition']['decision'], 'unresolved')
                self.assertIsNone(record['disposition']['implementation_reference'])

    def test_record_preserves_traceability_and_disconfirmation(self):
        record = json.loads((SKILLS / 'fleet-architecture/assets/improvement.template.json').read_text())
        self.assertIn('fix_ledger_reference', record)
        self.assertTrue({'source_references', 'source_kind', 'coverage_gaps', 'configuration_version'} <= record['observation'].keys())
        self.assertTrue({'scope', 'counterexamples', 'disconfirming_evidence_to_seek', 'supersedes_reference'} <= record['lesson'].keys())
        self.assertIn('existing_purpose_or_protection', record['proposal'])
        self.assertTrue({'baseline_references', 'minimum_sample', 'observation_window', 'acceptance_criteria', 'regression_checks', 'rollback_condition', 'rollback_version'} <= record['trial'].keys())
        self.assertTrue({'comparability_notes', 'confounders', 'protected_behavior_results', 'coverage_gaps'} <= record['outcome'].keys())
        self.assertIn('next_checkpoint', record['disposition'])

    def test_generated_contract_and_record_match(self):
        core = SKILLS / 'fleet-architecture'
        preset = SKILLS / 'fleet-preset'
        self.assertEqual((core / 'assets/improvement.template.json').read_bytes(), (preset / 'assets/improvement.template.json').read_bytes())
        expected = (core / 'references/evolution.md').read_text().replace('](../assets/', '](../../assets/')
        self.assertEqual(expected, (preset / 'references/core/evolution.md').read_text())


if __name__ == '__main__':
    unittest.main()
