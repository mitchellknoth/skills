# Local pilot validation — 2026-11-13

The local Codex path works on the owner's Mac using existing ChatGPT login.
This is evidence of a runnable, limited decision-probe harness, **not evidence
that adding these skills improves outcomes**. No API credentials or new API
billing were used. The PR remains a draft; nothing was merged into main.

Implementation tested from clean commit
`f6c2e6ecd18c29c42040e8802479e04c998c3bd1`, Codex CLI `0.156.1`, requested model
`gpt-6-luna`, low reasoning effort, Mise `2026.9.11`, pinned Python `3.12.14`.
Mise installed Python into an isolated task directory. The unrelated website
checkout and global security configuration were not modified.

| Check | Observed result |
| --- | --- |
| `mise run eval:check` | 47 package/runner/canary tests + 8 mocked Harbor tests + 21 adapter/collector/probe tests: **76 pass**; generated core current |
| `mise run eval:smoke` | Six mock trials pass; plumbing only |
| `mise run eval:codex:probe -- --otel` | Installed CLI completes one synthetic model request with **empty tools**, **no auth headers**, 8 MCP entries disabled; 12 native OTLP log records, no rejected requests; zero inference |
| Final `eval:run -- --allow-inference` | Eight live CLI calls, six complete trials; baseline **3/3**, candidate **3/3**; no observed deterministic regression or improvement; verdict **inconclusive** |
| Final `eval:codex:canary -- --allow-inference --otel` | All five checks pass: marker unchanged, no write, no marker disclosure, no tool events, expected decisions; 16 OTLP log records, zero rejected requests |
| Separate `eval:judge` on saved learning pair | Two completed live calls, answers blinded by A/B and reversed; judge chooses B in both orders, so mapped preferences **disagree**; no reliable quality preference |
| Independent review | Separate agent reviewed exact-version controls and adapter/runner; implementer reviewed its synthetic probe. Timeout, source hashing, malformed usage, missing trace coverage, canary reporting and interrupted-run journaling findings fixed |

The final paired run reports trace and usage coverage for **8/8 calls**, zero
observed tool events, 25,265 input tokens, 827 output tokens, zero reported cached
input and reasoning output tokens. The final canary reports 346 input and 44
output tokens. Together those final runs used nine live CLI calls and reported
25,611 input / 871 output tokens. The separate saved-answer judge stage reports
1,756 input / 106 output tokens in two calls. Its artifact binds the saved
answers, original fixture/manifest and the current judge code separately.

Final paired manifest ID:
`ec76e903042b1a7a561908e15a64ce357ef67bfc411907f2f169f28d95a67c79`.
Artifacts remain local under ignored `.eval-results/`: `final-paired/`,
`canary-final.json`, `probe-verified.json`, `live-judge-learning/`, and
`check-final.log`. Raw final answers are saved locally for grading; minimized
observers discard prompt text, account/resource attributes, reasoning text,
arguments, paths, IDs, tool outputs and raw spans. Inspect before sharing.

## Development attempts and usage accounting

An earlier 14-call planned run saved all eight agent responses (six trials,
both variants 3/3), but its process ended before saving judgments or a final
summary. The cause is unresolved. A process check confirmed it had stopped;
it is **not a completed 14-call run**. Its recorded agent usage is 25,256 input /
793 output tokens. Zero to six judge CLI calls might have been attempted;
their results and usage are unknown. The separate two-call stage above did
not rerun those agents or retroactively complete that run. The final eight-call
run was then repeated from frozen, clean source to verify complete execution.

One earlier canary completed inference but its result was rejected because an
unstable-feature startup warning appeared as an error item. That call's usage
was not retained. A minimal diagnostic completed with 194 input / 9 output
tokens, and an intermediate canary passed with 344 input / 44 output tokens.
Earlier configuration failures occurred before model events/inference. The
unstable-feature warning is now suppressed per invocation while unexpected
error/tool/unknown events still fail closed.

Across artifacts plus that diagnostic, **21 live CLI calls have known usage**:
53,161 input / 1,823 output tokens. This is a lower bound for the session;
the discarded canary and any unjournaled judge calls are excluded. Native
Codex transport retries can create additional provider requests. Subscription
allowance was consumed; dollar cost and remaining allowance are unavailable.
No subscription usage is labeled free, and CLI call limits are not dollar or
provider request caps. Synthetic local probes performed no model inference.

## What the evidence does not establish

- Actual backend model identity is **unverified**. The explicit requested slug
  is recorded; `actual_model=null`, `model_identity_verified=false`. Native
  telemetry's configured model label is not backend attestation.
- This uses a custom text-only system prompt/catalog with injected skill files,
  equally for both variants. It does not validate stock Codex, native lazy skill
  discovery, other harnesses, real merges or production actions.
- Deterministic gate ordering is a **declared proposed sequence**. Native events
  observe the actual text-only harness, where zero tools are expected. Tool
  rejection in a trace is detection after observation, not prevention; the
  independent configuration controls remove tools before inference.
- No hidden chain of thought is available. No reasoning summaries appeared in
  final runs; if they appear, only event counts are retained. Summaries would
  not be ground truth for grading.
- Native span experiments received some spans but also rejected requests. The
  final pilot exports **logs only**. Logs are not spans; no Phoenix/Langfuse UI
  integration or complete native span pipeline is claimed.
- Three public pointed families, one repeat and an order-sensitive judge do
  not establish generalization or persistent learning. The learning case only
  carries an earlier answer into a fresh hypothetical step. Human calibration,
  held-out scenarios and real action/state benchmarks remain future work.
- The host CLI and stable local/admin configuration remain trusted. Inventory
  is not an atomic lock against concurrent managed MCP changes; ephemeral is
  not a promise of zero host disk activity. Telemetry completeness is unknown.
- Harbor export/bridge tests are mocked; actual Docker/Harbor execution remains
  unverified. The installed Claude CLI remains incompatible/unauthenticated.

See [the run guide](fleet-evaluations.md) and
[adapter controls](../evals/adapters/README.md) for reproducible commands and
the collector alternatives considered. Hosted CI is recorded separately in
the PR; local passes do not prove hosted execution.
