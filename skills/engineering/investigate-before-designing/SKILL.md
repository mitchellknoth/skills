---
name: investigate-before-designing
description: Investigate existing implementations and adapt their patterns before designing a feature or integration. Use when relevant precedents may already exist in accessible code, documentation, or configuration.
---

# Investigate before designing

Find what already works before treating a design question as unanswered. Preserve the user's objective and constraints; a precedent is evidence, not a mandate to copy it.

1. Identify the capability, relevant boundaries, and consequential unknowns. Search the current repository and instructions first; inspect named reference implementations and accessible documentation or configuration when relevant. Follow the actual call or data path, ownership, and tests rather than relying on names or descriptions alone.
2. For each useful precedent, distinguish observed behavior from inference. Compare its context, dependencies, permissions, and constraints with the requested use case. Identify what can be reused, adapted, or should not be carried over, and why.
3. Resolve questions from available evidence before asking the user. Stop searching when further exploration is unlikely to change the decision; do not turn a small task into an open-ended survey. If a consequential uncertainty remains, propose or perform a bounded experiment within the user's authorization.
4. Present a concise adaptation map with source pointers, the proposed approach, material differences, and unresolved questions. Continue implementation when requested and sufficiently supported. Do not imply that a code path or example proves deployed behavior without observing it.

When multiple precedents conflict or the transfer is not obvious, consult [comparing precedents](references/comparing-precedents.md). Use it selectively; routine investigations need not load it.
