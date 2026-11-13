# Skill candidate assessment

Snapshot: 2026-11-13. These are **static design-fit assessments of inspected candidates**, not a grade of every bot's actual curated skills or proof of superior task performance. The current per-bot curated inventory is incomplete. Unread installed skills remain **U / ungraded**. Do not infer installation from this table.

## Source/version boundary

- Oakline's inspected Matt Pocock collection was pinned at `f3fc5632f401156837ee3872f14fe33ccf1024ea` (38 skills). Candidate review used upstream [`5863806`](https://github.com/mattpocock/skills/tree/5863806dd4e15c63174bee4e7515a4256792ecfa), which has 39 skill entry files. Installed and upstream copies are not interchangeable evidence.
- Cursor candidate review used [`24621db`](https://github.com/cursor/plugins/tree/24621dbcc59e205a7faadb0e06d540f91712b5cc). A plugin's packaging and runtime assumptions may differ from Grok.
- The local `implement-review-loop` remains a useful baseline and is not replaced.

A = strong design fit with explicit adaptation; B = useful selective technique; C = poor direct transplant; U = insufficient inspection. Evaluate trigger/scope, oracle/evidence, failure handling, authority, runtime portability and maintainability separately. Grades are judgments, not performance percentages.

## Matt Pocock candidates

Sources below are under the pinned [engineering collection](https://github.com/mattpocock/skills/tree/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering).

| Candidate | Fit / likely consumer | Evolution decision and caveat |
|---|---|---|
| code-review | A / Principal, QA, Product | Complement with separate Standards and Spec axes and pinned diff. Never replace independent security, UX or production acceptance merely because one review is broad. |
| tdd | A / Principal, QA | Fold independent oracles, public seams and meaningful red-before-green into the existing loop. Do not import mandatory owner confirmation for every seam or phase-specific prohibitions without testing their cost. |
| diagnosing-bugs | A / Principal, SRE | Complement with reproducible evidence and falsifiable hypotheses. Adapt its strict runnable-loop prerequisite for read-only incidents where reproduction is unavailable; label inference rather than invent it. |
| domain-modeling | A / Product, Data | Complement glossary, ADR and edge-case reasoning. Preserve the customer's domain truth and identity invariants. |
| retro | B / Eggbot | Useful session/environment lessons, not a substitute for the fleet's weekly outcomes, monthly prune, post-prune guard or owner calibration. |
| research | B / all applicable roles | Reuse bounded primary-source research. Do not force delegation for every small lookup. |
| implement-spec / to-tickets | B / Product, Principal | Reuse vertical slices, dependency frontier and isolated work. Adapt tracker, final gates and write authorization. |
| in-progress chief-of-staff | C / no direct adoption | Experimental. Dated provenance-rich knowledge is useful; blanket delegation and automatic maintenance/retro work are not Jarvis equivalence. Inspected relative links to several engineering skills did not resolve from its in-progress directory. |

## Cursor candidates

Pinned [pstack skills](https://github.com/cursor/plugins/tree/24621dbcc59e205a7faadb0e06d540f91712b5cc/pstack/skills).

| Candidate | Fit / likely consumer | Evolution decision and caveat |
|---|---|---|
| create-verification-skill / maintain-verification-skill | A / QA, UX | Strong user-path/run/drive/evidence/cleanup discipline; blocked is not clean. Adapt harness paths and deployment permissions; serialize shared live UI control. |
| correct | A / Eggbot, Principal | Complement repeated mistake → type/lint/test/schema/CI improvement, proved against the historical mistake. Do not automatically delete governance prose or make unapproved persistent changes. |
| blast-radius | A / SRE, Data, Blue | Complement an evidence ladder beyond grep to code/runtime reachability. Preserve read-only production limits. |
| reflect | B / Eggbot | Reuse different lenses and accepted/rejected/backlog synthesis. Do not import rigid model routing, four-agent cost or automatic backlog writes as defaults. |
| statechart | B / Principal, Data | Optional protocol reasoning. Model correctness is not proof the implementation conforms. |
| continual-learning | C / persona replacement | Its inspected memory updater compresses away rationale/provenance/confidence and caps bullets. That conflicts with preserving why this fleet's personas behave differently. Do not replace curated memory wholesale. |
| agent-compatibility | B for dimensions, C for copied scoring | Startup, validation, documentation and workflow dimensions can inform customer discovery. Do not copy a numerical score as if it predicts operational reliability. |

## Recommended evolutionary experiments

1. Existing implementation loop + independent test oracle + Standards/Spec review axes.
2. Existing UX/QA acceptance + reusable user-path verification skill, with actual render provenance.
3. Existing Eggbot retro/prune + structural correction method, preserving actual-work evidence, owner boundaries and regression guard.
4. Existing SRE diagnosis + blast-radius evidence, with explicit unavailable-runtime handling.

Each is a **proposal for paired evaluation**, not a proven fusion. Retain current successful cases, hard authority boundaries, counterexamples, held-out tasks and rollback. A longer blended prompt is not evolution.

## License and publication

Matt's inspected upstream is MIT, copyright 2026 Matt Pocock. pstack is MIT, copyright 2026 Lauren Tan. The inspected continual-learning and agent-compatibility plugins are MIT, copyright 2026 Cursor. Recheck the exact selected revision before copying and retain required notices. This assessment links and summarizes methods; it does not vendor third-party skill bodies. Other plugins require their own license check.

## What remains unfinished

A per-bot grade needs the actual curated source body and version, its real trigger, memories that alter its use, and comparative task evidence. Neither a public catalog nor this candidate table supplies that. No automatic skill replacement, installation or runtime activation is performed.

## Existing fleet skills: provisional excerpt-level assessment

The source-tagged coordinator report and current role interviews add **reported bindings and selected excerpts**, not complete current skill bodies or proven loading. The older on-box snapshot and newer profiles/interviews differ. These decisions are preservation/composition judgments, not overall bot grades or demonstrated superiority.

| Existing skill family | Provisional decision | Comparison and evidence limit |
|---|---|---|
| rendered-ui-validation + visual-sot-fidelity-audit | KEEP; complement | Preserve independent rendering and owner-locked visual-source acceptance. pstack verification adds driving, evidence and cleanup; it does not replace that acceptance gate. |
| data-domain-locks + multi-tenant-aws-postgres-scale | KEEP domain/platform preset | Matt domain-modeling adds glossary and ADR technique. Neutral architecture abstracts tenant isolation and authority/source-of-truth constraints; concrete identity fields and providers remain versioned preset choices. |
| review-when-work-claims-done | KEEP; reconcile overlaps | Preserve independent review and zero-reviewers-is-not-pass. Reconcile duplicated rules with fleet-review-rules, loop-engineering and kr-climb; Matt's dual axes are additive. |
| fleet-weekly-retrospective | KEEP longitudinal loop; evolve only after reconciliation | Older coordinator evidence describes cut-verification gaps; newer oversight prompt/interview includes a fix-verification ledger. Preserve chronology rather than declaring verification universally absent. Session retro is a complement. |
| Legal domain set | KEEP scoped verdict vocabulary | No inspected generic candidate demonstrates stronger domain replacement. Full bodies and effectiveness remain ungraded. |
| SRE domain set | KEEP; complement | Blast-radius and diagnosing-bugs add techniques without replacing production authority or domain constraints. Exact complete current bindings remain unverified. |
| entity-tax-framing | KEEP boundaries | Preserve entity/tax distinctions and no invented financial numbers; no replacement evidence. |
| white-hat-adversarial-review | A− static design; retain and tighten | Full exported body subsequently inspected; see focused assessment below. Runtime efficacy and current loading remain unproven. |
| hig | B static design; retain, correct before promotion | Full exported body inspected; contrast and target-size claims need correction. See below. |
| spec-auditor | B wrapper only; canonical rubric U | Export is still a wrapper. The host-local canonical dependency remains uninspected. |

Next evidence gate: obtain permission-safe complete bodies and current bindings, pin versions, and replay historical tasks with independent oracles. Retain source constraints until a proposed evolution wins that comparison. Do not equate a reported successful next run with a measured long-term recurrence reduction.

## Per-role disposition (not an overall performance grade)

| Role | Evidence-limited assessment / next comparison |
|---|---|
| Coordinator | Preserve review and fleet-retro orchestration; reconcile overlapping policies before folding. spec-auditor wrapper is provisionally B; canonical rubric remains ungraded. |
| Principal | Preserve domain/review/rendering bindings; compare Matt code-review, tdd and diagnosing-bugs on historical failures. IaC identifier/body unverified. |
| QA | Keep rendering/visual-reference gates; compare independent-oracle and verification techniques. Compliance binding excerpt is insufficient for a complete grade. |
| Product | No named current skill binding verified. Assess requirement-traceability behavior separately; domain-modeling and dual review axes are candidates, not installed skills. |
| UX | Keep rendering and locked-visual fidelity; pstack verification complements them. hig full export is provisionally B; correct contrast and target-size claims before promotion. |
| SRE | Preserve domain reasoning; compare blast-radius/diagnosing-bugs. Exact four-skill inventory and inherited cost bindings need full-body/version verification. |
| Blue | No named current active binding proven. Memory-driven checks need planted-break replay before judging efficacy; old review skill evidence does not prove current loading. |
| Red | Keep white-hat boundary; independence and late-review constraints need drift reconciliation. Full-body static assessment is A−; attack-finding effectiveness remains untested. |
| Data | Keep domain locks and tenant-scale skills; domain-modeling complements, not replaces, domain invariants. |
| Legal | Keep scoped compliance/health/privacy/insurance/audit/tax reasoning; full-body grade remains pending. No supported generic replacement. |
| Finance | Keep entity-tax boundaries; assess educator scope and classification cases. No evidence of a stronger generic substitute. |
| Oversight | Preserve current fleet-verification ledger and longitudinal retro. Matt retro/pstack reflect/correct add techniques only after authority and version reconciliation. |
| Marketing | No complete binding verified. Evaluate claims fidelity and asset-verification examples before choosing a replacement. |
| Disk Saver | Reports scripts rather than saved skills; assess script/guard behavior, especially inode versus byte pressure, not an imaginary skill grade. |
| FinOps | Historical spend-envelope reference; do not activate. Preserve cost-driver and alert-lag lessons under the reconciled active owner. |


## Focused full-export static assessment

Inspected 2026-11-13. These qualitative grades assess exported instruction design, **not observed runtime performance, active loading or the live installation version**. Raw private exports are not published here. Existing fleet skills are not silently replaced or edited by this assessment.

### White-hat adversarial review: A−, retain and tighten

The full export clearly bounds authorized scope, preserves independent Red/Blue review, covers concrete trust boundaries, requires live evidence for release-gate claims and states residual risks and non-claims. Retain those properties.

Proposed improvements, not claims of existing behavior:

- Reconcile inconsistent verdict vocabularies into one definition, including when residual risks block.
- Bind scope to the immutable reviewed commit and relevant configuration version; state evidence freshness.
- Add **BLOCKED / insufficient evidence** separately from a demonstrated defect or pass.
- Identify who can accept residual risk. Red reports risk; its verdict does not grant release authority.

Test against historical authorization/control failures and known-clean changes, measuring missed findings and false alarms. pstack blast-radius is a plausible complement, not a demonstrated replacement.

### HIG UI review: B, retain but correct before promotion

The full export requires rendered evidence, commit-stamped findings, broad state/input checks, separation of taste from blockers and acknowledgment of device-only limits. Review PASS is not activation authority. Preserve these strengths, but correct these static defects:

1. **Contrast:** the current wording can allow small bold text at the large-text threshold. WCAG AA normally requires 4.5:1; the 3:1 large-text threshold applies at **18pt regular or 14pt bold**, not any bold text. Applicable exceptions still matter. [W3C contrast minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
2. **Target size:** a blanket rejection below 24×24 CSS pixels overstates WCAG 2.2 AA. Its minimum criterion includes spacing, equivalent-control, inline, user-agent-control and essential exceptions. A stricter house policy may be selected, but must not be mislabeled as the standard. [W3C target size minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html).
3. **Verdict scope:** excluding pre-existing issues from change blockers is incompatible with claiming the entire surface meets the bar. Prefer a change-scoped result with explicit known baseline issues, not unearned full-surface compliance.
4. **Unavailable checks:** unsupported media modes and untested device states need explicit blocked/not-tested outcomes, not implicit passes.
5. **Requirement classes:** separate platform/editorial preferences from accessibility requirements. The complete Apple rule set was not independently verified in this pass.

Proposed fixtures: small bold low-contrast text, spaced small targets, inline links, baseline versus introduced defects, and unavailable device checks. These have not yet been executed as a comparative behavioral evaluation.

### Spec auditor: B for wrapper; canonical rubric remains U

The inspected export is the 35-line wrapper, not its host-local canonical rubric. It supplies a precise trigger, exclusions and useful ambiguity, acceptance, contradiction, hidden-input, feasibility and scope checks. It does not contain a complete scoring rubric, severity definitions, output schema or missing-context protocol. Its dependencies remain unresolved outside the original host.

Keep the whole skill ungraded until the canonical dependency is inspected. A portable package must supply that dependency or explicitly stop and report it unavailable rather than inventing the rubric.

### Export evidence pins

SHA-256 identifies the inspected export bytes, **not** a verified live installed version:

- Spec wrapper: `10f8f6cb38c6987b16c8cf4c5395bc2548ddc5c33468a36ff54117d9315a230f`
- White-hat: `db09f9a216beb57f9e7ac9910dddfbedd79e6ba036e5b047513907a80950965b`
- HIG: `fa719e30dd434cbda37146ff4e5c33e006c064def03f499302ffd99485d80d26`
