# PR #3 review follow-up — 2026-11-13

All six comments in Mitch's [review](https://github.com/mitchellknoth/skills/pull/3#pullrequestreview-5897351325)
were retrieved with their full thread bodies and checked against base `eb83ba9`.

| Concern | Result |
| --- | --- |
| Mise throughout | CI uses a pinned official Mise action and `eval:check`; local Python tasks use the same task graph. Adapter aliases use the active interpreter; the Harbor image version derives from the Python pin. Intentional runtime exceptions are in the [ADR](../decisions/0001-python-toolchain.md). |
| pytest and uv | Pinned uv and committed `uv.lock`; pytest runs all 76 original unittest cases unchanged. New history tests use pytest fixtures and parametrization. |
| Historical scores in Git | Three sanitized records in `evals/results/`: complete paired run, incomplete interrupted run, separate learning judge. Closed schema and content identities protect against accidental raw-text or inconsistent-score publication. |
| External release skill | Pinned upstream curate-release reference and [release procedure](../release-process.md). Its draft gate applies; no history rewrite, PR metadata edit, merge or release occurred. |
| Internal validation location | Original pilot note moved under `.github/knowledge/validation`; public-facing score history remains discoverable. |
| README writing skill | Applied writing-for-agents: short adapter router, branch-specific references, explicit task links, and pinned contributor guidance in `AGENTS.md`. |

Local verification used Mise `2026.9.11`, Python `3.12.14`, uv `0.12.5` and locked
pytest `9.2.0`. `mise run eval:check` passed **96 tests**, generated-core checks
and validation of three public score records. `eval:plan` and `eval:smoke` also
completed; the latter passed six mock trials and remains plumbing-only evidence.
No new provider inference or subscription usage was needed for this follow-up.

History tests started red before implementation. Independent review then found
and reproduced inconsistent parent IDs, incomplete judge coverage accepted as
complete, and contradictory public scores. Targeted tests reproduced those
failures before the fixes. Export now binds input artifacts and selected context,
uses a manifest-bound mode for new runs, treats incomplete legacy evidence
conservatively, and validates arithmetic as well as the closed schema.

The public records are exports of the earlier measurements, not new benchmark
results for these changed skill files. The exporter enforces append-only file
creation; preserving older files in Git remains a review responsibility. Local
hashes provide provenance, not proof that an untrusted harness executed honestly.
Live model identity, action safety, persistent learning and Harbor/Docker limits
from the [original note](2026-11-13-local-pilot.md) still apply. Hosted CI and
thread resolution are reported separately at the final PR head.
