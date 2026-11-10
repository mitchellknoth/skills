# Designing proof stages

Map the path from trigger to observable outcome, then pick stages around consequential unknowns rather than mirroring every component. A stage should have an observation that can fail and change the next decision. It need not be the smallest possible code change.

For each stage record: the claim, environment and identity, input and expected observation, authorized action and stopping condition, actual result, and what remains unproven. Keep these records proportional to the work. A local mock can validate a contract; it does not establish that a deployed provider accepts the real identity or that a real trigger reaches the service.

Example: a notification-driven agent may first parse a synthetic notification, then exercise a local worker with a fake tool, then verify a separately authorized read using the real workload identity, and finally trace a real trigger through the deployed path. Successful parsing does not prove the real trigger, and a successful tool read does not prove the agent called it. Skip stages that do not reduce a material uncertainty.

When a live proof is unavailable, make useful progress with a substitute, label the substituted boundary, and name the smallest next authorized check. If the observation contradicts the hypothesis, update the approach before retrying. Do not repeatedly exercise a failing live system without a changed condition or appropriate authority.
