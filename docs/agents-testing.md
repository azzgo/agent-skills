# Testing Standards

This document explains recommendations and requirements for unit and integration testing in this repository.

## Overview

All skills should have comprehensive test coverage including both unit tests (mocked dependencies) and integration tests (testing with real or mock services).

## Test Structure

### Basic Test Template

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

## Test Organization

| Test Type | Location | Purpose |
|-----------|----------|---------|
| Unit tests | `tests/unit/test_*.py` | Test individual functions/classes with mocked dependencies |
| Integration tests | `tests/integration/test_*.py` | Test with real or realistic mock services |

### Naming Conventions

- Test file names match module names: `test_rpc_client.py` tests `rpc_client.py`
- One test class per class being tested
- Descriptive test method names: `test_client_initialization_with_config`

## Running Tests

```bash
# Run all tests (unit + integration)
just test

# Run unit tests only
just test-unit

# Run integration tests only
just test-mock-server

# Run a specific test file
just test-file tests/unit/test_rpc_client.py

# Run a specific test method
python3 -m unittest tests.unit.test_rpc_client.TestAria2RpcClient.test_client_initialization
```

## Best Practices

- Test both success and failure cases
- Mock external dependencies (network, file system) in unit tests
- Use realistic test data
- Keep tests independent and idempotent
- Aim for >80% code coverage

## Navigation

- [Repository Structure](./agents-repo-structure.md) - Repository organization
- [Skill Development Standards](./agents-skill-standards.md) - Building skills
- [Python Code Style Guide](./agents-style-guide.md) - Code style requirements
- [Documentation Standards](./agents-docs.md) - Writing user-facing docs
- [Common Code Patterns](./agents-patterns.md) - Reusable patterns
- [Best Practices](./agents-best-practices.md) - Recommendations for quality
