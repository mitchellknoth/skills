---
name: audit-acceptance-claims
description: Audit whether acceptance tests substantiate claims about user-visible behavior and failure paths. Use when asked to assess test coverage, acceptance completion, or a claim that a workflow is fully covered.
---

# Audit acceptance claims

Treat a green test as evidence that its assertions passed, not proof of every behavior described by its title or documentation. Perform a read-only review unless the user also requests changes.

1. Identify the exact claims, acceptance criteria, revision, and relevant user-visible behavior. Trace the production path through the UI, providers, API, and data boundaries as applicable; inspect the tests, fixtures, mocks, and assertions at the same revision.
2. Map each important claim to the assertions that support it. Ask what realistic regression could still pass: stale or fabricated values, a missing branch, a failure state that hides only part of the data, a stuck range, or a mocked boundary that bypasses the real path. Use only scenarios relevant to the task.
3. Check test isolation, determinism, and available execution evidence where these affect the conclusion. Run safe checks when appropriate and authorized; distinguish tests you inspected from tests you actually ran. Do not claim production, real-provider, or deployment coverage from a mocked or local environment.
4. Report actionable gaps first with precise references, the failure scenario, and its impact. Separate defects from untested boundaries and overbroad wording. State when no material findings were identified and recommend the smallest meaningful behavior-level assertion or corrected claim.

For broad coverage claims or complex fixture boundaries, consult [claim mapping](references/claim-mapping.md).
