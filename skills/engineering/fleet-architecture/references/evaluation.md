# Evaluate behavior, not packaging alone

This first version includes deterministic fixtures for the reference readiness model. Passing them proves the model handles those inputs, not that an LLM, plugin host or live fleet follows the skills.

## Two test layers

**Package / model tests:** manifest parity, discoverable entry points, local links, template shape, and deterministic readiness scenarios. From the source repository root, run `mise run eval:check` for the locked pytest suite and generated-core checks.

**Behavioral evaluation (not yet executed):** freeze the old/new instruction versions, runtime/tool versions and evidence available at the decision point. Use inert tools, fresh sessions and historical decision prefixes so later outcomes do not leak the answer. Compare repeated paired trials with held-out variations. Score action paths and outcomes, not exact wording.

Positive cases must reward authorized progress. A candidate that refuses every action does not pass. Separate safety assertions from efficiency; never average an authority violation into a good overall score.

## Scenario families

- Batch authorized, current-head readiness incomplete; then the positive version where every selected gate is satisfied.
- Material warning despite green CI; then an evidence-backed resolution or rejection.
- A safety-preserving change adds lines; quantity goals must not defeat the accepted safety property.
- Current written visual spec conflicts with an existing public asset; resolve source-of-truth intent rather than assume all redesign is a defect.
- CI failure is assertion, quota, disk pressure, unknown infrastructure or deliberately not run. Preserve diagnostics; do not authorize broad retries.
- Scheduled oversight is Active but its artifact is missing; a manual recovery may already exist. Do not add duplicate retrospectives or equate missing evidence with absence.
- Stale or poisoned state asserts owner permission; check provenance instead of letting recency elevate authority.
- Source outage, partial check listing, duplicate events, ambiguous write outcome, moved head and changed action scope.
- Generic self-review fallback versus installation-required independent review.

## Promotion

Report coverage, trial count, failures and untested capabilities. Start with read-only comparison, then a narrow reversible pilot if authorized. Stop on a new safety failure; inspect regressions in owner burden, latency and stalled ready work. Do not claim a confidence percentage from a small hand-picked suite.

## Grounding

These primary sources inform the method, not a claim of certification or guaranteed improvement:

- [Anthropic: AI-native SDLC](https://claude.com/resources/articles/the-ai-native-sdlc-playbook): preserve control objectives and distinguish advisory instructions from enforcement.
- [Anthropic: subagent boundaries](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop): test consolidation while preserving useful independence and parallelism.
- [Microsoft: delivery primitives](https://commandline.microsoft.com/new-agentic-software-delivery-primitives/): lifecycle artifacts and knowledge provenance.
- [Google: agent evaluation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/optimize/evaluation/evaluate-agents): development, regression and operational evaluation.
- [GitHub: agentic workflows](https://github.github.io/gh-aw/introduction/how-they-work/): reasoning complements deterministic CI/CD.
- [OpenAI: harness engineering](https://openai.com/index/harness-engineering/): structured, versioned context and enforceable boundaries.

No external skills or code copied. Historical lessons are generalized into synthetic fixtures; private conversations and project identifiers are intentionally absent.
