"""Public-history privacy and score validity, using synthetic private artifacts."""
import copy
import json

import pytest

from evals import history, run


@pytest.fixture
def source(tmp_path):
    config=json.loads((run.ROOT/'evals/codex.example.json').read_text())
    path=tmp_path/'private-run'
    run.run(config,path,mock=True)
    return path


def test_export_recomputes_scores_and_excludes_all_private_text(source):
    trials=json.loads((source/'trials.json').read_text())
    trials[0]['outputs'][0]['rationale']='SYNTHETIC_SECRET /private/person@example.com'
    trials[0]['outputs'][0]['decisions']={}
    trials[0]['grade']={'passed':True,'complete':True,'private':'SYNTHETIC_SECRET'}
    trials[0]['transport']=[{'usage':{'input_tokens':17,'output_tokens':3,'account':'SYNTHETIC_SECRET'},
        'metadata':{'private':'SYNTHETIC_SECRET'},'trace':{'tool_events':0,
        'events':[{'command':'SYNTHETIC_SECRET'}]}}]
    (source/'trials.json').write_text(json.dumps(trials))
    summary=json.loads((source/'summary.json').read_text());summary['passing_trials']=999
    (source/'summary.json').write_text(json.dumps(summary))
    record=history.build(source,observed_on='2026-11-13')
    assert record['verdict']=='plumbing_only'
    assert sum(c['passed'] for c in record['cases'])==5
    assert record['usage']['input_tokens']==17
    assert 'SYNTHETIC_SECRET' not in json.dumps(record)
    assert '/private/' not in json.dumps(record)
    assert 'person@example.com' not in json.dumps(record)
    history.validate(record)


def test_unknown_fields_and_free_text_cannot_enter_committed_history(source):
    record=history.build(source,observed_on='2026-11-13')
    for mutate in (lambda r:r.update(prompt='SYNTHETIC_SECRET'),
                   lambda r:r['usage'].update(api_key='SYNTHETIC_SECRET'),
                   lambda r:r['source'].update(requested_model='SYNTHETIC_SECRET')):
        invalid=copy.deepcopy(record);mutate(invalid)
        with pytest.raises(ValueError):history.validate(invalid)


def test_missing_run_outputs_are_recorded_as_incomplete(source):
    trials=json.loads((source/'trials.json').read_text())
    (source/'trials.json').write_text(json.dumps(trials[:1]))
    record=history.build(source,observed_on='2026-11-13')
    assert record['execution']['status']=='incomplete'
    assert record['execution']['completed_trials']==1
    assert record['trace']['tool_events'] is None


def test_tampered_manifest_or_duplicate_trial_is_rejected(source):
    path=source/'manifest.json';original=path.read_text();manifest=json.loads(original)
    manifest['config']['model']='changed'
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError):history.build(source,observed_on='2026-11-13')
    path.write_text(original)
    trials=json.loads((source/'trials.json').read_text());trials[1]=trials[0]
    (source/'trials.json').write_text(json.dumps(trials))
    with pytest.raises(ValueError):history.build(source,observed_on='2026-11-13')


@pytest.mark.parametrize('bad',[-1,True,'17',float('nan')])
def test_invalid_measurements_cannot_be_archived(source,bad):
    trials=json.loads((source/'trials.json').read_text())
    trials[0]['transport']=[{'usage':{'input_tokens':bad,'output_tokens':0}}]
    (source/'trials.json').write_text(json.dumps(trials))
    with pytest.raises(ValueError):history.build(source,observed_on='2026-11-13')


def test_history_is_content_addressed_and_append_only(source,tmp_path):
    record=history.build(source,observed_on='2026-11-13')
    destination=history.write(record,tmp_path/'public')
    assert history.write(record,tmp_path/'public')==destination
    destination.write_text('{}')
    with pytest.raises(ValueError):history.write(record,tmp_path/'public')


def test_saved_judge_history_keeps_reversed_order_disagreement(source,tmp_path,monkeypatch):
    parent=json.loads((source/'manifest.json').read_text())
    parent['config'].update(judge_model='gpt-6-luna',max_calls=14)
    parent['id']=run.digest(run.encode({k:v for k,v in parent.items() if k!='id'}))
    (source/'manifest.json').write_text(json.dumps(parent))
    monkeypatch.setattr(run,'invoke',lambda *a,**kw:{'text':'{"winner":"B","reason":"SYNTHETIC_SECRET"}',
        'usage':{'input_tokens':5,'output_tokens':2}})
    stage=tmp_path/'judge'
    run.judge_saved(source,stage,'learning',allow=True)
    record=history.build(stage,observed_on='2026-11-13',parent=source)
    assert record['kind']=='saved_answer_judge'
    assert record['judge']['order_disagreements']==1
    assert record['execution']['completed_cli_calls']==2
    assert 'SYNTHETIC_SECRET' not in json.dumps(record)
    parent_record=history.build(source,observed_on='2026-11-13')
    assert record['source']['parent_manifest_id']==parent_record['source']['manifest_id']


def test_stale_live_label_does_not_promote_a_mock_without_transport(source):
    path=source/'summary.json';summary=json.loads(path.read_text());summary['mock']=False
    path.write_text(json.dumps(summary))
    # Bound manifests remain mock. Legacy unbound mode must stay unknown.
    record=history.build(source,observed_on='2026-11-13')
    assert record['mode'] in ('mock','unknown')
    assert record['verdict']!='inconclusive'


def test_judgments_must_cover_the_expected_case_repeat_and_order(source):
    path=source/'manifest.json';manifest=json.loads(path.read_text())
    manifest['config'].update(judge_model='gpt-6-luna',max_calls=14)
    manifest['calls']=14
    manifest['id']=run.digest(run.encode({k:v for k,v in manifest.items() if k!='id'}))
    path.write_text(json.dumps(manifest))
    judgments=[{'case':'readiness','repeat':repeat,'reversed':reverse,
        'response':{'winner':'tie','reason':'private'}} for repeat in (0,1,2) for reverse in (False,True)]
    (source/'judgments.json').write_text(json.dumps(judgments))
    with pytest.raises(ValueError):history.build(source,observed_on='2026-11-13')
    (source/'judgments.json').write_text(json.dumps(judgments[:2]))
    assert history.build(source,observed_on='2026-11-13')['execution']['status']=='incomplete'


def test_raw_artifact_hashes_change_when_private_answers_change(source):
    before=history.build(source,observed_on='2026-11-13')
    path=source/'trials.json';trials=json.loads(path.read_text())
    trials[0]['outputs'][0]['rationale']='new private evidence'
    path.write_text(json.dumps(trials))
    after=history.build(source,observed_on='2026-11-13')
    assert before['source']['trials_sha256']!=after['source']['trials_sha256']
    assert 'new private evidence' not in json.dumps(after)


def test_same_skill_with_different_context_has_different_public_identity(source):
    before=history.build(source,observed_on='2026-11-13')
    path=source/'manifest.json';manifest=json.loads(path.read_text())
    manifest['contexts']['candidate']['readiness']['sha256']='a'*64
    manifest['id']=run.digest(run.encode({k:v for k,v in manifest.items() if k!='id'}))
    path.write_text(json.dumps(manifest))
    after=history.build(source,observed_on='2026-11-13')
    assert before['source']['candidate_skill_sha256']==after['source']['candidate_skill_sha256']
    assert before['source']['contexts_sha256']!=after['source']['contexts_sha256']


def test_historical_fixture_is_loaded_from_its_recorded_commit(source,tmp_path,monkeypatch):
    expected=history.build(source,observed_on='2026-11-13')
    changed=tmp_path/'future-scenarios.json';changed.write_text('{"cases":[]}')
    monkeypatch.setattr(run,'SCENARIOS',changed)
    restored=history.build(source,observed_on='2026-11-13')
    assert restored['cases']==expected['cases']
    assert restored['source']['fixture_sha256']==expected['source']['fixture_sha256']


@pytest.mark.parametrize('mutation',[
    lambda r:r['cases'][0].update(complete=False,checks_passed=0),
    lambda r:r['execution'].update(status='incomplete'),
    lambda r:r['judge'].update(completed_calls=1),
    lambda r:r['comparison'].update(candidate_improvements=99),
])
def test_self_consistent_hash_does_not_hide_contradictory_scores(source,mutation):
    record=history.build(source,observed_on='2026-11-13');mutation(record)
    record['record_id']=run.digest(run.encode({k:v for k,v in record.items() if k!='record_id'}))
    with pytest.raises(ValueError):history.validate(record)
