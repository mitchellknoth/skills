# Capability-aware adaptation roadmap

**Status: design contract, not an implemented transpiler.** The first target is a reviewed, manually installed Grok Bot deployment. Other targets remain planned until tested. File installation does not recreate schedules, identities, memories or credentials.

## Know the installation

Start with [customer-profile.template.json](../assets/customer-profile.template.json): goals, repositories/languages, tools and versions, durable sources, risk policy, budget and timezone. Discover connected capabilities through supported read-only inspection when authorized. Ask only for consequential missing choices. Do not infer the customer's authority from a public preset.

## Compiler analogy

1. **Source:** selected template or preset, personas, skill bindings and routine intent.
2. **Intermediate representation:** roles, handoff/evidence schemas, policy references, dependencies and required capabilities. Platform names and live IDs remain bindings.
3. **Type/capability checks:** determine whether every required semantic property is implementable.
4. **Target plan:** explicit supported, emulated, manual, unsupported or unknown entries, with evidence and limitations.
5. **Review/install:** user-reviewed configuration; activation is a separate authorized step.
6. **Conformance:** replay behavior and fault cases, then a limited shadow/pilot. Generated text alone proves no parity.

Do not silently weaken a required independent review, approval provenance, atomic revision guard or failure signal. Emulation must describe the lost guarantee; a required missing guarantee blocks that action. Unknown is not unsupported, and manual is not automatically completed.

Recommendations explain fit and tradeoffs instead of selecting tools by popularity. Recommend consolidation only after testing whether context or independence is lost. Never copy credentials, enable schedules, send messages or expand permissions as a side effect of rendering a plan.

## Primitive map

The intermediate representation is the [thirteen primitives](primitives.md) (agent persona, peer message, routine, memory scope, skill, approval gate, standing authorization, outbound rule, shared workspace, source-of-truth board, review ledger, human channel, tool connector), data in [primitive-bindings.json](../assets/primitive-bindings.json). The [functions](functions.md) and [protocols](protocols.md) are written only in primitives. Provider names appear only in bindings. Targets today: Grok Bot (source), Claude Code, Codex, Cursor and Dot. Apart from `skill`, every non-Grok entry is `unknown` with a TODO, and none is promoted without a recorded conformance replay.

## Promotion boundary

A future compiler needs deterministic schema validation, versioned adapters, migration/rollback, conflict-safe state updates, unchanged private configuration, and a conformance suite. Targets should declare tested versions and exact coverage. Do not advertise one-click cross-harness replication before those exist.
