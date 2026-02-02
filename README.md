# Agent Skills

Skills follow the Agent Skills format: https://agentskills.io/

## Available Skills

### aria2-json-rpc

通过 JSON-RPC 控制 `aria2` daemon。

Use when:
- "download this URL / magnet / torrent"
- "pause/resume/remove this download"
- "list active/waiting/stopped downloads"
- "show global stats / speed / progress"

Skill definition: `skills/aria2-json-rpc/SKILL.md`

## Installation

If you use a Skills installer (e.g. `skills` CLI):

```bash
npx skills add <github-org-or-user>/<repo>
```

Or install by copying the skill folder into your agent's skills directory (agent-specific).

## Prerequisites

- `aria2c` running with RPC enabled (HTTP JSON-RPC endpoint)
- Network access to the RPC endpoint

Example (local):

```bash
aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port=6800
```

If you use a secret:

```bash
aria2c --enable-rpc --rpc-secret="YOUR_TOKEN" --rpc-listen-all=false --rpc-listen-port=6800
```

## Configuration

Example config file:
- `skills/aria2-json-rpc/config.example.json`

Recommended approach:
- Copy `skills/aria2-json-rpc/config.example.json` to `skills/aria2-json-rpc/config.json`
- Do not commit `config.json` (it may contain secrets)

Example:

```json
{
  "host": "localhost",
  "port": 6800,
  "secret": null,
  "secure": false,
  "timeout": 30000
}
```

## Repo Layout

```text
skills/
  aria2-json-rpc/
    SKILL.md                      # Skill definition
    config.example.json           # Configuration template
    scripts/                      # Implementation scripts
    references/                   # Technical documentation
openspec/
  changes/
    aria2-json-rpc-skill/         # Design + milestone plan
tests/
  unit/                           # Unit tests
  integration/                    # Integration tests
justfile                          # Test commands
pyproject.toml                    # Dependency configuration (UV)
run_tests.sh                      # Test runner (called by justfile)
AGENTS.md                         # AI agent guidelines
```

## Development

### Requirements

- Python 3.6+
- [UV](https://github.com/astral-sh/uv) for dependency management (optional, for Milestone 3 WebSocket features)
- [Just](https://just.systems/) command runner

### Running Tests

All test commands use `justfile`:

```bash
# Run all tests
just test

# Run specific milestone tests
just test-m1   # Milestone 1 (no external deps)
just test-m2   # Milestone 2 (no external deps)
just test-m3   # Milestone 3 (auto-installs websockets in isolated env)

# Run specific test file
just test-file tests/unit/test_rpc_client.py
just test-file-uv tests/unit/test_milestone3.py  # For files needing dependencies
```

### Installing Dependencies

UV is optional and only needed for Milestone 3 (WebSocket) features:

```bash
# Check if UV is installed
just check-uv

# Install UV (one-time setup)
just install-uv

# Or install manually
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Note**: Milestones 1-2 use only Python builtin libraries and have zero external dependencies.

### For AI Agents

See `AGENTS.md` for comprehensive development guidelines, including:
- Repository structure and naming conventions
- Dependency management with UV (critical: no global pollution)
- Testing standards and workflows
- Documentation requirements
- Code style guidelines

## Skill Features

### Three-Milestone Implementation

The skill is organized in three milestones for progressive feature adoption:

**Milestone 1 - Core Operations**
- `aria2.addUri` - Add HTTP/HTTPS/FTP downloads
- `aria2.tellStatus` - Query download progress and status
- `aria2.remove` - Remove downloads
- `aria2.getGlobalStat` - View global statistics

**Milestone 2 - Batch Operations**
- Pause/unpause individual or all downloads
- List downloads by state (active, waiting, stopped)
- Modify download and global options
- Maintenance operations (purge results, remove records)

**Milestone 3 - Advanced Features**
- BitTorrent support (`aria2.addTorrent`)
- Metalink support (`aria2.addMetalink`)
- WebSocket event notifications (optional)
- Batch multicall operations

### Testing

Comprehensive test coverage:
- Unit tests for all core functionality
- Integration tests with mock aria2 server
- Support for testing without real aria2 daemon

```bash
# Run unit tests
just test-m1
just test-m2
just test-m3

# Run integration tests
cd skills/aria2-json-rpc/tests/integration
python run_integration_tests.py
```

### Zero Dependencies (Milestones 1-2)

Core functionality requires only Python 3.6+ with builtin modules:
- `urllib.request` for HTTP POST
- `json` for JSON-RPC formatting
- `os` for environment variables
- `base64` for encoding (Milestone 3)

Optional: `websockets` library for real-time event notifications.

### Security

- Token-based authentication support
- Environment variable secret storage
- HTTPS transport option
- No secrets committed to repository

## Deployment

### Skill Registration

The skill is ready for OpenCode agent framework integration:

1. **Skill Structure**: `skills/aria2-json-rpc/`
   - `SKILL.md` - Skill definition and usage
   - `scripts/` - Implementation scripts
   - `assets/` - Configuration templates
   - `references/` - Documentation and release notes
   - `tests/` - Unit and integration tests

2. **Verification**: All artifacts present and validated
3. **Testing**: Full test suite passes
4. **Documentation**: Complete user and developer docs

### Rollback Capability

Each milestone is additive with no breaking changes:
- Milestone 1: Foundation (always required)
- Milestone 2: Adds batch operations (optional)
- Milestone 3: Adds torrent/WebSocket (optional)

To rollback:
- Remove milestone-specific scripts if needed
- Configuration format remains unchanged
- Core functionality preserved

### Release Notes

- [Milestone 1 Release Notes](skills/aria2-json-rpc/references/RELEASE_NOTES_M1.md)
- [Milestone 2 Release Notes](skills/aria2-json-rpc/references/RELEASE_NOTES_M2.md)
- [Milestone 3 Release Notes](skills/aria2-json-rpc/references/RELEASE_NOTES_M3.md)

## License

MIT (see `LICENSE`).
