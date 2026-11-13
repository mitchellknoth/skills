"""Offline integration-contract tests; no Harbor, Docker or provider call needed."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from evals.harbor.export import export
from evals.harbor.transport import execute
from evals import run


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name)/'bundle'
        self.config = json.loads((run.ROOT/'evals/local.example.json').read_text())
        self.config['model'] = 'pinned-test-model'
        self.commands = export(self.config, self.out)
        self.bundle = self.out/'host-bundle.json'
        self.task = sorted((self.out/'tasks').iterdir())[0]
        self.instruction = (self.task/'instruction.md').read_text()

    def verifier(self):
        with patch.dict(sys.modules, {'run': run}):
            spec = importlib.util.spec_from_file_location('fleet_verify', Path(__file__).with_name('verify.py'))
            module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        return module.verify

    def test_export_is_paired_and_separate(self):
        self.assertEqual(len(self.commands), 6)
        self.assertIn('environment_mode = "separate"', (self.task/'task.toml').read_text())
        self.assertNotIn('expected', self.instruction)
        self.assertTrue(all('mock=true' in c for c in self.commands))

    def test_mock_never_earns_behavioral_reward(self):
        answer = execute(self.bundle, self.instruction, mock=True)
        result = self.verifier()(json.loads((self.task/'tests/case.json').read_text()),
                                 json.loads((self.task/'tests/expected.json').read_text()), answer)
        self.assertTrue(result['passed']); self.assertEqual(result['reward'], 0)

    def test_no_implicit_inference(self):
        with patch.object(run, 'invoke') as call:
            with self.assertRaises(ValueError): execute(self.bundle, self.instruction)
            call.assert_not_called()

    def test_wrong_bundle_rejected(self):
        with self.assertRaises(ValueError): execute(self.bundle, '{"bundle_id":"wrong","trial_index":0}', mock=True)

    def test_live_adapter_contract_mocked(self):
        data = json.loads(self.bundle.read_text())
        case = next(c for c in data['cases'] if c['id']==data['manifest']['order'][0]['case'])
        replies = [{'text':json.dumps({'decisions':s['expected'],'rationale':'Evidence.'})} for s in case['steps']]
        with patch.object(run, 'invoke', side_effect=replies) as call:
            answer = execute(self.bundle,self.instruction,allow_inference=True)
        self.assertEqual(call.call_count, len(case['steps']))
        result = self.verifier()(case,json.loads((self.task/'tests/expected.json').read_text()),answer)
        self.assertEqual(result['reward'],1)
        answer['outputs']=[]
        self.assertEqual(self.verifier()(case,json.loads((self.task/'tests/expected.json').read_text()),answer)['reward'],0)

    def test_adapter_command_drift_rejected(self):
        data = json.loads(self.bundle.read_text()); data['adapter_argv'] = ['evil-command']
        self.bundle.write_text(json.dumps(data))
        with patch.object(run, 'invoke') as call:
            with self.assertRaisesRegex(ValueError, 'Adapter command'):
                execute(self.bundle, self.instruction, allow_inference=True)
            call.assert_not_called()

    def test_cases_tamper_rejected_even_with_recomputed_unbound_digest(self):
        data = json.loads(self.bundle.read_text()); data['cases'][0]['purpose'] = 'changed'
        data['cases_digest'] = run.digest(run.encode(data['cases']))
        self.bundle.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'Cases changed'):
            execute(self.bundle, self.instruction, mock=True)

    def test_selected_context_matches_local_runner(self):
        data = json.loads(self.bundle.read_text())
        index = next(i for i,t in enumerate(data['manifest']['order']) if t['variant']=='candidate')
        trial = data['manifest']['order'][index]
        case = next(c for c in data['cases'] if c['id']==trial['case'])
        instruction = json.dumps({'bundle_id':data['manifest']['id'], 'trial_index':index})
        replies = [{'text':json.dumps({'decisions':s['expected'],'rationale':'Evidence.'})} for s in case['steps']]
        with patch.object(run, 'invoke', side_effect=replies) as call:
            execute(self.bundle,instruction,allow_inference=True)
        selected = run.select_context(data['snapshots']['candidate'], self.config['context_files']['candidate'][case['id']])
        self.assertEqual(call.call_args_list[0].args[1]['prompt'],run.prompt_for(case,0,selected,[]))


if __name__ == '__main__': unittest.main()
