# Troubleshooting

Tips and solutions for common problems encountered during development, dependency management, and testing.

## Overview

This guide helps resolve common issues when developing skills or working with this repository.

## Common Issues

### Import Errors

**Problem**: `ImportError` or `ModuleNotFoundError` when running scripts

**Solutions**:
1. Ensure you're running from the correct directory
2. Add script directory to Python path:
   ```python
   import sys
   sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
   ```
3. Check that virtual environment is activated
4. Install missing dependencies: `uv pip install -e .`

### Test Failures

**Problem**: Tests fail unexpectedly

**Solutions**:
1. Run specific test to isolate: `just test-file tests/unit/test_specific.py`
2. Check for environment-specific issues (paths, permissions)
3. Verify test data is present
4. Check mock configurations in unit tests
5. Clear Python cache: `find . -type d -name __pycache__ -exec rm -rf {} +`

### Configuration Issues

**Problem**: Skill can't find or load configuration

**Solutions**:
1. Verify `config.json` exists (copied from `config.example.json`)
2. Check environment variables are set correctly
3. Ensure config file is in the correct location (skill directory)
4. Validate JSON syntax: `python3 -m json.tool config.json`

### Permission Denied

**Problem**: Can't execute scripts

**Solutions**:
1. Add execute permission: `chmod +x script.py`
2. Or run with Python explicitly: `python3 script.py`
3. Check file ownership on Linux/macOS

## Getting Help

### Where to Look

- **Skill-specific questions**: Read `skills/<skill-name>/SKILL.md` and `skills/<skill-name>/references/`
- **Repository structure**: See [Repository Structure](./agents-repo-structure.md)
- **Design decisions**: Check `openspec/changes/<skill-name>/` for planning docs
- **Examples**: Look at existing skills like `aria2-json-rpc` as reference

### Debug Tips

1. **Enable verbose logging** when available
2. **Check logs** for detailed error messages
3. **Isolate the issue** with minimal reproduction case
4. **Read error messages carefully** - they often contain the solution
5. **Search existing issues** or documentation

## UV-Specific Issues

### Slow Resolution

```bash
# Clear UV cache
rm -rf ~/.cache/uv

# Retry installation
uv pip install -e .
```

### Lock File Conflicts

```bash
# Regenerate lock file
uv pip compile pyproject.toml -o requirements.lock --upgrade
```

## Still Stuck?

1. Check all documentation in the `/docs` directory
2. Look at similar skills for working examples
3. Review the test files for usage patterns
4. Examine the justfile for available commands

## Navigation

- [Repository Structure](./agents-repo-structure.md) - Repository organization
- [Skill Development Standards](./agents-skill-standards.md) - Building skills
- [Python Code Style Guide](./agents-style-guide.md) - Code style requirements
- [Testing Standards](./agents-testing.md) - How to write tests
- [Documentation Standards](./agents-docs.md) - Writing user-facing docs
- [Common Code Patterns](./agents-patterns.md) - Reusable patterns
- [Best Practices](./agents-best-practices.md) - Recommendations for quality
