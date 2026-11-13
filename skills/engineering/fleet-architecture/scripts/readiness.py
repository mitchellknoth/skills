#!/usr/bin/env python3
"""Inert reference model. Inputs are assertions, not authenticated permissions."""
import json
import sys


class InvalidRecord(ValueError):
    pass


def validate_booleans(value, fields):
    for field in fields:
        if field in value and type(value[field]) is not bool:
            raise InvalidRecord(f'{field} must be boolean when present')


def evaluate(record):
    if not isinstance(record, dict):
        raise InvalidRecord('record must be an object')
    validate_booleans(record, ('evidence_complete',))
    revision = record.get('revision')
    action = record.get('action')
    target = record.get('target')
    if not all(isinstance(v, str) and v for v in (revision, action, target)):
        raise InvalidRecord('revision, action and target must be nonempty strings')
    policy = record.get('policy')
    if not isinstance(policy, dict):
        raise InvalidRecord('explicit policy is required')
    validate_booleans(policy, ('configured',))
    for key in ('required_reviews', 'required_checks', 'independent_reviews'):
        value = policy.get(key)
        if not isinstance(value, list) or not all(isinstance(x, str) and x for x in value) or len(set(value)) != len(value):
            raise InvalidRecord(f'{key} must be an explicit list of unique names')
    if not set(policy['independent_reviews']).issubset(policy['required_reviews']):
        raise InvalidRecord('independent_reviews must be a subset of required_reviews')
    if policy.get('configured') is not True:
        return {'status': 'not_ready', 'reasons': ['installation policy is not configured']}
    auth = record.get('authorization', {})
    if not isinstance(auth, dict):
        raise InvalidRecord('authorization must be an object')
    validate_booleans(auth, ('verified', 'scope_current', 'revision_bound'))
    # This cannot establish source authenticity. A real adapter must do that.
    if not (auth.get('verified') is True and auth.get('action') == action
            and auth.get('target') == target and auth.get('scope_current') is True):
        return {'status': 'not_authorized', 'reasons': ['current scoped authorization not established']}
    if auth.get('revision_bound') is True and auth.get('revision') != revision:
        return {'status': 'not_authorized', 'reasons': ['revision-bound authorization is stale']}
    reasons = []
    if record.get('evidence_complete') is not True:
        reasons.append('evidence inventory is incomplete')
    if record.get('action_revision') != revision:
        reasons.append('action target moved or is not revision-bound')
    for key, requirement, passed in [('reviews', 'required_reviews', 'pass'), ('checks', 'required_checks', 'passed')]:
        entries = record.get(key, {})
        if not isinstance(entries, dict):
            raise InvalidRecord(f'{key} must be an object')
        for name in policy[requirement]:
            item = entries.get(name)
            if isinstance(item, dict):
                validate_booleans(item, ('independent',))
            if not isinstance(item, dict) or item.get('revision') != revision or item.get('status') != passed:
                reasons.append(f'{key}:{name} lacks current passing evidence')
            elif key == 'reviews' and name in policy['independent_reviews'] and item.get('independent') is not True:
                reasons.append(f'reviews:{name} lacks required independence')
    findings = record.get('findings')
    if not isinstance(findings, list):
        raise InvalidRecord('findings must be an explicit list')
    for finding in findings:
        if not isinstance(finding, dict) or not isinstance(finding.get('id'), str) or type(finding.get('material')) is not bool:
            raise InvalidRecord('finding must have id and boolean material')
        validate_booleans(finding, ('material', 'evidence_verified', 'scope_current', 'acceptance_authorized', 'policy_allows_acceptance'))
        if not finding['material']:
            continue
        disposition = finding.get('disposition')
        valid = disposition in ('fixed', 'rejected', 'accepted') and finding.get('evidence_verified') is True
        if disposition == 'fixed':
            valid = valid and finding.get('verified_revision') == revision
        if disposition in ('rejected', 'accepted'):
            valid = valid and finding.get('scope_current') is True
        if disposition == 'accepted':
            valid = valid and finding.get('acceptance_authorized') is True and finding.get('policy_allows_acceptance') is True
        if not valid:
            reasons.append(f"finding:{finding['id']} lacks valid disposition")
    return {'status': 'not_ready' if reasons else 'ready', 'reasons': reasons}


def main():
    try:
        if len(sys.argv) != 2:
            raise InvalidRecord('usage: readiness.py RECORD.json')
        with open(sys.argv[1], encoding='utf-8') as stream:
            result = evaluate(json.load(stream))
        print(json.dumps(result, indent=2))
        return 0 if result['status'] == 'ready' else 1
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({'status': 'invalid', 'reasons': [str(exc)]}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
