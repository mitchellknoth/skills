# Release preparation

For commit-history curation, use the upstream
[curate-release skill](https://github.com/lousy-agents/skills/blob/7042a57853b52e9c513050e7d5a21dc7108f6146/skills/curate-release/SKILL.md),
including its referenced preflight and release-typing files. Read the pinned
source before executing it; changes to this upstream pin require review.

The skill is a history-only workflow. Its draft/closed/fork gates, merge-strategy
inspection, isolated worktree, original-tree equality check and guarded push
apply before any rewrite. It explicitly stops for a draft PR. PR #3 remains a
draft, so adopting it does not curate current commits, edit PR metadata, merge
the branch or publish a release.

This repository uses paired plugin manifest versions and a manual changelog.
It has no semantic-release configuration. Before a future release:

1. Verify scope, current tests, exact-head review and relevant benchmark records.
   Treat unchanged or negative measurements as evidence.
2. Update both plugin manifests together and describe user-visible changes and
   limitations in `CHANGELOG.md`.
3. With a ready PR and a specific history-curation request, invoke the upstream
   skill against that PR. Its merge-strategy gate decides whether to curate
   commits or propose a squash narrative. A tree comparison must show the same
   files before and after curation.
4. Report checks and the proposed release separately from publication. Use the
   owner's explicit release/merge authorization for those final actions.

Automatic releases can be considered when a publishing policy is chosen.
Installing that infrastructure or rewriting a draft would be a different change.
