# Milestone 1 Release Notes

## Version 1.0.0 - Core Operations

### Overview
Milestone 1 establishes the foundation of the aria2 JSON-RPC skill, providing essential download management capabilities. This release enables basic download operations, status monitoring, and global statistics retrieval.

### New Features

#### Core RPC Methods
- **aria2.addUri** - Add HTTP/HTTPS/FTP downloads with single or multiple URLs
- **aria2.tellStatus** - Query download progress, speed, and completion status by GID
- **aria2.remove** - Stop and remove active or waiting downloads
- **aria2.getGlobalStat** - View global statistics (active, waiting, stopped counts, speeds)

#### Infrastructure
- JSON-RPC 2.0 client with HTTP POST transport
- Token-based authentication support (`token:<SECRET>`)
- Three-tier configuration (environment variables → config.json → defaults)
- Natural language command mapping
- Python 3.6+ compatibility with zero external dependencies

#### Testing
- Unit tests for RPC client (HTTP POST, token injection, response parsing)
- Unit tests for configuration module (config.json, environment variables)
- Unit tests for natural language mapping
- Mock aria2 server for testing without real daemon

### Configuration

```json
{
  "host": "localhost",
  "port": 6800,
  "secret": null,
  "secure": false,
  "timeout": 30000
}
```

Environment variables: `ARIA2_RPC_HOST`, `ARIA2_RPC_PORT`, `ARIA2_RPC_SECRET`, `ARIA2_RPC_SECURE`

### Usage Examples

```bash
# Download a file
python -c "from scripts.rpc_client import Aria2RpcClient; from scripts.config_loader import load_config; c = Aria2RpcClient(load_config()); print(c.add_uri(['http://example.com/file.zip']))"

# Check status
python -c "from scripts.rpc_client import Aria2RpcClient; from scripts.config_loader import load_config; c = Aria2RpcClient(load_config()); print(c.tell_status('GID'))"
```

### Requirements
- aria2 daemon with RPC enabled (`--enable-rpc`)
- Python 3.6+
- Network access to aria2 RPC endpoint

### Known Limitations
- No BitTorrent support (coming in Milestone 3)
- No batch operations like pauseAll/unpauseAll (coming in Milestone 2)
- HTTP POST only (WebSocket support in Milestone 3)

### Documentation
- SKILL.md with usage instructions
- references/aria2-methods.md with method documentation
- Example configuration in assets/config.example.json

### Testing
Run unit tests:
```bash
cd skills/aria2-json-rpc
python -m unittest discover -s tests/unit -v
```

### Migration Notes
This is the initial release. No migration required.

### Rollback
Milestone 1 provides the foundation. All future milestones build upon this base.

---

**Release Date**: 2026-02-02
**Status**: Stable
**Dependencies**: Python 3.6+, aria2 daemon
