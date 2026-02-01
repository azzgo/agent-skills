# Aria2 RPC Method Reference

## Implemented Methods

### aria2.addUri

Add download tasks from URIs.

**Usage:**
```bash
python3 scripts/rpc_client.py addUri '["http://example.com/file.zip"]'
```

**Parameters:**
- `uris` (array of strings): List of URIs to download
- `options` (object, optional): Download options like `{"dir": "/path", "out": "filename"}`
- `position` (integer, optional): Position in download queue

**Returns:**
- GID (string): Global ID for the download task

**Natural Language Commands:**
- "download <url>"
- "add download <url>"
- "fetch <url>"

### aria2.tellStatus

Query status of a specific download task.

**Usage:**
```bash
python3 scripts/rpc_client.py tellStatus '["2089b05ecca3d829"]'
```

**Parameters:**
- `gid` (string): Global ID of the download
- `keys` (array of strings, optional): Specific keys to retrieve

**Returns:**
- Status object with fields: gid, status, totalLength, completedLength, downloadSpeed, etc.

**Natural Language Commands:**
- "show status for GID <id>"
- "check progress of <id>"

### aria2.remove

Remove a download task.

**Usage:**
```bash
python3 scripts/rpc_client.py remove '["2089b05ecca3d829"]'
```

**Parameters:**
- `gid` (string): Global ID of the download to remove

**Returns:**
- GID (string): GID of the removed task

**Natural Language Commands:**
- "remove GID <id>"
- "delete <id>"
- "cancel <id>"

### aria2.getGlobalStat

Get global download statistics.

**Usage:**
```bash
python3 scripts/rpc_client.py getGlobalStat
```

**Parameters:**
- None

**Returns:**
- Object with: numActive, numWaiting, numStopped, numStoppedTotal, downloadSpeed, uploadSpeed

**Natural Language Commands:**
- "show global stats"
- "what's downloading"
- "how many downloads active"

## Configuration Management

### Loading Configuration

**From environment variables:**
```bash
export ARIA2_RPC_HOST=localhost
export ARIA2_RPC_PORT=6800
export ARIA2_RPC_SECRET=mytoken
export ARIA2_RPC_SECURE=false
```

**From config.json:**
```bash
# Creates config.json interactively on first use
python3 scripts/config_loader.py
```

### Testing Connection

```bash
python3 scripts/config_loader.py --test
```

## Module Usage

### Dependency Check

Check if environment meets requirements:
```bash
python3 scripts/dependency_check.py [milestone]
```

Arguments:
- `milestone` (1, 2, or 3): Check dependencies for specific milestone

### Command Mapping

Test natural language command recognition:
```bash
python3 scripts/command_mapper.py
```

## Response Format

### Success Response
```json
{
  "result": "2089b05ecca3d829"
}
```

### Error Response
```json
{
  "error": {
    "code": 1,
    "message": "GID not found",
    "data": "2089b05ecca3d829"
  }
}
```

## Error Handling

### Common Errors

- **Connection refused**: aria2 daemon not running or wrong port
- **GID not found**: Invalid or expired download ID
- **Invalid URI**: Malformed URL or unreachable server
- **Auth failed**: Wrong or missing token

### Retry Logic

Network errors automatically retry up to 3 times with exponential backoff for idempotent methods (queries only, not modifications).

## File Structure

```
scripts/
├── config_loader.py     # Configuration loading and validation
├── dependency_check.py  # Environment dependency checks
├── rpc_client.py        # JSON-RPC 2.0 client implementation
└── command_mapper.py    # Natural language command parsing
```

## Configuration Priority

1. Environment variables (highest)
2. config.json in skill directory
3. Built-in defaults

## Token Authentication

When secret token is configured, it's automatically injected as the first parameter:
```
params: ["token:<SECRET>", ...userParams]
```

This applies to all `aria2.*` methods but not `system.*` methods.
