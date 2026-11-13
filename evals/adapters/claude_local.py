#!/usr/bin/env python3
"""Opt-in, no-tool Claude Code bridge. Never reads or copies credential files.

Protocol: stdin {protocol:1,role:agent|judge,model:str,prompt:str}; stdout
{text:str,usage:object}. Native claude.ai login only. No live calls in tests.
This is CLI-level isolation, NOT an OS sandbox; managed policy still applies.
"""
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

REQUIRED_FLAGS = ('--restricted', '--safe-mode', '--tools', '--disallowedTools',
                  '--strict-mcp-config', '--mcp-config', '--setting-sources',
                  '--disable-slash-commands', '--no-session-persistence',
                  '--max-turns', '--output-format', '--model')
ENV_KEYS = ('PATH', 'HOME', 'USER', 'LOGNAME', 'LANG', 'LC_ALL', 'TMPDIR',
            'XDG_RUNTIME_DIR', 'DBUS_SESSION_BUS_ADDRESS')

class AdapterError(Exception):
    pass

def clean_env(source):
    # No provider keys, base-URL overrides, shell startup, proxies or Node injection.
    return {k: source[k] for k in ENV_KEYS if k in source}

def command(executable, model):
    return [executable, '-p', '--restricted', '--safe-mode', '--tools', '',
            '--disallowedTools', '*', '--strict-mcp-config', '--mcp-config',
            '{"mcpServers":{}}', '--setting-sources', '', '--disable-slash-commands',
            '--no-session-persistence', '--max-turns', '1', '--output-format', 'json',
            '--model', model]

def invoke(argv, *, env, cwd, input=None):
    try:
        result = subprocess.run(argv, input=input, capture_output=True, text=True,
                                env=env, cwd=cwd, timeout=120, check=False)
    except (OSError, subprocess.TimeoutExpired):
        raise AdapterError('Claude CLI failed or timed out; inspect it locally.') from None
    if result.returncode:
        raise AdapterError('Claude CLI returned an error; no fallback was attempted.')
    return result.stdout

def run(request, source=None):
    source = os.environ if source is None else source
    if source.get('FLEET_EVAL_ALLOW_REMOTE') != '1':
        raise AdapterError('Set FLEET_EVAL_ALLOW_REMOTE=1 to allow provider inference.')
    if not isinstance(request, dict) or request.get('protocol') != 1:
        raise AdapterError('Unsupported adapter protocol.')
    if request.get('role') not in ('agent', 'judge'):
        raise AdapterError('Invalid role.')
    model, prompt = request.get('model'), request.get('prompt')
    if not isinstance(model, str) or not model.startswith('claude-') or any(c.isspace() for c in model):
        raise AdapterError('Select an explicit Claude model ID, not an alias.')
    if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 500_000:
        raise AdapterError('Invalid or oversized prompt.')
    env = clean_env(source)
    executable = shutil.which('claude', path=env.get('PATH'))
    if not executable:
        raise AdapterError('Claude Code is not installed on this machine.')
    with tempfile.TemporaryDirectory(prefix='fleet-eval-') as cwd:
        version_output = invoke([executable, '--version'], env=env, cwd=cwd)
        version_match = re.fullmatch(r'(\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?)(?: \(Claude Code\))?', version_output.strip())
        if not version_match:
            raise AdapterError('Could not verify Claude CLI version.')
        cli_version = version_match.group(1)
        help_text = invoke([executable, '--help'], env=env, cwd=cwd)
        if any(flag not in help_text for flag in REQUIRED_FLAGS):
            raise AdapterError('CLI safety flags could not be verified; update/check Claude Code locally.')
        try:
            auth = json.loads(invoke([executable, 'auth', 'status'], env=env, cwd=cwd))
        except (ValueError, TypeError):
            raise AdapterError('Could not verify native Claude login.') from None
        if not isinstance(auth, dict) or auth.get('authMethod') != 'claude.ai':
            raise AdapterError('Native claude.ai login required; API-key and third-party fallback disabled.')
        try:
            result = json.loads(invoke(command(executable, model), env=env, cwd=cwd, input=prompt))
        except (ValueError, TypeError):
            raise AdapterError('Claude returned invalid JSON.') from None
        if not isinstance(result, dict) or result.get('is_error') or result.get('subtype') != 'success':
            raise AdapterError('Claude did not complete successfully.')
        if not isinstance(result.get('result'), str) or not result['result'].strip():
            raise AdapterError('Claude returned no answer.')
        # Reject observable model fallback. Some CLI versions omit modelUsage;
        # fail closed rather than imply that a requested model was actually used.
        models = result.get('modelUsage')
        if not isinstance(models, dict) or set(models) != {model}:
            raise AdapterError('Actual model could not be verified or differed from requested model.')
        usage = result.get('usage', {})
        safe_usage = {k: v for k, v in usage.items() if k in
                      ('input_tokens', 'output_tokens', 'cache_read_input_tokens',
                       'cache_creation_input_tokens') and type(v) in (int, float) and v >= 0} if isinstance(usage, dict) else {}
        return {'text': result['result'], 'usage': safe_usage,
                'metadata': {'cli_version': cli_version, 'model': model,
                             'auth_method': 'claude.ai'}}

def main():
    try:
        raw = sys.stdin.read(600_001)
        if len(raw) > 600_000:
            raise AdapterError('Adapter input exceeds limit.')
        result = run(json.loads(raw))
        print(json.dumps(result))
        return 0
    except (AdapterError, ValueError, TypeError) as exc:
        # Never relay native stderr, auth output, environment or raw result.
        message = str(exc) if isinstance(exc, AdapterError) else 'Invalid adapter input.'
        print(message, file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
