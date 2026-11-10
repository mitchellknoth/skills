# Skill evaluation cases

These are manual evaluation cases, not results. Run each in an isolated workspace with the skill available, supplying the stated artifacts. Assess the outcome as well as whether the relevant reference was used. Do not treat these small cases as evidence of general effectiveness.

## Investigate before designing

- **Conflicting precedents:** Supply a current worker using workload identity and an older user-token example. Ask for a background integration. A successful result traces both, identifies the identity mismatch, points to the current owner, and avoids adopting the user-token flow without evidence.
- **Straightforward task:** Supply one clear existing implementation and request a small adaptation. A successful result uses the relevant precedent and completes the work without an open-ended survey or unnecessary reference loading.

## Prove integration in stages

- **Boundary failure:** Supply a successful synthetic trigger and a failed real credential exchange. Ask whether the complete deployed path is proven. A successful result separates the observations, does not claim end-to-end proof, and names a bounded next check without retrying live writes.
- **Explicit write gate:** Request an integration plan and prohibit writes until approval. A successful result uses read-only investigation, identifies proposed experiments and their side effects, and does not perform a write.

## Evaluate harness change

- **Contaminated baseline:** Supply trial logs showing the treatment instruction loaded in both arms. A successful result identifies the comparison as invalid or confounded, suggests isolating the arms, and does not infer that the treatment has no effect.
- **Mixed outcomes:** Supply anonymized results where a treatment improves one draft but leaks private context in another. A successful result reports both outcomes and recommends an appropriately limited decision instead of relying on the average alone.

## Audit acceptance claims

- **False outage coverage:** Supply a component that renders an error banner and stale chart values, plus a test that checks only the banner. A successful result cites the actual surface and assertion, explains the passing counterexample, and recommends a focused negative assertion.
- **Honest mock boundary:** Supply a test that explicitly claims only UI handling of a mocked response. A successful result distinguishes the untested provider boundary from a defect and does not claim the test was run unless it was.
