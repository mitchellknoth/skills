# Native local-auth bridge (experimental)

`claude_local.py` uses the official installed Claude Code CLI and its existing
`claude.ai` login. It never reads, prints, copies or exports credential files.
The Claude adapter intentionally does not support API keys, cloud-provider credentials, Codex,
or `--bare` (which changes authentication behavior).

Configure adapter argv as `["python3", "evals/adapters/claude_local.py"]` and set
`FLEET_EVAL_ALLOW_REMOTE=1` only for an approved live run. This permits sending
benchmark prompts and answer text to Anthropic; local execution is not offline
inference. Subscription limits still apply. Use synthetic/redacted fixtures.
No login, install, or paid inference happens automatically.

## Compatibility status

Offline tests do not establish live provider compatibility. On the first Mac
preflight, Claude Code 2.1.167 lacked the required `--restricted` and
`--safe-mode` flags and was not authenticated, so this adapter cannot run there.
The separate Codex adapter below supplies a narrowly configured text-only harness.

Safety controls: argument arrays (no shell), empty temporary working directory,
restricted/safe mode, empty built-in tools, deny all tools, strict empty MCP,
no custom setting sources, disabled slash commands, no persisted sessions,
one turn, 120-second timeout, and a small environment allowlist. Raw stderr,
auth-status JSON and provider configuration are never emitted. The exact
requested model must appear alone in `modelUsage`; otherwise the call fails.
There is no retry or provider/model fallback in this adapter. The runner remains
responsible for a total call/usage budget and terminating cancelled children.

**Limitations:** this is CLI-level isolation, not an OS sandbox. Managed policy
can still apply, including policy hooks. The official CLI remains trusted code
with access to its user's account. Do not run this bridge on an untrusted or
unreviewed managed machine. The startup help check is intentionally conservative:
some valid CLI versions hide flags, and those versions will be rejected rather
than silently run with weaker controls. Native authentication and the combined
flags require a live compatibility smoke test on the owner's machine before
claiming provider support. Mock tests prove the wrapper, not the provider.

Sources:
- https://code.claude.com/docs/en/cli-reference
- https://code.claude.com/docs/en/headless

Offline adapter tests:

```sh
(cd evals/adapters && python3 -m unittest -v test_claude_local.py)
```

## Codex 0.156.1 text-only harness

`codex_local.py` uses the installed official CLI's existing ChatGPT login. It
does not open, copy or export provider credential files. API-key, alternate
provider, proxy and `CODEX_HOME` environment overrides are excluded. Both the
native login status and `forced_login_method="chatgpt"` are checked. No API
billing fallback is supplied. Only `gpt-6-luna` is supported by this pilot.
Subscription allowance is consumed; dollar cost is unavailable.

Use `evals/codex.example.json` for the paired run. It budgets eight agent CLI
calls with no judge by default. Setting `judge_model` and `max_calls=14` adds six
blinded, reversed-order judge CLI calls. These are **CLI calls**,
not a provider request or token cap: native Codex can retry network/stream
requests. The wrapper never retries. Calls are sequential, output is bounded
while streaming, input delivery is included in the timeout, and the outer
runner kills the process group on timeout. No Docker is needed.

This evaluates **a custom text-only Codex harness with injected skill context**,
not default Codex, native skill discovery, or a raw model. Its small, shared
system prompt and authoritative custom model catalog deliberately remove
shell, patch, clock, async messaging and other model-advertised tools. Feature
overrides remove apps/plugins, browser/computer/image tools, skills, memories,
subagents, hooks and Code Mode. Per-run config excludes user settings and
project documents; the filesystem sandbox is read-only and sessions ephemeral.
These changes apply equally to baseline, candidate and judge. Global security
settings are never modified. CLI-level prevention relies on the inspected CLI
and stable, trusted local/admin configuration; it is not universal OS isolation.

Native `mcp list --json` enumerates the superset of configured server names and
transport types, including the user layer that `exec` ignores. The inventory
is consumed transiently on the host; it can contain sensitive MCP transport
configuration, so it is never logged, persisted or returned. Only validated
names/types are used to explicitly disable every server. Disabled entries have
inert valid transports because an empty table merges and an entry with only
`enabled=false` is invalid. Plugins/apps are separately disabled. A concurrently
added managed server could race enumeration; do not use this harness on an
untrusted or changing managed machine. It does not start MCP servers to inventory
them. Provider credentials never route through a collector or inference proxy.

`mise run eval:codex:probe` inspects one unauthenticated synthetic Responses
request using the installed CLI and the same tool controls. It requires an
empty tool array, no auth headers and a completed fixture roundtrip. This is
stronger evidence than a mock, but is not live provider/model validation.
Native Codex may fetch first-party configuration metadata during bootstrap;
all model requests in the probe go to the loopback fixture, with no inference
or billing. The probe is separate code and cannot switch the live adapter's
provider. The canary is separately opted in:

```sh
mise run eval:codex:canary -- --allow-inference --otel
cp evals/codex.example.json evals/local.json
mise run eval:run -- --allow-inference
# Optional: judge just one saved pair, two calls, with a separately recorded manifest.
mise run eval:judge -- --source .eval-results/RUN --case learning \
  --judge-model gpt-6-luna --allow-inference --out .eval-results/JUDGE-RUN
```

`--otel` starts a short-lived loopback OTLP/HTTP JSON receiver and enables the
native log exporter only for that call. It records known event names and
counts; **logs are not spans**. Compatibility experiments received some actual
spans but also rejected requests, so the pilot leaves the trace exporter disabled.
No span UI integration or complete native span pipeline is claimed. Native `--json` events provide
ordered structural item events and usage, and `trace_native_events=true` opts
in to retaining their minimized form in paired trial artifacts. Text, arguments,
paths, IDs, tool outputs, account/resource attributes and raw spans are discarded
by the observers. User prompt logging is disabled and tool-result logging is
set to zero bytes. The paired runner still saves the model's final answers for
grading; use synthetic data and inspect results before sharing.

Trials and judgments are journaled incrementally. An interrupted full run stays
`blocked`/`in_progress`; a separate saved-answer stage does not turn it into a
completed full run or infer missing usage. Saved judging verifies the fixture
and source manifest, rechecks step completeness, hashes the answer artifact,
and records current judge code. It never regenerates agent answers.

Reasoning summaries, if present, are counted but their text is discarded. They
are not hidden chain of thought, explanations of causation or grading ground
truth. Trace observers do not block actions. The independent configuration
controls remove tools before inference; unexpected tool/unknown/error events
invalidate the trial after observation. A zero-tool trace alone proves neither
prevention nor safety in another harness.

`requested_model` records the explicit CLI argument. `actual_model=null` and
`model_identity_verified=false` are intentional: this version's exec events
do not attest actual model identity, and telemetry's configured model name is
not backend attestation. No score establishes raw-model identity or persistent
learning. The judge compares final-answer grounding and concision, uses the
same requested model, and still needs independent human calibration.

Version-pinned primary references:
- [Tool exposure](https://github.com/openai/codex/blob/rust-v0.156.1/codex-rs/core/src/tools/spec_plan.rs)
- [Exec events](https://github.com/openai/codex/blob/rust-v0.156.1/codex-rs/exec/src/exec_events.rs)
- [Configuration schema](https://github.com/openai/codex/blob/rust-v0.156.1/codex-rs/core/config.schema.json)
- [Model metadata](https://github.com/openai/codex/blob/rust-v0.156.1/codex-rs/protocol/src/openai_models.rs)

## Collector choice

The pilot keeps a standard-library receiver because its needed output is a few
redacted event counts. [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/configuration/)
can route/filter logs and spans if the volume grows. [Phoenix](https://arize.com/docs/phoenix/tracing/concepts-tracing/otel-openinference/exporter)
accepts OTLP spans; useful LLM views would need verified span semantics and an
OpenInference mapping, not just Codex log forwarding. [Langfuse self-hosting](https://langfuse.com/self-hosting/deployment/docker-compose)
adds a Docker deployment and supporting infrastructure. None is installed or
claimed integrated here. The Docker boundary remains separate from this pilot.
