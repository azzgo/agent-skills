# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Cursor, Copilot, etc.) when working with code in this repository.

## Repository Overview

This is a **skills repository** that manages multiple agent skills. Each skill is a packaged set of instructions (and optionally scripts) that extends an agent's capabilities for specific tasks.

**Current Skills:**
- `skills/aria2-json-rpc/` - Control aria2 download manager via JSON-RPC 2.0

**To understand a specific skill:**
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

## Skill Development Standards

### Naming Conventions

- **Skill directory**: `kebab-case` (e.g., `aria2-json-rpc`)
- **Skill definition file**: `SKILL.md` (exact filename, UPPERCASE)
- **Python scripts**: `snake_case.py` (e.g., `rpc_client.py`, `command_mapper.py`)
- **Example scripts**: `kebab-case.py` (e.g., `pause-all.py`, `list-downloads.py`)
- **Configuration**: `config.example.json` (never commit real `config.json` with secrets)

### Required Files for Each Skill

**Minimum:**
- `SKILL.md` - Skill definition with frontmatter, trigger phrases, usage examples

**Recommended as skill grows:**
- `config.example.json` - Example configuration
- `scripts/*.py` - Implementation scripts
- `references/*.md` - Detailed documentation
- `assets/*` - Supporting files (images, diagrams)

### SKILL.md Format

Each `SKILL.md` should include:

1. **Frontmatter** (YAML):
   ```markdown
   ---
   name: skill-name
   description: When to use this skill; include trigger phrases
   ---
   ```

2. **Usage section**: Clear trigger phrases ("download this URL", "pause all downloads", etc.)
3. **Quick Start**: How to use the skill in 3-5 steps
4. **Examples**: Concrete usage examples
5. **Configuration**: How to configure (if needed)
6. **Requirements**: What's needed to use this skill

**Keep it concise** - Move lengthy reference material to `references/` directory.

### Configuration & Secrets

- **Never commit secrets**: Add `skills/*/config.json` to `.gitignore`
- **Provide examples**: Include `config.example.json` with safe defaults
- **Use environment variables**: For tokens and secrets (e.g., `ARIA2_RPC_SECRET`)
- **Document clearly**: Explain configuration priority (env vars > config file > defaults)

## Code Style Guidelines

### Language & Dependencies

- **Python 3.6+** (minimum version for type hints and f-strings)
- **Prefer standard library**: Minimize external dependencies
- **Cross-platform**: Code should work on Linux, macOS, Windows

### Python Code Style

**Import order (PEP 8):**
```python
#!/usr/bin/env python3
"""Module docstring describing purpose."""

import json
import os
import sys
from typing import Any, Dict, List, Optional, Union

# Local imports
from module_name import ClassName
```

**Naming:**
- Classes: `PascalCase` (e.g., `Aria2RpcClient`)
- Functions/methods: `snake_case` (e.g., `add_uri`, `tell_status`)
- Private methods: `_leading_underscore` (e.g., `_inject_token`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_CONFIG`)
- Variables: `snake_case` (e.g., `request_id`, `endpoint_url`)

**Type hints (required):**
```python
def add_uri(
    self,
    uris: Union[str, List[str]],
    options: Dict[str, Any] = None,
    position: int = None,
) -> str:
    """Add a new download task from URIs."""
    pass
```

**Docstrings (Google style, required for public APIs):**
```python
def method_name(self, param: str) -> int:
    """
    Brief description.

    Args:
        param: Description of parameter

    Returns:
        Description of return value

    Raises:
        ExceptionType: When this exception is raised
    """
```

**Error handling:**
- Use specific exceptions (not bare `except:`)
- Create custom exception classes for domain-specific errors
- Provide actionable error messages with context
- Re-raise when appropriate, wrap when adding context

**String formatting:**
- Use f-strings: `f"Error: {message}"`
- Triple quotes for multiline strings
- Raw strings for regex: `r"^pattern\s+"`

### Testing Standards

**Test structure:**
```python
import unittest
from unittest.mock import patch, Mock

class TestFeatureName(unittest.TestCase):
    """Test feature description."""
    
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def test_specific_behavior(self):
        """Test that specific behavior works correctly."""
        pass
```

**Test organization:**
- Unit tests in `tests/unit/test_*.py`
- Integration tests in `tests/integration/test_*.py`
- Test file names match module names: `test_rpc_client.py` tests `rpc_client.py`
- One test class per class being tested
- Descriptive test method names: `test_client_initialization_with_config`

## Documentation Standards

### File Purposes

- **README.md** (repository root): Overview of all skills, installation, prerequisites
- **SKILL.md** (in skill directory): Skill activation guide, trigger phrases, quick examples
- **references/*.md** (in skill directory): Deep technical documentation, API specs
- **openspec/** (repository): Design artifacts, milestone plans, specifications
- **AGENTS.md** (repository root): This file - guidance for AI agents

### Writing Style

- **Be concise**: Get to the point quickly
- **Use examples**: Show, don't just tell
- **Include trigger phrases**: Help agents know when to activate skills
- **Actionable errors**: Error messages should suggest solutions
- **Cross-reference**: Link to relevant docs when needed

### User-Facing Documentation Requirements (CRITICAL)

**All user-facing documentation must be written from the user's perspective, never from the implementation or development perspective.**

**Scope:** This applies to all externally-facing documentation:
- `SKILL.md` files
- `README.md` files  
- `references/*.md` files in skill directories
- Example script help text and comments
- Any documentation users will read

**Core principles:**

1. **Organize by user intent and use cases** - Not by implementation phases, milestones, or internal architecture
2. **Use natural, actionable language** - Not technical jargon or developer terminology
3. **Show what users can accomplish** - Not how the code works internally
4. **Provide concrete examples** - Real-world scenarios users can relate to
5. **Hide implementation details** - Development milestones, refactoring phases, internal module names should not appear in user docs

**What users care about:**
- What can I do with this?
- How do I use it?
- What will happen when I run this command?
- How do I configure it?
- How do I troubleshoot problems?

**What users don't care about:**
- Implementation milestones or phases
- Internal code architecture
- Development roadmap details
- Which sprint/version features were added

**Before publishing any user-facing documentation, ask:**
- Would a user who knows nothing about the codebase understand this?
- Is this organized around what users want to do, or how we built it?
- Does this help users accomplish their goals?

**Reference implementation:** Check existing `SKILL.md` files in the repository for examples of user-oriented documentation.

**Files that can include technical details:**
- `openspec/` design docs - These are for development planning
- Code comments and docstrings - These are for developers
- Test files - These are for development
- This file (`AGENTS.md`) - This is for AI agents working on the code

## Common Patterns

### Path Resolution

```python
# Get paths relative to current script
script_dir = os.path.dirname(os.path.abspath(__file__))
skill_dir = os.path.dirname(script_dir)
config_path = os.path.join(skill_dir, "config.json")

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

### Main Script Pattern

```python
if __name__ == "__main__":
    try:
        # Main logic here
        print("✓ Success message")
    except CustomError as e:
        print(f"✗ Specific error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)
```

### Configuration Loading Priority

1. **Environment variables** (highest priority)
2. **Configuration file** (`config.json` in skill directory)
3. **Default values** (fallback)

```python
# Environment variable naming: <SKILL_PREFIX>_<KEY>
# Example: ARIA2_RPC_HOST, ARIA2_RPC_PORT, ARIA2_RPC_SECRET
```

## Adding a New Skill

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

## Best Practices

### For Agent Authors

- Keep skills focused on specific tasks
- Make trigger phrases obvious and natural
- Provide working examples users can copy-paste
- Handle errors gracefully with helpful messages
- Document all configuration options
- Test on multiple platforms if possible

### For AI Coding Agents

- Read the skill's `SKILL.md` first to understand its purpose
- Check `references/` for technical details before making changes
- Follow existing code patterns in the skill
- Run tests after making changes
- Update documentation when changing behavior
- Never commit secrets or personal configuration

## Getting Help

- **Skill-specific questions**: Read `skills/<skill-name>/SKILL.md` and `skills/<skill-name>/references/`
- **Repository structure**: See this file (AGENTS.md)
- **Design decisions**: Check `openspec/changes/<skill-name>/` for planning docs
- **Examples**: Look at existing skills like `aria2-json-rpc` as reference
