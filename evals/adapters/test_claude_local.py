import json
import unittest
from unittest.mock import patch
import claude_local as adapter

class AdapterTests(unittest.TestCase):
    request = {'protocol': 1, 'role': 'judge', 'model': 'claude-sonnet-4-6', 'prompt': 'Test'}
    env = {'FLEET_EVAL_ALLOW_REMOTE': '1', 'HOME': '/fake', 'PATH': '/fake',
           'ANTHROPIC_API_KEY': 'secret', 'ANTHROPIC_BASE_URL': 'https://evil', 'NODE_OPTIONS': 'evil'}

    def test_no_opt_in_no_process(self):
        with patch.object(adapter, 'invoke') as invoke:
            with self.assertRaises(adapter.AdapterError): adapter.run(self.request, {})
            invoke.assert_not_called()

    def test_environment_excludes_secret_and_injection(self):
        self.assertEqual(adapter.clean_env(self.env), {'HOME': '/fake', 'PATH': '/fake'})

    def exercise(self, auth=None, result=None, help_text=None):
        outputs = ['2.1.300 (Claude Code)\n', ' '.join(adapter.REQUIRED_FLAGS) if help_text is None else help_text,
                   json.dumps(auth or {'authMethod': 'claude.ai'}),
                   json.dumps(result or {'subtype': 'success', 'result': 'OK',
                             'modelUsage': {self.request['model']: {}},
                             'usage': {'input_tokens': 10, 'output_tokens': 2}})]
        with patch.object(adapter.shutil, 'which', return_value='/fake/claude'), patch.object(adapter, 'invoke', side_effect=outputs) as invoke:
            answer = adapter.run(self.request, self.env)
            return answer, invoke.call_args_list

    def test_success_is_toolless_and_stdin(self):
        answer, calls = self.exercise()
        self.assertEqual(answer['text'], 'OK')
        self.assertEqual(answer['metadata'], {'cli_version': '2.1.300',
                         'model': self.request['model'], 'auth_method': 'claude.ai'})
        argv = calls[-1].args[0]
        self.assertEqual(argv[argv.index('--tools') + 1], '')
        self.assertEqual(argv[argv.index('--disallowedTools') + 1], '*')
        self.assertNotIn('Test', argv)
        self.assertEqual(calls[-1].kwargs['input'], 'Test')
        self.assertNotIn('ANTHROPIC_API_KEY', calls[-1].kwargs['env'])

    def test_api_auth_rejected(self):
        with self.assertRaises(adapter.AdapterError): self.exercise(auth={'authMethod': 'api_key'})

    def test_missing_safety_flag_rejected(self):
        with self.assertRaises(adapter.AdapterError): self.exercise(help_text='--tools')

    def test_fallback_model_rejected(self):
        with self.assertRaises(adapter.AdapterError):
            self.exercise(result={'subtype': 'success', 'result': 'OK', 'modelUsage': {'other': {}}})

    def test_error_result_rejected(self):
        with self.assertRaises(adapter.AdapterError): self.exercise(result={'is_error': True})

    def test_alias_rejected(self):
        with self.assertRaises(adapter.AdapterError): adapter.run({**self.request, 'model': 'sonnet'}, self.env)

if __name__ == '__main__': unittest.main()
