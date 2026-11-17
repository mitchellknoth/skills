# What this preset chooses, preserves and changes

## Prescriptive choices (strict by default)

The preset's defaults are the live fleet's strict rules. Everything looser is an opt-in recorded under [Opt-in relaxations](#opt-in-relaxations).

One coordination front door; meaningful increments; test-first behavioral work where practical; risk-routed independent acceptance; serialized conflicting writes; durable next actions; quiet actionable oversight; and the strict rules below.

- **Merge gate.** A change merges only on an **exact-head PASS from every routed reviewer seat** (no open must-fix), an **automated review on that same head that is clean or triaged** (in progress or absent means wait; untriaged threads block), required checks that actually ran, a clean merge against default state, one merge at a time with no deploy or apply running, and an expected-head guard on the merge call. A new head voids the approval and triggers a delta re-score. Merge authority itself is the human's to grant.
- **Net script delta at or below zero.** When a check blocks a change, delete or simplify the check and move what it protected into a test; never add an exception. Growth in control scripts is a last resort that needs the human's own words. Tests assert behavior; a test that regex-matches source text is deleted or replaced.
- **Fix ownership.** The seat that raises a must-fix owns the fix, sweeps the whole class, reports the sweep count and re-scores. The implementer does not fix other seats' must-fixes, and a seat never gives the only PASS on its own patch.
- **Round cap.** After three fix pushes without a PASS, the seats holding must-fixes send an approach note (keep, split or redesign) and the coordinator picks. The count does not restart by renaming the task.
- **Valid permission and technical readiness are distinct.** Every merge-capable entry point uses the same gate, including batch requests and short-lived per-change watchers. A batch "merge these" never waives a gate.
- **Routines.** Standing scheduled wakes (oversight, retros, hygiene) and ephemeral per-change watchers that delete themselves on merge or close. See [autonomy](core/autonomy.md).
- **Human interjection is for one-way doors only.** Everything else proceeds and is reported afterwards. Only the human's own words authorize a one-way door.
- **No blanket CI retry.** Recover a failed post-merge run with a catch-up fix-forward change. A future bounded exception needs recognized failure classes, immutable input, terminal prior attempts, no ambiguous side effects, a budget and retained diagnostic history.
- Unrelated pre-existing debt does not automatically expand scope. A change that activates or worsens an old flaw must account for that interaction.
- No retired deployment mechanism, historical budget, named cloud, fixed cadence, public-site workflow or model choice is embedded here.

The template path remains separate and does not inherit these choices.

## Opt-in relaxations

Each relaxation is the owner's recorded decision with its words, timestamp, scope and condition. None is a default, and none is implied by a batch request.

- **Script growth.** A justified safety-preserving addition to a control script, when the owner says so in their own words for that change. Retire a check only after evaluating its purpose and replacement evidence.
- **Fix-forward waiver.** The owner may waive waiting for every hosted check on staff PASS. It never covers a deterministic break the change causes, a readiness that triggers a plan still running, a merge during a running apply, or unapplied one-way-door plans on the default branch. It does not waive the exact-head reviewer PASS or the automated review.
- **Cadence and thresholds.** Round cap, approach-note length and windows are reference values an installation may tune and record.

## Where the live fleet matches the preset

Source: [field notes](grok-field-notes.md), 2026-11-17. The merge gate, script budget, fix ownership and round cap above are what the live fleet does.

- **Merge authority in practice:** the live coordinator merges reviewed product PRs under a standing grant, on staff PASS at the exact head, an automated review that is clean or triaged, empty threads and a clean merge against default state. Fix-forward waivers are the owner's recorded words, not a default.
- **Identity:** the live fleet defaults to one shared platform login for merges, because it is low friction. Attribution is lost, so ledgers record which seat acted, and a shared-login approval is never a human yes. The recommended target, not what runs today, is a distinct per-agent identity (for example a GitHub App or machine user per bot) with least-privilege scopes. The preset keeps this installation-specific; changing platform identities or scopes is a one-way door that needs the owner's yes.

## Before customization

State why the fence exists, what failure it prevents, what currently enforces it and what will prove a replacement preserves its purpose. Keep authority decisions separate from project facts and ordinary memory. Changes to the preset are versioned and regression-tested; installation-specific exceptions remain private and explicit.

## Boundaries

No active automations, accounts, credentials, tool permissions or standing authority are included. Installing this preset is not approval to merge, publish or deploy. It also does not replace repository requirements or platform safety rules.
