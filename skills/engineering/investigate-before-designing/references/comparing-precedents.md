# Comparing precedents

Trace each candidate far enough to answer the actual design question. An example can reveal the shape of a solution while relying on a different identity, lifecycle, data contract, or operating environment. Its presence alone does not establish that it is used or working in the target environment.

Compare only decision-relevant differences: entry point and caller, ownership, inputs and outputs, identity and permissions, failure behavior, dependencies, tests, and evidence of operation. Prefer the current owning implementation over a stale example when they conflict. Explain why a precedent is relevant, which parts transfer, and which assumptions need verification.

For example, an existing service may authenticate a tool call on behalf of a user, while the requested background worker needs a workload identity. Reuse the client and error handling if they fit; do not infer that the user's credential flow solves worker authentication. If the missing identity contract controls the design, identify its owner or test the authorized exchange before selecting the integration.

If sources disagree and the difference matters, identify their revision and scope, then check the current owner or runtime when accessible. Report any unresolved conflict rather than silently picking the most convenient source. Stop once remaining differences are unlikely to change the decision.
