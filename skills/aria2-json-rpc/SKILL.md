---
name: aria2-json-rpc
description: Interact with aria2 download manager via JSON-RPC 2.0. Manage downloads, query status, and control tasks through natural language commands.
---

Use this skill when working with aria2 download manager or when the user wants to:
- Download files from URLs (HTTP/HTTPS/FTP/Magnet)
- Check download progress and status
- Manage active downloads (pause, resume, remove)
- View global download statistics

## Quick Start

When the user wants to download something or manage aria2 downloads:

1. **Load the configuration** - the skill automatically reads from environment variables or config.json
2. **Map the command** - interpret natural language into aria2 RPC methods
3. **Execute the RPC call** - send request to aria2 daemon
4. **Return results** - present results in user-friendly format

## Available Operations

### Add Downloads
- "download <url>" - Start downloading from a URI
- "download <url1> <url2> ..." - Batch download from multiple URLs

### Check Status
- "show status for GID <id>" - Get detailed progress information
- "show global stats" - View overall download statistics

### Manage Downloads
- "remove GID <id>" - Stop and remove a download
- "cancel GID <id>" - Abort a download task

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

## Common Patterns

**Single file download:**
```
User: "download https://example.com/file.zip"
→ Calls aria2.addUri
→ Returns GID for tracking
```

**Check progress:**
```
User: "show status for GID 2089b05ecca3d829"
→ Calls aria2.tellStatus
→ Returns progress %, download speed, ETA
```

**Manage downloads:**
```
User: "remove GID 2089b05ecca3d829"
→ Calls aria2.remove
→ Confirms removal
```

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
