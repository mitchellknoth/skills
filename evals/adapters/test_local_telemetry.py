import json
import unittest
from local_telemetry import LocalTelemetry, read_payload
from io import BytesIO

class TelemetryTests(unittest.TestCase):
    def test_native_async_chunked_json_and_size_limits(self):
        self.assertEqual(b'{"x":1}',read_payload({'Transfer-Encoding':'chunked'},BytesIO(b'7\r\n{"x":1}\r\n0\r\n\r\n')))
        self.assertEqual(b'{}',read_payload({'Content-Length':'2'},BytesIO(b'{}')))
        for headers,payload in (({'Content-Length':'512001'},b''),({'Content-Length':'4'},b'{}'),
            ({'Transfer-Encoding':'chunked'},b'fffffff\r\n'),({'Transfer-Encoding':'chunked'},b'2\r\n{}bad')):
            with self.subTest(headers=headers,payload=payload),self.assertRaises(ValueError):read_payload(headers,BytesIO(payload))
    def test_sensitive_attributes_and_span_names_are_not_retained(self):
        # No socket required for offline CI.
        sink=LocalTelemetry.__new__(LocalTelemetry)
        from collections import Counter
        sink.counts=Counter();sink.events=Counter();sink.rejected=0
        sink.ingest('/v1/logs',{'resourceLogs':[{'resource':{'secret':'account'},'scopeLogs':[{
            'logRecords':[{'body':{'stringValue':'secret prompt'},'attributes':[
                {'key':'event.name','value':{'stringValue':'codex.tool_result'}},
                {'key':'output','value':{'stringValue':'private-token'}}]}]}]}]})
        sink.ingest('/v1/traces',{'resourceSpans':[{'scopeSpans':[{'spans':[{'name':'secret span','traceId':'private-id'}]}]}]})
        summary=sink.summary()
        self.assertEqual({'logRecords':1,'spans':1},summary['counts'])
        self.assertNotIn('secret',json.dumps(summary));self.assertNotIn('private',json.dumps(summary))
    def test_unknown_event_names_not_retained(self):
        sink=LocalTelemetry.__new__(LocalTelemetry)
        from collections import Counter
        sink.counts=Counter();sink.events=Counter();sink.rejected=0
        sink.ingest('/v1/logs',{'resourceLogs':[{'scopeLogs':[{'logRecords':[{'attributes':[
            {'key':'event.name','value':{'stringValue':'private-name'}}]}]}]}]})
        self.assertEqual({'other':1},sink.summary()['events'])

if __name__=='__main__':unittest.main()
