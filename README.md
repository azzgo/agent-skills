# Agent Skills

This repository contains high-quality skills for AI agents, following the [Agent Skills](https://agentskills.io/) standard.

## Installation

Add these skills to your agent using the [Skills CLI](https://skills.sh):

```bash
npx skills add azzgo/agent-skills
```

Alternatively, you can install by manually copying the specific skill folder into your agent's skills directory.

## Available Skills

### aria2-json-rpc

A comprehensive skill to control the `aria2` download manager via JSON-RPC.

**Key Features:**
- **Download Management**: Add HTTP/HTTPS/FTP, Magnet, Torrent, and Metalink downloads.
- **Control**: Pause, resume, and remove individual or all downloads.
- **Monitoring**: List active, waiting, and stopped downloads; view global stats and progress.
- **Zero Dependencies**: Core functionality uses standard libraries (no heavy pip installs required).
- **Secure**: Supports token-based authentication and secure connections.

#### Prerequisites

1.  **aria2c Daemon**: You need `aria2c` running with RPC enabled.
2.  **Network Access**: The agent needs access to the RPC port.
3.  **WebSocket Support** (Optional): If using WebSocket connections, ensure Python version matches the requirements of the `websockets` package.

**Quick Start (Local):**
```bash
aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port=6800
```

**With Secret Token:**
```bash
aria2c --enable-rpc --rpc-secret="YOUR_TOKEN" --rpc-listen-all=false --rpc-listen-port=6800
```

#### Configuration

The skill works out-of-the-box with default settings (localhost:6800). To customize:

1.  Copy `skills/aria2-json-rpc/config.example.json` to `skills/aria2-json-rpc/config.json`.
2.  Edit the file (do not commit it if it contains secrets):

```json
{
  "host": "localhost",
  "port": 6800,
  "secret": "YOUR_TOKEN",
  "secure": false,
  "timeout": 30000
}
```

---

## For Developers

### Repository Structure

```text
skills/
  aria2-json-rpc/         # The skill source code
    SKILL.md              # Definition
    scripts/              # Python implementation
    tests/                # Tests
```

### Development Requirements

- Python 3.6+
- [Just](https://just.systems/) (command runner)
- [UV](https://github.com/astral-sh/uv) (optional, for dependency management)

### Running Tests

```bash
# Run all tests
just test

# Run specific test file
just test-file tests/unit/test_rpc_client.py
```

## License

MIT (see `LICENSE`).
