---
name: aria2-json-rpc
description: Interact with aria2 download manager via JSON-RPC 2.0. Manage downloads, query status, and control tasks through natural language commands.
---

Use this skill when working with aria2 download manager or when the user wants to:
- Download files from URLs (HTTP/HTTPS/FTP/Magnet), Torrents, or Metalinks
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

## Capabilities

### Download Management

**Start downloads:**
- "download <url>" - Download a file from URL
- "download <url1> <url2> ..." - Download multiple files at once
- "add torrent <file>" - Download from a torrent file
- "add metalink <file>" - Download from a metalink file

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

## API Reference

### Download Operations

**aria2.addUri** - Add a new download
- Parameters: `uris` (array), `options` (object, optional)
- Returns: GID (16-character hex string)
- Example: `addUri(["http://example.com/file.zip"])`

**aria2.addTorrent** - Add torrent download
- Parameters: `torrent` (base64 string), `uris` (array, optional), `options` (object, optional)
- Returns: GID
- Example: `addTorrent(base64data, [], {"dir": "/tmp"})`

**aria2.addMetalink** - Add metalink download
- Parameters: `metalink` (base64 string), `options` (object, optional)
- Returns: Array of GIDs
- Example: `addMetalink(base64data, {"dir": "/tmp"})`

### Control Operations

**aria2.pause** - Pause active download
- Parameters: `gid` (string)
- Returns: GID of paused download
- Example: `pause("2089b05ecca3d829")`

**aria2.pauseAll** - Pause all active downloads
- Parameters: none
- Returns: "OK"
- Example: `pauseAll()`

**aria2.unpause** - Resume paused download
- Parameters: `gid` (string)
- Returns: GID of resumed download
- Example: `unpause("2089b05ecca3d829")`

**aria2.unpauseAll** - Resume all paused downloads
- Parameters: none
- Returns: "OK"
- Example: `unpauseAll()`

**aria2.remove** - Remove a download
- Parameters: `gid` (string)
- Returns: GID of removed download
- Example: `remove("2089b05ecca3d829")`

**aria2.purgeDownloadResult** - Clear completed download history
- Parameters: none
- Returns: "OK"
- Example: `purgeDownloadResult()`

**aria2.removeDownloadResult** - Remove specific download record
- Parameters: `gid` (string)
- Returns: "OK"
- Example: `removeDownloadResult("2089b05ecca3d829")`

### Monitoring Operations

**aria2.tellStatus** - Get download status
- Parameters: `gid` (string), `keys` (array, optional)
- Returns: Status object with progress, speed, and metadata
- Example: `tellStatus("2089b05ecca3d829")`

**aria2.tellActive** - List active downloads
- Parameters: `keys` (array, optional)
- Returns: Array of download status objects
- Example: `tellActive()`

**aria2.tellWaiting** - List waiting downloads
- Parameters: `offset` (int), `num` (int), `keys` (array, optional)
- Returns: Array of waiting download objects
- Example: `tellWaiting(0, 100)`

**aria2.tellStopped** - List stopped downloads
- Parameters: `offset` (int), `num` (int), `keys` (array, optional)
- Returns: Array of stopped download objects
- Example: `tellStopped(0, 100)`

**aria2.getGlobalStat** - Get global statistics
- Parameters: none
- Returns: Global stats object with active/waiting/stopped counts
- Example: `getGlobalStat()`

### Configuration Operations

**aria2.getOption** - Get download options
- Parameters: `gid` (string)
- Returns: Options object
- Example: `getOption("2089b05ecca3d829")`

**aria2.changeOption** - Change download options
- Parameters: `gid` (string), `options` (object)
- Returns: "OK"
- Example: `changeOption("2089b05ecca3d829", {"max-download-limit": "1M"})`

**aria2.getGlobalOption** - Get global options
- Parameters: none
- Returns: Global options object
- Example: `getGlobalOption()`

**aria2.changeGlobalOption** - Change global options
- Parameters: `options` (object)
- Returns: "OK"
- Example: `changeGlobalOption({"max-concurrent-downloads": "3"})`

### System Operations

**aria2.getVersion** - Get aria2 version info
- Parameters: none
- Returns: Version and enabled features
- Example: `getVersion()`

**system.listMethods** - List all available RPC methods
- Parameters: none
- Returns: Array of method names
- Example: `listMethods()`

## Natural Language Commands

### Downloads
- "download http://example.com/file.zip"
- "add torrent file.torrent"
- "add metalink file.metalink"

### Status & Monitoring
- "show status for GID 2089b05ecca3d829"
- "list active downloads"
- "list waiting downloads"
- "list stopped downloads"
- "show global stats"
- "monitor downloads via WebSocket"

### Control
- "pause GID 2089b05ecca3d829"
- "pause all downloads"
- "resume GID 2089b05ecca3d829"
- "resume all downloads"
- "remove download 2089b05ecca3d829"
- "purge completed downloads"

### Configuration & System
- "show options for GID 2089b05ecca3d829"
- "set speed limit for GID 2089b05ecca3d829 to 1M"
- "show aria2 version"
- "list available methods"

## Troubleshooting

### Connection Issues

**Error**: "Cannot connect to aria2 RPC server"
- Check if aria2 daemon is running: `ps aux | grep aria2c`
- Verify RPC is enabled: aria2c should be started with `--enable-rpc`
- Check firewall settings for port 6800
- Verify host/port configuration matches aria2 settings

**Error**: "Authentication failed"
- Check if secret token is correct
- Verify `ARIA2_RPC_SECRET` or config.json secret matches aria2 `--rpc-secret`
- Note: `system.listMethods` doesn't require authentication

### Download Issues

**Error**: "GID not found"
- The download may have been removed or completed
- Check stopped downloads: `tellStopped(0, 100)`
- Downloads are purged automatically based on aria2 settings

**Error**: "Download not active"
- Cannot pause a download that's not active
- Check current status with `tellStatus(gid)`
- May already be paused or completed

### Performance Issues

**Slow downloads**: Check and adjust options
```python
# Limit concurrent downloads
changeGlobalOption({"max-concurrent-downloads": "5"})

# Increase connections per server
changeOption(gid, {"max-connection-per-server": "4"})

# Enable split downloading
changeOption(gid, {"split": "10"})
```

## Security Best Practices

### Token Authentication
- Always use `--rpc-secret` when running aria2c in production
- Store secret in environment variable, not in code
- Use strong, random tokens (32+ characters)
- Regenerate tokens periodically

### Network Security
- Bind RPC to localhost only: `--rpc-listen-address=127.0.0.1`
- Use HTTPS with `--rpc-secure` if remote access needed
- Configure firewall to restrict access to port 6800
- Consider SSH tunnel for remote access instead of exposing RPC

### Configuration Security
```bash
# Set restrictive permissions
chmod 600 config.json

# Use environment variables for secrets
export ARIA2_RPC_SECRET=$(cat /secure/path/to/secret)

# Never commit secrets to version control
echo "config.json" >> .gitignore
```

## Error Messages and Solutions

| Error Code | Message | Solution |
|------------|---------|----------|
| 1 | GID not found | Check if download exists with tellStatus or list appropriate state |
| 1 | Download not active | Verify status before pause/unpause operations |
| -32601 | Method not found | Check method name spelling and aria2 version |
| -32700 | Parse error | Check JSON format in request |
| Connection refused | Cannot connect | Verify aria2 is running with RPC enabled |
| Auth failed | Invalid token | Check secret token configuration |

## Reference

See [references/aria2-methods.md](references/aria2-methods.md) for detailed RPC method documentation and advanced usage.
