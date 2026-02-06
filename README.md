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

The skill works out-of-the-box with default settings (localhost:6800). For custom configurations, the skill supports multiple configuration sources with the following priority:

**Priority (highest to lowest):**
1. Environment variables (temporary override)
2. Skill directory config (project-specific)
3. User config directory (global, update-safe) 🆕
4. Defaults

**Recommended Setup (Update-Safe):**

Initialize user configuration that survives skill updates:
```bash
# Navigate to the skill directory
cd skills/aria2-json-rpc

# Initialize user config
python3 scripts/config_loader.py init --user

# Edit the config file
nano ~/.config/aria2-skill/config.json
```

Example configuration:
```json
{
  "host": "localhost",
  "port": 6800,
  "secret": "YOUR_TOKEN",
  "secure": false,
  "timeout": 30000
}
```

**Alternative: Project-Specific Config**

For testing or project-specific settings (⚠️ lost on updates):
```bash
cd skills/aria2-json-rpc
python3 scripts/config_loader.py init --local
# Edit skills/aria2-json-rpc/config.json
```

**Alternative: Environment Variables**

For temporary overrides or CI/CD:
```bash
export ARIA2_RPC_HOST="localhost"
export ARIA2_RPC_PORT=6800
export ARIA2_RPC_SECRET="YOUR_TOKEN"
```

**Configuration Management:**
```bash
# Show current configuration
python3 scripts/config_loader.py show

# Test connection
python3 scripts/config_loader.py test
```

---

### quote0-dot-screen 🚧

A skill to control Quote/0 electronic screen devices via the Dot Developer Platform APIs.

**Status: In Development**

**Key Features:**
- **Device Management**: List devices, get device status, retrieve device serial numbers
- **Content Control**: Display text content, display images, switch to next content
- **Task Management**: List content tasks configured on devices
- **API Integration**: Full access to Dot API endpoints for automation

#### Prerequisites

1.  **Dot API Key**: Get an API key from the Dot. App (see https://dot.mindreset.tech/docs/service/service/open/get_api)
2.  **Environment Variable**: Set `DOT_API_KEY` environment variable with your API key
3.  **Network Access**: The agent needs access to api.mindreset.tech

**Quick Start:**
```bash
export DOT_API_KEY=your_api_key_here
```

#### Usage Examples

List all devices:
```bash
cd skills/quote0-dot-screen
python scripts/list_devices.py
```

Display text on a device:
```bash
python scripts/display_text.py <device_id> "Hello World" --title "Greeting" --signature "Today"
```

Display an image:
```bash
python scripts/display_image.py <device_id> "https://example.com/image.png"
```

Get device status:
```bash
python scripts/device_status.py <device_id>
```

Switch to next content:
```bash
python scripts/switch_next.py <device_id>
```

List device tasks:
```bash
python scripts/list_tasks.py <device_id>
```

#### Scripts

- `scripts/display_text.py` - Display text content on device
- `scripts/display_image.py` - Display image content on device
- `scripts/switch_next.py` - Switch device to next content
- `scripts/list_devices.py` - List all available devices
- `scripts/device_status.py` - Get device status
- `scripts/list_tasks.py` - List content tasks on device

#### API Documentation

For detailed API reference, see https://dot.mindreset.tech/docs/service/open or the skill's `references/api.md` file.

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
