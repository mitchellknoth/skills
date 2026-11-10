# Trial design

Select tasks that exercise the intended improvement, a plausible regression, and ordinary work where the change should not intrude. For example, evaluate a new writing instruction on a substantive draft, a privacy-sensitive edit, and a short outline. Define success and unacceptable failures before reviewing outputs.

Use isolated runs with the same task inputs and comparable model, tool access, repository state, and budgets. Record versions and actual loaded instructions. Inspect inherited repository and global guidance: if the treatment leaks into the control, or the treatment was not loaded, the trial does not compare the intended change. Fix isolation if possible; otherwise report the confounder and limit the conclusion.

When feasible, judge anonymized outputs in varied order, with a rubric that checks task completion and relevant regressions. Repeated runs help expose variability. Track which tasks improved or worsened and cite concrete examples; do not let an aggregate score hide a harmful failure. An independent judge improves separation but remains fallible. If unavailable, disclose self-assessment and avoid claiming independence.

Small samples support a tentative local decision, not a general performance claim. Compare implementation and maintenance cost as well as output quality when they matter. Recommend the narrowest intervention supported by the results, or more evidence when the outcome would change the decision.
