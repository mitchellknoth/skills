# Grok Bot first: manual deployment blueprint

**MVP status:** source package and manual setup contract. No automatic Grok account import/export, bot creation, routine installation or permission provisioning is implemented. The package does not claim the active account is identical to these files.

## Keep two choices visible

- Choose the author's preset for its risk-routed roles and operating choices.
- Choose the neutral architecture to select your own roles, cadence, review and authority policies.
- Both use the same evidence and honesty contracts. Fewer prescribed opinions does not grant broader permission.

## Field mapping

Each Grok mechanism is a binding of a provider-neutral [primitive](core/primitives.md). Plan another target from the primitive column, not the Grok column.

| Source | Primitive | Grok destination | Binding / verification |
|---|---|---|---|
| Persona purpose, lens and boundaries | `agent_persona` | Bot instructions/profile | Explicitly load relevant persona and shared contracts; verify saved text |
| Durable reusable lessons | `memory_scope` | Curated per-agent or owner-shared memory | Review provenance and conflicts; never bulk-copy private historical memory |
| Skill bindings | `skill` | Curated skills | Pin/select intended source; confirm actual loaded copy rather than filename alone |
| Routine intent | `routine` | Scheduled or event routine with a destination line | Review trigger, reads, output, authority, dedup and terminal behavior; leave inactive until authorized |
| Rooms and handoffs | `peer_message` | `SendToAgent` with priority, room membership, `SendToUser` | Verify actual participants and audience; no implied external messaging permission |
| One-way doors and yes records | `approval_gate`, `standing_authorization` | Approval card; memory entry holding the quote and timestamps | Only the owner's own words; relay verbatim |
| Outbound messages | `outbound_rule` | Draft card by default; saved send rule as the sole exception | A declined send is final; never retried by another route |
| State references | `source_of_truth_board`, `review_ledger`, `human_channel` | GitHub Project, scores-log file, the owner's one-to-one chat | Private installation-specific bindings, ownership and recovery checkpoints |
| Shared machine | `shared_workspace` | The box and per-bot desktops | Lock heavy runs; one checkout per seat per change |
| Tool requirements and identity | `tool_connector` | Integrations/permissions; one shared platform login by default (low friction, attribution lost, so record the acting seat), distinct per-bot identities with least-privilege scopes as the recommended target | Inspect effective capabilities, not just prompt promises |

## Installation sequence

1. Freeze a version of the source and inventory current bot instructions, memory, skills and routines. Mark unread surfaces unknown.
2. Build private bindings and select only applicable personas. Keep historical sources separate from active instructions.
3. Render/review the intended instructions and curated skill list manually. Existing configuration is not overwritten blindly.
4. Create or revise only explicitly authorized configuration. Review diffs before changing live bots. Installing this package alone authorizes none of these steps.
5. Verify exact saved content, actual skill source, integration scopes, state access and inactive routine definitions.
6. Replay inert cases: valid approved-ready work, stale evidence, known accepted residual, missing source, interrupted run, duplicate event and retrospective follow-through.
7. Activate a narrowly authorized shadow or pilot. Distinguish routine Active, run completed, artifact delivered and outcome verified.

## Settings the running fleet depends on

Lessons and anecdotes per primitive are in the [field notes](grok-field-notes.md#2-grok-bot-bindings-what-each-primitive-taught). Bind these deliberately; none is provisioned by this package.

- **Coordinator profile** (`agent_persona`): short and stable; the routing rule, the one-way door list and the anti-jobs. Roster detail and owner decisions live in `memory_scope`.
- **Specialist profiles** (`agent_persona`): one lane each, a hard gate where the owner set one, explicit anti-jobs, PASS or BOUNCE at the exact head.
- **Routine set** (`routine`, taxonomy in [autonomy](core/autonomy.md#3-routine-taxonomy-the-engine); Grok triggers in the [field notes](grok-field-notes.md#3-autonomy-on-grok-bot)): one repository-wide event listener, a twice-daily wake, a weekday brief, a production-alarm webhook, a pipeline result reporter, a board curator, narrow self-deleting merge-on-green watchers, and the monthly, post-prune and weekly retrospective loops. Leave inactive until authorized.
- **State** (`source_of_truth_board`, `review_ledger`): a project board (captain, lane, status, hold condition) for ownership, the pull request for head and checks, an append-only scores log for review evidence.
- **Shared machine** (`shared_workspace`): lock heavy runs, run them under `nice`, one checkout per seat per change, no edits to another bot's checkout, cleanup beyond rebuildable cache by proposal and the owner's yes.

The current source-system audit found conflicting copies and evolving policy. Preserve current owner decisions and make uncertainty visible. Do not resurrect retired confirmation ceremony from historical files or mistake batch permission for waived technical readiness.

See [personas](PERSONAS.md) and [adaptation roadmap](core/transpilation.md). Runtime invariants must be verified on Grok before any later target is declared equivalent.
