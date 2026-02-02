# Aria2 RPC Method Reference

Complete reference for all supported aria2 operations.

## Download Management

### Start a Download

**aria2.addUri** - Add download from URLs

**Parameters:**
- `uris` (array): List of URLs to download from
- `options` (object, optional): Settings like save directory, filename, speed limit
- `position` (integer, optional): Position in download queue

**Returns:** GID (download identifier)

**Natural language:**
- "download <url>"
- "add download <url>"
- "fetch <url>"

**Example:**
```bash
python3 scripts/rpc_client.py addUri '["http://example.com/file.zip"]'
```

### Check Download Status

**aria2.tellStatus** - Get progress and details for a download

**Parameters:**
- `gid`: Download identifier
- `keys` (optional): Specific fields to retrieve

**Returns:** Status object with progress, speed, size, etc.

**Natural language:**
- "show status for GID <id>"
- "check progress of <id>"

### Stop and Remove Downloads

**aria2.remove** - Stop and remove a download

**Parameters:**
- `gid`: Download identifier

**Returns:** GID of removed download

**Natural language:**
- "remove GID <id>"
- "delete <id>"
- "cancel <id>"

## Control Operations

## Control Operations

### Pause Downloads

**aria2.pause** - Pause a specific download

**Parameters:**
- `gid`: Download identifier

**Returns:** GID

**Natural language:**
- "pause GID <id>"
- "pause download <id>"

---

**aria2.pauseAll** - Pause all active downloads

**Returns:** "OK"

**Natural language:**
- "pause all downloads"
- "stop all tasks"
- "pause everything"

### Resume Downloads

**aria2.unpause** - Resume a paused download

**Parameters:**
- `gid`: Download identifier

**Returns:** GID

**Natural language:**
- "unpause GID <id>"
- "resume download <id>"
- "continue <id>"

---

**aria2.unpauseAll** - Resume all paused downloads

**Returns:** "OK"

**Natural language:**
- "resume all downloads"
- "continue everything"

## Monitor Downloads

### View Active Downloads

**aria2.tellActive** - List all currently downloading files

**Parameters:**
- `keys` (optional): Specific fields to retrieve

**Returns:** Array of download status objects

**Natural language:**
- "show active downloads"
- "what's currently downloading"

### View Queued Downloads

**aria2.tellWaiting** - List downloads waiting to start

**Parameters:**
- `offset`: Starting position (default: 0)
- `num`: How many to return (default: 100)
- `keys` (optional): Specific fields to retrieve

**Returns:** Array of download status objects

**Natural language:**
- "list waiting downloads"
- "show queued tasks"

### View Completed/Stopped Downloads

**aria2.tellStopped** - List finished or cancelled downloads

**Parameters:**
- `offset`: Starting position (default: 0)
- `num`: How many to return (default: 100)
- `keys` (optional): Specific fields to retrieve

**Returns:** Array of download status objects

**Natural language:**
- "show stopped downloads"
- "list completed tasks"

### Global Statistics

**aria2.getGlobalStat** - Get overall download statistics

**Returns:** Object with counts and speeds (numActive, numWaiting, downloadSpeed, etc.)

**Natural language:**
- "show global stats"
- "what's downloading"

## Configure Downloads

### Download-Specific Settings

**aria2.getOption** - Get settings for a download

**Parameters:**
- `gid`: Download identifier

**Returns:** Options object

**Natural language:**
- "show options for GID <id>"

---

**aria2.changeOption** - Modify settings for a download

**Parameters:**
- `gid`: Download identifier
- `options`: Settings to change (e.g., `{"max-download-limit": "1M"}`)

**Returns:** "OK"

**Use with example script:**
```bash
python3 scripts/examples/set-options.py --gid <id> --max-download-limit 1M
```

### Global Settings

**aria2.getGlobalOption** - Get aria2 global settings

**Returns:** Global options object

**Natural language:**
- "show global options"

---

**aria2.changeGlobalOption** - Modify aria2 global settings

**Parameters:**
- `options`: Settings to change

**Returns:** "OK"

**Use with example script:**
```bash
python3 scripts/examples/set-options.py --global --max-concurrent-downloads 5
```

## Maintenance

### Clean Up History

**aria2.purgeDownloadResult** - Remove all completed/stopped download records

**Returns:** "OK"

**Natural language:**
- "purge download results"
- "clear download history"

---

**aria2.removeDownloadResult** - Remove a specific download record

**Parameters:**
- `gid`: Download identifier

**Returns:** "OK"

**Natural language:**
- "remove download result <id>"

## System Information

### Version Information

**aria2.getVersion** - Get aria2 version and features

**Returns:** Version object with enabled features

**Natural language:**
- "show aria2 version"
- "get version"

### Available Methods

**system.listMethods** - List all available RPC methods

**Returns:** Array of method names

**Natural language:**
- "list available methods"
- "what methods are available"

**Note:** No authentication token required for this method.

### Batch Operations

**system.multicall** - Execute multiple commands in one request

**Parameters:**
- `calls`: Array of method calls with `methodName` and `params`

**Returns:** Array of results

**Example:**
```python
calls = [
    {"methodName": "aria2.tellStatus", "params": ["2089b05ecca3d829"]},
    {"methodName": "aria2.pause", "params": ["2089b05ecca3d829"]},
]
client.multicall(calls)
```

## Configuration

### How Configuration Works

The skill looks for settings in this order (first one found wins):

1. **Environment variables** - Best for secure tokens
2. **config.json file** - In the skill directory
3. **Built-in defaults** - localhost:6800, no authentication

### Environment Variables

```bash
export ARIA2_RPC_HOST=localhost
export ARIA2_RPC_PORT=6800
export ARIA2_RPC_SECRET=your-token-here
export ARIA2_RPC_SECURE=false
```

### Configuration File

Create `config.json` in the skill directory:
```json
{
  "host": "localhost",
  "port": 6800,
  "secret": null,
  "secure": false
}
```

### Test Your Connection

```bash
python3 scripts/config_loader.py --test
```

## Helper Scripts

### Example Scripts Location

```
scripts/examples/
├── pause-all.py       # Pause all downloads at once
├── list-downloads.py  # See all downloads with progress
└── set-options.py     # Change speed limits and settings
```

### Using Example Scripts

**Pause everything:**
```bash
python3 scripts/examples/pause-all.py
```

**View all downloads:**
```bash
# Show default (10 completed/stopped)
python3 scripts/examples/list-downloads.py

# Show more
python3 scripts/examples/list-downloads.py --limit 50
```

**Change settings:**
```bash
# Limit download speed to 1 MB/s
python3 scripts/examples/set-options.py --gid 2089b05ecca3d829 --max-download-limit 1M

# Limit upload speed
python3 scripts/examples/set-options.py --gid 2089b05ecca3d829 --max-upload-limit 100K

# Change max concurrent downloads
python3 scripts/examples/set-options.py --global --max-concurrent-downloads 5

# Set connections per server
python3 scripts/examples/set-options.py --gid 2089b05ecca3d829 --max-connection-per-server 4
```

## Troubleshooting

### Common Issues

**"Connection refused"**
- aria2 daemon isn't running
- Wrong port number in configuration
- Check: `aria2c --enable-rpc --rpc-listen-port=6800`

**"GID not found"**
- Download already completed and removed from memory
- Invalid GID (should be 16 hex characters)
- Try: "show stopped downloads" to see completed ones

**"Authentication failed"**
- Wrong or missing token
- Check your ARIA2_RPC_SECRET matches aria2's --rpc-secret

**"Invalid URI"**
- Malformed URL
- Server unreachable
- aria2 doesn't support that protocol

### Getting Help

Run any script with `--help`:
```bash
python3 scripts/examples/set-options.py --help
```
