# Execution Guide for AI Agents

This guide provides detailed instructions for AI agents on how to execute aria2-json-rpc skill commands.

## Core Principle

**NEVER manually construct JSON-RPC requests. ALWAYS use the provided Python scripts.**

## Execution Workflow

1. **Parse** the user's natural language command to identify intent
2. **Map** the intent to the appropriate script and method
3. **Execute** the script using the Bash tool with proper parameters
4. **Format** the output in a user-friendly way

## Available Scripts

### Primary Script
- `scripts/rpc_client.py` - Direct RPC method calls (main interface)

### Helper Scripts
- `scripts/command_mapper.py` - Parse natural language to RPC methods
- `scripts/examples/list-downloads.py` - List all downloads with formatting
- `scripts/examples/pause-all.py` - Pause all active downloads
- `scripts/examples/monitor-downloads.py` - Real-time monitoring
- `scripts/examples/add-torrent.py` - Add torrent downloads
- `scripts/examples/set-options.py` - Modify download options

## Command Mapping Table

| User Intent | Script Call |
|-------------|-------------|
| Download a file | `python scripts/rpc_client.py aria2.addUri '["{URL}"]'` |
| Check download status | `python scripts/rpc_client.py aria2.tellStatus {GID}` |
| Pause download | `python scripts/rpc_client.py aria2.pause {GID}` |
| Pause all downloads | `python scripts/rpc_client.py aria2.pauseAll` |
| Resume download | `python scripts/rpc_client.py aria2.unpause {GID}` |
| Resume all downloads | `python scripts/rpc_client.py aria2.unpauseAll` |
| Remove download | `python scripts/rpc_client.py aria2.remove {GID}` |
| List active downloads | `python scripts/rpc_client.py aria2.tellActive` |
| List waiting downloads | `python scripts/rpc_client.py aria2.tellWaiting 0 100` |
| List stopped downloads | `python scripts/rpc_client.py aria2.tellStopped 0 100` |
| Show global stats | `python scripts/rpc_client.py aria2.getGlobalStat` |
| Show aria2 version | `python scripts/rpc_client.py aria2.getVersion` |
| Purge download results | `python scripts/rpc_client.py aria2.purgeDownloadResult` |

## Parameter Formatting

### Pattern 1: No Parameters
```bash
python scripts/rpc_client.py aria2.getGlobalStat
python scripts/rpc_client.py aria2.pauseAll
python scripts/rpc_client.py aria2.getVersion
```

### Pattern 2: Single String (GID)
```bash
python scripts/rpc_client.py aria2.tellStatus 2089b05ecca3d829
python scripts/rpc_client.py aria2.pause 2089b05ecca3d829
python scripts/rpc_client.py aria2.remove 2089b05ecca3d829
```

### Pattern 3: Array of Strings (URLs)
```bash
# Single URL
python scripts/rpc_client.py aria2.addUri '["http://example.com/file.zip"]'

# Multiple URLs
python scripts/rpc_client.py aria2.addUri '["http://url1.com", "http://url2.com"]'
```

### Pattern 4: Multiple Parameters (Numbers)
```bash
python scripts/rpc_client.py aria2.tellWaiting 0 100
python scripts/rpc_client.py aria2.tellStopped 0 50
```

### Pattern 5: Helper Scripts
```bash
python scripts/examples/list-downloads.py
python scripts/examples/pause-all.py
python scripts/examples/add-torrent.py /path/to/file.torrent
```

## Step-by-Step Execution Examples

### Example 1: Download a File

**User Command:** "Please download http://example.com/file.zip"

**Thought Process:**
1. User wants to download → use `aria2.addUri`
2. Need to pass URL as array parameter
3. Call rpc_client.py with proper formatting

**Execute:**
```bash
python scripts/rpc_client.py aria2.addUri '["http://example.com/file.zip"]'
```

**Parse Output:** Extract GID from script output (e.g., "2089b05ecca3d829")

**Response:**
```
✓ Download started successfully!
GID: 2089b05ecca3d829

You can check progress with: "show status for GID 2089b05ecca3d829"
```

### Example 2: Check Download Status

**User Command:** "What's the status of GID 2089b05ecca3d829?"

**Thought Process:**
1. User wants status → use `aria2.tellStatus`
2. GID is the parameter
3. Parse JSON output and format nicely

**Execute:**
```bash
python scripts/rpc_client.py aria2.tellStatus 2089b05ecca3d829
```

**Parse Output:** Script returns JSON with fields like:
- `status`: "active", "paused", "complete", etc.
- `completedLength`: bytes downloaded
- `totalLength`: total file size
- `downloadSpeed`: current speed

**Response:**
```
Download Status:
- Status: active
- Progress: 45.2 MB / 100 MB (45%)
- Speed: 2.3 MB/s
- ETA: ~2 minutes
```

### Example 3: List All Downloads

**User Command:** "Show me what's downloading"

**Thought Process:**
1. User wants overview → use helper script for nice formatting
2. `list-downloads.py` shows active, waiting, and stopped

**Execute:**
```bash
python scripts/examples/list-downloads.py
```

**Response:** Summarize the output, for example:
```
Current Downloads:

Active (2):
- ubuntu-20.04.iso: 45% complete, 2.3 MB/s
- archive.zip: 78% complete, 1.5 MB/s

Waiting (1):
- movie.mp4: queued

Stopped (3):
- file1.zip: completed
- file2.tar.gz: completed
- file3.pdf: error
```

## Common Mistakes to Avoid

### ❌ WRONG: Manually construct JSON-RPC

```bash
# DON'T do this!
curl -X POST http://localhost:6800/jsonrpc \
  -d '{"jsonrpc":"2.0","method":"aria2.addUri",...}'

# DON'T do this!
echo '{"jsonrpc": "2.0", "method": "aria2.addUri", ...}'
```

### ✅ CORRECT: Use Python scripts

```bash
# DO this!
python scripts/rpc_client.py aria2.addUri '["http://example.com/file.zip"]'
```

### ❌ WRONG: Try to import aria2

```python
# DON'T do this!
import aria2  # aria2 is not a Python library!
```

### ✅ CORRECT: Call scripts via subprocess

```python
# DO this if needed!
import subprocess
result = subprocess.run(
    ["python", "scripts/rpc_client.py", "aria2.getGlobalStat"],
    capture_output=True, text=True
)
```

## Response Formatting Guidelines

### For addUri (download started)
```
✓ Download started successfully!
GID: {gid}
```

### For tellStatus (download progress)
```
Status: {status}
Progress: {completed}/{total} ({percentage}%)
Speed: {speed}
```

### For pause/unpause operations
```
✓ Download {paused/resumed}
GID: {gid}
```

### For batch operations (pauseAll, unpauseAll)
```
✓ All downloads {paused/resumed}
```

### For getGlobalStat
```
Active: {numActive}
Waiting: {numWaiting}
Stopped: {numStopped}
Download Speed: {downloadSpeed}
Upload Speed: {uploadSpeed}
```

## Troubleshooting

For detailed troubleshooting information, see **[troubleshooting.md](troubleshooting.md)**.

### Quick Troubleshooting

**Script not found:** Change to skill directory or use absolute path

**Connection refused:** Check if aria2 is running with `--enable-rpc`

**Parameter error:** Use single quotes around JSON: `'["url"]'`

**GID not found:** Check stopped downloads with `aria2.tellStopped 0 100`

## Configuration

Scripts automatically load configuration from:
1. Environment variables (highest priority)
2. `config.json` in skill directory
3. Defaults (localhost:6800)

You don't need to set configuration manually - scripts handle it automatically.

## See Also

- [aria2-methods.md](aria2-methods.md) - Detailed aria2 RPC method reference
- [Official aria2 documentation](https://aria2.github.io/) - aria2 daemon documentation
