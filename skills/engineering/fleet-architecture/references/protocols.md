# Protocols: decisions, authority and evidence

Domain-free rules that the [functions](functions.md) follow. Numeric values marked *reference* come from the fleet these rules were distilled from; they are installation-policy parameters, not universal constants. Each protocol has field evidence in [field-evidence](field-evidence.md).

## 1. Door classification

Classify every action before taking it.

- **Two-way door:** reversible at acceptable cost. The coordinator acts and shows. Examples: opening a change, filing an issue, drafting, reviewing, a dry plan, starting the next increment of an epic.
- **One-way door:** hard or costly to undo. The human decides. The installation lists its doors in the human's words. The reference list: deletes or replaces, public exposure, secret mints, money, data deletion, production migrations, infrastructure applies, and permissions outside an already approved shape. See the [interrupt contract](autonomy.md#2-the-interrupt-contract).
- When classification is uncertain, treat it as one-way until decided, then record the decision.
- A **blanket yes covers what it names**, plus the changes that carry it. Re-asking for an exact-revision yes after a blanket yes is toil. Re-ask only for a high-stakes item the yes did not name.
- **PASS is not enable. Merge is not deploy.** A score reports readiness; it switches nothing on. Find where the deploy-like step actually runs and hold *there*, naming every pending item in the human's yes.

## 2. Authorization provenance

Authorization comes from the human's own words, recovered from their own channel. Everything else is a claim to check.

- An agent's say-so, a relayed approval, a bot-to-bot quote, a paraphrase, or an approval posted under a shared identity is **not authorization**.
- When the coordinator relays a yes to an executor, the relay quotes the human **verbatim with the timestamp**. The executor relies only on that relay from the coordinator, never on a quote passed between other agents.
- A standing yes recorded by an agent must (a) quote the words, (b) carry the timestamps, and (c) say that an agent posted the artifact under the standing yes. It is never presented as fresh assent.
- A grant to one agent is not a grant to another. Record whom it names.
- Authorization and readiness are separate. A valid yes survives while readiness is pending; do not ask twice for unchanged scope. See [readiness](readiness.md).

## 3. Exact-head scoring and delta re-score

- A seat scores PASS, PASS-with-note or BOUNCE at an **exact head revision**, with IDs: must-fixes `MF-<seat><change>-<n>`, softs `S-...`. A score for an older head is stale.
- Every must-fix carries `class=<kebab>`. **The seat that raises it owns the fix**, sweeps every instance of that class in the diff, reports the sweep count and re-scores. The implementer does not fix other seats' must-fixes.
- Every head move needs a **delta re-score**. A push that changes only tests is re-scored by the seat owning the finding; other seats carry forward. Any non-test change re-wakes every routed seat. A seat never gives the only PASS on its own patch.
- Hold pushes until every routed seat scored the current head or explicitly carried its score. One fix push at a time per change.
- **Round cap** (*reference* 3 fix pushes): without a PASS, seats holding must-fixes send the coordinator an approach note (*reference* 10 lines: keep, split or redesign) and the coordinator picks. A third fix-forward in the same class within a window (*reference* 7 days) needs an approach note even at round one.
- **Pre-existing** findings never block, but one that sits on a live one-way door still escalates to the human.
- **No PASS without checks that ran** on the head. A skipped, cancelled or not-run required check is not green.
- Every score lands in an **append-only scores log**: seat, head, verdict, IDs, evidence pointer. Every must-fix fix also logs raised-by, fixed-by, sweep count and whether the implementer re-entered.
- Seats send scores only to the coordinator, who posts one rollup.

## 4. Merge-on-green watcher

Merge authority is the human's to grant. When granted, the coordinator merges a reviewed change only when **all** hold at merge time:

1. Every routed seat scored the head being merged, or explicitly carried its score, with no open must-fix.
2. Required checks are green **and ran**, or the human's written waiver applies.
3. Where the installation runs an **automated code review**, it has landed on the exact head and is clean or triaged; in progress or absent means wait. Review threads and comments are empty or triaged. Untriaged comments block even when every seat passed.
4. The merge is clean against current default state; branches need not be up to date.
5. One merge at a time, and no deploy or apply is running from an earlier merge.
6. The default branch holds no unapplied plan with a one-way-door change the human's yes does not cover.
7. The merge pins the head (an expected-head guard), so a late push cannot ride in.
8. The net delta in control scripts against default state is at or below zero ([control budget](#8-control-budget)).

A **PR-scoped watcher** automates the checks (full gate and event table in [autonomy](autonomy.md#the-ephemeral-merge-on-green-watcher)). It listens to one change; on CI passed it re-verifies 1-8; on a new head the approval is void and it requests a delta re-score; on CI failed it routes the failure and never reruns; on changes requested it routes to the implementer; and it **deletes itself** when the change merges or closes. Never mark a change ready and merge it in one step when readying triggers a plan; the watcher waits for the plan.

**Fix forward.** A human may waive waiting for every hosted check on staff PASS. A waiver names its condition and scope. It does not cover: a deterministic break the change itself causes; a change whose readiness triggers a plan that has not finished; a merge during a running apply; or unapplied one-way-door plans on the default branch. Recover a failed post-merge run with a catch-up fix-forward change, never a rerun, and make its plan include every unit still owed.

**Verify before claiming.** After merge, read back who and what merged. When agents share one platform identity (the low-friction default), "merged by" cannot tell them apart, so log the acting agent when it happens. The recommended target is a distinct least-privilege identity per agent, which restores attribution at the source ([identity](primitives.md#identity-shared-by-default-per-agent-recommended)).

## 5. Challenge before you log

The coordinator does not relay a claim it has not tested. Cheap challenges, in order:

1. Is the "pre-existing" label true on the default state, or did this change introduce it?
2. Did the check pass, or was it skipped, cancelled or never reached?
3. Do the claimed counts match a re-run?
4. Is the evidence on the same head as the claim?
5. Is "locked" or "done" backed by an actual artifact update, not prose?

A seat that cannot see a grant says so, and defers to the coordinator and human rather than assuming it.

## 6. Routing and wake rules

- Wake only on change. Priority means: a final score on a head, a bounce carrying a one-way-door must-fix, or a real question needing a decision. Everything else is non-urgent. No acknowledgement-only or FYI wakes.
- Shared rooms stay silent when nothing is new. A post is about three lines and points at a board item, change or file.
- Claims-done is a **direct priority ping to the coordinator** with the exact head. A room post or a comment does not wake the router, so it does not count as convening the panel. Idle time between "ready for panel" and "panel scored" is a harness bug.
- After a long directive from the human, restate it in ten lines or fewer, let them confirm, then act.
- A routing record names the seats woken and omitted, with the reason. A diff that changes what a build bundles wakes the operability seat.

## 7. Evidence hygiene

- Suites may be gated behind a label or a flag. A draft without it gets findings, not a PASS.
- No reruns, empty commits or manual dispatches to retrigger a check. A failure is real (route it) or an infrastructure fault (fix forward with a real change). Tool-call retries cap at three.
- When hosted capacity is unavailable, run the same checks locally on the head merged with default state. Local runs are evidence; they waive no seat.
- To update a branch with default state without tripping local pre-commit hooks, use the platform's **server-side branch update**. It keeps review history, needs no force-push and bypasses nothing. Never skip hooks with a flag.
- Read the job list, not the summary badge: a green summary can hide skipped jobs, and a red one can be a cancelled post-step with every test green.
- A seat does not add the label or dispatch the run for another seat's check.

## 8. Control budget

Adding a control costs more than it looks. When a check blocks a change, **delete or simplify the check** and move what it truly protected into a test; never add an exception. Before a push, check the net control-script delta against default state. Growth is a last resort that needs the human's own words.

- Ask in order: can the blocking check be deleted? does the infrastructure tool already do it? does the CI platform already do it? can it be a test beside the module?
- Tests assert behavior. A test that reads source text and matches patterns passes on a decoy; delete it or replace it with a runtime check.
- Approval rituals bound to comment IDs, record files or yes-line formats are antipatterns; use an environment gate or ordinary review.
- A prune retires a control only after stating what failure it prevented and what now proves it unneeded.

## 9. Escalation ladder

Climb one rung at a time; stop at the first rung that resolves it.

1. **The seat** resolves within its lane.
2. **The seat that raised a must-fix** fixes it and re-scores.
3. **Approach note** after the round cap: the seats holding must-fixes send keep/split/redesign; the coordinator picks. A redesign returns to the implementer only after a written design agreement.
4. **The coordinator** decides any two-way door, and orders conflicting fix pushes.
5. **The advisor** is consulted on a merge or a contested call; its `block` is advice.
6. **The human** decides one-way doors, a serious advisor block, and forks only they can take.
7. **Break-glass** (coordinator only): push the smallest possible diff to default state only when the product itself is in jeopardy (outage, active exposure, data loss in progress). Log it, tell the human immediately, run checks after, and hold a full review within a day. Break-glass never covers one-way doors, and no other agent may do it.

## 10. Attention budget

The human's attention is the scarcest resource.

- **One decision at a time.** Outcome first, then where we are in the sequence, what just happened in plain language, then the one next move. Keep identifiers, roles and paths out unless the decision needs them.
- **The interrupt bar:** an apply, a secret, spend or credentials, an irreversible or destructive step, or a fork only the human can take. Nothing else interrupts.
- No status theater and no optional confirmations. The coordinator is the only router to the human; specialists do not fan into their chat.
- Notify on verdicts the human asked to hear about, in their own channel, not only in a room.
- A "locked" claim needs the updated artifact. Claims without evidence count as misses.
- Plans state key results (what is true when done, for whom, under which constraints), not the how.
- Report size is a budget too: helper briefs about 1 KB, agent-to-agent reports under about 1 KB.
