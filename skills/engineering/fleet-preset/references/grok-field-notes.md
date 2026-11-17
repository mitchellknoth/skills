# Grok fleet field notes: domain seats and Grok Bot bindings

First-hand notes from the coordinator of a running Grok Bot fleet, snapshot 2026-11-17: one coordinator, a dozen specialist bots, one human owner, a life-insurance SaaS as the product. Written from the coordinator's memory, routine definitions, curated fleet skills, teammate profiles and its append-only review log.

**Where things live.** The provider-neutral lessons (routing, doors, provenance, exact-head scoring, merge-on-green, evidence hygiene, escalation, attention, routines, board, coaching, memory, shared workspace) are in the architecture core: [functions](core/functions.md), [protocols](core/protocols.md), [practices](core/practices.md) and [field evidence](core/field-evidence.md). This file keeps only what is specific to the prescriptive path: lessons the **named domain seats** learned, and lessons about the **Grok Bot binding** of each [primitive](core/primitives.md).

**Read as evidence, not spec.** Practices that worked and the mistakes behind them; not measured effectiveness, not transferable permissions, not a memory export. Names, identifiers, hashes, run numbers, customers, addresses and cloud-account details are removed; "the owner" is the human, "the product" is the SaaS. Where the preset chose differently from the live fleet, [choices](choices.md) says so.

## 1. Domain seats

Each seat is a [risk-owned reviewer](core/functions.md#risk-owned-reviewer) (or a paired adversary, interrogator or implementer) with its domain slots filled. Persona cards carry the short form; these are the lessons with stories.

**QA (done-ness interrogator).**
- A UI or frontend PASS requires a rendered surface on the same head as the claim; a diff alone is a bounce. The owner set this as a hard gate.
- Re-run the claim. QA re-ran a writer test that claimed 8 passing and 0 failing and got 7 and 1.
- Plant small defects and report how many the tests caught.

**Security pair (defender and adversary).**
- The defender checks closed enums, redaction and fail-closed paths; the adversary tries to defeat those assumptions on the system's own surfaces and never writes attack artifacts. The adversary does not accept the defender's pass.
- A pattern-over-source contract test is the classic decoy: three of four planted defects survived one, so it was deleted. Delete such tests or replace them with runtime checks.
- Each seat stays in its lane on CI: the adversary does not add labels or dispatch runs, and says so.

**Data (schema and tenancy).**
- Wake only on migration, schema, grant or tenancy changes. Stay quiet otherwise.
- **Merge is not migrate.** A schema PR raised whether merging would run the production migration. The data seat traced the repository: no merge workflow runs it, and the operations image that does is published by a manual dispatch. The hold point is therefore the next run of that image, which applies every pending migration in it. The owner's yes must name all of them, not only the new one.
- Tenant identity comes from the session, never the client; migrations are expand then contract.

**SRE (operability, with the cloud-spend seat folded in).**
- Own default-branch-only proof. A container-build change cannot be proven by pull-request CI, so the SRE seat wrote revert triggers before merge. They turned a bad default-branch build into a lookup (see [field evidence](core/field-evidence.md)).
- Wake on diffs that change what a build bundles, not just infrastructure files.
- Read the job list, not the badge. Treat a skipped or cancelled required check as not green.
- Own the spend envelope with a hard ceiling; bounce a path that blows it without the owner's yes. Never invent a dollar figure; read prices from the pricing source and usage from the cloud CLI.

**UX.**
- Two verdicts stay separate on owner-locked visual references: UX and information architecture, and visual taste. A material miss against the reference is a bounce. The stamp names the reference, the head, both verdicts and the deltas or "no material visual delta".
- A taste bounce after a locked reference is patched by this seat on the head and re-stamped. It does not restart the implementer.

**Product.**
- On journey or requirement changes with acceptance scenarios, check that each Then matches the written requirement. Green is mechanical; fidelity is this seat's verdict. Consulted on priority before the coordinator reorders the next climb.

**Legal and compliance (not counsel).**
- Score against enumerated rulings point by point (for example required fields, caps, rejection copy, retention, visibility) and name residuals as messy-but-defensible instead of rounding up to PASS.
- When hardening a contract for the owner's side, validate clauses against published sources, keep non-waivable statutory items and list off-market terms as flags. Say when counsel is required.

**Finance, marketing, housekeeping.**
- Finance reads money from connected sources, never invents a balance and never moves money. Marketing never invents customers, certifications or partners, and routes compliance claims to Legal. The housekeeper proposes cleanup and deletes nothing beyond rebuildable cache without a yes.

## 2. Grok Bot bindings: what each primitive taught

| Primitive | Binding lesson |
|---|---|
| `peer_message` | A room post does not wake the router. Claims-done is a priority `SendToAgent` to the coordinator with the exact head. Messages arrive on a later turn, so no one waits on a live reply. |
| `routine` | Per-PR babysitting routines burned the owner's usage limit. The shape that worked: one repository-wide event listener, a twice-daily wake, narrow self-deleting merge-on-green watchers and a destination line that says who receives the result. Prompts state intent, not frozen tool arguments. |
| `approval_gate` | A blocked action escalates to an approval card the human answers in their own client. A merge once went through that card after an automatic safety review blocked it; the scoreboard recorded the yes as unquoted. A card answer is the human's act, but the record still needs the words. |
| `standing_authorization` | Stored as a memory entry with the quote, timestamps and "an agent posted this". A grant addressed to the coordinator alone is recorded as such. |
| `outbound_rule` | Anything leaving under the owner's name is a draft card by default. A saved send rule is the only standing exception, and a declined or blocked send is final: no retry through another route. |
| `memory_scope` | Owner-shared memory for preferences, principles and curated skills; per-agent dated facts and monthly logs. Roster detail lives in memory, not in the profile text, so profiles stay short. |
| `shared_workspace` | The box is one machine shared by all bots, with a desktop per bot. Heavy runs take a lock and run under `nice`; never edit another bot's checkout; scratch lives under the agent's folder. |
| `source_of_truth_board` | A GitHub Project with Captain, Lane, Status and Hold condition. Under the shared-login default the platform's "merged by" cannot tell humans from bots, so log the acting bot at merge time (see `tool_connector` for the recommended per-bot identity). |
| `human_channel` | The owner's one-to-one chat is one continuous session. A reply in a room does not count as having told the owner. |
| `tool_connector` | Inspect effective capabilities, not prompt promises. Live cloud facts come from the cloud CLI read-only, never from memory. **Identity:** the default is one shared platform login for merges and other code-host actions, because it is low friction. The tradeoff is lost attribution, so the ledger must record which seat actually acted. The recommended target is a distinct identity per bot (for example a GitHub App or a machine user) with least-privilege scopes. |
| `agent_persona`, `skill`, `review_ledger` | Profiles stay short and name anti-jobs; skills are pinned and confirmed loaded; the scores log is a plain append-only file, and the merge record is one row with one owner. |

## Provenance and limits

Sources: the coordinator's profile and routine definitions, a first-hand read of every teammate's profile, the curated fleet skills, and the coordinator's own review log. The log is one participant's record, not an independent audit; anecdotes are single occurrences. Nothing here installs a routine, grants authority or proves the practices transfer. Evaluate with the [evaluation guidance](core/evaluation.md) before adopting.
