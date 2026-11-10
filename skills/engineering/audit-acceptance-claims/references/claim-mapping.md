# Claim mapping

For each significant claim, map the customer-visible surface, relevant production path, test setup and assertions, and the boundary actually exercised. Use exact references where possible. Identify whether the evidence is inspected code, a test run, or an observation in a deployed environment.

Ask a concrete counterfactual: what change could violate this claim while the current test still passes? For example, an outage test that checks for an error banner could pass while a chart legend still displays stale totals. Confirm the production surface and assertion before reporting this as a gap; do not assume every screen has a legend or stale-data risk.

Look at the boundaries fixtures replace. A mock may verify UI handling of a known response without testing upstream data shape, authentication, cache behavior, or real provider availability. Such a boundary is not automatically a defect: it becomes a finding when the stated requirement needs that coverage or the claim overstates the evidence.

Propose a focused assertion at the user-visible boundary where feasible, or narrow the claim if the omitted behavior is outside the intended coverage. Separate test defects, product defects, and residual limitations. Do not claim a test failed or passed unless it was actually run.
