---
name: fleet-preset
description: Use Mitchell Knoth's opinionated delivery-fleet preset: coordinator ownership, risk-routed independent review, evidence-bound readiness, bounded review loops and durable follow-through. Use when the user explicitly asks for this prescriptive preset or invokes fleet-preset; not for the neutral architecture template.
---

# Opinionated delivery-fleet preset

A proposed reusable distillation of an experienced fleet, not an exact export of a live account. This first version deliberately reconciles known inconsistencies and leaves installation authority private. It has not been proven equivalent to the source runtime.

## Shared core, bundled for standalone installation

Read [architecture](references/core/architecture.md), [readiness and authority](references/core/readiness.md), and [runtime adapters](references/core/adapters.md) before applying the preset. Read [evaluation](references/core/evaluation.md) before changing or testing it. These are generated copies of the canonical architecture core, included so this skill works when installed alone. Do not edit generated copies; use the repository synchronization script.

The `fleet-architecture` skill is the neutral alternative, not a required additional installation. This preset supplies explicit process choices below; it does not grant permissions.

## Preset workflow

1. **One front door owns completion.** The coordinator decomposes and routes work while retaining integration ownership. Specialists return evidence and next actions, not merely opinions.
2. **Frame meaningful milestones.** Capture intent, non-goals, acceptance, dependencies and source-of-truth references. Surface conflicting visual or product references before committing to derivatives.
3. **Test behavioral changes first where practical.** Record meaningful failing evidence, then implement and verify. When test-first is unsuitable, explain why and use the best available evidence. Do not manufacture a red commit or claim tests ran when they did not.
4. **Route by risk.** Use [role cards](references/roles.md). Separate implementation from independent acceptance. Do not invoke every role for every change or conflate QA, domain correctness and UX fidelity.
5. **Resolve findings and bound loops.** Serialize conflicting fix pushes and final merges. The implementer retains integration ownership. A reviewer may propose or make an authorized patch, but cannot be its sole independent acceptance. After three substantive review rounds without convergence, stop automatic cycling and propose keep/split/redesign with evidence. Do not restart the count merely by renaming the task.
6. **Separate authorization from readiness.** Batch permission is not a waiver of required final-head reviews, checks or material findings. Preserve valid approval while preparing the work; do not ask twice for unchanged scope. Use the core action contract on every execution entry point.
7. **Observe completion.** Record the actual resulting revision/action and verify the relevant outcome. Carry deployment dependencies and residual risks forward. A merge, green summary or completed routine is not sufficient proof of deployment or user acceptance.
8. **Close the feedback loop.** Reuse existing oversight. Significant findings have an owner, disposition, checkpoint and evidence of closure. Track last successful output, not merely Active status. Keep quiet when healthy; surface actionable changes rather than recurring noise.

## Adoption

Copy [preset.template.json](assets/preset.template.json) to private installation configuration and fill the placeholders. It supplies process preferences, **not permission**. Persistent bot creation, schedule activation, external messages, merges and deployments remain unconfigured until authorized and supported. Read [preset choices](references/choices.md) before adopting or modifying the preset.
