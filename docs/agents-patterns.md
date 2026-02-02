# Common Code Patterns

Frequently used patterns and code snippets for this project: path resolution, script structure, configuration loading, etc.

## Overview

These patterns are used consistently across skills in this repository. Follow these conventions to ensure code consistency and maintainability.

## Path Resolution

### Get Paths Relative to Current Script

```python
import os
import sys

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
skill_dir = os.path.dirname(script_dir)
config_path = os.path.join(skill_dir, "config.json")

# Add parent directory to Python path (for imports)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

## Main Script Pattern

### Standard Main Block

```python
import sys

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

### Key Elements

- Use checkmark (✓) and x-mark (✗) for clear status indication
- Catch specific exceptions first
- Provide actionable error messages
- Always exit with non-zero code on failure

## Configuration Loading Priority

### Priority Order

1. **Environment variables** (highest priority)
2. **Configuration file** (`config.json` in skill directory)
3. **Default values** (fallback)

### Environment Variable Naming

```python
# Format: <SKILL_PREFIX>_<KEY>
# Examples:
#   ARIA2_RPC_HOST
#   ARIA2_RPC_PORT
#   ARIA2_RPC_SECRET
```

### Configuration Loading Pattern

```python
import os
import json
from typing import Dict, Any, Optional

def load_config(skill_dir: str) -> Dict[str, Any]:
    """Load configuration with priority: env vars > config file > defaults."""
    config = {}
    
    # 1. Load from config file if exists
    config_path = os.path.join(skill_dir, "config.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
    
    # 2. Override with environment variables
    env_prefix = "ARIA2_"  # Skill-specific prefix
    for key in config:
        env_key = f"{env_prefix}{key.upper()}"
        if env_key in os.environ:
            config[key] = os.environ[env_key]
    
    return config
```

## Navigation

- [Repository Structure](./agents-repo-structure.md) - Repository organization
- [Skill Development Standards](./agents-skill-standards.md) - Building skills
- [Python Code Style Guide](./agents-style-guide.md) - Code style requirements
- [Testing Standards](./agents-testing.md) - How to write tests
- [Documentation Standards](./agents-docs.md) - Writing user-facing docs
- [Best Practices](./agents-best-practices.md) - Recommendations for quality
- [Troubleshooting](./agents-troubleshooting.md) - Common issues and solutions
