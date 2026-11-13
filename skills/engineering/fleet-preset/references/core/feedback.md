# Configurable feedback, curation and recovery

Feedback is a set of distinct contracts, not one generic periodic report. Configure only the loops this installation needs: trigger, scope, evidence sources, comparison window, output, recipient, authority, checkpoint and terminal behavior. The architecture template does not impose the preset's cadence, roster, scoring rubric or proposal limits.

## Separate the loops

- **Context curation:** turn changed sources into compact current state with provenance. Read incrementally; advance each bookmark only after successful reading. Check live status before replacing facts. Preserve failed bookmarks, section ownership and append-only history. Carry project-close outcomes and lessons into the existing learning ledger.
- **Operational oversight:** find stalled commitments, missing decisions, repeated findings and failed dependencies. Check whether earlier advice changed behavior. A delivered recommendation is not a resolved action.
- **Outcome retrospective:** compare actual work and prior outcomes, explain repeated failure classes, and propose bounded changes. Do not grade idle capabilities or infer quality from message volume.
- **Coordinator calibration:** examine persistent misunderstandings, stale beliefs and user friction. Personal memory correction and policy changes have their own authorization requirements; task completion is not permission for permanent self-modification.
- **Evidence accounting:** link executed changes to goals, review/evidence and observed outcome. Account identity does not establish a human decision. Missing evidence is not automatically a missing control.
- **Harness hygiene:** evaluate obsolete/duplicated context, routines or roles. Record what protection each proposed cut supplied and how non-regression will be evaluated.
- **Post-change regression:** look for losses after a simplification. Missing telemetry is unknown, not healthy. Restore the smallest justified protection only with applicable authorization.

## Corrective-action ledger

Use [fix-ledger.template.json](../../assets/fix-ledger.template.json). Append a dated observation even for a quiet successful check, without creating an owner notification. Link the original finding, supporting evidence, advice, decision, owner, next checkpoint and observed behavior. Keep rejected, accepted, deferred, implemented and verified outcomes distinct. Reopen a settled finding only with new evidence or a changed decision; do not endlessly re-litigate the same advice.

For each accepted change record a prediction, affected control, scope, validation, rollback condition and later result. Preserve contradictory evidence and the original rationale instead of silently rewriting history.

## Reliable observation

Use [feedback-run.template.json](../../assets/feedback-run.template.json) to distinguish:

1. A schedule or listener was configured.
2. A run was attempted or started.
3. The run completed.
4. An evidence-backed output was saved.
5. The intended recipient received it, when delivery is part of the contract.
6. Follow-up work actually changed behavior.

None implies the next. A failed startup may prevent an in-agent failure handler from running. Record a known quota or integration failure as such, without generalizing it to every failed run. A manual artifact can recover the same period; verify scope and evidence before scheduling duplicate work. Preserve the last successfully processed checkpoint and retry only permitted, uncompleted work.

## Change authority

A retrospective proposes changes; it does not authorize persistent memory writes, role/persona edits, schedule changes, tool permissions or deletion. Follow the installation's actual confirmation policy and platform rules. A peer recommendation or recent Page cannot expand authority. A previously approved action may proceed within scope without another unnecessary ask.

## Evaluation boundary

`scripts/feedback.py` is an inert reference classifier for synthetic records. It checks a small subset of evidence and recovery properties. It cannot inspect artifacts, authenticate approval, measure outcomes, deliver messages or alter memory/routines. The adapter must establish the facts before supplying them. Test actual loop behavior separately in an isolated runtime.

The private `feedback-run.template.json` captures a rich operational record; it is not the classifier input schema. `feedback.py` accepts the deliberately normalized shape in `assets/feedback.example.json`, with one selected period, evidence-backed artifact, advice outcomes and optional proposal. A real adapter must verify and map the rich record to that shape. Passing an identifier string still does not prove the referenced evidence exists or is authentic.

## Close the learning loop

Use [learning and evolution](evolution.md) to connect an observation to a durable lesson, a bounded change trial and a measured keep/revise/revert decision. This includes proving the value of new practices, not only detecting regressions after pruning. The [improvement record](../../assets/improvement.template.json) links to the fix ledger; it does not replace it or authorize action.
