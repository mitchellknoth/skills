"""Opt-in loopback OTLP/HTTP JSON sink; records counts, never raw attributes.

No external infrastructure, dependencies, auth, prompt text, account identity,
tool arguments/results, reasoning text, or raw spans are retained.
"""
from collections import Counter
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading

EVENTS=frozenset(('codex.conversation_starts','codex.api_request','codex.sse_event',
    'codex.user_prompt','codex.tool_decision','codex.tool_result','codex.turn_cost',
    'codex.sandbox_outcome','codex.startup_phase','codex.turn_ttft'))

def read_payload(headers, stream):
    """Bound both Content-Length and native async HTTP chunked payloads."""
    if headers.get('Transfer-Encoding','').lower()=='chunked':
        payload=bytearray()
        while True:
            line=stream.readline(100)
            if not line.endswith(b'\r\n'):raise ValueError('chunk_framing')
            size=int(line.split(b';',1)[0],16)
            if not 0<=size<=512000-len(payload):raise ValueError('payload_size')
            if size==0:
                if stream.readline(3)!=b'\r\n':raise ValueError('chunk_trailer')
                return bytes(payload)
            part=stream.read(size)
            if len(part)!=size or stream.read(2)!=b'\r\n':raise ValueError('chunk_framing')
            payload.extend(part)
    size=int(headers.get('Content-Length','0'))
    if not 0<size<=512000:raise ValueError('payload_size')
    payload=stream.read(size)
    if len(payload)!=size:raise ValueError('payload_size')
    return payload

class LocalTelemetry:
    def __init__(self):
        self.counts=Counter(); self.events=Counter(); self.rejected=0;self.rejection_categories=Counter()
        owner=self
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                category='transport_or_shape'
                try:
                    self.connection.settimeout(2)
                    if self.path not in ('/v1/logs','/v1/traces'):
                        category='route';raise ValueError()
                    category='payload'
                    payload=read_payload(self.headers,self.rfile)
                    category='json'
                    data=json.loads(payload)
                    category='shape'
                    owner.ingest(self.path,data)
                    self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers()
                    self.wfile.write(b'{}')
                except (ValueError,TypeError,KeyError,OSError):
                    owner.rejected+=1;owner.rejection_categories[category]+=1
                    try:self.send_error(400)
                    except OSError:pass
        self.server=HTTPServer(('127.0.0.1',0),Handler)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True)

    def ingest(self,path,data):
        if not isinstance(data,dict):raise ValueError()
        resource_key,scope_key,item_key=('resourceLogs','scopeLogs','logRecords') if path=='/v1/logs' else ('resourceSpans','scopeSpans','spans')
        def objects(parent,key):
            value=parent.get(key,[])
            if not isinstance(value,list) or any(not isinstance(x,dict) for x in value):raise ValueError()
            return value
        for resource in objects(data,resource_key):
            for scope in objects(resource,scope_key):
                for item in objects(scope,item_key):
                    self.counts[item_key]+=1
                    if item_key=='logRecords':
                        for attribute in objects(item,'attributes'):
                            if attribute.get('key')=='event.name':
                                value=attribute.get('value',{})
                                if not isinstance(value,dict):raise ValueError()
                                name=value.get('stringValue')
                                if not isinstance(name,str):name='other'
                                self.events[name if name in EVENTS else 'other']+=1

    @property
    def endpoint(self):return f'http://127.0.0.1:{self.server.server_port}'

    def __enter__(self):self.thread.start();return self
    def __exit__(self,*args):
        self.server.shutdown();self.thread.join(timeout=2);self.server.server_close()

    def summary(self):
        return {'source':'native-otlp-http-json','counts':dict(self.counts),
            'events':dict(self.events),'rejected_requests':self.rejected,
            'rejection_categories':dict(getattr(self,'rejection_categories',{})),
            'content_policy':'Counts and known event names only; logs and spans counted separately.'}
