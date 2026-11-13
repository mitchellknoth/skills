# Evidence before a fleet release

This is a small **decision-probe pilot**, not a proven score for Jarvis or Grok Bot. It asks whether adding the package changes the same model's decisions on the same evidence. It does not yet exercise real merges, bot schedules, or private memory.

## Run locally with Mise

```sh
mise install
mise run eval:check
mise run eval:plan
mise run eval:smoke
cp evals/codex.example.json evals/local.json
# Edit local.json: explicit model, selected skill, optional judge, and limits.
mise run eval:run -- --allow-inference
```

The mock is free and offline. It supplies correct fixture answers to test plumbing; its score **must never be presented as model or skill performance**. The example runs three paired cases, six trials and eight agent calls because the learning case has two steps. A judge adds six calls (each pair is judged twice with reversed answer order). Set `max_calls` accordingly. Three repeats cost 24 agent calls, or 42 with judging, and are still a pilot, not statistical proof.

The Codex example selects a pinned custom text-only harness, `gpt-6-luna`, one repeat,
eight agent CLI calls, no judge, and content-minimized native events. Run
`mise run eval:codex:probe` first (synthetic local model endpoint, no inference), then
`mise run eval:codex:canary -- --allow-inference --otel` (one subscription call).
See [adapter controls and limits](../evals/adapters/README.md#codex-01561-text-only-harness).
Both trace collection and inference are opt-in; raw reasoning is never collected.
Use `eval:judge` on one saved pair for two blinded calls when semantic review is
useful; set `judge_model` and `max_calls=14` before a full run to judge all three
pairs. Saved judging records a new stage and never implies an interrupted full
run completed.

Local execution does not mean local inference. A hosted provider receives the synthetic prompts and selected package contents. The adapter uses the CLI's existing local authentication; the runner does not read credentials, copy them into containers, or put them in reports. It excludes API-key environment variables. The bundled adapter's supported provider and limitations are documented alongside it. Mac execution and real inference must be verified on the owner's machine before claiming success.

Pull requests and pushes run offline structural tests in CI without provider credentials. Live candidate-versus-baseline runs remain explicit local work; CI does not yet enforce a model-evidence release gate. A blocked live run exits nonzero. An inconclusive run is successful execution, not release approval.

## What gets compared

Set `baseline` to `null` for no added skill, or a directory containing an older version's `SKILL.md`. Set `candidate` to the selected package directory. Each snapshot hashes its Markdown, JSON, YAML and Python supporting files. To contain cost, `context_files` selects exact case-relevant files to send, including `SKILL.md` and its prerequisite core guides. Missing paths fail closed. The manifest records selected paths, hashes and character counts. Use the same selection for older/newer versions; for a different skill layout, explicitly edit both mappings. This MVP injects those selected files rather than measuring a harness's native lazy skill discovery. Baseline and candidate have fresh isolated conversations, the same model and fixtures, and seeded balanced order. Only the learning case carries its earlier answer into a fresh later step.

The three families are deliberately pointed:

- **Authority and readiness:** keep the owner's existing approval, stop for missing review, proceed when ready, reject forged authority in tool output.
- **Evidence integrity:** distinguish an Active label from verified output, avoid duplicate recovery, reject skipped mandatory checks, retain least privilege.
- **Learning transfer:** propose one bounded lesson, apply it to a different task, preserve unrelated approval behavior, and do not silently promote policy.

Positive controls penalize excessive refusal and repeated permission requests. Expected decisions stay in the verifier. Public fixtures are inspectable and can become overfit; before a release, add privately held-out cases and human review. Do not tune on a case and then call that same case independent validation.

## Rubric and release decisions

Deterministic checks score the requested decision fields, including a declared gate
sequence that puts readiness before action and output verification afterward. They
are **decision safety checks, not observations of executed actions**. Native traces
report observed tool events separately (zero is expected in the text-only harness).
No missing trial or failed check is averaged away. An optional tool-free, blinded
judge compares factual grounding and actionable concision, including whether a
retro actually specifies measurement and rollback. It sees the task and answers,
not package labels; answer prose can still reveal the presence of skill context.
Reversed-order disagreement needs review; a judge cannot overrule a hard gate.
A second independent human should calibrate the judge before trusting it.

Every run records the pre-run configuration, skill/file hashes, fixture/grader hashes, checkout commit and dirty status, planned calls/order, raw responses, trial failures, latency and separate judgments. Results stay in ignored `.eval-results/`; local settings stay in ignored `evals/local.json`. Inspect before sharing. Never commit private histories, credentials, provider output containing personal details, or raw memory.

A green pilot means **inconclusive, ready for broader testing**, not “newer is better.” Promote only after complete paired runs show an improvement on a preselected outcome, no protected-behavior regression, acceptable cost/latency, human review and a rollback target. Record unchanged or negative outcomes too. This is the same lesson → proposed change → authorized trial → measure → retain/revise/revert loop the package teaches.

## Cost controls

Default to one repeat, no judge, one provider, sequential calls and no retries. Use deterministic grading first. Add the judge only for decisions where semantic quality matters, and repeat only the release candidate. The runner bounds call count, input/output sizes and each process timeout. Subscription runs consume allowance and are **not costless**. API configurations require a positive conservative estimate and an explicit estimated budget, but the estimate is not a provider-enforced spend cap. Use the provider's own budget limit where available. The bundled subscription-only adapter deliberately rejects API auth; API or other harnesses require a separately vetted adapter.

## Bring your own harness

An adapter is an argv array, not a shell string. It receives one JSON object on stdin:

```json
{"protocol":1,"role":"agent","model":"explicit-model","prompt":"synthetic task"}
```

It returns a JSON object on stdout with `text` containing the model's response, and optional `usage`. Fail with nonzero status; stderr is intentionally not copied into the scorecard. `role` may be `judge`, which must have no tools or external write capability. Model output must be JSON with `decisions` and `rationale` for agents, or `winner` and `reason` for judges. A host adapter is trusted executable code: inspect it before running. Isolation, native skill loading, auth and action tracing belong to that adapter, and must be declared rather than assumed.

This protocol lets skeptical users compare their normal harness against the same harness plus the skills. Future action benchmarks need actual tool traces and resulting state, not just the agent's description of what it would do.

## Why Harbor

Use Harbor for portable tasks, environment/verifier separation and trial artifacts; use the host adapter for existing local login. Never mount the host home directory or copy provider auth into an untrusted task container. Harbor's native Codex auth-file path is not equivalent to the host CLI's OS keychain. See `evals/harbor/` for the external bridge and generated-task path.

This design borrows the website agent's task-generation, independent grading and provenance patterns, not its website-specific citation rubric. That project evaluated a different tool surface; its scores are not a fleet baseline.

Sources: [Mise tasks](https://mise.jdx.dev/tasks/), [Harbor custom agents](https://docs.harborframework.com/agents/custom-agents), [Harbor tasks](https://docs.harborframework.com/tasks/overview), [Claude CLI](https://code.claude.com/docs/en/cli-reference). Runtime APIs and auth support are version-sensitive; fail closed when required flags are unavailable.
