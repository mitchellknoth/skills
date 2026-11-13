"""Export allowlisted numeric scores; keep private run artifacts on the host."""
import argparse
from datetime import date
import json
import math
from pathlib import Path
import re
import subprocess

from jsonschema import Draft202012Validator, ValidationError
from evals import run

RESULTS = run.ROOT / 'evals/results'
SCHEMA = Path(__file__).with_name('history.schema.json')
CASE_IDS = {'readiness', 'evidence', 'learning'}
MODELS = {'gpt-6-luna'}
TOKEN_KEYS = ('input_tokens', 'cached_input_tokens', 'output_tokens', 'reasoning_output_tokens')


def load(path):
    if path.stat().st_size > 20_000_000:
        raise ValueError('Artifact exceeds history import limit')
    return json.loads(path.read_text())


def uint(value):
    if type(value) is not int or not 0 <= value <= 10**12:
        raise ValueError('Invalid numeric measurement')
    return value


def model(value):
    return value if value in MODELS else ('other' if value else None)


def commit(value):
    if value is not None and (not isinstance(value, str) or not re.fullmatch('[0-9a-f]{40}', value)):
        raise ValueError('Invalid source commit')
    return value


def source_cases(manifest):
    raw = run.SCENARIOS.read_bytes()
    if run.digest(raw) != manifest['cases_sha256']:
        revision = commit(manifest.get('git_commit'))
        if revision is None:
            raise ValueError('Historical fixture unavailable')
        raw = subprocess.check_output(['git', 'show', f'{revision}:evals/scenarios.json'], cwd=run.ROOT)
    if run.digest(raw) != manifest['cases_sha256']:
        raise ValueError('Historical fixture hash mismatch')
    cases = json.loads(raw)['cases']
    if {c['id'] for c in cases} != CASE_IDS or run.digest(run.encode(cases)) != manifest['case_objects_sha256']:
        raise ValueError('Unsupported or changed fixture')
    return cases


def verified_manifest(path):
    manifest = load(path / 'manifest.json')
    if manifest.get('id') != run.digest(run.encode({k: v for k, v in manifest.items() if k != 'id'})):
        raise ValueError('Invalid source manifest')
    return manifest


def measurements(transports):
    usage = dict.fromkeys(TOKEN_KEYS, 0)
    usage['reporting_calls'] = 0
    tool_events = 0
    trace_calls = 0
    for transport in transports:
        if not isinstance(transport, dict):
            raise ValueError('Invalid transport measurement')
        counts = transport.get('usage')
        if counts is not None:
            if not isinstance(counts, dict):
                raise ValueError('Invalid usage')
            for key in TOKEN_KEYS:
                usage[key] += uint(counts.get(key, 0))
            if {'input_tokens', 'output_tokens'} <= counts.keys():
                usage['reporting_calls'] += 1
        trace = transport.get('trace')
        if trace is not None:
            if not isinstance(trace, dict):
                raise ValueError('Invalid trace')
            tool_events += uint(trace.get('tool_events'))
            trace_calls += 1
    return usage, {'reporting_calls': trace_calls,
                   'tool_events': tool_events if transports and trace_calls == len(transports) else None}


def judge_scores(judgments, expected_selectors):
    result = {'expected_calls': len(expected_selectors), 'completed_calls': 0, 'order_disagreements': 0,
              'baseline_preferences': 0, 'candidate_preferences': 0, 'ties': 0}
    pairs = {}
    transports = []
    for judgment in judgments:
        if 'error' in judgment:
            continue
        cid, repeat, reverse = judgment['case'], judgment['repeat'], judgment['reversed']
        if cid not in CASE_IDS or type(reverse) is not bool or (cid, repeat, reverse) not in expected_selectors:
            raise ValueError('Invalid judge selector')
        uint(repeat)
        winner = judgment['response']['winner']
        if winner not in ('A', 'B', 'tie'):
            raise ValueError('Invalid judge score')
        key = (cid, repeat)
        pair = pairs.setdefault(key, {})
        if reverse in pair:
            raise ValueError('Duplicate judgment')
        mapped = winner if not reverse else {'A': 'B', 'B': 'A', 'tie': 'tie'}[winner]
        pair[reverse] = mapped
        result[{'A': 'baseline_preferences', 'B': 'candidate_preferences', 'tie': 'ties'}[mapped]] += 1
        result['completed_calls'] += 1
        transports.append(judgment.get('transport', {}))
    result['order_disagreements'] = sum(len(pair) == 2 and pair[False] != pair[True] for pair in pairs.values())
    if result['completed_calls'] > len(expected_selectors):
        raise ValueError('Unexpected extra judgments')
    return result, transports


def build(source, *, observed_on, parent=None):
    source = Path(source)
    original = load(source / 'manifest.json')
    saved = original.get('kind') == 'saved-answer-judge-stage'
    if saved:
        if parent is None:
            raise ValueError('Saved judging requires the original paired run as --parent')
        parent = Path(parent)
        manifest = verified_manifest(parent)
        if original['source_manifest_id'] != manifest['id'] or original['source_trials_sha256'] != run.digest((parent / 'trials.json').read_bytes()):
            raise ValueError('Saved answers changed')
        source_code = original['current_code']
        records = [r for r in load(parent / 'trials.json') if r['case'] == original['case'] and r['repeat'] == original['repeat']]
        expected_order = [t for t in manifest['order'] if t['case'] == original['case'] and t['repeat'] == original['repeat']]
        mode, judge_expected, planned = 'live', 2, 2
        parent_id = manifest['id']
    else:
        manifest = verified_manifest(source)
        source_code = manifest
        records = load(source / 'trials.json')
        expected_order = manifest['order']
        summary = load(source / 'summary.json') if (source / 'summary.json').exists() else {}
        mode = manifest.get('execution_mode')
        if mode not in ('live', 'mock'):
            mode = {True: 'mock', False: 'live'}.get(summary.get('mock')) if type(summary.get('mock')) is bool else 'unknown'
        judge_expected = len(CASE_IDS) * manifest['config']['repeats'] * 2 if manifest['config'].get('judge_model') else 0
        planned = manifest['calls']
        parent_id = None
    cases = source_cases(manifest)
    expected_keys = [(t['case'], t['repeat'], t['variant']) for t in expected_order]
    actual_keys = [(r['case'], r['repeat'], r['variant']) for r in records]
    if len(set(expected_keys)) != len(expected_keys) or len(set(actual_keys)) != len(actual_keys) or not set(actual_keys) <= set(expected_keys):
        raise ValueError('Unexpected or duplicate trial')
    scores, agent_transports = [], []
    duration = 0.0
    for record in records:
        cid, repeat, variant = record['case'], record['repeat'], record['variant']
        case = next(c for c in cases if c['id'] == cid)
        grade = run.grade(case, record.get('outputs', []))
        complete = grade['complete'] and 'error' not in record
        scores.append({'case': cid, 'repeat': repeat, 'variant': variant, 'complete': complete,
                       'passed': complete and grade['passed'], 'checks_passed': sum(c['passed'] for c in grade['checks']),
                       'checks_total': len(grade['checks'])})
        if not saved:
            seconds = record['seconds']
            if type(seconds) not in (int, float) or not math.isfinite(seconds) or seconds < 0:
                raise ValueError('Invalid runtime measurement')
            duration += seconds
            agent_transports.extend(record.get('transport', []))
    judgments = load(source / 'judgments.json') if (source / 'judgments.json').exists() else []
    expected_judges = {(original['case'], original['repeat'], reverse) for reverse in (False, True)} if saved else {
        (case['id'], repeat, reverse) for case in cases for repeat in range(manifest['config']['repeats'])
        for reverse in (False, True)} if judge_expected else set()
    judge, judge_transports = judge_scores(judgments, expected_judges)
    if saved and any(j.get('case') != original['case'] or j.get('repeat') != original['repeat'] for j in judgments):
        raise ValueError('Judge selector changed')
    transports = ([] if saved else agent_transports) + judge_transports
    expected_agent_calls = sum(len(next(c for c in cases if c['id'] == r['case'])['steps']) for r in records)
    if not saved and mode == 'live' and 'execution_mode' not in manifest and len(agent_transports) != expected_agent_calls:
        mode = 'unknown'
    usage, trace = measurements(transports)
    comparisons = {'candidate_improvements': 0, 'candidate_regressions': 0}
    for candidate in (s for s in scores if s['variant'] == 'candidate'):
        baseline = next((s for s in scores if s['case'] == candidate['case'] and s['repeat'] == candidate['repeat'] and s['variant'] == 'baseline'), None)
        if baseline and baseline['complete'] and candidate['complete']:
            comparisons['candidate_improvements'] += candidate['passed'] and not baseline['passed']
            comparisons['candidate_regressions'] += baseline['passed'] and not candidate['passed']
    complete = len(scores) == len(expected_order) and all(s['complete'] for s in scores) and judge['completed_calls'] == judge_expected and not any('error' in j for j in judgments)
    if mode == 'live' and len(transports) != planned:
        complete = False
    verdict = 'plumbing_only' if mode == 'mock' else ('blocked' if not complete or mode == 'unknown' or any(not s['passed'] for s in scores if s['variant'] == 'candidate') else 'inconclusive')
    code_hashes = sorted(source_code['adapter_files'].values())
    record = {'schema': 1, 'observed_on': observed_on, 'kind': 'saved_answer_judge' if saved else 'paired_decision_probe',
        'mode': mode, 'source': {'manifest_id': run.digest(run.encode(original)) if saved else manifest['id'], 'parent_manifest_id': parent_id,
            'trials_sha256': run.digest(((parent if saved else source) / 'trials.json').read_bytes()),
            'judgments_sha256': run.digest((source / 'judgments.json').read_bytes()) if (source / 'judgments.json').exists() else None,
            'summary_sha256': run.digest((source / 'summary.json').read_bytes()) if (source / 'summary.json').exists() else None,
            'git_commit': commit(source_code.get('git_commit')), 'git_dirty': source_code.get('git_dirty', True),
            'fixture_sha256': manifest['cases_sha256'], 'runner_sha256': source_code['runner_sha256'],
            'contexts_sha256': run.digest(run.encode(manifest['contexts'])),
            'exporter_sha256': run.digest(run.encode({'exporter': run.digest(Path(__file__).read_bytes()),
                'schema': run.digest(SCHEMA.read_bytes()), 'regrader': run.digest(Path(run.__file__).read_bytes())})),
            'adapter_sha256': run.digest(run.encode(code_hashes)),
            'baseline_skill_sha256': manifest['skills']['baseline']['sha256'],
            'candidate_skill_sha256': manifest['skills']['candidate']['sha256'],
            'requested_model': None if saved else model(manifest['config']['model']),
            'judge_model': model(original.get('judge_model', manifest['config'].get('judge_model'))),
            'model_identity': 'unverified'},
        'execution': {'status': 'completed' if complete else 'incomplete', 'planned_cli_calls': planned,
            'completed_cli_calls': len(transports), 'expected_trials': len(expected_order), 'completed_trials': len(scores),
            'duration_seconds': None if saved else round(duration, 3)},
        'cases': sorted(scores, key=lambda s: (s['case'], s['repeat'], s['variant'])),
        'comparison': comparisons, 'judge': judge, 'usage': usage, 'trace': trace, 'verdict': verdict}
    record['record_id'] = run.digest(run.encode(record))
    validate(record)
    return record


def validate(record):
    try:
        Draft202012Validator(load(SCHEMA)).validate(record)
        date.fromisoformat(record['observed_on'])
        json.dumps(record, allow_nan=False)
        expected = run.digest(run.encode({k: v for k, v in record.items() if k != 'record_id'}))
        if record['record_id'] != expected:
            raise ValueError()
        for case in record['cases']:
            if case['checks_passed'] > case['checks_total']:
                raise ValueError()
            if case['passed'] != (case['complete'] and case['checks_total'] > 0 and case['checks_passed'] == case['checks_total']):
                raise ValueError()
        execution, judge, trace, cases = record['execution'], record['judge'], record['trace'], record['cases']
        selectors = {(c['case'], c['repeat'], c['variant']) for c in cases}
        if execution['completed_trials'] != len(cases) or len(selectors) != len(cases) or not 0 < execution['expected_trials'] >= len(cases):
            raise ValueError()
        if judge['completed_calls'] != sum(judge[k] for k in ('baseline_preferences', 'candidate_preferences', 'ties')) or judge['completed_calls'] > judge['expected_calls'] or judge['order_disagreements'] > judge['completed_calls'] // 2:
            raise ValueError()
        calls = execution['completed_cli_calls']
        if calls > execution['planned_cli_calls'] or record['usage']['reporting_calls'] > calls or trace['reporting_calls'] > calls:
            raise ValueError()
        if (trace['tool_events'] is not None) != (calls > 0 and trace['reporting_calls'] == calls):
            raise ValueError()
        complete = len(cases) == execution['expected_trials'] and all(c['complete'] for c in cases) and judge['completed_calls'] == judge['expected_calls']
        if record['mode'] == 'live' and calls != execution['planned_cli_calls']:
            complete = False
        if (execution['status'] == 'completed') != complete:
            raise ValueError()
        verdict = 'plumbing_only' if record['mode'] == 'mock' else ('blocked' if not complete or record['mode'] == 'unknown' or any(not c['passed'] for c in cases if c['variant'] == 'candidate') else 'inconclusive')
        if record['verdict'] != verdict:
            raise ValueError()
        comparison = {'candidate_improvements': 0, 'candidate_regressions': 0}
        for candidate in (c for c in cases if c['variant'] == 'candidate'):
            baseline = next((c for c in cases if c['case'] == candidate['case'] and c['repeat'] == candidate['repeat'] and c['variant'] == 'baseline'), None)
            if baseline and baseline['complete'] and candidate['complete']:
                comparison['candidate_improvements'] += candidate['passed'] and not baseline['passed']
                comparison['candidate_regressions'] += baseline['passed'] and not candidate['passed']
        if comparison != record['comparison']:
            raise ValueError()
    except (ValidationError, ValueError, TypeError, KeyError):
        raise ValueError('Invalid public score record; values suppressed') from None


def write(record, directory=RESULTS):
    validate(record)
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
    destination = directory / f'{record["observed_on"]}-{record["record_id"][:12]}.json'
    text = json.dumps(record, indent=2, sort_keys=True, allow_nan=False) + '\n'
    if destination.exists():
        if destination.read_text() != text:
            raise ValueError('Existing history record differs; append a new record instead')
        return destination
    with destination.open('x') as handle:
        handle.write(text)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['export', 'check'])
    parser.add_argument('--source', type=Path)
    parser.add_argument('--parent', type=Path)
    parser.add_argument('--date', default=date.today().isoformat())
    parser.add_argument('--out-dir', type=Path, default=RESULTS)
    args = parser.parse_args()
    try:
        if args.action == 'export':
            if args.source is None:
                raise ValueError('Export requires --source')
            print(write(build(args.source, observed_on=args.date, parent=args.parent), args.out_dir))
        else:
            paths = sorted(args.out_dir.glob('*.json'))
            for path in paths:
                record = load(path); validate(record)
                if path.name != f'{record["observed_on"]}-{record["record_id"][:12]}.json':
                    raise ValueError('History filename does not match record identity')
            print(f'{len(paths)} public score records validated')
    except (ValueError, TypeError, KeyError, OSError, subprocess.SubprocessError):
        parser.exit(2, 'History validation/export failed; private values suppressed.\n')


if __name__ == '__main__':
    main()
