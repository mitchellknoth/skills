# Autonomy: the human is interjected only when it counts

The point of the workflow is that the human stays out of the loop. Work proceeds, is reviewed and merged, and the human hears about **results** and about **one-way doors**, nothing else. This file is the layer that makes that true: an interrupt filter, a contract for when the human is asked, the routines that keep the work moving without them, and a loop that starts the next piece unprompted. It uses the [functions](functions.md) and [protocols](protocols.md); provider bindings are in [primitives](primitives.md).

## 1. The autonomy model

Five mechanisms absorb interruptions before they reach the human.

| Mechanism | What it absorbs | Where defined |
|---|---|---|
| **Door classification** is the core interrupt filter | Every two-way action: the coordinator acts now. Only one-way doors reach the human. | [protocols 1](protocols.md#1-door-classification) |
| **Standing authorization and blanket yes** | Repeat asks. A yes covers what it names and the changes that carry it, so it is not asked again. | [protocols 1-2](protocols.md#2-authorization-provenance) |
| **Saved rules** (act and send) | Recurring low-risk actions and messages. A saved, scoped rule is the only standing exception to drafting for review. | [primitives: `outbound_rule`](primitives.md) |
| **Escalation ladder** | Disputes and blockers. The seat, the raiser, an approach note, the coordinator and the advisor all come before the human. | [protocols 9](protocols.md#9-escalation-ladder) |
| **Attention budget** | Noise. One decision at a time, a single structured question, no status theater. | [protocols 10](protocols.md#10-attention-budget) |

If a question can be answered by one of these, it is not asked.

## 2. The interrupt contract

**The human is interjected for exactly these, and for nothing else:**

1. Deletes and replaces.
2. Public exposure.
3. Secret mints.
4. Money.
5. Data deletion.
6. Production migrations and infrastructure applies.
7. IAM or equivalent permissions outside an already approved shape.

An installation may add doors in the human's own words. It may not remove one by inference. When classification is uncertain, treat it as a door until decided, then record the decision ([protocols 1](protocols.md#1-door-classification)).

**Everything else proceeds.** That includes status, scores, reviews, drafts, dry plans, opening and fixing changes, merges within granted authority, starting the next increment, and re-asking for something a standing yes already covers. None of these interrupts.

**How the human is asked.**
- One decision at a time, as a **single structured question** (a decision card or widget where the runtime has one, plain text otherwise): the action, the options, the recommendation and what each costs. Not a list of questions and not a status digest.
- Prepared, not pending: the coordinator finishes all reversible work first, then asks. Work behind the door waits; work beside it continues.
- Provenance: **only the human's own words authorize** ([protocols 2](protocols.md#2-authorization-provenance)). A relayed approval, an agent's paraphrase or a shared-identity click is not a yes.
- After the answer, the work proceeds without confirmation rounds. A blanket yes is recorded verbatim with the timestamp, so the next carrier of the same change is covered.

## 3. Routine taxonomy: the engine

A [routine](primitives.md) has two independent dimensions.

- **kind:** `scheduled` (a clock trigger) or `event` (a repository, chat, pipeline or webhook trigger).
- **lifecycle:** `standing` (durable, recurs) or `ephemeral` (created for one purpose, ends on a condition).

Prefer events to polling. Any clock trigger runs at the coarsest useful cadence, and every routine is silent when nothing changed.

| Routine | kind | lifecycle | Job | Speaks only when |
|---|---|---|---|---|
| Twice-daily wake | scheduled | standing | Read curated state, find the lowest unmet goal condition, assign it before reporting | A decision is pending or something changed |
| Weekday brief | scheduled | standing | One short outcome-first brief to the human | Something changed or a decision is pending |
| Board curator | scheduled | standing | Keep the [source of truth](practices.md#2-one-source-of-truth) true | A hold is bare, met or unowned |
| Peer check-in | scheduled | standing | Press a less proactive peer for shipped, next, blocked on ([coaching](practices.md#3-coaching-a-peer-agent)) | The peer is stalled or off-pattern |
| Weekly retro and huddle draft | scheduled | standing | Add-or-cut review of the week; draft the huddle | A proposal needs the human |
| Monthly prune and post-prune check | scheduled | standing | Cut, then verify the cut did not regress | A restore candidate exists |
| Repository listener | event | standing | Wake the coordinator on opened, merged, review, comment, unresolved thread, default-state CI failed | Something needs routing |
| Pipeline result reporter | event | standing | Read the default branch's pipeline after a merge and report the result | There is a result, good or bad |
| Alarm responder | event | standing | Parse a monitoring alert, write a short root-cause note, route one seat | A real alarm arrives |
| **Merge-on-green watcher** | event | **ephemeral** | Merge one reviewed change when every gate holds, then end | A result, or a one-way door |
| Deadline watch | scheduled or event | ephemeral | Follow one finite job to completion or its deadline, then end | The job finishes or the deadline passes |

### The ephemeral merge-on-green watcher

Created **when a merge is promised**, scoped to one change, with the gates written into its prompt. On each event it checks, and merges only when all hold:

1. Every routed reviewer seat scored PASS on the **exact head**, or explicitly carried its score ([protocols 3](protocols.md#3-exact-head-scoring-and-delta-re-score)).
2. The **automated code review**, where the installation runs one, has landed on that exact head and is clean or triaged. In progress or absent means wait.
3. Required checks ran and are green, or the human's written waiver applies.
4. Review threads are empty or triaged.
5. No deploy or apply from an earlier merge is running on the default branch, and no unapplied one-way-door plan sits there.
6. The net delta in control scripts is at or below zero ([protocols 8](protocols.md#8-control-budget)).
7. The merge pins the head.

Behavior by event:

| Event | Action |
|---|---|
| All gates hold | Merge with the pinned head, log the acting routine, then end (delete or pause) |
| Waiting on another merge's apply, or a review not yet landed | Stay armed and silent |
| New head | The approval is void; request a delta re-score; do not merge |
| Check failed | Route to the owner of the failure; never rerun, retrigger or push an empty commit |
| Changes requested | Route to the implementer; do not merge |
| Merged or closed | End. Delete or pause if this routine did not do the merge |

Stay silent when there is nothing to do. **Wake the human only for a result they asked about or a one-way door.**

### Promises become routines

If the coordinator says it will watch, merge, apply-check or ping later and the turn will end first, it creates the routine **in the same turn**. An event listener is preferred over polling; a deadline schedule that deletes itself is the fallback. A chat commitment with no routine does not count.

### Routine hygiene

- Pause stale routines (a finished change, a superseded head, an unreadable source). A paused watcher for a finished change is clutter; delete it.
- No retrigger hacks: no reruns, empty commits, manual dispatches or cancel-and-restart to force a check. Fix forward with a real change.
- One bookmark per source, advanced only after a successful read. An unreadable source emits one line naming it, never "nothing moved". A source failing twice in a row goes to the human.
- Re-read standing rules each run instead of baking a stale copy into the prompt. Re-verify live state and confirm each write before reporting.
- State intent and destination in the prompt, not frozen tool arguments.

## 4. The proactive loop

The loop that keeps the work moving without being told.

1. A climb (an epic's increment) closes and merges.
2. The coordinator **asks the domain-priority seat** (whichever reviewer seat owns product priority) for the next priority, instead of waiting for "continue".
3. The coordinator **starts the two-way-door work** immediately: opens the change, routes the slice, files the issues.
4. Work that ends at a one-way door is prepared in full and queued as one structured question. Holding a live apply is not a pause: everything before the door still runs.
5. The coordinator reports the outcome, not the activity.

Repeat until the epic's unmet key results are met or only doors remain.

## 5. What the human experiences

Outcomes arrive. One question at a time arrives only at a door, already prepared, with a recommendation. The rest of the machinery (reviews, merges, watchers, wakes, retros) runs without them and is visible only through the board and the ledger if they choose to look. Field evidence is in [field-evidence](field-evidence.md#autonomy).
