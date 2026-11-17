# Package design and validation boundary

## Why two paths

The goal is a provider-agnostic framework of the author's Grok Bot configuration, in the way a compiler front end does not care which language it emits. Two paths serve it:

- **Abstract path, `fleet-architecture`:** pure functions (coordinator, advisor to the coordinator, implementer, risk-owned reviewer, adversary paired with a defender, done-ness interrogator, curator, watcher and reporter, housekeeper, human gatekeeper), the protocols that bind them, and thirteen provider-neutral primitives with per-target bindings. No domain is prescribed.
- **Prescriptive path, `fleet-preset`:** the same core, bundled, plus named domain seats (each binds one function), the author's process choices and field notes. Every Grok Bot mechanism is a binding of a neutral primitive.

Neither path grants authority or silently activates runtime behavior. The primitive map is the intermediate representation for cross-provider plans; apart from `skill`, non-Grok bindings are `unknown` until a conformance replay says otherwise.

## Canonical sources and standalone distribution

Shared contracts, the inert readiness model and synthetic scenarios are canonical under `fleet-architecture`. The preset includes generated copies because a single-skill installation must not rely on an absent sibling. `scripts/sync-fleet-core.py` copies the declared files and adjusts bundled asset links for the deeper preset reference directory; `--check` detects drift. Both plugin manifests enumerate the same skill directories. Isolated-copy tests exercise links and evaluator behavior without the repository beside them.

Edit canonical support, run synchronization, then test. Keep preset-specific roles and choices separate. Existing `implement-review-loop` remains unchanged; its disclosed self-review fallback is useful generically but cannot satisfy a preset installation's required independent seat.

## Versioning

This draft uses package version 0.3.0 in both manifests. Publication of the files does not activate a runtime or establish behavioral parity. Future changes need migration notes, preserved user configuration and a rollback path. Do not overwrite private installation state when refreshing managed files.

## First-version evidence

Automated checks cover package discovery, manifest parity, standalone local links, generated-copy parity, dormant template defaults, malformed records and a synthetic readiness scenario suite. These are structural/model tests, not proof an agent follows the instructions.

Behavioral acceptance remains: fresh-session skill selection, role routing, correct source hierarchy, no invented permission, authorized-ready progress, blocker recovery and complete current-revision evidence under the actual target runtime. Evaluate paired old/new trials and held-out cases before any live pilot.

## Provenance

The package distills the user's requested architecture and prescriptive workflow. No pstack skills, scripts or opinions were copied. Its packaging inspired separation of canonical content, runtime adaptation and dormant activation. No private incident transcript or sensitive installation data is distributed.

## First-hand field notes

The packages also carry [core field evidence](../skills/engineering/fleet-architecture/references/field-evidence.md) and the preset's [field notes](../skills/engineering/fleet-preset/references/grok-field-notes.md), written by the coordinator of a running fleet, with short per-role additions on each persona card. The provider-neutral lessons live in the architecture core's field evidence; the preset keeps domain-seat and Grok-binding lessons. They are practice evidence and mistakes that produced rules, scrubbed of identifiers, customers, addresses, hashes and run numbers. They are not a memory export and do not claim effectiveness. Preserve that scrub when extending them.

## Learning-loop refinement

The initial package contained generic feedback principles, not a faithful port of the distinct retrospective machinery. This refinement adds configurable core feedback contracts and preset playbooks based on a fuller live-routine and referenced-skill inspection. Source copies differed on pruning authority; the draft preserves the current stricter owner-confirmed behavior. It does not claim the exact runtime-loaded source version has been verified.

Automated feedback fixtures test an inert record classifier only. They do not prove that a real curator runs, a retrospective is delivered, or advice improves behavior. Those still require runtime evaluation.

## Persona and target evolution

Personas preserve source-grounded decision lenses and reusable learned behavior without exporting private memories. The neutral path provides a schema; the preset supplies a reviewed catalog. The first runtime target is a manual Grok Bot blueprint. Future targets require capability-aware planning and conformance tests, not word substitution.
