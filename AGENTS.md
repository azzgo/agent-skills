This file provides guidance to AI coding agents (Claude Code, Cursor, Copilot, etc.) when working with code in this repository.

## Repository Overview

This is an agent-skills repository focused on controlling `aria2c` via JSON-RPC 2.0. Skills are packaged instructions (and optionally scripts) that extend an agent's capabilities.

Primary skill today:
- `skills/aria2-json-rpc/`

Design and planning artifacts live under:
- `openspec/changes/aria2-json-rpc-skill/`

## How Skills Are Organized

Each skill lives in `skills/<skill-name>/`.

Minimum expected files:

```text
skills/
  <skill-name>/
    SKILL.md
```

Optional files (recommended as implementation grows):

```text
skills/
  <skill-name>/
    scripts/
      <script-name>.(sh|py)
    references/
      *.md
    config.example.json
```

## Naming Conventions

- Skill directory: `kebab-case` (e.g. `aria2-json-rpc`)
- Skill definition file: `SKILL.md` (exact filename)
- Scripts: `kebab-case` (e.g. `add-uri.py`, `tell-status.py`, `pause-all.sh`)
- Example config: `config.example.json` (never commit real secrets)

## SKILL.md Expectations

Keep `SKILL.md` optimized for activation:

- Include clear trigger phrases (“download this URL”, “pause all downloads”, ...)
- Keep it concise; move long reference material into `references/`
- Prefer deterministic CLI scripts for heavy lifting; keep the agent instructions focused on orchestration

If you adopt frontmatter later (compatible with the Agent Skills ecosystem), use:

```markdown
---
name: <skill-name>
description: <when to use this skill; include trigger phrases>
---
```

## Configuration and Secrets

- Treat `skills/*/config.json` as local-only.
- Add `skills/*/config.json` to `.gitignore` if/when such files are introduced.
- Prefer environment variables for tokens (e.g. `ARIA2_RPC_SECRET`) in CI and shared environments.

## Working With aria2 JSON-RPC

When you modify the `aria2-json-rpc` skill:

- Keep JSON-RPC 2.0 compliance (`jsonrpc`, `id`, `method`, `params`).
- Token auth, when used, is typically `token:<SECRET>` as the first param for `aria2.*` methods.
- Make error output actionable (connection refused, auth failed, method not found).

## Docs Hygiene

- Keep the repo README focused on: what skills exist, when to use them, and where the skill lives.
- Put deep design docs and milestone plans under `openspec/` (already present).
