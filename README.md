# Skills

Reusable workflows for coding agents. Each skill is a portable `SKILL.md` with its supporting files, organized by category.

## Skills

- [implement-review-loop](skills/engineering/implement-review-loop/SKILL.md) — implement substantial milestones with test-first cycles and independent review.

## Install

Choose one installation method per agent to avoid duplicate skills.

### Vercel Skills

Install in the current project, choosing your agent interactively:

```sh
npx skills@latest add mitchellknoth/skills
```

To install only this skill for a specific agent, add `--skill implement-review-loop --agent codex`; add `--global` for a user-wide installation. Run `npx skills@latest check` to check for updates and `npx skills@latest update` to update installed skills. Re-run `add` to discover and install newly added skills.

### Codex plugin

```sh
codex plugin marketplace add mitchellknoth/skills
codex plugin add knoth-skills@knoth
```

Use `codex plugin marketplace upgrade knoth` to refresh the marketplace. Plugin updates depend on the client and its configuration.

### Claude Code plugin

```sh
claude plugin marketplace add mitchellknoth/skills
claude plugin install knoth-skills@knoth
```

Manage marketplace auto-updates in Claude Code, or run `claude plugin marketplace update knoth` to refresh it.

### Cursor

For individual use, install through Vercel Skills with `--agent cursor`. Teams can import this repository as a team marketplace in Cursor's **Dashboard → Plugins & MCPs**, then install `knoth-skills` from Customize. GitHub imports can enable Auto Refresh; this requires the Cursor GitHub App on the repository. See [Cursor's plugin documentation](https://cursor.com/docs/plugins) for plan requirements and update behavior.

## Invoke

Ask your agent to use `implement-review-loop` for an issue or feature. The implementer works through test-first cycles within a substantial milestone, then an independent reviewer evaluates the milestone before the next one begins.

## Contributing skills

Place each skill in `skills/<category>/<skill-name>/SKILL.md`. List each distributed skill directory in both plugin manifests, and bump both plugin versions together when publishing changes. Keep the skill in one place; all distribution methods point to the same source.

## License

[MIT](LICENSE)
