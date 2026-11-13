---
name: fleet-architecture
description: Design or operate a portable agent delivery architecture with configurable roles, handoffs, readiness, state and feedback. Use when the user asks for an agent fleet template, multi-agent delivery architecture, or invokes fleet-architecture. Does not impose the opinionated fleet-preset.
---

# Fleet architecture

A configurable architecture, not a roster of mandatory bots. Start with the smallest arrangement that can do the work and preserve the user's required independence and authority boundaries. One coordinator with on-demand capabilities may be enough; persistent specialist identities are optional.

## Choose the mode

- **Design:** turn the user's needs into an installation policy and capability map. No live setup or activation is implied.
- **Operate:** load an existing explicit installation policy, recover the current task record, then act only within the user's authorization and the runtime's permissions.
- **Evaluate:** replay a frozen case with inert tools. Label simulated decisions as simulated; do not mutate the live system.

Do not infer operate mode, standing permissions, schedules or merge authority from installation. If no policy exists, start in design mode and use [the template](assets/installation.template.json).

## Read progressively

1. Read [the architecture contract](references/architecture.md) for roles, state and lifecycle.
2. When preparing a consequential action, read [readiness and authority](references/readiness.md).
3. Before delegation, automation or a cross-harness move, read [adapter requirements](references/adapters.md).
4. For curation, oversight, retrospectives or recovery, read [feedback](references/feedback.md).
5. To evaluate or change the harness, read [evaluation](references/evaluation.md).

No dependency on a named company, repository, cloud, model, roster, review count, cadence or deployment platform. The template has **unset policy choices**, not concealed defaults from the opinionated preset. If the user wants the author's more prescriptive workflow, select `fleet-preset` explicitly.

## Configure, then deliver

Record which capabilities are needed, who owns integration, what evidence establishes done, where durable state lives, and what actions require authorization. Derive these from the task and installation, not an organizational chart. Do not require a meeting or a question for every empty optional field; use supported routine choices and surface consequential unresolved choices.

For work in flight: recover current facts, frame acceptance, execute bounded work, verify with the chosen independent/deterministic checks, reconcile findings, then evaluate the applicable action boundary. Advance authorized and ready work. If blocked, preserve valid authorization and make independent progress; do not repeatedly ask for the same decision.

Use [task.template.json](assets/task.template.json) as a portable example of durable evidence. A record is not itself authorization, trusted evidence, a transactional queue or proof of an external outcome. Bind references to the real source and revision. Keep private state outside the public package.

## Report honestly

Separate implementation, review, verification, execution and observed outcome. A process that ran successfully may still have produced a failed result. A missing record is not proof a control never occurred. A green summary is not proof skipped checks ran. Name unsupported capabilities instead of silently substituting a weaker workflow.
