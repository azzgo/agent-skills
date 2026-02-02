# AGENTS.md

This file serves as the entry point for AI coding agents (Claude Code, Cursor, Copilot, etc.) working in this repository. It provides a high-level introduction and progressive navigation to specialized topic guides for best practices and automation.

## Documentation Audience Guide

**Understanding who each document is for:**

- **`/skills/` directory** - All documentation is **agent-facing**
  - `SKILL.md` files instruct AI agents on how to use the skill's capabilities
  - `references/*.md` provide detailed execution instructions for agents
  - Example: aria2-json-rpc SKILL.md tells agents which Python scripts to call
  
- **`/openspec/` directory** - All documentation is **specification-facing**
  - Design documents, proposals, and technical specifications
  - Used for planning and architectural decisions
  - Not intended for direct execution by agents during normal operation

- **`/docs/` directory** - Most documentation is **user-facing** (with exceptions)
  - `agents-*.md` files are **agent-facing** (guides for AI agents working in this repo)
  - `manual-test/` subdirectory is **agent-facing** (instructions for testing workflows)
  - Other documentation typically explains features from the user's perspective

**Key principle**: When users give natural language commands, agents should:
1. Read agent-facing docs (SKILL.md, agents-*.md) to understand how to execute
2. Call appropriate scripts or tools
3. Format output in a user-friendly way based on user-facing documentation style

## Quick Navigation

For detailed guidance, consult the topic-specific documents in the [/docs](./docs) folder:

| Document | Purpose |
|----------|---------|
| [Repository Structure & Skill Organization](./docs/agents-repo-structure.md) | Repository layout, understanding skills, build/test commands |
| [Skill Definition & Development Standards](./docs/agents-skill-standards.md) | Naming conventions, SKILL.md format, adding new skills |
| [Python Code Style Guide](./docs/agents-style-guide.md) | Import order, naming, type hints, docstrings, error handling |
| [Testing Standards](./docs/agents-testing.md) | Unit and integration test structure, running tests |
| [Documentation/User Guide Standards](./docs/agents-docs.md) | Writing user-focused docs, file purposes, style guide |
| [Dependency & UV Management](./docs/agents-uv-dependency.md) | UV package manager usage, dependency best practices |
| [Common Code Patterns](./docs/agents-patterns.md) | Path resolution, main script patterns, config loading |
| [Best Practices](./docs/agents-best-practices.md) | Recommendations for authors and agents |
| [Troubleshooting](./docs/agents-troubleshooting.md) | Common issues and solutions |

**This file only provides a basic overview. For in-depth instructions or reference, open the relevant document in the /docs directory.**

---

## Key Guidelines Summary

### For Skill Authors

1. **Start with SKILL.md**: Define trigger phrases and usage examples
2. **Follow naming conventions**: kebab-case directories, snake_case scripts
3. **Never commit secrets**: Use config.example.json and environment variables
4. **Write tests**: Both unit and integration tests
5. **Document for users**: Focus on what users can do, not implementation

### For AI Coding Agents

1. **Read SKILL.md first**: Understand the skill's purpose before modifying
2. **Follow existing patterns**: Use established code patterns from the skill
3. **Run tests**: Execute `just test` after changes
4. **Update docs**: Keep documentation in sync with code changes
5. **Never commit secrets**: Always use environment variables for sensitive data

### Quick Commands

```bash
# Run all tests
just test

# Run specific test file
just test-file tests/unit/test_example.py

# Install dependencies
uv pip install -e .
```

---

*For any AI agent or contributor: Always refer to and keep the guidance within /docs up to date as repository conventions evolve.*
