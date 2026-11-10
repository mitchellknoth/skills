---
name: prove-integration-in-stages
description: De-risk an uncertain integration through bounded experiments that build toward an end-to-end outcome. Use when a user wants to validate integration assumptions or establish what an early proof actually demonstrates.
---

# Prove an integration in stages

Break the requested outcome into meaningful hypotheses, prioritizing uncertainties that could change the architecture or stop progress. An early proof is a step toward the goal, not permission to declare the full integration complete.

For each stage:

1. State the hypothesis, relevant boundary, and observation that would support or refute it. Select the smallest realistic experiment that can distinguish the alternatives, using existing facilities where practical.
2. Identify prerequisites, permissions, side effects, and a stopping condition. Respect explicit approval gates; use a synthetic or local substitute when a live action is not authorized or available, and say what that substitution cannot establish.
3. Run the experiment within scope. Record the environment, inputs, observations, failures, and source of evidence. Distinguish simulated, local, deployed, and end-to-end results; do not infer identity, access, provider behavior, or production readiness from a narrower check.
4. Decide whether to continue to the next stage, revise the approach, or report a blocker. Pursue independent work while a prerequisite is unavailable. Avoid repeating a failed experiment without a changed hypothesis or condition.

Report the outcome against the user's objective, the evidence and its limits, and the next consequential proof or action. If implementation was requested, continue beyond the proof when authorized and supported by the results.

For multi-boundary integrations or when a stage's result could be mistaken for end-to-end proof, consult [designing proof stages](references/designing-proof-stages.md).
