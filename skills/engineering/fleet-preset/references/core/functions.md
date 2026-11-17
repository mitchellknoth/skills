# Functions: the roles that make the workflow work

The abstract path names **functions**, not domains or personalities. A function is a guarantee the workflow needs, expressed as the question it answers and the authority it holds. Any domain plugs into the reviewer function; none is prescribed here.

A function may live in its own agent, share an agent with another function, or be played by a person. Combine functions freely **except where a protocol requires independence**: the function that implements may not be the only function that accepts, an adversary may not simply restate its defensive pair, and the advisor holds no execution authority. A missing function blocks the claim it supports. Self-review is not a substitute for a required independent function.

| Function | Question it answers | Holds | Never holds |
|---|---|---|---|
| [Coordinator](#coordinator) | Is the outcome owned through to verified completion? | Routing, the thread, the final verdict, merge authority when the human grants it | Specialist work it can route; any one-way door |
| [Advisor to the coordinator](#advisor-to-the-coordinator) | Is the orchestration working, and what is the coordinator not seeing? | Measurement, pressure-testing, recommendations | Execution, merges, applies, veto, wake-ups without a finding |
| [Implementer](#implementer) | Does the integrated change meet the contract? | Decomposition, integration, the verification table | Its own independent acceptance; other seats' must-fixes |
| [Risk-owned reviewer](#risk-owned-reviewer) | Is this risk acceptable, at this exact head? | A scored verdict in its lane | Enabling anything; implementing the change it scores |
| [Adversary paired with a defender](#adversary-paired-with-a-defender) | What defeats the defender's assumptions? | An independent attack-the-assumptions pass, defensive must-fixes | Attack artifacts; rubber-stamping the defender's pass |
| [Done-ness interrogator](#done-ness-interrogator) | Do tests and observation prove "done"? | The completion claim's evidence audit | Implementation; passing on a summary |
| [Curator of the single source of truth](#curator-of-the-single-source-of-truth) | Does the state record match reality? | Keeping the record current | Another owner's fields |
| [Watcher and reporter automations](#watcher-and-reporter-automations) | Did something change that someone must act on? | Narrow listeners, one report per event | Judgement calls; reruns; spending |
| [Housekeeper](#housekeeper) | Is the shared machine staying healthy? | Audits and proposals | Deletion beyond rebuildable cache |
| [Human gatekeeper](#human-gatekeeper) | Is this one-way door worth opening? | Every one-way yes, in the human's own words | Routine two-way work |

## Coordinator

**Router and thread holder.** Slices work honestly, sends each slice to the first seat that owns its risk, and holds the thread until the outcome is verified. Specialists answer the coordinator, not the room and not the human; the coordinator posts one rollup and is the only router to the human.

- Acts on two-way doors without asking and brings the human only one-way doors ([door classification](protocols.md#1-door-classification)).
- Gives the final verdict. A reviewer's patch is never the final verdict.
- Records which seats were woken and which were omitted, with the reason.
- Challenges claims instead of relaying them ([challenge before you log](protocols.md#5-challenge-before-you-log)).
- Converts every promised follow-up into a routine in the same turn.
- Does not do specialist work it can route. Doing it blurs router and reviewer.

## Advisor to the coordinator

The pattern that keeps the coordinator honest. It sits beside the coordinator, not above it.

- **Measures orchestration:** wake patterns, repeated must-fix classes, rounds over the cap, merge records, stalled commitments, ceremony regrowth, and whether earlier advice changed any behavior.
- **Pressure-tests decisions:** before a merge, checks the merge protocol and answers `ok` or `block` with a cite. A block is advice; the coordinator may overrule it, and a serious block goes to the human.
- **Has no execution authority:** no merges, applies, product changes, edits to another agent's persona or routines without the human's yes, and no waking agents without a finding.
- **Reports** to the coordinator by default, and to the human only for actual one-way risk, a proposed role change, or a serious miss the coordinator declined to act on.
- Stays quiet when clean. Never re-argues a settled decision without new evidence.
- Runs outside the coordinator's failure domain where possible. A routine that never starts is invisible to a coordinator that only reads its own output.

## Implementer

Decomposes into narrow tasks, integrates, and verifies. At claims-done it hands the panel the exact head, the verification table and the checks that actually ran. It does not certify its own work, does not fix another seat's must-fix, and returns to a change only for redesign outside a seat's lane or for new scope ([escalation ladder](protocols.md#9-escalation-ladder)).

## Risk-owned reviewer

The generic seat. **Any domain plugs in** by filling this contract:

| Slot | Meaning |
|---|---|
| Risk owned | The single failure class this seat is responsible for |
| Wake surfaces | The paths, artifacts or claims that wake it; silence otherwise |
| Evidence type | What counts as proof in its lane (a rendered surface, a run, a ledger read, a source citation) |
| Hard gates | Conditions the human set that turn a score into a bounce when unmet |
| Anti-jobs | What the seat refuses to do, and who owns it instead |
| Verdict form | PASS, PASS-with-note or BOUNCE, bound to an exact head, with IDs |

Seats that own a domain's analysis without scoring changes (for example finance or marketing) use the same slots, with the verdict form replaced by a sourced recommendation.

The panel is the set of seats that own the risks a change carries. It is selected by risk, not by roster size. The [protocol](protocols.md#3-exact-head-scoring-and-delta-re-score) fixes how seats score; the domain fills the slots.

## Adversary paired with a defender

Two seats on one boundary. The defender designs and checks controls; the adversary tries to defeat the defender's assumptions on **the system's own surfaces only**.

- The adversary never rubber-stamps the defender's pass, and the defender never accepts the adversary's pass as its own.
- Both return defensive must-fixes. Neither produces attack artifacts, exploit procedures or third-party targeting. If an external test is needed, the seat says so.
- Pair them when both an authorization-style risk and an abuse-path risk are present; one seat suffices when only one is.
- Both may plant small deliberate defects and check that the tests catch them. A pass reports how many plants were caught.

## Done-ness interrogator

Called when work claims done. Does not implement. Interrogates the claim across test layers: what ran, what was skipped, whether claimed counts match a re-run, and whether the evidence is on the same head as the claim. UI claims need a rendered surface; a diff alone is a bounce. Waits for the claims-done signal instead of reacting to partial pushes.

## Curator of the single source of truth

Keeps one authoritative state record (a project board with owner, lane, status and hold-condition fields) aligned with platform truth. Adds new items, sets status from facts, and flags unowned items, bare holds and met hold conditions. Never changes another owner's fields. See [one source of truth](practices.md#2-one-source-of-truth).

## Watcher and reporter automations

Narrow, event-driven automations: a repository listener, a [merge-on-green watcher](protocols.md#4-merge-on-green-watcher) scoped to one change, a pipeline result reporter that reads the default branch after merge, an alarm responder that writes a short root-cause note, and a twice-daily wake that finds the lowest unmet goal condition and assigns it before reporting. They route; they do not judge, rerun or spend. See [routines](practices.md#1-routines).

## Housekeeper

Audits shared-machine disk and resource use and proposes safe cleanup for the human's approval. Rebuildable cache may go; anything else needs a proposal and a yes.

## Human gatekeeper

The only authority for one-way doors. Their own words are the only authorization; no agent can relay, paraphrase or synthesize one. They can grant a blanket yes, a standing merge authority or a waiver, and each must be recorded verbatim with a timestamp ([provenance](protocols.md#2-authorization-provenance)). Everything else belongs to the workflow, so the human's attention is spent on decisions that need a human ([attention budget](protocols.md#10-attention-budget)).

## Binding functions to a domain

A domain installation fills the reviewer slots with named seats (for example a data seat, a legal seat, a UX seat) and may name the advisor or the housekeeper. That is the prescriptive path; see the `fleet-preset` skill's persona index for the author's mapping. The functions above stay the same when the domains change.
