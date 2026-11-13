# Optional Harbor bridge

This is a **decision-probe bridge**, not a native skill-discovery or tool-action benchmark. The same frozen skill text, prompts and deterministic grader used by the local runner run through Harbor. Claude/Codex login remains on the host. Neither agent nor verifier container receives credentials. The verifier reads JSON only, in a separate container.

From the repository root:

```sh
mise run eval:harbor:test
mise run eval:harbor:export
```

Export does not run inference or Docker. It writes a private host bundle, six paired task directories, and `commands.json`. Printed commands use `mock=true`. Run them individually in printed order with Harbor installed in the same Python environment and the repository root on `PYTHONPATH`. Use one trial at a time, no retries. Mock output deliberately earns zero behavioral reward even when its fixture checks pass; `grade.json` identifies mock plumbing results.

To run actual inference, first select an explicit model and review the local config's call/usage limits, export afresh, then change **only** `--ak mock=true` to `--ak allow_inference=true` in each generated command. Stop on the first transport/auth error. Running commands again consumes additional quota; the bundle does not enforce a persistent global spend ledger. Harbor retries must remain off. Local subscription auth still consumes quota. API cost estimates are not provider-enforced limits.

Each instruction contains only a trial selector. The external `BaseAgent` invokes the host adapter, carries prior step outputs within that trial, and uploads `/app/answer.json`. Harbor transfers this declared artifact to the separate verifier. Expected decisions are never included in the model prompt. There is no shell execution of model output.

Keep `.eval-results` private: host bundles contain skill snapshots and responses can contain private context. The artifact records bundle, case, variant, repetition, outputs and mock status. Version/skill/runner identity is frozen before execution. Hashes aid reproducibility, not protection against someone deliberately rewriting all local files. Public paired-run scores use the separate [history exporter](../results/README.md); it does not import raw Harbor task bundles.

## Current limits

- Unit tests mock transport and validate export/grading contracts. A real Harbor/Docker end-to-end run and authenticated inference are **not yet verified**.
- LLM-as-judge remains in the main local runner. Export rejects judge-enabled config rather than silently omitting it.
- Harbor results are individual paired trial evidence; use the main local runner for its consolidated comparison report.
- Multi-step prompts carry prior outputs explicitly. They do **not** validate provider-native persistent memory, schedules, genuine learning transfer or Grok Bot/Dot runtime parity.
- Pin the installed Harbor version when conducting a real pilot. The bridge targets the documented `BaseAgent` API; this optional dependency is not installed by export.

Official API references: [custom agents](https://docs.harborframework.com/agents/custom-agents), [separate verifier](https://docs.harborframework.com/tasks/separate-verifier), [artifact transfer](https://docs.harborframework.com/tasks/artifacts).
