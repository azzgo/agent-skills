# Documentation Standards & User-Facing Docs

How to write, structure, and present documentation for users and developers in this repository.

## Overview

Documentation is critical for both users (who want to use skills) and developers (who want to understand or modify skills). This guide ensures all documentation is consistent and audience-appropriate.

## Documentation by Audience

### Agent-Facing Documentation

**Purpose**: Instruct AI agents on how to use skills and work in this repository

**Locations**:
- `skills/*/SKILL.md` - Instructions for agents on which scripts to call, parameters to use
- `skills/*/references/*.md` - Detailed execution guides for agents
- `docs/agents-*.md` - Guides for AI agents working on code
- `docs/manual-test/` - Test instructions for agents

**Style**:
- Direct instructions ("Execute script X", "Call function Y")
- Technical parameter details
- Command examples with exact syntax
- Reference to implementation scripts

### User-Facing Documentation

**Purpose**: Help end users understand what they can accomplish and how to use features

**Locations**:
- Repository root `README.md` - Overview, installation
- `docs/*.md` (except `agents-*.md` and `manual-test/`)
- Example script help text

**Style**:
- Natural language, use cases
- Focus on outcomes, not implementation
- Hide internal details
- Conversational and helpful

### Spec-Facing Documentation

**Purpose**: Design planning and architectural decisions

**Locations**:
- `openspec/changes/` - Design artifacts, proposals
- `openspec/specs/` - Specifications

**Style**:
- Technical, detailed
- Architecture and design decisions
- Implementation planning

## File Purposes

| File | Location | Purpose | Audience |
|------|----------|---------|----------|
| README.md | Repository root | Overview of all skills, installation, prerequisites | User |
| SKILL.md | In skill directory | Instructions on how agents should use the skill | Agent |
| references/*.md | In skill directory | Detailed execution instructions for agents | Agent |
| openspec/ | Repository | Design artifacts, milestone plans, specifications | Spec |
| AGENTS.md | Repository root | Entry point for AI agents working on code | Agent |
| docs/agents-*.md | docs/ | Guides for AI agents developing in this repo | Agent |
| docs/manual-test/ | docs/ | Test instructions for agents | Agent |

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

## Agent-Facing Documentation Requirements

**Purpose**: Instruct AI agents clearly and precisely on how to use skills.

### Core Principles

1. **Be explicit and prescriptive** - Tell agents exactly what to do ("Execute: `python scripts/...`")
2. **Include exact commands** - Show the full command with parameters
3. **Explain the flow** - User intent → Agent action → Output formatting
4. **Prevent common mistakes** - Use warnings like "⚠️ DO NOT manually construct..."
5. **Reference implementation** - Point to actual scripts and functions

### Writing Style for Agent Docs

```markdown
**User says**: "download this file"

**You should do**:
1. Identify intent: Add new download
2. Execute: `python scripts/rpc_client.py aria2.addUri '["<url>"]'`
3. Parse the returned GID and format a user-friendly response

**Do NOT**: Manually construct JSON-RPC requests
```

### Agent Doc Checklist

- [ ] Clear mapping from user intent to agent action
- [ ] Exact commands with parameter examples
- [ ] Links to relevant scripts and references
- [ ] Common mistakes section with warnings
- [ ] Example of expected output format

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
