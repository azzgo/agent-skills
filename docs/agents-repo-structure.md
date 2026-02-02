# Repository Structure and Skill Organization

This document details the structure of this repository and the conventions used for organizing skills.

## Overview

This is a **skills repository** that manages multiple agent skills. Each skill is a packaged set of instructions (and optionally scripts) that extends an agent's capabilities for specific tasks.

## Documentation Audience by Directory

Different directories contain documentation for different audiences:

- **`/skills/`** - All documentation is **agent-facing**
  - `SKILL.md` instructs AI agents on how to use the skill
  - `references/*.md` provide detailed execution instructions for agents
  - Scripts in `scripts/` are the implementation that agents should call

- **`/openspec/`** - All documentation is **spec-facing**
  - Design documents, proposals, and specifications
  - Used for planning and architectural decisions

- **`/docs/`** - Mixed audience
  - `agents-*.md` files are **agent-facing** (guides for AI agents)
  - `manual-test/` is **agent-facing** (test instructions for agents)
  - Other docs are typically **user-facing**

## Current Skills

- `skills/aria2-json-rpc/` - Control aria2 download manager via JSON-RPC 2.0

## Understanding a Specific Skill

To understand how to use or modify a specific skill:

1. Read `skills/<skill-name>/SKILL.md` - Main skill definition with usage examples
2. Check `skills/<skill-name>/scripts/` - Implementation scripts
3. See `skills/<skill-name>/references/` - Detailed technical documentation
4. Review `openspec/changes/<skill-name>/` - Design artifacts and planning docs (if exists)

## Repository Structure

```
skills/                      # All skills live here
  <skill-name>/
    SKILL.md                 # Skill definition (REQUIRED)
    config.example.json      # Example configuration
    scripts/                 # Implementation scripts
      *.py                   # Core modules
      examples/              # Example usage scripts
    references/              # Long-form documentation
    assets/                  # Images, diagrams
openspec/                    # Design and planning artifacts
  changes/
    <skill-name>/            # Skill-specific design docs
  specs/                     # Main specifications
tests/                       # All tests
  unit/                      # Unit tests
  integration/               # Integration tests
justfile                     # Test commands
README.md                    # Repository overview
```

## Build, Lint & Test Commands

### Running Tests

```bash
# Run all tests (unit + integration)
just test

# Run unit tests only
just test-unit

# Run integration tests only
just test-mock-server

# Run a specific test file
just test-file tests/unit/test_rpc_client.py

# Run a specific test method (unittest format)
python3 -m unittest tests.unit.test_rpc_client.TestAria2RpcClient.test_client_initialization
```

### Running Scripts

Scripts are located in `skills/<skill-name>/scripts/`. Most scripts can be run directly:

```bash
# Run a script directly (if it has shebang and is executable)
python3 skills/<skill-name>/scripts/script_name.py

# Example: Test the aria2 RPC client
python3 skills/aria2-json-rpc/scripts/rpc_client.py
```

## Navigation

- [Skill Development Standards](./agents-skill-standards.md) - Conventions for building skills
- [Python Code Style Guide](./agents-style-guide.md) - Code style requirements
- [Testing Standards](./agents-testing.md) - How to write tests
- [Documentation Standards](./agents-docs.md) - Writing user-facing docs
- [Common Code Patterns](./agents-patterns.md) - Reusable patterns
- [Best Practices](./agents-best-practices.md) - Recommendations for quality
- [Troubleshooting](./agents-troubleshooting.md) - Common issues and solutions
