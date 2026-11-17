# Fleet visual guide

These diagrams explain the design. They do not certify that a runtime has implemented it or that improvements have been proven in live use. The three SVGs are the generic lifecycle, learning and adoption views; the Mermaid diagrams after them show roles, the merge gate, routines and where the human is asked. Each depicts only what the protocols describe, and the review panel has no fixed seat order: seats are chosen by risk and score the same exact head independently.

## How the pieces work together

![Fleet architecture: frame, execute, verify, authorize, observe and learn](diagrams/fleet-architecture.svg)

The coordinator owns the outcome. Skills and delegated roles supply capabilities; they do not transfer that ownership. Readiness and permission are separate checks. Durable state keeps evidence and next actions visible across handoffs.

[Read the architecture contract](../skills/engineering/fleet-architecture/references/architecture.md).

## Who advises whom, and who decides

```mermaid
flowchart TB
    H["Human gatekeeper<br/>one-way doors only, in their own words"]
    C["Coordinator<br/>router and thread holder<br/>the only router to the human"]
    A["Advisor to the coordinator<br/>measures and pressure-tests<br/>no execution authority"]
    I["Implementer<br/>integrates and verifies"]
    P["Risk-owned reviewer seats<br/>chosen by risk; domains plug in"]
    X["Adversary paired with a defender"]
    D["Done-ness interrogator<br/>called at claims-done"]
    R["Routines bound to the coordinator<br/>curator, watchers, reporters, wakes"]
    K["Housekeeper<br/>audits and proposes"]
    C -- "routes slices" --> I
    C -- "wakes seats for the risks a change carries" --> P
    C --> X
    C --> D
    I -- "claims-done with exact head" --> C
    P -- "scores go to the coordinator only" --> C
    X -- "scores go to the coordinator only" --> C
    D -- "evidence audit" --> C
    A -. "advice; a block can be overruled" .-> C
    A -. "only for one-way risk, a role change or a declined serious miss" .-> H
    C -- "one prepared question at a door" --> H
    R --- C
    K -. "proposals" .-> H
```

Specialists answer the coordinator, not the room and not the human. The advisor sits beside the coordinator: it cannot merge, apply, change product code or wake agents without a finding. A function may share an agent with another unless a protocol requires independence.

## The merge gate

```mermaid
flowchart TD
    G["Merge authority granted by the human"] --> W["Ephemeral watcher created for one change<br/>gates written into its prompt"]
    W --> E{"Event"}
    E -- "new head" --> V["Approval void<br/>request delta re-score"]
    V --> E
    E -- "check failed" --> F["Route to the failure's owner<br/>never rerun or retrigger"]
    E -- "changes requested" --> Q["Route to the implementer"]
    E -- "CI passed" --> T{"All gates hold on the exact head?<br/>1 every routed seat scored PASS, no open must-fix<br/>2 required checks ran and are green<br/>3 automated review landed, clean or triaged<br/>4 threads empty or triaged<br/>5 clean merge, no deploy or apply running, no unapplied one-way plan<br/>6 net control-script delta at or below zero<br/>7 merge pins the head"}
    T -- "no or still waiting" --> E
    T -- "yes" --> M["Merge with pinned head<br/>log which seat acted"]
    M --> Z["Watcher ends<br/>pipeline reporter reads the result"]
```

The watcher automates the checks; it does not create authority. A human waiver is recorded in their words and never covers the exact-head reviewer scores or an unapplied one-way-door plan. When all agents merge under one shared platform login (the low-friction default), the platform cannot tell them apart, so the ledger records the acting seat. The recommended target is a distinct least-privilege identity per agent.

## Routines: standing and ephemeral

```mermaid
flowchart LR
    subgraph S["Standing: durable, recur, silent when nothing changed"]
        direction TB
        S1["Scheduled: twice-daily wake, weekday brief, board curator, peer check-in, weekly retro, monthly prune"]
        S2["Event: repository listener, pipeline result reporter, alarm responder"]
    end
    subgraph T["Ephemeral: one purpose, end on a condition"]
        direction TB
        T1["Event: merge-on-green watcher, ends on merge or close"]
        T2["Scheduled or event: deadline watch, ends at completion or deadline"]
    end
    C["Coordinator turn that makes a promise"] -- "creates the routine in the same turn" --> T
    S -- "wake the coordinator only for something to route" --> C
```

## Where the human is asked

```mermaid
flowchart LR
    W["Work item"] --> Q{"One-way door?<br/>deletes or replaces, public exposure, secret mints, money, data deletion, production migrations and applies, IAM outside an approved shape"}
    Q -- "no (two-way)" --> GO["Coordinator acts, then reports the outcome"]
    Q -- "uncertain" --> DOOR
    Q -- "yes" --> DOOR["Prepare all reversible work first<br/>ask one structured question"]
    DOOR --> Y["Only the human's own words authorize<br/>relayed or shared-login approvals do not count"]
    Y --> GO2["Proceed without confirmation rounds<br/>record a blanket yes verbatim with timestamp"]
```

Status, scores, reviews, drafts, dry plans, opening and fixing changes, merges within granted authority and starting the next increment never interrupt the human.

## Learning and evolution

![Evidence-backed learning and measured evolution, including unknown outcomes](diagrams/fleet-evolution.svg)

**Learning** retains a scoped, evidence-backed lesson. **Evolution** changes a skill, routine or operating rule and checks whether behavior improves. A written retro is neither proof of learning nor proof of benefit. An inconclusive result is different from a measured lack of benefit.

The Grok Bot preset uses distinct loops rather than one generic retrospective: daily oversight, weekly fleet retro, coordinator calibration, monthly hygiene and a post-prune watch. They serve different purposes and should not silently replace each other.

[Read the evolution contract](../skills/engineering/fleet-architecture/references/evolution.md) · [Read the preset retrospective routines](../skills/engineering/fleet-preset/references/retrospectives.md).

## Preset or build-your-own

![Shared core branching into configurable architecture and opinionated Grok Bot preset](diagrams/fleet-adoption.svg)

The abstract path (`fleet-architecture`) defines functions, protocols, an autonomy layer and thirteen provider-neutral primitives, and leaves domains and tunable values to the installation. The prescriptive path (`fleet-preset`) binds named domain seats to those functions and defaults to the strict rules: exact-head reviewer PASS, an automated review that is clean or triaged, no deploy or apply running, and a net control-script delta at or below zero. Relaxations are recorded opt-ins. Translation to other runtimes is a plan from the primitive map; apart from skill install, non-Grok bindings are unverified and it is not an implemented compiler today.

## Editable assets

The SVG files and the Mermaid blocks in this file are the source. The SVGs include titles and descriptions for accessibility and need no renderer; Mermaid renders on the code host.
