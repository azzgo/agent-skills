# aria2 JSON RPC Skill

**Description**: Skill for interacting with aria2 download manager via JSON-RPC protocol

**Version**: 1.0.0

**Author**: OpenCode

**Capabilities**:
- Connect to aria2 daemon via JSON-RPC
- Manage downloads (add, pause, resume, remove)
- Query download status and progress
- Configure aria2 settings
- Handle torrent and metalink files

**Configuration**:
- `aria2.rpc.host`: Aria2 RPC host (default: localhost)
- `aria2.rpc.port`: Aria2 RPC port (default: 6800)
- `aria2.rpc.secret`: RPC secret token (optional)
- `aria2.rpc.secure`: Use HTTPS (default: false)

**Requirements**:
- aria2 daemon running with RPC enabled (`--enable-rpc`)
- Network access to aria2 RPC endpoint

**Examples**:
```json
{
  "command": "addDownload",
  "params": {
    "uri": "https://example.com/file.iso"
  }
}
```

```json
{
  "command": "getStatus",
  "params": {
    "gid": "1234567890"
  }
}
```

**Related Documentation**:
- [aria2 Manual](https://aria2.github.io/manual/en/html/)
- [aria2 JSON-RPC API](https://aria2.github.io/manual/en/html/aria2c.html#jsonrpc)
