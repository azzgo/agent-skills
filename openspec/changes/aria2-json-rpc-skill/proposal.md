## Why

AI agents need a comprehensive skill to call aria2's JSON-RPC 2.0 interface for download management. The current placeholder skill lacks full-spectrum support for aria2's RPC methods, limiting agents to basic operations while missing critical features like torrent handling, batch operations, and fine-grained task control. A complete aria2 JSON-RPC skill enables agents to autonomously invoke all aria2 RPC methods through HTTP or WebSocket connections.

## What Changes

- **New agent skill**: Comprehensive aria2 JSON-RPC 2.0 client skill in `skills/aria2-json-rpc/`
- **JSON-RPC 2.0 only**: Focused implementation (no XML-RPC support) with proper `jsonrpc: "2.0"` field handling
- **HTTP/WebSocket transport**: Support both HTTP POST and WebSocket connections to aria2 RPC endpoints
- **Token authentication**: Secure authentication via `token:<SECRET_TOKEN>` injection in params array (first position)
- **Three-milestone rollout**:
  - Milestone 1 (Core): Basic download operations and monitoring (`addUri`, `tellStatus`, `remove`, `getGlobalStat`)
  - Milestone 2 (Advanced): Task control and batch management (`pause`/`unpause`, `pauseAll`/`unpauseAll`, `tellActive`/`tellWaiting`/`tellStopped`)
  - Milestone 3 (Complete): Full protocol support with torrent/metalink (`addTorrent`, `addMetalink`) and dynamic configuration (`changeOption`, `getVersion`, `system.listMethods`)
- **Natural language interface**: Enable agents to interpret commands like "download this file", "pause all downloads", "show me what's downloading"
- **Base64 encoding support**: Handle torrent file uploads via Base64 encoding for `addTorrent` method

## Capabilities

### New Capabilities

- `aria2-task-creation`: Add download tasks via URI, torrent files (Base64), and metalink files
- `aria2-task-monitoring`: Query task status, list active/waiting/stopped tasks, and retrieve global statistics
- `aria2-task-control`: Pause, resume, remove individual tasks or batch control all tasks simultaneously
- `aria2-configuration`: Dynamically modify task options (speed limits, connections) and retrieve system information
- `aria2-rpc-client`: Core JSON-RPC 2.0 client with authentication, error handling, and method invocation

### Modified Capabilities

<!-- No existing capabilities are being modified -->

## Impact

**New Components**:
- Agent skill implementation in `skills/aria2-json-rpc/SKILL.md` (expanded from placeholder)
- JSON-RPC 2.0 client logic for HTTP POST requests
- WebSocket client support for persistent connections (optional, depending on milestone)
- Skill configuration for RPC endpoint URL, port, secret token, and transport protocol
- Documentation and usage examples for all supported RPC methods (aligned with three milestones)

**Dependencies**:
- External aria2 daemon with RPC enabled (out of scope - user responsibility)
- HTTP client library (e.g., `fetch`, `axios`, or native Node.js `http`)
- WebSocket library if WebSocket transport is implemented (e.g., `ws`)
- Base64 encoding utilities (native JavaScript `btoa`/`Buffer.from`)
- Environment variable or configuration file support for secure token storage

**Affected Systems**:
- OpenCode agent skill registry (skill registration/loading)
- Agent natural language command parser (to map user intents to RPC methods)
- User workflows (enables new download automation capabilities)
