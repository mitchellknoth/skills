# Provider-neutral primitives and their bindings

The compiler analogy in [adaptation](transpilation.md) needs a concrete intermediate representation. These thirteen **primitives** are that representation: what the [functions](functions.md) and [protocols](protocols.md) are made of, with no provider names. A provider binding says how a runtime implements one. The machine-readable form is [primitive-bindings.json](../../assets/primitive-bindings.json).

Source-system bindings are for Grok Bot, where the architecture was built and operated. Every other target starts at `unknown` with a TODO. A binding that only lists a lead (a feature the repository's adapter notes mention) is still `unknown`: the name of a feature does not establish its semantics.

## The primitives

| Primitive | Neutral meaning | Invariant a target must preserve | Grok Bot binding |
|---|---|---|---|
| `agent_persona` | Durable behavioral contract for one function | Loaded explicitly; independent seats have separate context | Bot profile, curated skills, routines, group-chat membership |
| `peer_message` | Addressed, asynchronous message with a priority flag | No live reply assumed; priority is reserved; carries information, never authorization | `SendToAgent` with a priority flag; room posts; `SendToUser` for the human |
| `routine` | Intent plus trigger plus destination | Explicit trigger, reads, output, dedup key, terminal behavior; silent when clean; scoped watchers delete themselves | Saved prompt with a cron schedule, or a repository, chat or webhook listener, ending in a destination line |
| `memory_scope` | Shared owner-wide, per-agent and task-scoped memory | Scope explicit; human decisions verbatim with timestamp | Owner-shared memory, per-agent dated facts and logs, recall tools; task state on the board |
| `skill` | Instruction package loaded on demand | Intended source and version actually loaded | A skill package in the skills store |
| `approval_gate` | Human decision bound to one action | Only the human can produce it; bound to action and revision; a decline is final | Approval card; blocked actions escalate to it; outbound messages are send cards |
| `standing_authorization` | Recorded grant with scope, quote, timestamps, recorder | Verbatim; says an agent posted it; names whom it covers | Memory entry with the quote; relayed verbatim by the coordinator |
| `outbound_rule` | What an agent may send without review | Explicit scope; default is a draft the human sends | Saved send rule in instructions; otherwise a draft card |
| `shared_workspace` | Shared machine for checkouts, scratch, locks, logs | One checkout per seat per change; lock plus low priority for heavy runs; no killing others' work | The box: one persistent machine, a desktop per agent |
| `source_of_truth_board` | One state record: owner, lane, status, hold condition | Each fact lives once; holds name lift conditions | A GitHub Project via the GitHub CLI or connector |
| `review_ledger` | Append-only record of scores and merges | Append-only; exact heads; one-row merge record | A file in the shared workspace plus comments on the change |
| `human_channel` | The one channel to the human | One router; one decision at a time; interrupt bar | The owner's one-to-one chat with the coordinator |
| `tool_connector` | Integration or CLI with a permission scope, acting under an identity | Effective capabilities inspected, not assumed; read-only means read-only; the acting identity is known | MCP connectors and CLIs the bot is granted |

## Reading the bindings

Each entry in the JSON has:

- `invariants`: testable statements a binding must keep. Conformance means replaying cases that exercise them ([evaluation](evaluation.md)), not generating text.
- `guarantee_lost_if_emulated`: what a weaker substitute loses. Name it in the plan.
- `blocks_if_missing`: the action or claim that must stop when the primitive is `unsupported`. A missing `approval_gate` blocks every one-way door; there is no weaker substitute.
- `grok`: the source binding and its evidence label.
- `targets`: one entry each for Claude Code, Codex, Cursor and Dot. Status uses `supported`, `emulated`, `manual`, `unsupported` or `unknown`. Only `skill` is `supported` today, on the evidence of the repository's own install paths; discovery and loading are not tested. Everything else is `unknown`, with a `lead` where this repository's adapter notes mention a related feature, and a `todo`.

## Identity: shared by default, per-agent recommended

Every tool call acts under some platform identity. Two arrangements:

- **Shared login (default).** All agents act under one platform account. It is low friction: nothing to provision or rotate. The cost is attribution: the platform's "who did this" is identical for every agent and for the human, and a shared-login approval is never a human yes ([provenance](protocols.md#2-authorization-provenance)). So the [review ledger](protocols.md#3-exact-head-scoring-and-delta-re-score) must record **which seat actually acted** at the moment it acted.
- **Per-agent identity (recommended target).** Each agent gets a distinct identity with least-privilege scopes, for example an app identity or a machine user per agent on the code host. Attribution comes from the platform, scopes shrink to what the seat needs, and one agent's credential can be revoked alone. It costs provisioning, scoping and rotation work, so it is a one-way-door change to a platform setting that needs the human's yes.

Moving from the first to the second is a private installation change. The package ships no account names or secrets.

## Rules for a transpiler

1. Emit nothing for an `unknown` entry. Report it and the todo.
2. Do not silently weaken `approval_gate`, `standing_authorization` provenance or the expected-head guard the merge protocol uses. Emulation states the loss; an unsupported required guarantee blocks the action.
3. Keep provider names out of function and protocol text. They live only in bindings.
4. Rendering a plan never copies credentials, enables a routine, sends a message or widens a permission.
5. A binding earns `supported` by a conformance replay on the named target and version, recorded with its date.
