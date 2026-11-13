#!/usr/bin/env python3
"""Inert feedback-record classifier; never reads live sources or changes state."""
import json
import sys


class InvalidRecord(ValueError):
    pass


def validate_reference(value, label):
    if not isinstance(value, str) or not value.strip():
        raise InvalidRecord(f'{label} must be a nonempty reference string')


def classify(record):
    if not isinstance(record, dict) or not isinstance(record.get('period'), str) or not record['period']:
        raise InvalidRecord('record must name its period')
    for key in ('delivery_required', 'confirmation_required'):
        if type(record.get(key)) is not bool:
            raise InvalidRecord(f'{key} must be boolean')
    scores = record.get('scores', [])
    if not isinstance(scores, list):
        raise InvalidRecord('scores must be a list')
    for score in scores:
        if not isinstance(score, dict) or type(score.get('worked')) is not bool:
            raise InvalidRecord('each score must say whether work occurred')
        if score['worked'] is False and score.get('grade') is not None:
            raise InvalidRecord('idle capabilities cannot receive effectiveness scores')
    artifact = record.get('artifact')
    valid = isinstance(artifact, dict) and artifact.get('period') == record['period']
    if isinstance(artifact, dict):
        for key in ('evidence_checked', 'source_complete', 'delivered'):
            if type(artifact.get(key)) is not bool:
                raise InvalidRecord(f'artifact.{key} must be boolean')
        if artifact.get('kind') not in ('scheduled', 'manual'):
            raise InvalidRecord('artifact kind must be scheduled or manual')
        validate_reference(artifact.get('reference'), 'artifact.reference')
        valid = valid and artifact['evidence_checked'] and artifact['source_complete']
        if record['delivery_required']:
            valid = valid and artifact['delivered']
    followups = []
    if not valid:
        followups.append('verify or recover an evidence-backed output for this period')
    advice = record.get('advice', [])
    if not isinstance(advice, list):
        raise InvalidRecord('advice must be a list')
    for item in advice:
        if not isinstance(item, dict) or not isinstance(item.get('id'), str):
            raise InvalidRecord('advice requires id')
        if item.get('status') == 'verified' or item.get('outcome_evidence') is not None:
            validate_reference(item.get('outcome_evidence'), 'advice.outcome_evidence')
        if item.get('status') not in ('verified', 'rejected', 'deferred'):
            followups.append(f"advice:{item['id']} still needs disposition or behavior evidence")
    proposal = record.get('proposal')
    proposal_status = 'none'
    if proposal is not None:
        if not isinstance(proposal, dict) or type(proposal.get('confirmed')) is not bool:
            raise InvalidRecord('proposal confirmation must be explicit boolean')
        if proposal.get('confirmation_source') is not None:
            validate_reference(proposal['confirmation_source'], 'proposal.confirmation_source')
        if record['confirmation_required'] and not (proposal['confirmed'] and proposal.get('confirmation_source')):
            proposal_status = 'pending_confirmation'
        else:
            proposal_status = 'recorded_for_policy_check'
    # This is evidence classification, never permission or an execution instruction.
    status = 'unverified'
    if valid:
        status = 'manual_recovery' if artifact['kind'] == 'manual' else 'recorded'
    return {'status': status, 'followups': followups, 'proposal_status': proposal_status}


def main():
    try:
        if len(sys.argv) != 2:
            raise InvalidRecord('usage: feedback.py RECORD.json')
        with open(sys.argv[1], encoding='utf-8') as stream:
            result = classify(json.load(stream))
        print(json.dumps(result, indent=2))
        return 0 if result['status'] != 'unverified' else 1
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({'status': 'invalid', 'reasons': [str(exc)]}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
