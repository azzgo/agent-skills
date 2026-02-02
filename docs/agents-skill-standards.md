# Skill Definition and Development Standards

This document describes the conventions and requirements for defining and building new skills in this repository.

## Overview

Skills are packaged sets of instructions (and optionally scripts) that extend an agent's capabilities for specific tasks. Each skill lives in its own directory under `skills/`.

## Naming Conventions

- **Skill directory**: `kebab-case` (e.g., `aria2-json-rpc`)
- **Skill definition file**: `SKILL.md` (exact filename, UPPERCASE)
- **Python scripts**: `snake_case.py` (e.g., `rpc_client.py`, `command_mapper.py`)
- **Example scripts**: `kebab-case.py` (e.g., `pause-all.py`, `list-downloads.py`)
- **Configuration**: `config.example.json` (never commit real `config.json` with secrets)

## Required Files for Each Skill

### Minimum Required

- `SKILL.md` - Skill definition with frontmatter, trigger phrases, usage examples

### Recommended as Skill Grows

- `config.example.json` - Example configuration
- `scripts/*.py` - Implementation scripts
- `references/*.md` - Detailed documentation
- `assets/*` - Supporting files (images, diagrams)

## SKILL.md Format

Each `SKILL.md` should include:

### 1. Frontmatter (YAML)

```markdown
---
name: skill-name
description: When to use this skill; include trigger phrases
---
```

### 2. Required Sections

- **Usage section**: Clear trigger phrases ("download this URL", "pause all downloads", etc.)
- **Quick Start**: How to use the skill in 3-5 steps
- **Examples**: Concrete usage examples
- **Configuration**: How to configure (if needed)
- **Requirements**: What's needed to use this skill

**Keep it concise** - Move lengthy reference material to `references/` directory.

## Configuration & Secrets

### Security Rules

- **Never commit secrets**: Add `skills/*/config.json` to `.gitignore`
- **Provide examples**: Include `config.example.json` with safe defaults
- **Use environment variables**: For tokens and secrets (e.g., `ARIA2_RPC_SECRET`)
- **Document clearly**: Explain configuration priority (env vars > config file > defaults)

### Configuration Priority

1. **Environment variables** (highest priority)
2. **Configuration file** (`config.json` in skill directory)
3. **Default values** (fallback)

```python
# Environment variable naming: <SKILL_PREFIX>_<KEY>
# Example: ARIA2_RPC_HOST, ARIA2_RPC_PORT, ARIA2_RPC_SECRET
```

## Adding a New Skill

### Step-by-Step Process

1. **Create directory structure**:
   ```bash
   mkdir -p skills/new-skill/{scripts,references,assets}
   ```

2. **Create SKILL.md** with frontmatter and usage examples

3. **Implement scripts** in `scripts/` directory

4. **Add example configuration** as `config.example.json`

5. **Write tests** in `tests/unit/` and `tests/integration/`

6. **Update repository README.md** to list the new skill

7. **Optional**: Create design docs in `openspec/changes/new-skill/`

## Navigation

- [Repository Structure](./agents-repo-structure.md) - Repository organization
- [Python Code Style Guide](./agents-style-guide.md) - Code style requirements
- [Testing Standards](./agents-testing.md) - How to write tests
- [Documentation Standards](./agents-docs.md) - Writing user-facing docs
- [Common Code Patterns](./agents-patterns.md) - Reusable patterns
- [Best Practices](./agents-best-practices.md) - Recommendations for quality
