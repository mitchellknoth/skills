# Python workflow: Mise owns tools, uv owns dependencies

Accepted 2026-11-13 after PR #3 review.

Mise pins Python and uv and owns the task interface. CI calls the same
`eval:check` graph used locally. uv synchronizes `uv.lock` into `.venv` with
Mise's exact Python interpreter and Python downloads disabled. Task commands
use `uv run --locked --no-sync` after that dependency step. Refresh the lock
with `mise run eval:lock` after intentional dependency edits.

Pytest runs the existing unittest cases; rewriting working assertions would add
churn without strengthening the checks. All 76 original cases passed unchanged
under pytest before new tests were added. New history tests use pytest fixtures
and parametrization where they reduce repetition. `jsonschema` validates the
closed public score format; its dependencies and pytest are locked by uv.

Python adapter aliases resolve to the active interpreter. An explicit path
supports a deliberately different external harness. Native Codex/Claude
installations retain their own login and version checks; Mise does not install
or reconfigure them. Client installation commands remain native to each client.

The optional Harbor verifier keeps a minimal Python container rather than
installing a development toolchain or mounting host authentication. Export
derives its image version from `mise.toml`. The verifier's internal Python
command and portable skill-script shebangs are intentional: they execute in
their own runtime, not the source checkout. Docker execution remains unverified.
