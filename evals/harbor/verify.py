"""No-model verifier. Only reads JSON, never executes agent output."""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from run import grade


def verify(case, expected, answer):
    identity = all(answer.get(k) == expected[k] for k in ('bundle_id', 'trial_index', 'trial'))
    outputs = answer.get('outputs', [])
    result = grade(case, outputs if isinstance(outputs, list) else [])
    result['identity_valid'] = identity
    result['mock'] = answer.get('mock') is True
    result['reward'] = int(identity and answer.get('mock') is False and result['complete'] and result['passed'])
    return result


if __name__ == '__main__':
    target = Path('/logs/verifier'); target.mkdir(parents=True, exist_ok=True)
    try:
        case = json.loads(Path('/tests/case.json').read_text())
        expected = json.loads(Path('/tests/expected.json').read_text())
        answer = json.loads(Path('/app/answer.json').read_text())
        result = verify(case, expected, answer)
    except (OSError, ValueError, TypeError, AttributeError, KeyError):
        result = {'reward': 0, 'error': 'invalid_or_missing_artifact'}
    (target/'reward.txt').write_text(str(result['reward']))
    (target/'grade.json').write_text(json.dumps(result, indent=2))
