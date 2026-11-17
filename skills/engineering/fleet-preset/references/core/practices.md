# Operating practices

Domain-free habits that keep the [functions](functions.md) and [protocols](protocols.md) cheap to run. Field evidence is in [field-evidence](field-evidence.md).

## 1. Routines

The taxonomy (kind scheduled or event, lifecycle standing or ephemeral), the canonical routine set and the ephemeral merge-on-green watcher are in [autonomy](autonomy.md#3-routine-taxonomy-the-engine). Rules that hold for every routine:

- **Event listeners over polling.** Any clock trigger runs hourly or slower and stays silent when clean.
- **Per-change babysitting routines are banned**; they burn usage for nothing. The narrow, self-ending merge-on-green watcher is the exception.
- **Promised follow-up is not banter**: create the routine in the same turn.
- **Housekeeping and learning loops:** a monthly prune, a regression check two weeks later, a weekly retrospective (add or cut) and a daily advisor pass. See [feedback](feedback.md).
- **Hygiene:** one bookmark per source, advanced only after a successful read; an unreadable source emits one line naming it, never "nothing moved"; standing rules are re-read each run; live status is re-verified and each write confirmed before reporting. No retrigger hacks.
- A less proactive peer agent gets its own check-in routine with a fixed three-line format ([coaching](#3-coaching-a-peer-agent)).

## 2. One source of truth

A project board is canonical for ownership. Pages, files, scores and chat are evidence.

- Fields: **Captain** (one owner), **Lane**, **Status**, **Hold condition**. Each fact lives once: head and checks on the change; ownership and holds on the board.
- A hold names its lift condition when placed. A bare "held" is flagged. A met condition is lifted.
- Writes follow the flow: the implementer sets *In review* at claims-done; reviewers write to the scores log and the change, never the board; the coordinator sets *Done* or back to *In progress* at verdict.
- Stay in your lane: never edit, push to or hold another captain's item without changing Captain or asking that captain.
- Durable reference (decisions, specs, architecture) may live on pages. A status table on a page drifts from the board and gets acted on stale.
- A record nobody fills at the moment of the event gets reconstructed from guesses. Make the merge record one row maintained by one owner.

## 3. Coaching a peer agent

An agent from another provider, reached through a browser or another thin channel, may be careful but not proactive. What helps:

- **Decide on two-way doors.** Say "doing X unless you object". Ask only about one-way doors and other parties' work.
- **Check staleness yourself.** An old draft with no recent commits does not block you.
- **One ask with a recommendation.** When genuinely blocked, bring one question and the answer you would pick, then work on something else.
- **Three-line check-in:** shipped, next, blocked on.
- **Server-side branch update** when a local hook blocks a merge of default state ([evidence hygiene](protocols.md#7-evidence-hygiene)).
- **Invite correction.** Let the peer verify your reasoning; it may catch a mistake.
- The panel reviews the peer's work at an exact head like anyone else's. The peer makes its own fixes.

## 4. Memory scopes

- **Shared (owner-wide):** the human's standing preferences, principles and the curated skills every agent needs.
- **Per-agent:** one agent's enduring facts, one dated fact per line, plus short periodic logs. Roster detail lives in durable memory, not in the persona text, so the persona stays short.
- **Task-scoped:** the current head, blocker and next action. Lives on the board and the change.
- Record the human's decisions **verbatim with a timestamp** and who recorded them. Paraphrase loses scope, and scope is what a blanket yes depends on.
- Curate hard. A prune compresses duplicates and deletes unused non-gate routines with proof; it never softens a fail-closed gate. A check two weeks later looks for regressions and surfaces restore candidates.

## 5. Shared workspace

When agents share one machine:

- **Heavy runs take a lock and run at low priority.** Never kill another worker's processes. Hand off the full head, not "my latest".
- **One checkout or worktree per seat per change**, reused across rounds. Scratch lives under your own folder. Keep fresh clones to about three per change fleet-wide. Create worktrees with the version-control tool; never delete clones or shared temp paths. Test runs clean up their own temp files.
- Cleanup beyond rebuildable cache goes through the housekeeper's proposal and the human's yes.
- Each agent may have its own interactive desktop on the shared machine; files, tools and logins persist for everyone.

## 6. Context budget

- Keep working context under a budget (*reference* about 100k). The human's one-to-one thread stays one continuous session.
- For long work, one fresh executor holds the whole connected chain. Do not split dependent steps across briefs. Independent work may fan out.
- Brief helpers in about 1 KB and point at files, board items and changes. State lives in files and on the board; update them rather than re-pasting.
- Batch independent reads. Tool output over about 8 KB goes to a file, then filter. Prefer event triggers to sleep or poll loops.
