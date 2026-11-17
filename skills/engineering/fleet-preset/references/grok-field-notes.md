# Grok fleet field notes

First-hand notes from the coordinator of a running Grok Bot fleet: one coordinator, a dozen specialist bots, one human owner, and a life-insurance SaaS as the product. Snapshot: 2026-11-17. The coordinator wrote them from its own memory, routine definitions, curated fleet skills, teammate profiles and its append-only review log.

**Read this as evidence, not as a spec.** These are practices that worked, and the mistakes that produced them. They are not measured effectiveness, not transferable permissions and not a full memory export. Where the preset chose differently, [choices](choices.md) says so. Names, identifiers, hashes, run numbers, customers, addresses and cloud-account details are removed on purpose; "the owner" is the human, "the product" is the SaaS.

Pair with the [Grok MVP blueprint](grok-mvp.md) for installation and the [role cards](roles.md) for who does what.

| Need | Section |
|---|---|
| How work moves and who hears about it | 1 Routing, 7 Routines, 8 Board |
| What needs the human, and what does not | 2 Doors |
| How reviews are scored and challenged | 3 Panel |
| When and how to merge | 4 Merge, 5 CI |
| Keeping the process light | 6 Fewer scripts, 10 Attention |
| Peer agents, memory, the shared machine | 9 Coaching, 11 Memory, 12 Box |

## 1. Routing: the coordinator holds the thread

**Practice.** Slice the work, pick the first specialist who owns the risk, send the slice to that one seat, and keep the thread until the outcome is verified. Specialists reply to the coordinator, not to the room and not to the human. The coordinator posts one rollup.

- Wake only on change. Priority is for three things: a final score on a commit, a bounce that carries a one-way-door must-fix, and a real question that needs a decision. Everything else is non-urgent. No acknowledgement-only or FYI wakes.
- Function rooms stay silent when nothing is new. A post is about three lines and points at a board item, a PR or a file.
- Claims-done is a direct priority ping to the coordinator with the exact head commit. A room post or a PR comment does not wake the router, so it does not count as convening the panel. Idle time between "ready for panel" and "panel scored" is a harness bug, not a feature of the interrupt bar.
- After a long directive from the owner, restate it in ten lines or fewer, let the owner confirm, then act.

**Field lesson.** I audited my own routing and found two habits to fix. I sometimes did specialist work myself (I re-ran a script comparison that reversed my own earlier close of a data must-fix), which blurs router and reviewer. And one change that touched user creation in the identity provider went to the data and legal seats only; neither security seat was woken, and no routing line said why. Remedy: each routing line names the seats woken and the seats omitted, with the reason.

## 2. Doors: act on two-way, ask on one-way

**Practice.** Classify every action before taking it.

- **Two-way doors:** do and show. Starting the next piece of an epic, opening a PR, filing an issue, drafting, reviewing, a dry plan. The coordinator consults the product seat on priority, then starts, without waiting for "continue".
- **One-way doors:** ask the human, and only these: infrastructure applies, minting secrets, making something public, deletes or replaces, money, data deletion. Merge is not on the list when the owner has granted merge authority for reviewed product changes (see 4).
- A **blanket yes covers what it names**, plus the PRs that carry it. Re-asking for an exact-commit yes after a blanket yes is toil. Re-ask only for a high-stakes item the yes did not name.
- **Only the human's own words authorize.** An agent's say-so, a bot-to-bot quote, a paraphrase, or an approval posted under a shared login is not authorization. When the coordinator relays a yes, it quotes the human's words verbatim with the chat timestamp. When an agent records a standing yes, the record quotes it, timestamps it, and says an agent posted the artifact, so nobody reads it as fresh assent.
- **PASS is not enable. Merge is not deploy.** Reviewers score readiness; they do not switch anything on.

**Field lessons.**
- The owner gave the coordinator alone a grant to act on his behalf when intent is clearly good and confidence is high. That grant was once sent to the implementer by mistake. Memory now records it as coordinator-only, and the implementer's profile says every production apply needs the owner's own yes.
- A schema-change PR asked whether merging would run the migration in production. The data seat checked the repository: no workflow runs it on merge, and the ops image that does is published by a manual dispatch. So the hold point is the next run of that image, and it applies every pending migration in it. The owner's yes must therefore name all of them, not just the new one.
- One security seat closed its score with "Merging needs the owner's yes" because it had no record of the owner granting merge authority. It declined to assume a grant it could not see. That is the right default for a seat; whether the grant exists is between the coordinator and the owner.

## 3. The risk-owned panel

**Practice.** The panel is the set of seats that own the risks a change carries, not a roster that reviews everything. See [roles](roles.md) for the capabilities.

- Each seat scores PASS, PASS-with-note or BOUNCE at an **exact head commit**, with IDs: `MF-<seat><pr>-<n>` for must-fixes and `S-...` for softs. A score for an older commit is stale.
- A must-fix carries `class=<kebab>`. The **seat that raises it owns the fix**, sweeps every instance of that class in the diff, and says how many sites it swept. The implementer does not fix other seats' must-fixes.
- Every head move needs a **delta re-score**. A push that changes only tests is re-scored by the seat that owns the finding; every other seat carries its score forward. Any non-test change re-wakes every routed seat. A seat never gives the only PASS on its own patch.
- Round cap: three fix pushes. Without a PASS after round three, the seats holding must-fixes send an approach note (ten lines or fewer: keep, split or redesign) and the coordinator picks. A third fix-forward in the same class within a week needs an approach note even at round one.
- Every score lands in an **append-only scores log**: one line per score with seat, commit, verdict, IDs and evidence pointer. Every must-fix fix also gets a line (raised-by, fixed-by, sweep count, whether the implementer re-entered).
- `PRE` (pre-existing) findings never block. A live one-way-door `PRE` still escalates to the owner.
- No PASS without green checks on the head that actually ran. A skipped, cancelled or not-run required check is not green.
- The coordinator **challenges claims** and never rubber-stamps them. The cheap challenges: is this "pre-existing" on main? is this check skipped rather than passed? do the claimed test counts match the run?

**Field lessons.**
- *"Pre-existing" was the PR's own commit.* My log recorded a type error as pre-existing and unchanged. The implementer then showed the error came from a function the PR itself had added; it was absent on main. And the hosted run that was expected to show it never reached typecheck: it was cancelled during a setup step and the step was skipped. Two rules came out of it: confirm "pre-existing" against main before logging it, and treat a skipped suite as no evidence either way.
- *A full-panel PASS on a draft whose infrastructure tests never ran.* The label that gates the suites was missing. A bug in a size precondition (it measured pretty-printed JSON) slipped through to the next PR. That is why a draft can get findings but not a PASS.
- *The implementer came back for rounds three, four and five* because other seats' must-fixes were sent to it. That produced churn, so the seat that raises a must-fix now owns it, and re-entry needs a cite and the coordinator's approval.
- *Test counts that did not match.* A change claimed 8 passing and 0 failing on one writer test; the reviewer ran it and got 7 passing and 1 failing. Claims carry a command and a count, and reviewers re-run them.
- *Planted defects.* Security and QA seats plant small deliberate defects and check that the tests catch them. A regex-over-source contract test let three of four plants survive, so it was deleted (see 6). A PASS notes how many plants the tests caught.
- *Self-correction in the log.* Once a seat did a full score because my "re-anchor only" claim was wrong. The correction goes in the same log.

## 4. Merge authority

**Practice.** The owner granted the coordinator authority to merge reviewed product PRs. The conditions, all checked at merge time:

1. Every routed seat scored the head being merged (or explicitly carried its score), with no open must-fix.
2. Required checks are green and actually ran, or the owner's batch waiver applies (below).
3. Review threads and review comments are empty or triaged. Untriaged comments block even if every seat said PASS.
4. The merge-tree is clean against current main. Branches need not be up to date with main.
5. One merge at a time, and no on-merge apply is running.
6. Main holds no unapplied infrastructure plan with IAM, delete or replace, public-exposure, secret or data-deletion changes that the owner's yes does not cover.
7. Merge with the head commit pinned (`gh pr merge --squash --match-head-commit <sha>`), so a late push cannot ride in.

**Fix forward.** When the owner said to batch PRs and fix forward on a staff PASS without waiting for CI, the coordinator did so. The waiver does not cover: a deterministic break the PR itself causes, an infrastructure PR that just left draft (wait for its ready-for-review plan), merging during an on-merge apply, or unapplied risky plans. Recover a failed on-merge with a catch-up fix-forward PR, never a rerun or manual dispatch. The catch-up plan must include every unit main still owes.

**Verify before claiming.** After merge, read back who and what merged, not just that it did. All merges here run under one shared login, so the platform's "merged by" field is the same for the human's merges and the coordinator's. I recorded the acting bot in the log at merge time, and a later audit still found two contradictory memory entries about who merged a revert: the platform could not settle it. Log the actor when it happens.

**Field lessons.**
- *Proof that only main can give.* A container-build change was merged on the SRE seat's code PASS, because pull-request CI does not build the image. The seat wrote four revert triggers before merge. Main's build then timed out, and a trigger fired. I reverted, and merged the revert on tree equivalence with the known-good state, with no rerun. Pre-agreed revert triggers turned the decision into a lookup instead of a debate.
- *A merge that the checks could not see.* A change to what the ops bundle imports merged with a browser-test shard timeout I judged unrelated. Main's image build then broke on the PR's own change. All merges were held until the fix-forward landed. The image job is skipped on pull requests, so no seat had proof, and the SRE seat had not been routed. The lesson I took: a diff that changes what a build bundles should wake the operability seat.
- *Wrong tip.* One merge landed at the parent of the tip, before the last commit. The squash was empty and nothing applied. Pinning the head is the guard against it.

## 5. CI realities

- The suites are **label-gated**. A draft without the label gets no suites, and a skipped required check is not green.
- **No reruns, no empty commits, no manual dispatches to retrigger.** A failure is either real (route it to its owner) or an infrastructure fault (fix forward with a real change). Tool-call retries cap at three; CI is never rerun.
- When hosted minutes run out or hosted runners time out, run the same checks locally on the head merged with main. Local runs are a vehicle for evidence; they do not waive the panel.
- To bring a branch up to date with main without tripping local pre-commit hooks that fail on main's existing files, use the platform's **server-side update-branch**. It keeps the PR and review history, needs no force-push and bypasses nothing. Never skip hooks with a flag.
- A suite that did not run is **not a pass**. Read the job list, not the summary badge: a green summary can hide skipped jobs, and a red one can be a cancelled post-step with every test green.
- A reviewer that does not own the label or the workflow does not add them. One seat wrote, correctly, "I don't add labels or dispatch CI; that's yours."

## 6. Fewer scripts: net delta at or below zero

The owner's view, paraphrased: needing a script to do something usually means the approach is wrong, and guardrails that only add toil should go.

**Practice.** When a CI script check blocks a change, delete or simplify the check and move what it truly protected into a test. Never add an exception, allowlist entry or special case. Before each push, check the net script delta against main; if it is positive, stop and fix. Growth needs the owner's own words.

- Ask in order: can the blocking check just be deleted? does the infrastructure tool already do this (dependency blocks, shared locals, import blocks you then delete)? does the CI platform (environment gates, `needs`, `concurrency`) already do it? can it be a test beside the module?
- **Tests, not source text.** A test that reads source files and regex-matches them is banned: it passes on a decoy. Delete it, or replace it with a runtime check.
- Approval rituals bound to comment IDs, record files, single-parent commit checks or yes-line formats are antipatterns. Use an environment gate or normal review.

**Field lesson.** A security seat bounced an enum-parity test that read the schema file and the shared types by regex. No shared runtime array existed to compare, so the implementer deleted the test instead of building one, and shipped a one-line change. The reviewer re-scored shortly after.

**Where this differs from the preset.** The preset keeps a flexible stance (see [choices](choices.md)): it allows a justified, safety-preserving addition. The live fleet treats growth as a last resort that needs the owner's yes. Choose the strictness that fits your installation and say which you chose.

## 7. Routines

**Practice.**
- **Event listeners over polling.** One repo-wide listener (PR opened or merged, review requested, changes requested, comment, unresolved thread, main CI failed) wakes the coordinator. Hourly or slower for any cron. Silent when clean.
- **PR-scoped merge-on-green watcher**, named `#<PR> merge on green`. It listens to that PR only. On CI passed it checks the head is still the approved commit, required checks ran and are green, threads are empty and no apply is running on main, then merges with the pinned head. On a new head the approval is void and it asks for a delta re-score. On CI failed it routes the failure and never reruns. It **deletes itself** when the PR merges or closes. A paused watcher for a finished PR is clutter.
- Never mark a PR ready and merge it in one step if readying triggers a plan; the watcher waits for the plan.
- A **pipeline result reporter** reads the main branch's deploy run and reports after merge, so the PR watcher does not have to.
- **Twice-daily wake** checks curated state, finds the lowest unmet goal condition and assigns it before reporting. A weekday morning brief goes to the owner only when something changed or a decision is pending. A weekday debt scan looks for security PRs and quiet failures. A **board curator** keeps the project board honest (see 8).
- An **alarm webhook** receives monitoring alerts, writes a short root-cause note with blast radius, and routes one specialist if a bounded fix is clear. It never merges and never spends money.
- A **monthly prune** and a **post-prune regression check** two weeks later, a **weekly retrospective** (add or cut), and a **daily oversight** pass by the advisor. See [retrospectives](retrospectives.md).
- **Promised follow-up is not banter.** If I say I will watch, merge or ping later and the turn will end first, I create a short-lived routine in the same turn. A chat commitment with no routine does not count.
- **Routine hygiene:** one bookmark per source, advanced only after a successful read; if a source is unreadable, emit one line naming it instead of "nothing moved"; re-read standing rules from memory each run rather than baking a stale copy into the prompt; re-verify live status and confirm each write landed before reporting.
- **Peer check-in routines.** A less proactive peer agent gets its own check-in routine with a fixed three-line format (see 9).

**Field lessons.** Per-PR babysitting routines burned the owner's usage limit, so they were banned and the weekday brief flags stuck PRs instead. The narrow merge-on-green watcher is the exception: it is armed only after approval and deletes itself. Once, I paused a watcher when a peer reported seven integration failures at the armed head. The fix arrived as a new head, and the seats re-scored it before the merge went ahead.

## 8. One source of truth for ownership

**Practice.** The team's GitHub Project board is canonical for who owns what, which lane, status, and what is holding it. Pages, files, scores and chat are evidence.

- Fields: **Captain** (one owner), **Lane**, **Status**, **Hold condition**. Each fact lives once: commit and checks on the PR; ownership and holds on the board.
- A hold names its lift condition when placed ("lift when QA passes at the head commit"). A bare "held" gets flagged. A met condition gets lifted.
- Write rules follow the review flow: the implementer sets In review at claims-done; reviewers write to the scores log and the PR, never the board; the coordinator sets Done or back to In progress at verdict.
- Stay in your lane: never edit, push to, or hold another captain's item without changing Captain on the board or asking that captain.
- The curator adds new items, sets Status from platform truth, and flags unowned items and met holds. It never changes another captain's fields.

**Field lesson.** A status table on a Page and the board drifted apart, and bots acted on the stale one. The Page became durable reference only (decisions, specs, architecture).

## 9. Coaching a peer agent

A peer agent from another vendor, reached through a browser, owned a large UI port. It was careful but not proactive: it stopped to ask questions it could answer itself and waited for permission on reversible work. What helped:

- **Decide on two-way doors.** Say "doing X unless you object" instead of asking. Ask only about production, secrets, public changes or another party's work.
- **Check staleness yourself.** An old draft with no commits for weeks does not block your work; look at its last commit date before asking whether it conflicts.
- **One ask, with a recommendation.** When genuinely blocked, bring one question plus the answer you would pick, then work on something else while waiting.
- **Three-line check-in:** shipped, next, blocked on.
- **Use the platform's server-side update-branch** to merge main into a branch when the local commit hook blocks (see 5).
- **Verify your own reasoning.** The peer caught a mistake in my advice (a PR's old commits stay reachable, but the branch pointer moves on push), and said it would confirm reachability before relying on it. Invite that.
- The panel reviews the peer's work at an exact head like anyone else's. In the UI port, the review-only boundary held: seats reviewed and the peer made its own fixes.

## 10. Protect the human's attention

- **One decision at a time**, outcome first, then where we are in the sequence, what just happened in plain language, and the one next move. The owner follows technical topics when they are broken down; keep hashes, role names and paths out unless a decision needs them.
- **No status theater.** No optional confirmations. The interrupt bar is: an apply, a secret, spend or credentials, an irreversible or destructive step, or a fork only the owner can take.
- The coordinator is the only router to the human. Specialists do not fan into the owner's chat.
- A "locked" claim needs evidence that the file, skill or issue was actually updated; a claim made from prose alone counts as a miss.
- Plans state Key Results (what is true when done, for whom, under which constraints), not the how. Implementation stays challengeable.

## 11. Memory

- **Shared** surfaces carry what every bot needs: the owner's standing preferences, principles and the curated fleet skills. **Per-agent** memory carries one bot's enduring facts, one dated fact per line, and short monthly logs. Roster detail lives in durable memory, not in the profile text, so the profile stays short.
- Record the owner's decisions **verbatim with the timestamp**, and who recorded them. Paraphrase loses scope, and scope is what a blanket yes depends on.
- Curate hard. A monthly prune compresses duplicates and deletes unused non-gate routines with proof; it never softens a fail-closed gate. A check two weeks after the prune looks for regressions and surfaces restore candidates.
- **Field lesson:** a merge ledger that required a line at merge time was repeatedly backfilled by the advisor with "unrecorded" fields. The owner replaced it with one row in the advisor's scoreboard as the merge record, and the extra line was dropped. A record nobody fills at the moment of the event gets reconstructed from guesses.

## 12. The shared box

- The box is one persistent machine shared by all bots; each bot gets its own desktop. Files, installed tools and logins persist for everyone.
- **Heavy runs take a lock and run under `nice`.** Never kill another worker's processes. Hand off the full head commit, not "my latest".
- **One checkout or worktree per seat per PR**, reused across rounds. Scratch lives under your own folder. At most three fresh clones per PR across the fleet. Create worktrees with git; never `rm -rf` clones or shared temp paths. Test runs clean up their own temp files.
- Cleanup beyond rebuildable cache goes through a disk-cleanup bot's proposal and the owner's yes.
- Briefs to helpers are 1 KB or less and point at files and PRs. Bot-to-bot reports are 800 bytes or less. Tool output over about 8 KB goes to a file, then filter. Keep working context under about 100k, and give one fresh executor the whole connected chain rather than splitting dependent steps across briefs.

## Provenance and limits

Sources: the coordinator's profile and routine definitions, a first-hand read of every teammate's profile, the curated fleet skills named above, and the coordinator's own scores log. The log is the coordinator's record, not an independent audit; some anecdotes are single occurrences. Nothing here installs a routine, grants authority or proves the practices transfer. Evaluate them with the [evaluation guidance](core/evaluation.md) before adopting.
