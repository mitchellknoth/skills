"""Offline privacy and negative controls for the installed-CLI request probe."""
import json
import unittest

import probe_codex as probe


class ProbeTests(unittest.TestCase):
    def test_allowlist_excludes_synthetic_prompt_credentials_and_tool_arguments(self):
        summary = probe.request_summary({'model': probe.MODEL, 'tools': [{
            'type': 'function', 'name': 'unexpected_tool', 'arguments': 'synthetic-secret'}],
            'input': 'synthetic-secret', 'headers': {'Authorization': 'synthetic-secret'}}, False)
        self.assertEqual(1, summary['tool_count'])
        self.assertEqual(['unexpected_tool'], summary['tool_names'])
        self.assertNotIn('synthetic-secret', json.dumps(summary))

    def test_positive_shape_and_auth_model_negative_controls(self):
        summary = probe.request_summary({'model': probe.MODEL, 'tools': []}, False)
        self.assertEqual(0, summary['tool_count'])
        self.assertTrue(summary['requested_model_matches'])
        self.assertFalse(summary['authorization_header_present'])
        negative = probe.request_summary({'model': 'wrong-model', 'tools': []}, True)
        self.assertFalse(negative['requested_model_matches'])
        self.assertTrue(negative['authorization_header_present'])

    def test_malformed_and_untrusted_tool_names(self):
        for value in (None, {}, {'tools': None}, {'tools': [None]}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                probe.request_summary(value, False)
        result = probe.request_summary({'model': probe.MODEL, 'tools': [{
            'type': 'function', 'name': 'synthetic-secret\n/private/path'}]}, False)
        self.assertEqual(['unsupported-name'], result['tool_names'])
        self.assertNotIn('synthetic-secret', json.dumps(result))


if __name__ == '__main__':
    unittest.main()
