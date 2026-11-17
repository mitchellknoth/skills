# Grok field notes validation — 2026-11-17

The field notes and per-role additions are first-hand documentation from the
coordinator of a running Grok Bot fleet. This note records how they were checked.
It is **not evidence that the practices improve outcomes** or that an agent
follows them.

| Check | Observed result |
| --- | --- |
| `mise run eval:check` in a scratch copy with git history available | 96 tests pass; generated core copies current; history check passes. The history test reads a recorded commit, so it needs a git repository with a resolvable `HEAD`. |
| Added files are standalone | The preset link test copies the skill alone and resolves every relative link, including the new field-notes links from each persona card. |
| Scrub | A pattern grep over the added lines for addresses, long digit runs, cloud resource identifiers, key and token prefixes, long hex strings, links, pull-request and run numbers, customer and product names and private paths returned nothing. |

Source categories: the coordinator's profile and routine definitions, a first-hand
read of each teammate's profile, the curated fleet skills, and the coordinator's
own review log. The log is a single participant's record. Anecdotes describe single
occurrences and are labeled as such.
