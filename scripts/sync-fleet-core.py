#!/usr/bin/env python3
"""Copy canonical shared support into the standalone preset; never activate anything."""
from pathlib import Path
import argparse
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills/engineering/fleet-architecture'
TARGET = ROOT / 'skills/engineering/fleet-preset'
MAPPINGS = [(SOURCE / 'references' / name, TARGET / 'references/core' / name)
            for name in ('architecture.md', 'readiness.md', 'adapters.md', 'evaluation.md')]
MAPPINGS += [(SOURCE / category / name, TARGET / category / name) for category, name in (
    ('scripts', 'readiness.py'), ('evals', 'readiness-cases.json'),
    ('assets', 'task.template.json'), ('assets', 'readiness.example.json'))]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    for source, target in MAPPINGS:
        if args.check:
            if not target.is_file() or source.read_bytes() != target.read_bytes():
                stale.append(str(target.relative_to(ROOT)))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    if stale:
        parser.exit(1, 'Stale generated core copies:\n' + '\n'.join(stale) + '\n')
    print('Fleet core copies verified.' if args.check else 'Fleet core copies synchronized.')
