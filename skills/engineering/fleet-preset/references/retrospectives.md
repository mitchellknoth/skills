# Preset learning and maintenance loops

These are distinct workflows, distilled from the inspected routines and the deeper fleet-retro/prune skill. The preset supplies their shape and defaults; installation-specific timing, recipients, permissions, metrics availability and state stores remain private and configurable. Nothing here installs a schedule or authorizes a mutation.

Read the bundled [feedback contract](core/feedback.md), then use the relevant loop. Do not replace existing oversight with another bot or duplicate its ledger.

## 1. Curate, then wake

The curator prepares current state before proactive work. Read only changed sources using byte/line/update bookmarks; read Pages only when their sources changed. Advance a bookmark only after successful reading and live-state re-verification. Preserve failed-source bookmarks, repeated-failure evidence and each specialist's section ownership. Keep compact current state, append-only archives and the last 20 run records. On project closure, record outcomes and copy durable lessons into the existing fix ledger.

The coordinator's wake checks curation status, finds the lowest unmet goal condition, and assigns or nudges the responsible capability **before reporting**. Record what was briefed to avoid repetition. Distinguish quiet healthy work, unreadable sources, pending owner decisions, overdue specialist work and already-resolved work. A routine is not a substitute for doing the authorized next step.

## 2. Daily operational oversight

Default: weekday check after the coordinator's brief. The oversight capability advises the coordinator, not a competing commander.

- Read actual goals, checkpoints, Pages, merge evidence and the existing fix ledger.
- Check ready-but-unasked approvals, goal risk, stalled commitments, scope creep, fourth-or-later review rounds, repeated must-fix classes, missing completion records and approval provenance, ceremony regrowth, unhandled runner/CI/resource blockers and avoidable context/chatter cost.
- Verify whether prior advice produced a behavior change. Append a dated ledger entry each run, including a quiet check; do not claim “fixed” merely because advice was sent.
- Use source-backed telemetry for urgent-send share, no-op wakes, room re-wakes, report size and usage pace. If unavailable, mark it unknown rather than estimate a favorable number.
- Route routine findings to the coordinator with an owner and checkpoint. Do not reargue a settled decision absent new evidence. Direct owner escalation is reserved for actual one-way authority risk, a proposed role change, or a persistent serious miss after the coordinator declined advice, subject to installation instructions.

## 3. Weekly fleet outcome retro

Default: one weekly comparison against the previous period, using [retro.template.json](../assets/retro.template.json). Read the ledger and saved evidence before asking agents for summaries. Inventory only agents/capabilities that actually worked; idle roles are not scored as failures. In the configured risk-owned panel, each scorer must leave one same-turn evidence-backed sentence when recording PASS, Bounce or a must-fix: work assessed, pitfall/catch and citation. Use these completion logs instead of a weekly fan-out. Ask only for missing evidence about actual owned work.

For each worked capability, record effective/mixed/miss with the actual task, evidence and pitfall; do not treat a profile paragraph as behavior proof. Cultivate at most one durable memory/learned constraint or existing skill reference per worked capability as a proposal, not a wholesale persona replacement.

Produce:
- A supported overall assessment, goal progress out of ten with its basis, and week-over-week trend. Do not score unavailable evidence.
- Impact-ranked misses, landed fixes, open issues and proof of which advice changed behavior.
- Routing/decomposition findings: right first specialist, panel timing, slicing versus dumping a task into a room, real catches versus rubber stamps, invented facts, unfulfilled follow-up, time-to-artifact and unnecessary chatter.
- State quality: stale Pages, curator misses, context size and retained history. A compact target of roughly 2 KB plus the last 10 log lines is a preference, not permission to discard required evidence. Context-reduction targets need a measured installation baseline/export; no fabricated savings.
- At most **three** proposed changes for the next period, each tagged as reversible or consequential, with owner, predicted benefit, validation and rollback.
- A short 3–7-bullet digest and at most one owner decision at a time. Do not hide urgent independent decisions behind that presentation preference.

Save the full dated retrospective before delivering its digest. Update the health line only when it changed; send a short owner scorecard and one nonurgent coordinator note through configured destinations. Evaluate the usefulness of same-turn completion logs as keep/tweak/drop; a proposal to change them does not disable the current contract. Durable lessons persisting for two or more weeks become a proposed rule/skill change, not automatic policy. Reversible task-level work may go to the coordinator within existing authority; persona, routine and consequential changes require the appropriate owner confirmation.

## 4. Weekly coordinator calibration

This is separate from the fleet's product/delivery retro, even in a low-signal week. Draft a short reflection around seven questions:

1. What durable knowledge was learned?
2. Which corrections repeated?
3. Which beliefs are stale or wrong?
4. Which decisions should change future behavior?
5. What was misunderstood or required unnecessary clarification?
6. What belongs in a routine, skill or delegation instead of recurring chat effort?
7. What knowledge gap still matters?

Propose explicit memory writes/forgets and routine/skill changes, with rationale. **Wait for owner confirmation before permanent changes.** Do not conflate a successful weekly draft with an authorized update.

## 5. Merge evidence scoreboard

On relevant change events, use a lightweight inline check, normally one or two source reads and no subagent. Recheck live state and append the resulting goal contribution and timestamp, panel-to-merge timing, stale-state observations and original approval words/timestamp or an explicit unquoted marker. Flag a stale Page row without editing that Page from the scoreboard. Bind review and verification evidence to the relevant revision. Shared account attribution never proves a human approved; distinguish an unlocated quote from evidence of an unauthorized action. For an apply-triggering or other one-way action with an unquoted approval, prioritize a coordinator request to locate the quote; the preset escalates the missing record to the owner at the next weekday check if still absent. This paperwork path must not delay escalation of independent evidence of an actual unauthorized one-way action. Respect installation-specific urgency and avoid duplicate reporting already owned by a production reporter.

## 6. Monthly harness hygiene and pruning

Inventory active profiles, memories, routines, room membership, shared-skill usage, duplicated context, experiments past sunset and idle rooms. Classify keep/compress/sunset/escalate with evidence, not just age or message count.

For each proposed cut, preserve its former purpose and protection, owner, scope, replacement evidence, expected benefit and rollback condition. Cultivate a small durable lesson or reuse an existing skill; do not replace whole personas or add duplicate prose for every incident. Never soften or delete fail-closed safety, merge, review, implementer-independence or follow-up protections merely to reduce ceremony. Preserve the installation's no-local-apply and docs-first boundaries and the requirement to attach promised future follow-up to a supported named routine rather than a chat promise. If unsure whether a rule supplies such a protection, escalate rather than cut it. Apply changes only within explicit authorization.

## 7. Post-prune regression guard

Default: examine the changed surface 7–14 days after cuts, or at the next weekly review after a cut or health regression. Use real CI, product and harness signals; absent telemetry is **dark**, not green. Classify hold-cut, watch or restore-candidate. A restore proposal must link the regression to lost protection; restore the smallest justified control rather than reinstating all old ceremony. Present at most one restore decision. Stay quiet when there were no relevant cuts and health did not worsen. No automatic restore or deletion is implied.

## 8. Cross-fleet dry-run retro

After substantial multi-party refinement/review-room orchestration, not routine one-to-one work, inspect the work trajectory: slicing versus room dumping, right first specialist, actual decomposition, panel contribution, time-to-artifact/chatter, invented facts and skipped source verification. For product/experience work, check that Product/domain and UX assessment preceded Principal/implementation. Produce a short note with 3–5 concrete improvements and proposed durable lessons, then select only the bounded authorized work. Durable changes still need the applicable confirmation. This diagnosis is not a mandate to enlarge the next weekly change budget.

## 9. Turn repeated corrections into the right artifact

On the second repetition of the same correction, consider a test, lint rule, schema, existing skill or evidence stamp when that expresses the invariant better than more persona text. Existing gate stamps stay stamps; do not duplicate them into prose. Keep deterministic checks deterministic. A proposed artifact still needs regression testing and authorization; do not create a new gate merely because a correction repeated.

## Classified and retained misses

Do not reopen a previously classified and deliberately retained miss without new evidence or owner reversal; reopen only a reviewer surface that changed. Do not loosen tests or patch around a classified miss merely to make a summary green. The inspected shipping routine references this rule, but the separate original skill body was not yet verified when this draft was written. This is a bounded captured instruction, not a claim to reproduce all of that skill's exceptions.
