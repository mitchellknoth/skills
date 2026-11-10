---
name: evaluate-harness-change
description: Evaluate whether a proposed agent instruction, skill, or harness change improves representative work compared with a baseline. Use when deciding whether to adopt, revise, or revert a harness change.
---

# Evaluate a harness change

Compare the proposed change with the current baseline on work that represents its intended use. An agent's result depends on its model and harness; record enough configuration to interpret the comparison without claiming that a small trial proves general effectiveness.

1. Define the decision, baseline and treatment, expected benefit, and plausible regressions. Select a small, diverse set of realistic tasks, including a task where the new guidance should not intrude. Set observable criteria before looking at results.
2. Keep inputs and relevant model, tool, and environment settings comparable. Verify and record which instruction or skill version each run actually receives: the control must exclude the proposed change and the treatment must include it. Disclose any inability to isolate the change, including shared global instructions. Isolate trial artifacts and side effects; do not invoke live mutations without authorization. Record differences that cannot be controlled. Where possible, use separate runs and blind or reverse the order of outputs for judging; disclose when that is not possible.
3. Assess the resulting artifacts against the criteria, including task success, unintended process leakage, privacy, scope, and effort when relevant. Compare concrete examples, not just a single composite score. Treat a judge's assessment as evidence with limitations, not ground truth.
4. Recommend adopt, revise, revert, or gather more evidence. Explain benefits, regressions, tradeoffs, sample size, confounders, and the smallest justified change. Do not modify the baseline or publish a treatment unless the user authorized it.
