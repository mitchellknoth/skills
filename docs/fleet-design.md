# Package design and validation boundary

## Why two paths

The architecture is reusable without the author's review roster or process preferences. A separate preset makes those opinions visible and selectable. Neither path grants authority or silently activates runtime behavior.

## Canonical sources and standalone distribution

Shared contracts, the inert readiness model and synthetic scenarios are canonical under `fleet-architecture`. The preset includes generated copies because a single-skill installation must not rely on an absent sibling. `scripts/sync-fleet-core.py` copies the declared files; `--check` detects drift. Both plugin manifests enumerate the same skill directories. Isolated-copy tests exercise links and evaluator behavior without the repository beside them.

Edit canonical support, run synchronization, then test. Keep preset-specific roles and choices separate. Existing `implement-review-loop` remains unchanged; its disclosed self-review fallback is useful generically but cannot satisfy a preset installation's required independent seat.

## Versioning

This draft uses package version 0.2.0 in both manifests. Publication of the files does not activate a runtime or establish behavioral parity. Future changes need migration notes, preserved user configuration and a rollback path. Do not overwrite private installation state when refreshing managed files.

## First-version evidence

Automated checks cover package discovery, manifest parity, standalone local links, generated-copy parity, dormant template defaults, malformed records and a synthetic readiness scenario suite. These are structural/model tests, not proof an agent follows the instructions.

Behavioral acceptance remains: fresh-session skill selection, role routing, correct source hierarchy, no invented permission, authorized-ready progress, blocker recovery and complete current-revision evidence under the actual target runtime. Evaluate paired old/new trials and held-out cases before any live pilot.

## Provenance

The package distills the user's requested architecture and prescriptive workflow. No pstack skills, scripts or opinions were copied. Its packaging inspired separation of canonical content, runtime adaptation and dormant activation. No private incident transcript or sensitive installation data is distributed.
