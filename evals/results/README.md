# Benchmark score history

Commit sanitized score records here after each evaluation worth retaining,
including unchanged, regressed and incomplete results. Keep raw artifacts in
ignored `.eval-results/` and private configuration in `evals/local.json`.

Export from the repository root:

```sh
mise run eval:archive -- --source .eval-results/RUN --date 2026-11-13
# A saved-answer judge stage also binds the original paired run:
mise run eval:archive -- --source .eval-results/JUDGE-RUN \
  --parent .eval-results/RUN --date 2026-11-13
mise run eval:history:check
```

Inspect the generated JSON and commit it with the skill change being evaluated.
The exporter writes a content-addressed filename and refuses to overwrite a
different record. A correction is a new record; retain the earlier evidence.
CI validates every record against the [closed schema](../history.schema.json).

Records contain fixed labels, numeric scores/usage/coverage, source hashes and
commit identity. The exporter recomputes deterministic checks from recorded
decisions and the original hashed fixture. Summary scores, rationale, judge
reasons, prompts, paths, account identifiers, tool payloads, environment and
configuration text are excluded. Model labels use an allowlist; an unknown
name becomes `other`, and backend identity stays `unverified`.

Compare records with matching fixture, harness, model and context provenance.
`adapter_sha256` fingerprints recorded adapter-file hashes after removing file
paths. A paired `source.manifest_id` is the runner's canonical manifest ID;
`parent_manifest_id` joins a separate judge stage to that paired run. A saved
stage's own manifest is hashed in full because that format has no embedded ID.
Raw artifact hashes bind the measured inputs without publishing their contents.
`contexts_sha256` identifies the selected injected context; `exporter_sha256`
binds the exporter, public schema and regrading code used to create the record.
`git_dirty=true` and missing token/trace coverage limit reproducibility. Hashes
bind local artifacts; they do not attest execution by an untrusted harness.
Source mode is declared evidence, and mock scores remain `plumbing_only`.
Git review remains responsible for preserving earlier files.
Records labeled `other` or `unknown` need private provenance review before
comparing model configurations.

The seeded records describe the earlier pilot, **not the current skill
revision's performance**. The final pair passes 3/3 for each variant, the learning
judge disagrees after order reversal, and the interrupted run stays blocked.
None proves a skill benefit or persistent learning. For canary checks,
development attempts and usage gaps, read the [validation note](../../.github/knowledge/validation/2026-11-13-local-pilot.md).
