# Dependency Management and UV Usage Guide

How to manage dependencies safely with UV and best practices for keeping Python environments clean in this project.

## Overview

This repository uses [UV](https://github.com/astral-sh/uv) for fast, reliable Python package management. UV is a modern Python package installer and resolver written in Rust.

## Why UV?

- **Speed**: 10-100x faster than pip
- **Reliable**: Deterministic resolution with lock files
- **Unified**: Handles both package installation and virtual environment management
- **Standards-compliant**: Uses standard pyproject.toml

## Installation

```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or on macOS with Homebrew
brew install uv
```

## Common Commands

### Install Dependencies

```bash
# Install from pyproject.toml
uv pip install -e .

# Install with all extras
uv pip install -e ".[dev]"

# Install specific package
uv pip install requests
```

### Lock Dependencies

```bash
# Generate/update lock file
uv pip compile pyproject.toml -o requirements.lock

# Install from lock file (reproducible builds)
uv pip sync requirements.lock
```

### Virtual Environment

```bash
# Create virtual environment
uv venv

# Create with specific Python version
uv venv --python python3.11

# Activate (standard activation)
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

## Project Configuration

### pyproject.toml Example

```toml
[project]
name = "aria2-json-rpc-skill"
version = "1.0.0"
dependencies = [
    "requests>=2.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
    "mypy>=1.0.0",
]
```

## Best Practices

1. **Pin major versions**: Use `>=` for flexibility but pin major versions to avoid breaking changes
2. **Separate dev dependencies**: Use optional-dependencies for development tools
3. **Lock for production**: Use lock files for reproducible production deployments
4. **Regular updates**: Run `uv pip compile` regularly to get security updates
5. **Minimize dependencies**: Prefer standard library when possible

## Troubleshooting

### Slow Resolution

If dependency resolution is slow:
```bash
# Clear cache and retry
rm -rf ~/.cache/uv
uv pip install -e .
```

### Conflicts

UV provides clear error messages for conflicts. Read them carefully and adjust version constraints.

## Navigation

- [Repository Structure](./agents-repo-structure.md) - Repository organization
- [Skill Development Standards](./agents-skill-standards.md) - Building skills
- [Python Code Style Guide](./agents-style-guide.md) - Code style requirements
- [Testing Standards](./agents-testing.md) - How to write tests
- [Documentation Standards](./agents-docs.md) - Writing user-facing docs
- [Common Code Patterns](./agents-patterns.md) - Reusable patterns
- [Best Practices](./agents-best-practices.md) - Recommendations for quality
- [Troubleshooting](./agents-troubleshooting.md) - Common issues and solutions
