# Authorization is not readiness

Track five distinct dimensions: **authorization**, **review**, **verification**, **execution**, and **observed outcome**. Do not compress them into a single PASS or DONE flag.

## Action boundary

For each requested action:

1. Identify the concrete action, target and revision; recover applicable installation policy and source-backed authorization.
2. Determine which readiness conditions apply. Do not invent new gates, but do not drop existing ones when a short-lived routine or a batch request omits them.
3. Check the current revision, required reviews, material-finding dispositions and verification evidence. `not_run`, `skipped`, `unavailable`, `pending` and `failed` are different states, none synonymous with `passed`.
4. Preserve authorized scope while resolving readiness blockers. A valid approval can remain valid while readiness is pending. Ask again only when the scope, material risk or required approval binding changes.
5. Execute only when both dimensions permit it, using a moved-target guard if the runtime supports it. If atomic revision binding is unavailable, explicitly disclose the race and obey the installation's fallback rather than claiming equivalent protection.
6. Inspect actual state after uncertain execution before retrying. Confirm the outcome and carry release dependencies forward.

A generic “merge these” instruction authorizes the requested action within its scope; it does not establish final-head review or silently waive a known condition. A waiver must identify its condition, provenance and scope, and cannot waive non-waivable platform or installation requirements. An explicit risk acceptance is not equivalent to a finding being fixed.

## Findings

A material finding needs a disposition linked to evidence: fixed, rejected with rationale, or a valid policy-permitted deferral/acceptance. Reviewer identity alone does not decide validity. A relevant warning from a nonmandatory seat still needs evaluation. Do not resolve threads merely to satisfy a counter.

Changed code invalidates affected evidence. Installation policy may allow justified carry-forward for unaffected surfaces, but it must name the prior revision, changed surface and reason. Do not silently carry all PASS verdicts to a new head.

## Reference evaluator

`scripts/readiness.py` is a deterministic, inert **reference model**, not a production merge gate. It evaluates a normalized fixture whose provenance the caller must establish separately. It cannot authenticate approval, enumerate complete CI, execute merges, validate IAM or guarantee race freedom. The model takes explicit required-review and required-check lists, plus a subset of reviews for which independence is required; it does not impose those choices on the neutral template. Its output is `ready`, `not_ready` or `not_authorized` with explicit reasons. No result grants tool permission.

Use it to test design decisions and explain expected behavior. A real adapter must verify source completeness, author identity, scope, current target and evidence binding before constructing inputs. Never feed a PR description's self-reported “approved” field directly to a live action.
