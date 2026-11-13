"""Offline runner tests. No model calls, credentials or external network."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('fleet_eval',ROOT/'evals/run.py')
eval=importlib.util.module_from_spec(spec); spec.loader.exec_module(eval)

class EvalTests(unittest.TestCase):
    def config(self): return json.loads((ROOT/'evals/local.example.json').read_text())
    def test_plan_pairs_every_case_and_counts_learning(self):
        manifest,_,cases=eval.plan(self.config())
        self.assertEqual(8,manifest['calls'])
        for case in cases:
            self.assertEqual({'baseline','candidate'},{t['variant'] for t in manifest['order'] if t['case']==case['id']})
    def test_budget_refuses_extra_judge_calls(self):
        c=self.config(); c['judge_model']='explicit-model'
        with self.assertRaises(ValueError): eval.plan(c)
        c['max_calls']=14
        self.assertEqual(14,eval.plan(c)[0]['calls'])
    def test_api_requires_explicit_conservative_budget(self):
        c=self.config(); c['billing']='api'
        with self.assertRaises(ValueError): eval.plan(c)
        c.update(estimated_usd_per_call=.1,max_estimated_usd=.8)
        self.assertAlmostEqual(.8,eval.plan(c)[0]['estimated_usd'])
    def test_mock_is_never_efficacy_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            summary=eval.run(self.config(),Path(temp)/'run',mock=True)
            self.assertEqual('plumbing_only',summary['verdict'])
            self.assertEqual(6,summary['completed'])
    def test_live_requires_optin_before_creating_output(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'run'
            with self.assertRaises(ValueError): eval.run(self.config(),p)
            self.assertFalse(p.exists())
    def test_missing_steps_fail_closed(self):
        case=eval.load_cases()[2]
        self.assertFalse(eval.grade(case,[])['passed'])
        self.assertFalse(eval.grade(case,[{'decisions':case['steps'][0]['expected']}])['complete'])
    def test_blanket_refusal_fails_positive_controls(self):
        case=eval.load_cases()[0]
        self.assertFalse(eval.grade(case,[{'decisions':{'A':'hold','B':'hold','C':'hold'}}])['passed'])
    def test_changed_skill_changes_snapshot_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp); (p/'SKILL.md').write_text('first')
            a=eval.snapshot(p)['sha256']; (p/'SKILL.md').write_text('second')
            self.assertNotEqual(a,eval.snapshot(p)['sha256'])
    def test_symlinks_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp); (p/'SKILL.md').symlink_to(ROOT/'README.md')
            with self.assertRaises(ValueError): eval.snapshot(p)
    def test_expected_answers_not_in_prompt(self):
        case=eval.load_cases()[0]
        prompt=eval.prompt_for(case,0,{'text':''},[])
        self.assertNotIn('"expected"',prompt)
    def test_safety_regression_blocks_overall(self):
        manifest,_,_=eval.plan(self.config())
        records=[{'variant':'baseline','case':'readiness','repeat':0,'grade':{'passed':True}}, {'variant':'candidate','case':'readiness','repeat':0,'grade':{'passed':False}}]
        report=eval.summarize(manifest,records,False)
        self.assertEqual('blocked',report['verdict'])
        self.assertEqual(1,len(report['candidate_regressions']))
    def test_env_does_not_inherit_api_keys(self):
        with patch.dict('os.environ',{'ANTHROPIC_API_KEY':'secret','OPENAI_API_KEY':'secret'}):
            self.assertNotIn('ANTHROPIC_API_KEY',eval.safe_env())
    def test_selected_context_is_exact_and_fail_closed(self):
        skill={'files':{'SKILL.md':'a','references/x.md':'b','secret.md':'excluded'}}
        context=eval.select_context(skill,['SKILL.md','references/x.md'])
        self.assertEqual({'SKILL.md','references/x.md'},set(context['files']))
        self.assertNotIn('excluded',context['text'])
        with self.assertRaises(ValueError): eval.select_context(skill,['SKILL.md','references/missing.md'])
        with self.assertRaises(ValueError): eval.select_context(skill,['references/x.md'])
    def test_malformed_decisions_fail_without_crashing(self):
        self.assertFalse(eval.grade(eval.load_cases()[0],[{'decisions':None}])['passed'])
    def test_real_subprocess_protocol_offline(self):
        c=self.config()
        result=eval.invoke([__import__('sys').executable,'-c',
            'import json,sys; x=json.load(sys.stdin); print(json.dumps({"text":x["prompt"]}))'],
            {'prompt':'offline'},c)
        self.assertEqual('offline',result['text'])
    def test_transport_error_does_not_echo_stderr(self):
        with self.assertRaises(RuntimeError) as caught:
            eval.invoke([__import__('sys').executable,'-c',
                'import sys; print("private detail",file=sys.stderr); sys.exit(3)'],{'prompt':'x'},self.config())
        self.assertNotIn('private',str(caught.exception))
    def test_all_pass_still_not_proven(self):
        manifest,_,_=eval.plan(self.config())
        records=[dict(t,grade={'passed':True}) for t in manifest['order']]
        self.assertEqual('inconclusive',eval.summarize(manifest,records,False)['verdict'])
    def test_malformed_transport_envelope_fails_closed(self):
        for payload in ('[]','null','42'):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                eval.invoke([__import__('sys').executable,'-c',f'print({payload!r})'], {'prompt':'x'},self.config())
    def test_malformed_optional_usage_and_trace_fail_closed(self):
        for extra in ({'usage':'bad'},{'usage':{'input_tokens':'bad'}},{'trace':{}},{'trace':{'tool_events':-1}}):
            payload=json.dumps(dict(text='{}',**extra))
            with self.subTest(extra=extra),self.assertRaises(ValueError):
                eval.invoke([__import__('sys').executable,'-c',f'print({payload!r})'],{'prompt':'x'},self.config())
    def test_cli_blocked_result_exits_nonzero(self):
        with patch('sys.argv',['run.py','mock']), patch.object(eval,'run',return_value={'verdict':'blocked'}):
            with self.assertRaises(SystemExit) as caught: eval.main()
            self.assertEqual(1,caught.exception.code)
    def test_baseline_failure_with_passing_candidate_is_not_blocker(self):
        manifest,_,_=eval.plan(self.config())
        records=[dict(t,grade={'passed':t['variant']=='candidate','complete':True}) for t in manifest['order']]
        summary=eval.summarize(manifest,records,False)
        self.assertEqual('inconclusive',summary['verdict'])
        self.assertEqual(3,len(summary['candidate_improvements']))
    def test_baseline_transport_failure_is_not_improvement(self):
        manifest,_,_=eval.plan(self.config())
        records=[dict(t,grade={'passed':t['variant']=='candidate','complete':t['variant']=='candidate'}) for t in manifest['order']]
        summary=eval.summarize(manifest,records,False)
        self.assertEqual('blocked',summary['verdict'])
        self.assertEqual([],summary['candidate_improvements'])
    def test_plan_is_reproducible(self):
        self.assertEqual(eval.plan(self.config())[0],eval.plan(self.config())[0])
    def test_missing_traces_are_unknown_not_zero(self):
        c=self.config();c.update(model='explicit',trace_native_events=True)
        with tempfile.TemporaryDirectory() as temp,patch.object(eval,'invoke',return_value={'text':'{"decisions":{},"rationale":"synthetic"}','usage':None}):
            summary=eval.run(c,Path(temp)/'run',allow=True)
            self.assertIsNone(summary['observed_tool_events'])
            self.assertEqual(0,summary['trace_reporting_calls'])
    def test_saved_judging_is_explicit_bounded_and_journaled(self):
        c=self.config();c.update(judge_model='explicit',max_calls=14)
        with tempfile.TemporaryDirectory() as temp:
            source=Path(temp)/'source';eval.run(c,source,mock=True)
            with self.assertRaises(ValueError):eval.judge_saved(source,Path(temp)/'no-spend','learning')
            with patch.object(eval,'invoke',return_value={'text':'{"winner":"tie","reason":"synthetic"}','usage':None}) as invoke:
                result=eval.judge_saved(source,Path(temp)/'judge','learning',True)
                self.assertEqual(2,invoke.call_count)
                self.assertTrue(all(call.args[1]['role']=='judge' for call in invoke.call_args_list))
            self.assertTrue(result['position_agreement'])
            self.assertEqual(2,len(json.loads((Path(temp)/'judge/judgments.json').read_text())))
            records=json.loads((source/'trials.json').read_text());records[0]['outputs']=[]
            (source/'trials.json').write_text(json.dumps(records))
            # Reject missing step on the requested pair, independently of old grade fields.
            cid=records[0]['case']
            with self.assertRaises(ValueError):eval.judge_saved(source,Path(temp)/'invalid',cid,True)

if __name__=='__main__': unittest.main()
