---
name: aria2-json-rpc
description: Interact with aria2 download manager via JSON-RPC 2.0. Manage downloads, query status, and control tasks through natural language commands. Use when working with aria2, download management, or torrent operations.
license: MIT
compatibility: Requires Python 3.6+. WebSocket support requires websockets package (pip install websockets).
metadata:
  author: ISON
  version: "1.0"
---

## What This Skill Does

This skill enables you to control aria2 download manager through natural language commands:
- Download files (HTTP/HTTPS/FTP/Magnet/Torrent/Metalink)
- Monitor download progress and status
- Control downloads (pause, resume, remove)
- Manage batch operations (pause all, resume all)
- View statistics and configure options

## How to Use (For AI Agents)

**⚠️ CRITICAL: DO NOT manually construct JSON-RPC requests.**

**✅ ALWAYS use the Python scripts in the `scripts/` directory.**

**⚠️ IMPORTANT: Use `python3` command, NOT `python`** (especially on macOS where `python` symlink doesn't exist)

### Quick Start

1. **Identify** what the user wants (download, status, pause, etc.)
2. **Look up** the appropriate command in the execution guide
3. **Execute** the Python script with the Bash tool using `python3`
4. **Format** the output in a user-friendly way

### Example

**User:** "download http://example.com/file.zip"

**You execute:**
```bash
python3 scripts/rpc_client.py aria2.addUri '["http://example.com/file.zip"]'
```

**You respond:** "✓ Download started! GID: 2089b05ecca3d829"

## Documentation Structure

**For detailed execution instructions, see:**
- **[references/execution-guide.md](references/execution-guide.md)** - Complete guide for AI agents with:
  - Command mapping table (user intent → script call)
  - Parameter formatting rules
  - Step-by-step examples
  - Common mistakes to avoid
  - Response formatting guidelines

**For aria2 method reference, see:**
- **[references/aria2-methods.md](references/aria2-methods.md)** - Detailed aria2 RPC method documentation

## Common Commands Quick Reference

| User Intent | Command Example |
|-------------|----------------|
| Download a file | `python3 scripts/rpc_client.py aria2.addUri '["http://example.com/file.zip"]'` |
| Check status | `python3 scripts/rpc_client.py aria2.tellStatus <GID>` |
| List active downloads | `python3 scripts/rpc_client.py aria2.tellActive` |
| List stopped downloads | `python3 scripts/rpc_client.py aria2.tellStopped 0 100` |
| Pause download | `python3 scripts/rpc_client.py aria2.pause <GID>` |
| Resume download | `python3 scripts/rpc_client.py aria2.unpause <GID>` |
| Show statistics | `python3 scripts/rpc_client.py aria2.getGlobalStat` |
| Show version | `python3 scripts/rpc_client.py aria2.getVersion` |
| Purge results | `python3 scripts/rpc_client.py aria2.purgeDownloadResult` |

For detailed usage and more commands, see [execution-guide.md](references/execution-guide.md).

## Available Scripts

- `scripts/rpc_client.py` - Main interface for RPC calls
- `scripts/examples/list-downloads.py` - Formatted download list
- `scripts/examples/pause-all.py` - Pause all downloads
- `scripts/examples/add-torrent.py` - Add torrent downloads
- `scripts/examples/monitor-downloads.py` - Real-time monitoring
- `scripts/examples/set-options.py` - Modify options

## Configuration

Scripts automatically load configuration from:
1. Environment variables (`ARIA2_RPC_HOST`, `ARIA2_RPC_PORT`, etc.)
2. `config.json` in skill directory
3. Defaults (localhost:6800)

**You don't need to configure anything** - scripts handle it automatically.

## Key Principles

1. **Never** construct JSON-RPC requests manually
2. **Always** call Python scripts via Bash tool using `python3` (not `python`)
3. **Parse** script output and format for users
4. **Refer to** execution-guide.md when unsure

## Supported Operations

### Download Management
- Add downloads (HTTP/FTP/Magnet/Torrent/Metalink)
- Pause/resume (individual or all)
- Remove downloads
- Add with custom options

### Monitoring
- Check download status
- List active/waiting/stopped downloads
- Get global statistics
- Real-time monitoring

### Configuration
- Get/change download options
- Get/change global options
- Query aria2 version
- List available methods

### Maintenance
- Purge download results
- Remove specific results

## Need Help?

- **Execution details:** [references/execution-guide.md](references/execution-guide.md)
- **Method reference:** [references/aria2-methods.md](references/aria2-methods.md)
- **Troubleshooting:** [references/troubleshooting.md](references/troubleshooting.md)
- **aria2 official docs:** https://aria2.github.io/
