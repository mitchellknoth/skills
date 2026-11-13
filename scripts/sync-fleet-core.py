#!/usr/bin/env python3
"""Copy canonical shared support into the standalone preset; never activate anything."""
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills/engineering/fleet-architecture'
TARGET = ROOT / 'skills/engineering/fleet-preset'
MAPPINGS = [(SOURCE / 'references' / name, TARGET / 'references/core' / name)
            for name in ('architecture.md', 'readiness.md', 'adapters.md', 'evaluation.md', 'feedback.md', 'personas.md', 'transpilation.md', 'skill-evolution.md')]
MAPPINGS += [(SOURCE / category / name, TARGET / category / name) for category, name in (
    ('scripts', 'readiness.py'), ('evals', 'readiness-cases.json'),
    ('assets', 'persona.template.json'), ('assets', 'customer-profile.template.json'),
    ('assets', 'task.template.json'), ('assets', 'readiness.example.json'),
    ('assets', 'feedback-run.template.json'), ('assets', 'fix-ledger.template.json'),
    ('scripts', 'feedback.py'), ('evals', 'feedback-cases.json'), ('assets', 'feedback.example.json'))]

def generated_bytes(source):
    content = source.read_bytes()
    if source.parent == SOURCE / 'references' and source.suffix == '.md':
        # Preset references are one level deeper than their canonical source.
        content = content.replace(b'](../assets/', b'](../../assets/')
    return content


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    for source, target in MAPPINGS:
        if args.check:
            if not target.is_file() or generated_bytes(source) != target.read_bytes():
                stale.append(str(target.relative_to(ROOT)))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(generated_bytes(source))
    if stale:
        parser.exit(1, 'Stale generated core copies:\n' + '\n'.join(stale) + '\n')
    print('Fleet core copies verified.' if args.check else 'Fleet core copies synchronized.')
