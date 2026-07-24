# Workright

Portable Agent Skills for careful, complete software work.

## Layout

```text
workright/
├── skills/
│   ├── make-feature/      # Build an approved feature end to end
│   └── test-product/      # Plan and execute traceable product testing
├── LICENSE
└── README.md
```

`skills/` is the source of truth. Each child directory becomes one independent
Agent Skill and can be installed in Codex, Claude Code, or another compatible
client.

## A skill, at minimum

One file is enough:

```text
skills/<skill-name>/
└── SKILL.md
```

`SKILL.md` starts with YAML metadata (`name`, `description`) followed by the
instructions. The description decides when an agent loads the skill; the body
describes how to do the work.

## Optional resources

Create these only when the skill genuinely needs them:

```text
skills/<skill-name>/
├── SKILL.md
├── references/   # Long or conditional guidance; read only when relevant
├── scripts/      # Tested, deterministic commands an agent can run
└── assets/       # Templates or files copied into the result
```

Keep the core workflow in `SKILL.md`. Put a database schema, API reference, or
rare edge-case guide in `references/` so it does not load for every task. Put
repeated mechanical logic in `scripts/`. Most early skills need only `SKILL.md`.

## Included skills

- `make-feature` classifies, designs, implements, and verifies an approved feature.
- `test-product` analyzes requirements, builds an RTM and risk-based test plan, creates
  approved test artifacts, executes applicable testing, and reports evidence and defects.
  It never fixes defects or modifies production code.

## Naming

Use lowercase kebab-case. A skill folder name and its `name` field must match:

```text
make-feature/
fix-bug/
investigate-issue/
analyze-codebase/
```

## Quality bar

Every skill should state:

1. When it applies.
2. The workflow to follow.
3. What evidence proves the work is complete.

Validate a completed skill with `skills-ref validate skills/<skill-name>`.
