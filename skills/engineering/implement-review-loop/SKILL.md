---
name: implement-review-loop
description: Implement a feature or issue through substantial milestones using test-first development and an independent review of each completed milestone. Use when the user requests an implementer–reviewer loop or invokes implement-review-loop.
---

# Implement and review

Deliver the requested work in substantial, reviewable milestones. Use red/green cycles within each milestone; bring in an independent reviewer after the milestone is coherent, not after each test or small change. A small issue can be one milestone.

## 1. Frame the milestone

Read the task, applicable repository instructions, existing behavior, and relevant tests. Identify the intended outcome, acceptance criteria, dependencies, and required checks. Choose a milestone that delivers a meaningful capability or integration boundary and is small enough to review. Scale its size to the task; do not use fixed limits on tests, files, or lines. State consequential assumptions and proceed with decisions supported by the request and available evidence.

## 2. Implement

For behavioral changes, use focused red/green cycles at the appropriate public or customer-facing boundary:

- Write a test for a meaningful behavior and run it before the fix. Confirm the failure reflects the missing behavior rather than broken setup.
- Implement enough to pass, then run the test. Repeat as needed until the milestone's behavior is covered.
- Follow repository requirements for acceptance coverage and quality gates. For work where test-first is unsuitable, use the best available verification and report why.

Complete the milestone, run relevant checks, and self-review the diff before requesting independent review. Preserve the user's scope and existing work. A thin initial proof may be one step within a milestone; it is not automatically the review boundary.

## 3. Review independently

Delegate a read-only review to a separate agent when the environment supports it. This workflow calls for delegation. Give the reviewer the milestone objective, acceptance criteria, exact diff or revision and its base, relevant repository instructions, and verification results. Ask for prioritized, actionable findings with file references and evidence: correctness, meaningful test coverage and test validity, integration, maintainability, and fit with existing patterns. The implementer retains ownership of changes.

If an independent reviewer is unavailable or not authorized in the environment, perform a separate self-review and clearly report that independent review did not occur. Do not represent it as independent.

## 4. Resolve and advance

Verify each finding against the actual code and requirements. Fix valid findings; explain rejected or deferred findings and their implications. Rerun affected tests and required checks after changes. Request another targeted independent review only when fixes substantially change behavior or scope, or a material concern remains unresolved. Avoid automatic review loops for routine fixes.

Continue to the next milestone when the current one meets its acceptance criteria, required checks pass, and material findings are resolved or explicitly reported. Honor any user-requested checkpoints and applicable external-action boundaries. If a prerequisite or required check cannot be completed, make independent progress and report the specific limitation; do not claim the milestone is fully verified.

## 5. Report

Summarize the delivered behavior, meaningful red/green evidence, reviewer identity or independence limitation, findings and their disposition, checks run, and remaining gaps. Where an observed repeatable failure suggests a harness improvement, recommend the appropriate instruction, skill, or test change; make that change only when within the user's authorized scope.
