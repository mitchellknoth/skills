"""Synthetic tests: never invoke a provider or read credentials."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import codex_local as c


class CodexTests(unittest.TestCase):
    def event(self, kind, **kw):
        return json.dumps(dict(type=kind, **kw))

    def stream(self, extra=()):
        return '\n'.join([self.event('thread.started', thread_id='private-id'),
            self.event('turn.started'), *extra,
            self.event('item.completed', item={'id':'a','type':'agent_message','text':'{"decisions":{},"rationale":"ok"}'}),
            self.event('turn.completed', usage={'input_tokens':4,'output_tokens':2})])

    def test_complete_native_events_and_usage(self):
        result=c.parse_events(self.stream())
        self.assertEqual(4,result['usage']['input_tokens'])
        self.assertEqual(0,result['trace']['tool_events'])
        self.assertNotIn('private-id',json.dumps(result['trace']))

    def test_reasoning_content_not_retained(self):
        result=c.parse_events(self.stream([self.event('item.completed',item={
            'id':'r','type':'reasoning','text':'synthetic-secret abc@example.com'})]))
        self.assertNotIn('synthetic-secret',json.dumps(result))
        self.assertEqual(1,result['trace']['reasoning_summary_events'])

    def test_tool_attempts_invalidate_even_when_answer_is_correct(self):
        for kind in ('command_execution','file_change','mcp_tool_call','web_search','collab_tool_call','unknown_future_tool'):
            with self.subTest(kind=kind),self.assertRaises(c.AdapterError):
                c.parse_events(self.stream([self.event('item.started',item={'id':'t','type':kind,'command':'private'})]))

    def test_incomplete_failed_and_malformed_fail_closed(self):
        for stream in ('{}','null','not JSON',self.event('turn.completed',usage={}),
                       self.stream()+ '\n'+self.event('turn.failed',error={'message':'private'})):
            with self.subTest(stream=stream),self.assertRaises(c.AdapterError):c.parse_events(stream)

    def test_native_auth_and_no_environment_billing_fallback(self):
        env=c.clean_env({'HOME':'/native','PATH':'/bin','OPENAI_API_KEY':'secret',
            'CODEX_HOME':'/other','OPENAI_BASE_URL':'https://other','NODE_OPTIONS':'bad'})
        self.assertEqual({'HOME':'/native','PATH':'/bin'},env)
        with self.assertRaises(c.AdapterError):c.validate_request({'protocol':1,'role':'judge','model':'other','prompt':'x'})
        with self.assertRaises(c.AdapterError):c.run({'protocol':1,'role':'agent','model':'gpt-6-luna','prompt':'x'},source={})

    def test_command_removes_tools_before_observation(self):
        argv=c.command('/codex','gpt-6-luna',Path('/tmp/work'),{'one':'stdio'})
        for flag in ('--ignore-user-config','--strict-config','--ephemeral','--json','read-only'):
            self.assertIn(flag,argv)
        self.assertIn('mcp_servers.one.enabled=false',argv)
        self.assertIn('forced_login_method="chatgpt"',argv)
        catalog=c.catalog('gpt-6-luna')['models'][0]
        self.assertIsNone(catalog['apply_patch_tool_type'])
        self.assertEqual('disabled',catalog['shell_type'])
        self.assertEqual([],catalog['experimental_supported_tools'])
        sink=type('Sink',(),{'endpoint':'http://127.0.0.1:1234'})()
        logged=c.command('/codex','gpt-6-luna',Path('/tmp/work'),{},sink)
        self.assertIn('otel.trace_exporter="none"',logged)
        self.assertTrue(any(x.startswith('otel.exporter={') for x in logged))

    def test_mcp_preflight_disables_every_configured_server(self):
        with patch.object(c,'call',return_value=json.dumps([{'name':'one','transport':{'type':'stdio'}},{'name':'two','transport':{'type':'streamable_http'}}])):
            self.assertEqual({'one':'stdio','two':'streamable_http'},c.mcp_names('/codex',{},'/tmp'))
        for payload in ('null','{}','[{"name":"bad.name"}]'):
            with patch.object(c,'call',return_value=payload), self.assertRaises(c.AdapterError):c.mcp_names('/codex',{},'/tmp')

if __name__=='__main__':unittest.main()
