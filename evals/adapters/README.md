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
