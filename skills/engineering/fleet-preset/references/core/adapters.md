# Runtime adapters and activation

An installed skill is not an installed operating system. Validate capabilities for the selected runtime rather than relying on model names or familiar tool labels.

| Capability | Questions the adapter must answer |
|---|---|
| Delegation | Fresh context? Durable identity? Separate permissions? Can results be recovered? |
| State | Which private store? Revision/conflict handling? Checkpoint after successful read only? |
| Review | Can verdicts bind to exact revision and surface? Does the reviewer have independent context? |
| CI inventory | Complete required checks, including skipped/pending and pagination? |
| Actions | Scope/identity verification? Atomic expected-head guard? Uncertain-outcome recovery? |
| Events | Supported triggers/filters? Duplicate/out-of-order delivery? Live-state recheck? |
| Scheduling | Actually installed? Last successful output? Startup/quota failure visibility? |
| Oversight | Shares coordinator's failure domain? Can it detect a run that never starts? |

## Initial adapter status

- **Grok Bot:** use installation-specific bot/room bindings, existing routines and private state. This package does not export or install them. A copied routine description is not a verified subscription.
- **Cursor / Claude Code / Codex:** the repository manifests distribute skills. Agent wrappers and tasks depend on that client's available tools. Do not assume a shared GitHub account creates independent review identities.
- **Dot:** one coordinator can use specialist work threads where available. Scheduled/event-triggered work, persistent identities and watchdog independence require separate verification. No claim of full Grok parity.

These are setup contracts, not executable integrations. No client-specific API calls are bundled in this first version.

## Safe installation sequence

1. Install the skills and verify the selected entry point(s) are discoverable.
2. Choose the template or preset explicitly; copy its configuration to a private installation location.
3. Bind real tools, sources and roles. Verify least privilege and separate authority from convenience credentials.
4. Run inert fixtures, then read-only historical replay. Record capability gaps.
5. Obtain scoped authorization for any live pilot. Keep one authoritative executor; a shadow must not compete for merges, notifications or state ownership.
6. Activate each schedule, event or mutation path separately and verify it. Retain previous configuration and a rollback path.

Do not commit credentials, private chats, bot/room identifiers, active approvals, personal or customer data, operational run history or current production state into the public package. Use placeholders and synthetic cases.
