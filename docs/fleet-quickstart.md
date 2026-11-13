# Try the fleet package

This is a first-version draft. No live bots, automations or actions are installed by it.

## Choose your entry point

| | Architecture template | Opinionated preset |
|---|---|---|
| Invoke | `fleet-architecture` | `fleet-preset` |
| Best for | Adapt the architecture to your own workflow | Start from the author's more prescriptive delivery flow |
| Process | You configure roles, review, cadence and authority | Risk-routed review, meaningful test-first work, bounded loops, durable follow-through |
| Permission | Installation-specific, unset | Installation-specific, unset |
| Independent install | Self-contained | Self-contained, with generated shared core |

### Example requests

**Template:** “Use fleet-architecture to design a two-person team's release workflow. We want one implementer and independent QA on behavioral changes, no scheduled bots, and all publication remains manual. Produce the private installation policy and one sample task handoff.”

**Preset:** “Use fleet-preset for this feature. Keep the coordinator accountable through verification; route only the roles relevant to the change. Prepare the implementation and review evidence, but do not merge or deploy.”

**Evaluation:** “Use fleet-architecture in evaluate mode. Replay an approved batch where one required review is for an older revision. Explain the next permitted action. Do not contact any service.”

Installing both skills does not mean both policies apply. Select the entry point per task and keep that selection in the private installation record. Choosing the template must not silently import the preset.

## Local validation

```sh
mise install
mise run eval:check
mise run fleet:readiness -- \
  skills/engineering/fleet-architecture/assets/readiness.example.json
```

The reference evaluator runs locally, uses no network, and changes no external state. Exit 0 means its input fixture is modeled as ready; exit 1 means not ready/authorized; exit 2 means invalid input. It is **not a live gate or approval checker**.

## Configuration

Copy the selected skill's JSON template to a private location. Fill state store, role bindings, review/check requirements and authorization sources. Neither sample is an executable automation configuration. The template deliberately has unset process choices; the preset supplies process preferences while leaving authority unset.

Validate runtime support using the bundled adapter contract. A standalone test of these files does not prove that a client loads them correctly. Before relying on the bundle, test discovery and behavior in a fresh client session with inert or read-only tools.

## Publication and privacy

The repository is public. This draft contains general reusable practices and synthetic cases, not exported bot prompts, private approval quotes, account configuration, identifiers or live operational memory. Review the diff before publication. Do not activate schedules, writes or production authority as an installation side effect.

## What is deliberately not implemented

No Grok Bot export/import, scheduler, webhook listener, credential manager, GitHub merge executor, persistent agent runtime or migration of private state. The adapters document capability requirements; they do not claim runtime parity. Behavioral LLM replays and live integration tests remain future work requiring an appropriate isolated environment and authorization.

## Retrospectives and follow-through

The neutral template lets you choose feedback loops and cadence. The preset separately captures curation before proactive work, daily advisory oversight, weekly fleet retrospectives, weekly coordinator calibration, merge evidence, monthly hygiene, post-prune regression and dry-run orchestration reviews. It uses private run/ledger/retro/prune templates and leaves all activation dormant.

```sh
mise run fleet:feedback -- \
  skills/engineering/fleet-architecture/assets/feedback.example.json
```

This classifier is an inert example, not a scheduler or a policy-change authorizer.

## Grok-first persona setup (manual, dormant)

1. Choose the neutral `fleet-architecture` or opinionated `fleet-preset` explicitly.
2. For a custom architecture, fill the neutral persona and customer-profile templates privately. For the preset, inspect `references/PERSONAS.md` and its coverage catalog; select applicable cards, not every historical role.
3. Read the selected card's baseline and proposed-refinement sections separately. Resolve source conflicts and unavailable memory/skill inventory before claiming a faithful port.
4. Follow `fleet-preset/references/grok-mvp.md` to map profile, curated memory, skills, routine intent, rooms and state. Save installation bindings outside the public source.
5. Verify what the target actually loads and which capabilities are available. Do not activate or alter live bots merely because files are installed.
6. Evaluate with inert cases and a separately authorized shadow. Future target adaptation follows `references/transpilation.md`; no executable transpiler is supplied yet.

Candidate skill assessments are in [the research report](skill-candidate-assessment.md). They are proposals for comparative evaluation, not permission to replace existing curated skills.
