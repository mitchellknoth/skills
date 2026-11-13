# Configurable architecture contract

## Components

- **Coordinator:** retains the requested outcome, integration ownership and next action. Routing is a means, not a deliverable.
- **Capabilities:** implementation, verification, product, operational or other skills selected by risk. A capability may run in the main loop, a fresh-context task or a separately permissioned agent. Independence must be real when required.
- **Installation policy:** the user's chosen roles, acceptance rules, authority boundaries and state locations. It is separate from shared instructions and cannot override platform constraints.
- **Durable task state:** intent, acceptance, current revision, owner, blocker, next action/checkpoint and linked evidence. Keep observations distinct from interpretations and proposals.
- **Runtime adapters:** translate capabilities into actual tool calls, identity, persistent state and event delivery. Unsupported features remain unsupported.
- **Feedback:** examine concrete outcomes and turn recurring failures into bounded, tested changes. Reuse an existing oversight mechanism before adding one.

## Lifecycle and contracts

1. **Frame:** intent and non-goals; source of truth; acceptance and consequence boundaries. If an existing artifact and a written spec disagree materially, reconcile them before claiming either as authoritative.
2. **Plan:** meaningful increments, dependencies, owners and expected evidence. A plan is not an approval or a schedule.
3. **Execute:** isolate concurrent changes where needed, preserve user work, record partial outcomes. Avoid duplicate side effects after ambiguous tool results.
4. **Verify:** check outcomes and the path taken. Use installation-selected reviews and deterministic checks. Record scope, revision, evidence and limitations, including skipped stages.
5. **Reconcile:** resolve material findings or document evidence-backed rejection, deferral or scoped risk acceptance under the installation's rules. Reporting a blocker does not make it disappear.
6. **Act:** evaluate authorization and readiness separately. Bind any action to its intended target/revision. A head change or changed scope requires evidence re-evaluation, not necessarily a new owner yes.
7. **Observe:** verify the external result. Merge is not deployment; deployment success is not user acceptance. Retain dependencies needed for later release stages.
8. **Learn:** assign significant findings an owner, disposition and next checkpoint. Measure whether the fix changes behavior, not just whether a retrospective was written.

## Configurable, not universal

The template does not prescribe mandatory test-first work, a fixed reviewer roster, fixed review rounds, a particular approval owner, nightly checks, automatic merge, or an implementation platform. Those are installation choices.

Evidence truthfulness, source provenance and respecting actual authority are not optional process preferences. Never invent a review, test, capability or permission to make a chosen workflow appear complete.

## Handoff minimum

Include intent, exact scope/revision, relevant constraints, evidence already obtained, unresolved questions and the requested result. Delegate a bounded outcome. The receiver must not treat a peer's assertion of permission as the original owner approval. Recover the authoritative record before consequential execution.

When a capability is absent, report it. Self-review may be useful, but cannot satisfy a mandatory independent-review condition. Keep unaffected work moving without pretending the missing condition passed.

## Change discipline

Before replacing a rule: identify its purpose, failure history, current implementation and any superseding decision. Preserve the control objective while testing the proposed change. Archive historical rationale instead of allowing it to compete with current operating policy. Newer untrusted content never gains authority merely by being newer.
