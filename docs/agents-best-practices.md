# Best Practices

General recommendations and practices for agent authors and AI coding agents working in this repository.

## Overview

Following these best practices ensures high-quality, maintainable skills that are easy to use and extend.

## For Agent Authors

### Skill Design

- **Keep skills focused**: Each skill should do one thing well
- **Make trigger phrases obvious**: Use natural, discoverable phrases
- **Provide working examples**: Users should be able to copy-paste and run
- **Handle errors gracefully**: Provide helpful, actionable error messages
- **Document all configuration**: Every option should be explained
- **Test on multiple platforms**: Linux, macOS, Windows when possible

### Code Quality

- **Follow style guide**: Adhere to the [Python Code Style Guide](./agents-style-guide.md)
- **Write tests**: Both unit and integration tests
- **Use type hints**: Required for all public APIs
- **Document thoroughly**: Docstrings and comments where needed
- **Handle edge cases**: Empty inputs, network failures, etc.

### Security

- **Never commit secrets**: Use environment variables
- **Validate inputs**: Sanitize user input before processing
- **Use least privilege**: Request minimal permissions needed
- **Log carefully**: Don't log sensitive information

## For AI Coding Agents

### Before Making Changes

- Read the skill's `SKILL.md` first to understand its purpose
- Check `references/` for technical details
- Look at existing code patterns in the skill
- Understand the context before modifying

### While Making Changes

- Follow existing code patterns
- Maintain backwards compatibility when possible
- Add/update tests for new functionality
- Update documentation when changing behavior
- Run tests frequently during development

### After Making Changes

- Run the full test suite: `just test`
- Verify documentation is accurate
- Check for any broken links or references
- Ensure no secrets or personal data was added
- Review changes before committing

### Never Do

- Never commit secrets or personal configuration
- Never break existing functionality without migration path
- Never ignore test failures
- Never remove documentation without replacement
- Never use non-cross-platform code without good reason

## Adding a New Skill Checklist

- [ ] Create directory structure with all required folders
- [ ] Write `SKILL.md` with frontmatter and usage examples
- [ ] Implement core scripts in `scripts/`
- [ ] Add `config.example.json` (never real config with secrets)
- [ ] Write unit tests in `tests/unit/`
- [ ] Write integration tests in `tests/integration/`
- [ ] Update repository `README.md`
- [ ] Optional: Create design docs in `openspec/changes/`

## Navigation

- [Repository Structure](./agents-repo-structure.md) - Repository organization
- [Skill Development Standards](./agents-skill-standards.md) - Building skills
- [Python Code Style Guide](./agents-style-guide.md) - Code style requirements
- [Testing Standards](./agents-testing.md) - How to write tests
- [Documentation Standards](./agents-docs.md) - Writing user-facing docs
- [Common Code Patterns](./agents-patterns.md) - Reusable patterns
- [Troubleshooting](./agents-troubleshooting.md) - Common issues and solutions
