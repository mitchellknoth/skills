"""Host-only execution. Provider credentials never enter Harbor environments."""
import json
from pathlib import Path
from evals import run as runner


def execute(bundle_path, instruction, allow_inference=False, mock=False):
    bundle = json.loads(Path(bundle_path).read_text())
    if bundle['schema'] != 1:
        raise ValueError('Unsupported bundle')
    manifest_copy = dict(bundle['manifest'])
    identity = manifest_copy.pop('id')
    if runner.digest(runner.encode(manifest_copy)) != identity:
        raise ValueError('Manifest changed since export')
    if runner.digest(runner.encode(bundle['cases'])) != bundle['manifest']['case_objects_sha256']:
        raise ValueError('Cases changed since export')
    selector = json.loads(instruction)
    if selector.get('bundle_id') != bundle['manifest']['id']:
        raise ValueError('Task and bundle mismatch')
    index = selector['trial_index']
    if type(index) is not int or index < 0 or index >= len(bundle['manifest']['order']):
        raise ValueError('Invalid trial index')
    if runner.digest(Path(runner.__file__).read_bytes()) != bundle['manifest']['runner_sha256']:
        raise ValueError('Runner changed since export; export a new bundle')
    trial = bundle['manifest']['order'][index]
    case = next(c for c in bundle['cases'] if c['id'] == trial['case'])
    config = bundle['manifest']['config']
    argv = runner.resolve_argv(config['adapter'])
    if bundle['adapter_argv'] != argv:
        raise ValueError('Adapter command changed since export')
    current_files = {a: runner.digest(Path(a).read_bytes()) for a in argv if Path(a).is_file()}
    if current_files != bundle['manifest']['adapter_files']:
        raise ValueError('Adapter files changed since export')
    if not mock and not allow_inference:
        raise ValueError('Live inference requires allow_inference=true')
    if not mock and 'REPLACE' in config['model']:
        raise ValueError('Select an explicit provider model')
    skill = bundle['snapshots'][trial['variant']]
    expected_digest = runner.digest(runner.encode(skill['files'])) if skill['files'] else runner.digest(b'')
    if expected_digest != bundle['manifest']['skills'][trial['variant']]['sha256']:
        raise ValueError('Skill snapshot digest mismatch')
    skill = runner.select_context(skill, config['context_files'][trial['variant']][case['id']])
    expected_context = bundle['manifest']['contexts'][trial['variant']][case['id']]
    if runner.digest(skill['text'].encode()) != expected_context['sha256']:
        raise ValueError('Selected context changed since export')
    outputs = []
    for i, step in enumerate(case['steps']):
        if mock:
            output = {'decisions': step['expected'], 'rationale': 'MOCK: plumbing only'}
        else:
            data = runner.invoke(bundle['adapter_argv'], {
                'protocol': 1, 'role': 'agent', 'model': config['model'],
                'prompt': runner.prompt_for(case, i, skill, outputs)}, config)
            output = json.loads(data['text'])
            if not isinstance(output, dict) or not isinstance(output.get('rationale'), str):
                raise ValueError('Invalid decision output')
        outputs.append(output)
    return {'schema': 1, 'bundle_id': bundle['manifest']['id'], 'trial_index': index,
            'trial': trial, 'mock': mock, 'outputs': outputs}
