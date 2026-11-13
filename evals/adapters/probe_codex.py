#!/usr/bin/env python3
"""Inspect installed Codex's model request against a synthetic loopback provider.

No model inference or billing. All model requests go to an unauthenticated
fixture, never through a credential proxy. Native HOME is preserved to exercise
the same configuration: Codex may still fetch first-party bootstrap metadata.
Raw requests, headers, native stderr and response content are never persisted.
"""
import argparse
from contextlib import nullcontext
from collections import Counter
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import threading

from codex_local import AdapterError, VERSION, call, catalog, clean_env, command, mcp_names, parse_events
from local_telemetry import LocalTelemetry, read_payload

MODEL = 'gpt-6-luna'
MAX_REQUEST_BYTES = 256_000
AUTH_HEADERS = ('Authorization', 'Cookie', 'X-API-Key', 'API-Key', 'ChatGPT-Account-ID')


def request_summary(body, authorization_present):
    """Allowlist structural fields; no text, arguments, credentials or paths."""
    if not isinstance(body, dict) or not isinstance(body.get('tools'), list):
        raise ValueError('Unsupported request shape.')
    names = []
    for tool in body['tools']:
        if not isinstance(tool, dict):
            raise ValueError('Unsupported tool shape.')
        name = tool.get('name', tool.get('type', 'unknown'))
        names.append(name if isinstance(name, str) and re.fullmatch(r'[A-Za-z0-9_.-]{1,128}', name)
                     else 'unsupported-name')
    return {'requested_model_matches': body.get('model') == MODEL,
            'authorization_header_present': bool(authorization_present),
            'tool_count': len(body['tools']), 'tool_names': sorted(names)}


def fixture_response():
    answer = json.dumps({'decisions': {'probe': 'complete'}, 'rationale': 'Synthetic fixture; no inference.'})
    item = {'id': 'fixture-message', 'type': 'message', 'role': 'assistant',
            'status': 'completed', 'content': [{'type': 'output_text', 'text': answer, 'annotations': []}]}
    response = {'id': 'fixture-response', 'object': 'response', 'status': 'completed',
                'model': MODEL, 'output': [item],
                'usage': {'input_tokens': 0, 'output_tokens': 0, 'total_tokens': 0}}
    events = [('response.created', {'type': 'response.created', 'response': dict(response, status='in_progress', output=[])}),
              ('response.output_item.added', {'type': 'response.output_item.added', 'output_index': 0, 'item': dict(item, status='in_progress', content=[])}),
              ('response.output_text.delta', {'type': 'response.output_text.delta', 'item_id': item['id'], 'output_index': 0, 'content_index': 0, 'delta': answer}),
              ('response.output_item.done', {'type': 'response.output_item.done', 'output_index': 0, 'item': item}),
              ('response.completed', {'type': 'response.completed', 'response': response})]
    return ''.join('event: ' + name + '\ndata: ' + json.dumps(event) + '\n\n' for name, event in events).encode()


class Fixture:
    def __init__(self):
        self.requests = []
        self.rejected = 0
        self.authorization_observed = False
        self.rejection_categories = Counter()
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                category = 'request_shape'
                try:
                    # Inspect header presence only; never read an authentication value.
                    authorization_present = any(name in self.headers for name in AUTH_HEADERS)
                    owner.authorization_observed |= authorization_present
                    self.connection.settimeout(2)
                    if authorization_present:
                        category = 'authorization'; raise ValueError('Unexpected authorization.')
                    if self.path != '/v1/responses':
                        category = 'route'; raise ValueError('Unexpected route.')
                    category = 'payload'
                    payload = read_payload(self.headers, self.rfile)
                    if len(payload) > MAX_REQUEST_BYTES:
                        raise ValueError('Oversized request.')
                    category = 'json'
                    body = json.loads(payload)
                    category = 'shape'
                    summary = request_summary(body, authorization_present)
                    owner.requests.append(summary)
                    category = 'model_or_tools'
                    if summary['tool_count'] or not summary['requested_model_matches']:
                        raise ValueError('Unexpected model or tools.')
                    data = fixture_response()
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/event-stream')
                    self.send_header('Content-Length', str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                except (ValueError, TypeError, KeyError, OSError):
                    owner.rejected += 1
                    owner.rejection_categories[category] += 1
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"error":{"type":"invalid_request_error","message":"Synthetic request rejected"}}')

        self.server = HTTPServer(('127.0.0.1', 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *args):
        self.server.shutdown()
        self.thread.join(timeout=2)
        self.server.server_close()

    @property
    def base_url(self):
        return 'http://127.0.0.1:' + str(self.server.server_port) + '/v1'


def probe(otel=False):
    env = clean_env(os.environ)
    executable = shutil.which('codex', path=env.get('PATH'))
    if not executable:
        raise AdapterError('Official Codex CLI required.')
    with tempfile.TemporaryDirectory(prefix='fleet-codex-probe-') as temp, Fixture() as fixture:
        cwd = Path(temp)
        if call([executable, '--version'], env=env, cwd=cwd, timeout=10).strip() != VERSION:
            raise AdapterError('Only inspected Codex 0.156.1 is supported.')
        servers = mcp_names(executable, env, cwd)
        # Same authoritative tool metadata as the real adapter. HTTP transport is
        # selected by the fixture provider's supports_websockets=false default.
        (cwd / 'catalog.json').write_text(json.dumps(catalog(MODEL)))
        telemetry = LocalTelemetry() if otel else None
        argv = command(executable, MODEL, cwd, servers, telemetry)[:-1]
        provider = ('{name="Synthetic loopback fixture",base_url=' + json.dumps(fixture.base_url)
                    + ',wire_api="responses",requires_openai_auth=false,supports_websockets=false,'
                    'request_max_retries=0,stream_max_retries=0}')
        argv += ['-c', 'model_provider="synthetic_loopback_fixture"',
                 '-c', 'model_providers.synthetic_loopback_fixture=' + provider, '-']
        failure = None
        with (telemetry if telemetry is not None else nullcontext()):
            try:
                result = parse_events(call(argv, env=env, cwd=cwd,
                    input='Return JSON {"decisions":{"probe":"complete"},"rationale":"synthetic"}.', timeout=60))
                completed = json.loads(result['text']).get('decisions', {}).get('probe') == 'complete'
            except (AdapterError, ValueError, TypeError):
                completed = False
                failure = 'native_fixture_roundtrip_failed'
        success = (completed and len(fixture.requests) == 1 and fixture.rejected == 0
                   and fixture.requests[0]['tool_count'] == 0
                   and not fixture.authorization_observed)
        report = {'schema': 1, 'kind': 'installed-cli-synthetic-request-inspection',
                  'success': success, 'cli_version': VERSION, 'requested_model': MODEL,
                  'inference_calls': 0, 'synthetic_requests': fixture.requests,
                  'authorization_header_observed': fixture.authorization_observed,
                  'rejected_requests': fixture.rejected, 'rejection_categories': dict(fixture.rejection_categories),
                  'fixture_response_completed': completed,
                  'failure': failure, 'disabled_mcp_count': len(servers),
                  'limits': 'Fixture verifies request shape, not live provider execution or model identity. '
                            'Native Codex may fetch first-party config/auth bootstrap metadata; '
                            'all model requests use the unauthenticated loopback provider.'}
        if telemetry is not None:
            report['telemetry'] = telemetry.summary()
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--otel', action='store_true', help='Opt in to native loopback OTLP log counts; no inference')
    args = parser.parse_args()
    try:
        result = probe(otel=args.otel)
    except (AdapterError, OSError):
        result = {'success': False, 'failure': 'local_preflight_failed', 'inference_calls': 0}
    print(json.dumps(result, indent=2))
    return 0 if result['success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
