# Local provider adapters

Use a host adapter to run paired probes with an existing provider login.
The runner supplies synthetic prompts over stdin and retains final answers in
private local artifacts. Subscription calls consume allowance.

| Adapter | Configuration | Verified scope |
| --- | --- | --- |
| `codex_local.py` | `evals/codex.example.json` | Codex 0.156.1 / existing ChatGPT login / requested `gpt-6-luna`; live pilot completed |
| `claude_local.py` | `evals/local.example.json` | Mock-tested; installed Claude 2.1.167 lacks required flags and login |

Run commands from the repository root through Mise:

```sh
mise run eval:adapter:test
mise run eval:codex:probe -- --otel
```

For live runs, follow the [run guide](../../docs/fleet-evaluations.md), which
sets explicit inference opt-in, selected skill context and call limits.
`python` or `python3` as an adapter executable selects the current Mise/uv
interpreter; an absolute executable path selects a deliberate external harness.

Read [Codex controls](references/codex.md) before changing isolation, authentication,
judging or telemetry. It explains the custom text-only tool surface, native
events, logs-only collector, MCP inventory and unverified backend model identity.
Read [Claude compatibility](references/claude.md) before trying that adapter.

Final-answer decisions and declared gate order are scored separately from observed
tool events. Reasoning summary text is discarded; hidden chain of thought is
unavailable. The [public score history](../results/README.md) contains validated
counts and hashes; raw responses and trace data remain private.
