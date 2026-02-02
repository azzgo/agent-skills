# Documentation Standards & User-Facing Docs

How to write, structure, and present documentation for users and developers in this repository.

## Overview

Documentation is critical for both users (who want to use skills) and developers (who want to understand or modify skills). This guide ensures all documentation is consistent and user-focused.

## File Purposes

| File | Location | Purpose |
|------|----------|---------|
| README.md | Repository root | Overview of all skills, installation, prerequisites |
| SKILL.md | In skill directory | Skill activation guide, trigger phrases, quick examples |
| references/*.md | In skill directory | Deep technical documentation, API specs |
| openspec/ | Repository | Design artifacts, milestone plans, specifications |
| AGENTS.md | Repository root | Guidance for AI agents working on code |

## Writing Style

- **Be concise**: Get to the point quickly
- **Use examples**: Show, don't just tell
- **Include trigger phrases**: Help agents know when to activate skills
- **Actionable errors**: Error messages should suggest solutions
- **Cross-reference**: Link to relevant docs when needed

## User-Facing Documentation Requirements (CRITICAL)

**All user-facing documentation must be written from the user's perspective, never from the implementation or development perspective.**

### Scope

Applies to all externally-facing documentation:
- `SKILL.md` files
- `README.md` files
- `references/*.md` files in skill directories
- Example script help text and comments
- Any documentation users will read

### Core Principles

1. **Organize by user intent and use cases** - Not by implementation phases, milestones, or internal architecture
2. **Use natural, actionable language** - Not technical jargon or developer terminology
3. **Show what users can accomplish** - Not how the code works internally
4. **Provide concrete examples** - Real-world scenarios users can relate to
5. **Hide implementation details** - Development milestones, refactoring phases, internal module names should not appear in user docs

### What Users Care About

- What can I do with this?
- How do I use it?
- What will happen when I run this command?
- How do I configure it?
- How do I troubleshoot problems?

### What Users Don't Care About

- Implementation milestones or phases
- Internal code architecture
- Development roadmap details
- Which sprint/version features were added

### Quality Check

Before publishing any user-facing documentation, ask:
- Would a user who knows nothing about the codebase understand this?
- Is this organized around what users want to do, or how we built it?
- Does this help users accomplish their goals?

### Reference Implementation

Check existing `SKILL.md` files in the repository for examples of user-oriented documentation.

## Technical Documentation

Files that CAN include technical details:
- `openspec/` design docs - These are for development planning
- Code comments and docstrings - These are for developers
- Test files - These are for development
- `AGENTS.md` - This is for AI agents working on the code

## Navigation

- [Repository Structure](./agents-repo-structure.md) - Repository organization
- [Skill Development Standards](./agents-skill-standards.md) - Building skills
- [Python Code Style Guide](./agents-style-guide.md) - Code style requirements
- [Testing Standards](./agents-testing.md) - How to write tests
- [Common Code Patterns](./agents-patterns.md) - Reusable patterns
- [Best Practices](./agents-best-practices.md) - Recommendations for quality
