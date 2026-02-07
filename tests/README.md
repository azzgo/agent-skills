# Test Organization

This directory contains tests for agent-skills project, organized by test type and skill.

## Directory Structure

```
tests/
├── unit/                           # Unit tests
│   ├── aria2-json-rpc-skill/       # Tests for aria2-json-rpc skill
│   │   ├── test_rpc_client.py      # RPC client tests
│   │   ├── test_config_loader.py   # Configuration loader tests
│   │   ├── test_command_mapper.py  # Command mapper tests
│   │   └── test_milestone3.py     # Milestone 3 features tests
│   └── quote0-dot-screen-skill/    # Tests for quote0-dot-screen skill
│       ├── test_api_client.py      # API client tests
│       ├── test_list_devices.py    # Device listing tests
│       ├── test_device_status.py   # Device status tests
│       ├── test_display_text.py    # Text display tests
│       ├── test_display_image.py   # Image display tests
│       ├── test_switch_next.py     # Content switching tests
│       └── test_list_tasks.py     # Task listing tests
│
├── integration/                    # Integration tests
│
└── README.md                       # This file
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

Tests are organized by the skill and features they cover:

### aria2-json-rpc Skill

**Core Features:**
- **RPC client functionality**: HTTP POST, token injection, response parsing
- **Configuration loading**: config.json, environment variables, validation
- **Command mapping**: Natural language command parsing

**Advanced Features:**
- **Download control**: Pause, resume, remove operations
- **Global statistics and options**: Server-wide configuration
- **Torrent and metalink operations**: BitTorrent support
- **WebSocket client support**: Real-time notifications (requires `websockets` package)

### quote0-dot-screen Skill

**Device Management:**
- **Device listing**: API client calls, response formatting
- **Device status**: Status queries, markdown formatting

**Content Display:**
- **Text display**: API requests, optional parameters (title, signature, icon, link)
- **Image display**: Base64 encoding, dithering options, border settings

**Content Control:**
- **Switch next**: Navigation between content items
- **List tasks**: Task enumeration, task type filtering

All tests:

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
