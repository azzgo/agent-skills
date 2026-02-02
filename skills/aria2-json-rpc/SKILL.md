---
name: aria2-json-rpc
description: Interact with aria2 download manager via JSON-RPC 2.0. Manage downloads, query status, and control tasks through natural language commands.
---

Use this skill when working with aria2 download manager or when the user wants to:
- Download files from URLs (HTTP/HTTPS/FTP/Magnet)
- Check download progress and status
- Manage active downloads (pause, resume, remove)
- View global download statistics
- Control batch operations (pause all, resume all)
- List downloads by state (active, waiting, stopped)
- Modify download and global options

## Quick Start

When the user wants to download something or manage aria2 downloads:

1. **Load the configuration** - the skill automatically reads from environment variables or config.json
2. **Map the command** - interpret natural language into aria2 RPC methods
3. **Execute the RPC call** - send request to aria2 daemon
4. **Return results** - present results in user-friendly format

## What You Can Do

### Download Management

**Start downloads:**
- "download <url>" - Download a file from URL
- "download <url1> <url2> ..." - Download multiple files at once

**Control downloads:**
- "pause GID <id>" - Pause a specific download
- "pause all downloads" - Pause everything that's downloading
- "resume GID <id>" - Continue a paused download
- "resume all downloads" - Resume all paused downloads
- "remove GID <id>" - Stop and remove a download
- "cancel GID <id>" - Abort a download

### Monitor Progress

**Check individual downloads:**
- "show status for GID <id>" - See progress, speed, and completion time

**View all downloads:**
- "show active downloads" - What's downloading right now
- "list waiting downloads" - What's queued up
- "show stopped downloads" - Completed or cancelled downloads
- "show global stats" - Overall statistics (active, waiting, speed)

### Customize Behavior

**Download settings:**
- "show options for GID <id>" - See settings for a download
- Use example scripts to change speed limits, connections, etc.

**Global settings:**
- "show global options" - View aria2 configuration
- Use example scripts to change concurrent downloads, global limits, etc.

### Maintenance

**Clean up:**
- "purge download results" - Clear completed download history
- "remove download result GID <id>" - Remove a specific record

**Information:**
- "show aria2 version" - Check aria2 version and features
- "list available methods" - See all available commands

## Configuration

The skill automatically loads configuration from (priority order):

1. **Environment variables** (highest priority):
   - `ARIA2_RPC_HOST` - aria2 server address
   - `ARIA2_RPC_PORT` - RPC port (default: 6800)
   - `ARIA2_RPC_SECRET` - Authentication token (optional)
   - `ARIA2_RPC_SECURE` - Use HTTPS (true/false)

2. **Configuration file** (`config.json` in skill directory):
   ```json
   {
     "host": "localhost",
     "port": 6800,
     "secret": null,
     "secure": false
   }
   ```

3. **Defaults** (fallback when no configuration found):
   - host: localhost
   - port: 6800
   - secure: false

## Usage Examples

### Basic Downloads

**Download a file:**
```
User: "download https://example.com/file.zip"
→ Returns GID for tracking (e.g., 2089b05ecca3d829)
```

**Check progress:**
```
User: "show status for GID 2089b05ecca3d829"
→ Shows: 45% complete, 2.3 MB/s, 5 minutes remaining
```

**Remove unwanted download:**
```
User: "remove GID 2089b05ecca3d829"
→ Stops and removes the download
```

### Batch Control

**Pause everything temporarily:**
```
User: "pause all downloads"
→ All active downloads pause immediately
```

**Resume specific download:**
```
User: "resume GID 2089b05ecca3d829"
→ Resumes that one download
```

**See what's happening:**
```
User: "show active downloads"
→ Lists all currently downloading files with progress

User: "list waiting downloads"
→ Shows queued downloads
```

### Advanced Configuration

**Check download settings:**
```
User: "show options for GID 2089b05ecca3d829"
→ Shows max speed, connections, save directory, etc.
```

**Using example scripts for detailed control:**
```bash
# Pause all downloads at once
python scripts/examples/pause-all.py

# See detailed status of all downloads
python scripts/examples/list-downloads.py

# Limit download speed to 1 MB/s
python scripts/examples/set-options.py --gid 2089b05ecca3d829 --max-download-limit 1M

# Set max concurrent downloads to 3
python scripts/examples/set-options.py --global --max-concurrent-downloads 3
```

## Example Scripts

The `scripts/examples/` directory contains ready-to-use scripts:

- **pause-all.py** - Pause all active downloads
- **list-downloads.py** - List all downloads across all states with progress
- **set-options.py** - Modify download or global options with user-friendly interface

## Output Format

Results are returned as structured data with:
- **Success**: Human-readable summary with key metrics
- **Error**: Clear error message explaining what went wrong

## Requirements

- aria2 daemon running with RPC enabled (`--enable-rpc`)
- Network access to aria2 RPC endpoint
- Python 3.6+ for script execution

## Reference

See [references/aria2-methods.md](references/aria2-methods.md) for detailed RPC method documentation and advanced usage.
