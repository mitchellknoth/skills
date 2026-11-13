# Native local-auth bridge (experimental)

`claude_local.py` uses the official installed Claude Code CLI and its existing
`claude.ai` login. It never reads, prints, copies or exports credential files.
It intentionally does not support API keys, cloud-provider credentials, Codex,
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
Codex 0.156.1 was authenticated, but a tool-free mode was not established.
There is **no bundled Codex adapter or working local-auth judge on that setup**.
Read-only filesystem sandboxing does not prevent reads, all tool use, or prompt
injection; rejecting tool events after they occur is not preventive isolation.
Do not weaken the judge's no-tools contract or copy credentials into Harbor
containers to work around this. A compatible provider CLI or a separately
verified, contained host-auth bridge is required before live evaluation.

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

## Codex host-auth research (not implemented)

Codex CLI **0.156.1** on the owner's Mac was authenticated with ChatGPT during
the Mac preflight. This is
not yet a compatible adapter. A host-side process could preserve the native
login without extracting tokens or copying `auth.json` into Harbor containers.
We intentionally do not bundle an adapter that cannot satisfy the trial contract.

The inspected CLI offers `exec --ignore-user-config` (authentication still uses
`CODEX_HOME`), `--ignore-rules`, `--ephemeral`, `--strict-config`, `--json`,
`--output-schema`, and `--sandbox read-only`. Candidate per-call controls include
turning off web search and automatic project instructions; disabling shell,
browser/computer use, apps/plugins/hooks, memories, subagents, image tools and
skill discovery/install; and using a fresh temporary working directory with
synthetic input over stdin. These flags are a research direction, not a verified
isolation recipe. They do not establish a universal no-tools mode.

Two concrete blockers remain:

1. **Effective MCP configuration:** `codex mcp list --json --ignore-user-config`
   is rejected by this CLI. Therefore that command cannot verify the same
   configuration used by isolated `exec`. An empty `mcp_servers` table is not
   proof that inherited servers were removed.
2. **Actual model identity:** the exact-version `exec` JSON event definitions
   contain thread IDs, items and token usage, but no effective model field.
   The requested `--model` value cannot be reported as verified actual identity.

Do not weaken the existing judge contract, silently relabel requested model as
actual model, or accept a contaminated trial to work around these blockers.
Tool-event rejection would invalidate a trial *after* an attempted action; it
would not prevent that action. Read-only does not prevent all host reads or
external side effects, and ephemeral does not promise zero disk activity.

Before implementing a live bridge, establish effective tool/MCP controls and
model attestation for the pinned CLI (or a separately inspected transport).
Then run an explicitly authorized synthetic canary covering attempted file,
shell and network/tool access, malformed output and model mismatch. Record
observed behavior and remaining limits. No such live canary has run.

Any future bridge needs bounded runtime/output/call counts, no automatic retry,
no API-key or billing fallback, stripped provider/environment overrides, and
native authentication without credential copying. It would evaluate the
**Codex harness**, not a raw model. Host execution still sends inference to the
provider. Subscription authentication is neither free/unlimited usage nor
local inference; plan limits and provider billing must be checked before runs.
A no-tools Responses API adapter is a separate option requiring separately
authorized API authentication and billing, not repurposed ChatGPT credentials.

References:
- https://developers.openai.com/codex/noninteractive
- https://developers.openai.com/codex/config-reference
- https://github.com/openai/codex/blob/rust-v0.156.1/codex-rs/exec/src/exec_events.rs
