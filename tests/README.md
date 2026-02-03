# Test Organization

This directory contains tests for the aria2-json-rpc-skills project, organized by test type and skill.

## Directory Structure

```
tests/
├── unit/                           # Unit tests
│   └── aria2-json-rpc-skill/      # Tests for aria2-json-rpc skill
│       ├── test_rpc_client.py     # RPC client tests
│       ├── test_config_loader.py  # Configuration loader tests
│       ├── test_command_mapper.py # Command mapper tests
│       └── test_milestone3.py     # Milestone 3 features tests
│
├── integration/                    # Integration tests
│
└── README.md                       # This file
```

## Design Rationale

### Why This Structure?

The test directory is organized with **test type first, skill second**:
- `tests/{unit,integration}/aria2-json-rpc-skill/...`

This structure provides several benefits:

1. **Clear Test Type Separation**: Unit tests and integration tests are clearly separated at the top level
2. **Skill Isolation**: Each skill's tests are grouped in their own subdirectory, preventing confusion between different features
3. **Future-Proof**: When new skills are added, they can follow the same pattern without interfering with existing tests
4. **Standard Convention**: This follows the common pattern of organizing tests by type first

### Alternative Considered

We considered `tests/aria2-json-rpc-skill/{unit,integration}/...` but chose the current structure because:
- Integration tests include shared components (mock server, evaluation framework) that may be reused across skills
- The type-first organization is more conventional in Python projects

## Running Tests

### Quick Commands (using just)

```bash
# Run all unit tests
just test

# Run all unit tests (alias)
just test-unit

# Run specific test file
just test-file-uv tests/unit/aria2-json-rpc-skill/test_rpc_client.py
```

### Direct Script Usage

```bash
# Run all unit tests
./run_unit_tests.sh
```

### Using pytest Directly

```bash
# Run all unit tests
uv run pytest tests/unit/ -v

# Run tests for specific skill
uv run pytest tests/unit/aria2-json-rpc-skill/ -v

# Run specific test file
uv run pytest tests/unit/aria2-json-rpc-skill/test_rpc_client.py -v

# Run specific test
uv run pytest tests/unit/aria2-json-rpc-skill/test_rpc_client.py::TestAria2RpcClient::test_client_initialization -v
```

## Test Organization

Tests are organized by the features they cover:

### Core Features
- **RPC client functionality**: HTTP POST, token injection, response parsing
- **Configuration loading**: config.json, environment variables, validation
- **Command mapping**: Natural language command parsing

### Advanced Features
- **Download control**: Pause, resume, remove operations
- **Global statistics and options**: Server-wide configuration
- **Torrent and metalink operations**: BitTorrent support
- **WebSocket client support**: Real-time notifications (requires `websockets` package)

All tests are automatically run together and include all necessary dependencies.

## Adding Tests for New Skills

When adding a new skill, follow this pattern:

1. Create skill-specific directories:
   ```bash
   mkdir -p tests/unit/your-skill-name
   mkdir -p tests/integration/your-skill-name
   ```

2. Add `__init__.py` files:
   ```bash
   touch tests/unit/your-skill-name/__init__.py
   touch tests/integration/your-skill-name/__init__.py
   ```

3. Create test files following naming conventions:
   ```
   test_<component_name>.py
   ```

4. Update `run_tests.sh` and `justfile` if needed to support the new skill's test patterns

## Test Dependencies

Tests use UV for isolated dependency management:

- **Unit Tests**: Generally require no external dependencies beyond Python stdlib
- **Integration Tests**: Manual semi-automated testing via justfile commands (e.g., `just manual-test-setup`, `just manual-test-run`). See `justfile` for available commands and `docs/manual-test/` for detailed instructions.
- **Dependency Isolation**: UV ensures test dependencies don't pollute the global Python environment

See `run_tests.sh` for automatic dependency management.
