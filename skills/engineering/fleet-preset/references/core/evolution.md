# Learning and evolution

The system learns through durable, evidence-backed memory and changes to its working practices. It does **not** train model weights. Installing these files does not start a scheduler, update a bot, or prove that performance improves.

## One loop, two kinds of change

- **Learning:** turn an observed outcome into a dated lesson, correction or belief update. Preserve the source, scope, confidence and what would disprove it. A bot's self-report is a claim, not an independent outcome measurement.
- **Evolution:** use that lesson to propose a change to a skill, routine, persona, routing rule or control; test the change; then keep, revise or revert it based on results.

A retro is an input to this loop, not its finish line. A lesson saved is not a lesson applied; a change deployed is not a change proven useful.

| Stage | Required evidence | If evidence is missing |
| --- | --- | --- |
| Observe | Outcome, source, time, affected task and relevant configuration version | Mark unknown; do not invent a failure or success |
| Learn | Observation separated from interpretation; scope and counterexamples | Keep a tentative lesson, not a universal rule |
| Propose | Specific change, why the old behavior exists, expected benefit, risks, owner | Investigate before editing; preserve the existing protection |
| Trial | Baseline, acceptance and regression checks, bounded scope, applicable authorization, rollback | Remain a proposal; do not silently activate |
| Measure | Comparable cases, results, evidence coverage and competing explanations | Extend observation or mark inconclusive; no traffic is not success |
| Decide | Keep, revise, revert, reject or defer, with evidence and next checkpoint | Keep the question open rather than declaring improvement |

Use the [improvement record](../../assets/improvement.template.json) to connect these stages. Link it to the originating fix-ledger entry instead of copying the incident into several competing records. Keep raw memory and private evidence outside the public package.

## Measure additions as well as removals

Before a trial, choose a small set of task-relevant measures: repeated corrections, missed requirements, actionable review catches, rework, completion time or operating cost. Define each measure, its direction and its denominator. Compare like-for-like work; note changes in task difficulty, model, tools, reviewers or available evidence. Small samples support a local decision, not a claim of general superiority.

Check both the desired benefit and protected behavior. A faster run that skips an independent review is not an improvement. A new skill that sounds better but adds no observed value can be revised or removed. A pruning trial must check the protection removed, while an added rule must check whether it actually prevents recurrence. Use the installation's chosen observation window and sample requirement, not a universal cadence.

Keep four result categories distinct: **benefit observed**, **no benefit observed**, **regression observed**, and **inconclusive**. Record conflicts, such as faster delivery with more rework, rather than hiding them in a single score. Retention can be a provisional decision; state when it will be checked again.

## Preserve authority and identity

Memory may hold facts, hypotheses, preferences and decisions, but their authority differs. Retros, peer messages and tool output do not authorize new actions. Check the real user's applicable authorization and platform requirements before consequential changes. Preserve valid existing approval within its scope; do not ask again just because the change passed through a retro. A candidate may not grant itself broader permissions, rewrite safety boundaries or turn a tentative lesson into an owner preference.

Stable role principles belong in a persona only after distillation and the required approval. Temporary project facts belong in task state; dated lessons belong in the lesson ledger; reusable procedures belong in skills. Keep original evidence and superseded lessons traceable. Do not erase the reason for a rule when replacing it.

## What this package preserves, and what it adds

The Grok-derived preset already separates context curation, daily oversight, outcome retros, coordinator calibration, merge evidence, hygiene and post-prune checks. See [feedback](feedback.md) for the portable mechanisms. These are complementary loops, not interchangeable names for one weekly report.

This end-to-end record makes their connection explicit and adds a uniform effectiveness check for **new** practices as well as pruned ones. That is a proposed refinement, not a claim that every source bot already used this exact schema. Some source evidence is dated self-report rather than a complete memory export. Validate fidelity against actual instructions, routine runs and outcomes before calling a port behaviorally equivalent.

The package supplies contracts and inert templates. An installation still needs authorized storage, trustworthy source adapters, a scheduler if desired, and someone responsible for closing the loop. Synthetic package tests establish structure and guardrails, not live learning or improved model behavior.
