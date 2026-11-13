# Skill evaluation and evolution

A large collection is not necessarily a strong collection. Grade a skill for the bot's actual job, not author reputation or the number of instructions.

## Evidence-first rubric

Record source/version, inspected files, intended task, target runtime, license and dependencies. Use **A (strong fit), B (useful with specific adaptation), C (weak fit or major gap), D (unsuitable), U (ungraded)**. These are qualitative design judgments, not measured success probabilities. A catalog title or reported usage is insufficient for a skill-quality grade.

Judge six dimensions: task fit; evidence and verification; scope/authority; clarity and token cost; failure/recovery behavior; portability and maintenance. Also record whether the skill was read, statically checked, replayed or exercised in a live task. Do not average away an authority or evidence-integrity defect.

## Evolution decisions

- **Keep:** distinct, demonstrated purpose and acceptable implementation.
- **Complement:** another skill adds a missing method without replacing role-specific judgment.
- **Fold:** overlapping procedures can share a canonical component while preserving meaningful differences.
- **Adapt:** valuable method needs explicit target bindings or narrowed authority.
- **Retire candidate:** no unique benefit after replacement evidence and regression check; never delete automatically.
- **Investigate:** source/runtime evidence is incomplete.

Compare the current skill against an alternative on the same frozen tasks. Include successful progress and valid stops. Preserve independent-review boundaries, provenance, operator decisions and retry limits. Measure task quality, owner burden, repeatability and cost where available. Skill fusion must remove duplication, not create a longer prompt with incompatible rules.

## License and publication

Link external sources and pin reviewed revisions. Do not vendor or blend third-party text/code until its license and attribution requirements have been checked. Installed copies can differ from upstream. Public persona cards contain sanitized learned behavior, not private source memories. A skill recommendation is not permission to install or activate it.

## Current evaluation boundary

A per-installation curated-skill audit must establish the actual source inventory. Do not interpret the persona catalog or candidate mapping as a completed grade of every referenced source. Unsupported grades remain U until source bodies and target context are inspected. Behavioral superiority requires comparative runs, not a static review alone.
