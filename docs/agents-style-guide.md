# Python Code Style Guide

Enforced code style and best practices for Python code in this repository.

## Overview

All Python code in this repository must follow consistent style guidelines to ensure readability, maintainability, and collaboration.

## Language & Dependencies

- **Python 3.6+** (minimum version for type hints and f-strings)
- **Prefer standard library**: Minimize external dependencies
- **Cross-platform**: Code should work on Linux, macOS, Windows

## Import Order (PEP 8)

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

**Order:**
1. Standard library imports
2. Third-party imports (if any)
3. Local imports

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `Aria2RpcClient` |
| Functions/methods | snake_case | `add_uri`, `tell_status` |
| Private methods | _leading_underscore | `_inject_token` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_CONFIG` |
| Variables | snake_case | `request_id`, `endpoint_url` |

## Type Hints (Required)

All public APIs must include type hints:

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

## Docstrings (Google Style)

All public methods must include docstrings:

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

## Error Handling

- Use specific exceptions (not bare `except:`)
- Create custom exception classes for domain-specific errors
- Provide actionable error messages with context
- Re-raise when appropriate, wrap when adding context

```python
class CustomError(Exception):
    """Domain-specific error with context."""
    pass

try:
    result = risky_operation()
except ValueError as e:
    raise CustomError(f"Invalid configuration: {e}") from e
```

## String Formatting

- Use f-strings: `f"Error: {message}"`
- Triple quotes for multiline strings
- Raw strings for regex: `r"^pattern\s+"`

## Navigation

- [Repository Structure](./agents-repo-structure.md) - Repository organization
- [Skill Development Standards](./agents-skill-standards.md) - Building skills
- [Testing Standards](./agents-testing.md) - How to write tests
- [Documentation Standards](./agents-docs.md) - Writing user-facing docs
- [Common Code Patterns](./agents-patterns.md) - Reusable patterns
- [Best Practices](./agents-best-practices.md) - Recommendations for quality
