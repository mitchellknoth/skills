"""Export frozen paired decision probes for local Harbor execution; no inference."""
import argparse
import json
from pathlib import Path
import shlex
import shutil
import tomllib
import re
from evals import run as runner


def export(config, out):
    manifest, snapshots, cases = runner.plan(config)
    if config.get('judge_model'):
        raise ValueError('Harbor bridge currently supports deterministic grading only; use local runner for judge')
    python_version = tomllib.loads((runner.ROOT/'mise.toml').read_text())['tools']['python']
    if not isinstance(python_version,str) or not re.fullmatch(r'\d+\.\d+\.\d+',python_version):
        raise ValueError('Harbor export requires an exact Python version in mise.toml')
    out = Path(out).resolve(); out.mkdir(parents=True, exist_ok=False)
    bundle = {'schema': 1, 'manifest': manifest, 'snapshots': snapshots, 'cases': cases,
              'adapter_argv': runner.resolve_argv(config['adapter'])}
    bundle_path = out/'host-bundle.json'
    bundle_path.write_text(json.dumps(bundle, indent=2)); bundle_path.chmod(0o600)
    commands = []
    for index, trial in enumerate(manifest['order']):
        case = next(c for c in cases if c['id'] == trial['case'])
        task = out/'tasks'/f'{index:03d}-{trial["case"]}-{trial["variant"]}'
        (task/'environment').mkdir(parents=True); (task/'tests').mkdir()
        selector = {'bundle_id': manifest['id'], 'trial_index': index}
        (task/'instruction.md').write_text(json.dumps(selector))
        (task/'environment/Dockerfile').write_text(f'FROM python:{python_version}-slim\nWORKDIR /app\n')
        (task/'task.toml').write_text('version = "1.0"\nartifacts = ["/app/answer.json"]\n[agent]\ntimeout_sec = 600\n[verifier]\nenvironment_mode = "separate"\ntimeout_sec = 30\n')
        (task/'tests/case.json').write_text(json.dumps(case))
        (task/'tests/expected.json').write_text(json.dumps({**selector, 'trial': trial}))
        shutil.copyfile(runner.__file__, task/'tests/run.py')
        shutil.copyfile(Path(__file__).with_name('verify.py'), task/'tests/verify.py')
        (task/'tests/test.sh').write_text('#!/bin/sh\nset -eu\npython /tests/verify.py\n')
        (task/'tests/test.sh').chmod(0o755)
        commands.append(['harbor', 'run', '-t', str(task), '-a', 'evals.harbor.agent:LocalFleetAgent',
                         '--ak', f'bundle={bundle_path}', '--ak', 'mock=true'])
    (out/'commands.json').write_text(json.dumps(commands, indent=2))
    return commands


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', default='evals/local.example.json')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    commands = export(json.loads(Path(args.config).read_text()), args.out)
    print('\n'.join(shlex.join(c) for c in commands))
