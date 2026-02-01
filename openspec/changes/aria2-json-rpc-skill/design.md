## Context

The aria2 JSON-RPC skill enables AI agents to interact with aria2's JSON-RPC 2.0 interface for download management. aria2 is a lightweight multi-protocol command-line download utility supporting HTTP/HTTPS, FTP, SFTP, BitTorrent, and Metalink. The skill will provide comprehensive access to aria2's RPC methods through a natural language interface.

The existing placeholder skill lacks full-spectrum support. This design implements a complete JSON-RPC 2.0 client with three-milestone rollout strategy:

- **Milestone 1**: Core operations (addUri, tellStatus, remove, getGlobalStat)
- **Milestone 2**: Task control and batch operations (pause/unpause, batch control, list operations)
- **Milestone 3**: Complete protocol support (torrent/metalink, dynamic configuration, system methods)

The skill runs within the OpenCode agent framework and must integrate with the skill registry and command parser.

## Goals / Non-Goals

**Goals:**
- Implement a complete JSON-RPC 2.0 client for aria2 with HTTP POST transport (primary) and WebSocket support (optional for Milestone 3)
- Support token-based authentication via parameter injection (`token:<SECRET_TOKEN>`)
- Provide flexible configuration from config.json, environment variables, or interactive prompts
- Enable natural language command mapping to aria2 RPC methods
- Deliver milestone-based implementation for iterative testing and validation
- Handle errors gracefully with clear error messages and debugging context

**Non-Goals:**
- XML-RPC support (out of scope, JSON-RPC 2.0 only)
- aria2 daemon installation or configuration management (user responsibility)
- Persistent connection management for HTTP (HTTP POST is stateless, WebSocket for Milestone 3)
- aria2 session management beyond what aria2 RPC provides
- Custom download scheduling logic beyond aria2's capabilities

## Decisions

### JSON-RPC 2.0 Implementation Strategy

**Decision**: Implement JSON-RPC 2.0 specification directly using standard HTTP POST requests, not a third-party JSON-RPC library.

**Rationale**: 
- JSON-RPC 2.0 is simple (request with jsonrpc, method, params, id; response with result or error)
- Avoids unnecessary dependency on a library for a well-documented protocol
- Full control over request formatting, especially token injection
- Simplifies error handling and debugging by having direct access to raw requests/responses

**Alternatives considered**:
- Use `json-rpc-2.0` npm package: Rejected due to additional dependency for minimal functionality
- Use `axios` with JSON-RPC wrapper: Rejected as over-engineering for simple protocol

**Note**: For Milestone 3 WebSocket support, may use `ws` library for WebSocket client implementation.

### Configuration Management

**Decision**: Three-tier configuration priority: Environment variables → config.json → Interactive defaults.

**Rationale**:
- Environment variables enable secure token storage (ARIA2_RPC_SECRET) without committing to code
- config.json provides persistent configuration for development and testing
- Interactive fallback ensures skill works on first use without pre-configuration
- Priority order allows overrides at different deployment levels

**Configuration schema**:
```json
{
  "host": "localhost",
  "port": 6800,
  "secret": "optional-token-or-null",
  "secure": false,
  "timeout": 30000
}
```

**Environment variables**: ARIA2_RPC_HOST, ARIA2_RPC_PORT, ARIA2_RPC_SECRET, ARIA2_RPC_SECURE, ARIA2_RPC_TIMEOUT

### Token Authentication

**Decision**: Inject token as first parameter in params array with format `token:<SECRET_TOKEN>` for all aria2.* methods.

**Rationale**:
- aria2 expects token as first parameter when secret is configured
- Token injection should be automatic and transparent to skill users
- system.* methods (listMethods) do not require token injection

**Implementation**: Before sending RPC request, if secret is configured and method starts with `aria2.`, prepend `token:${secret}` to params array.

### Transport Protocol

**Decision**: Primary HTTP POST for all milestones. WebSocket optional for Milestone 3 for event notifications.

**Rationale**:
- HTTP POST is sufficient for request/response pattern (Milestones 1-2)
- All aria2 RPC methods are callable via HTTP POST
- WebSocket adds complexity for event notifications (onDownloadStart, onDownloadComplete) needed for Milestone 3
- WebSocket enables real-time updates but is not required for core functionality

**HTTP POST flow**:
1. Construct JSON-RPC request
2. Send POST to `http://host:port/jsonrpc`
3. Parse JSON response (result or error)
4. Return result or throw error with context

**WebSocket flow** (Milestone 3):
1. Establish persistent WebSocket connection
2. Subscribe to server notifications (aria2.onDownloadStart, etc.)
3. Register event handlers for download lifecycle events
4. Handle JSON-RPC requests/responses over WebSocket

### Error Handling Strategy

**Decision**: Structured error handling with error classification (network, parse, JSON-RPC, aria2) and context preservation.

**Rationale**:
- Different error types require different handling (retry for network errors, no retry for parse errors)
- Preserving request ID in errors enables debugging
- Clear error messages help users understand what went wrong

**Error types**:
- Network errors (connection timeout, refused): May retry for idempotent methods
- Parse errors (invalid JSON): Do not retry, report line/column if available
- JSON-RPC errors (error response from server): Return aria2's error code and message
- Aria2 errors (GID not found, invalid options): Return specific aria2 error details

### Milestone-Based Implementation

**Decision**: Implement in three milestones to enable iterative testing and user feedback.

**Rationale**:
- Reduces risk by validating core functionality first
- Allows users to adopt basic features while advanced features are developed
- Tests integration with aria2 daemon incrementally
- Mirrors aria2's own progressive feature set

**Milestone breakdown**:
- **Milestone 1** (Core): aria2-task-creation (URI only), aria2-task-monitoring (tellStatus, getGlobalStat), aria2-task-control (remove), aria2-rpc-client (HTTP, config)
- **Milestone 2** (Advanced): aria2-task-creation (URI options), aria2-task-monitoring (tellActive/tellWaiting/tellStopped), aria2-task-control (pause/unpause/batch)
- **Milestone 3** (Complete): aria2-task-creation (torrent/metalink), aria2-configuration (changeOption, getVersion), aria2-rpc-client (WebSocket events)

### File Encoding for Torrent/Metalink

**Decision**: Use Base64 encoding for torrent and metalink file content before sending to aria2.

**Rationale**:
- aria2.addTorrent and aria2.addMetalink expect Base64-encoded strings
- Binary files cannot be sent directly in JSON
- JavaScript provides native Base64 support (btoa, Buffer.from)
- Base64 is standard for binary data in JSON payloads

**Implementation**: Read file as binary buffer, convert to Base64 string, pass as first parameter to addTorrent/addMetalink.

### Natural Language Mapping

**Decision**: Map natural language commands to aria2 RPC methods using keyword detection and intent classification.

**Rationale**:
- Enables agent to interpret user commands like "download this file" or "pause all downloads"
- Simple keyword-based approach works well for aria2's method names
- Avoids complex NLP library dependencies

**Command mapping examples**:
- "download <url>" → addUri
- "pause <gid>" or "pause all" → pause or pauseAll
- "show status <gid>" → tellStatus
- "what's downloading" → tellActive
- "global stats" → getGlobalStat

## Risks / Trade-offs

### Configuration Security Risk
[Secret token in config.json] → Mitigation: Document security best practices, recommend environment variables for production, set appropriate file permissions (600). Token is optional and aria2 can run without authentication.

### Network Connectivity Risk
[aria2 daemon not running or unreachable] → Mitigation: Validate connection on first use, provide clear error messages, support configuration testing command. Skill will throw errors if aria2 is unavailable.

### Version Compatibility Risk
[aria2 version differences in RPC method availability] → Mitigation: Use getVersion and system.listMethods to detect capabilities (Milestone 3), gracefully handle unsupported methods with descriptive errors. Core methods (addUri, tellStatus) are stable across aria2 versions.

### Base64 Encoding Performance Risk
[Large torrent/metalink files encoded as Base64] → Mitigation: This is aria2's requirement, not a skill limitation. Warn users about large files, but performance is acceptable for typical torrent/metalink sizes.

### WebSocket Complexity Risk
[WebSocket adds complexity for persistent connections] → Mitigation: WebSocket is optional (Milestone 3). HTTP POST remains primary transport. WebSocket fallback to HTTP if connection fails.

### Error Recovery Trade-off
[Automatic retry for network errors] → Trade-off: Retry may succeed for transient issues but could mask real problems. Mitigation: Limit retries to 3 with exponential backoff, only for idempotent methods (status queries, not task modification).

### Milestone Scope Trade-off
[Three milestones extend timeline] → Trade-off: Sequential implementation delays full feature set. Mitigation: Milestone 1 provides useful functionality immediately, users can adopt incrementally.

## Migration Plan

### Milestone 1 Deployment
1. Implement core RPC client (HTTP POST, config loading, token injection)
2. Implement aria2.addUri, aria2.tellStatus, aria2.remove, aria2.getGlobalStat
3. Add natural language command mapping for core methods
4. Write tests for basic operations with mock aria2 or real daemon
5. Update skill documentation with Milestone 1 capabilities
6. No rollback needed (new skill, incremental features)

### Milestone 2 Deployment
1. Add batch operations (pauseAll/unpauseAll, tellActive/tellWaiting/tellStopped)
2. Extend command mapping for batch and list operations
3. Add tests for batch workflows
4. Update documentation with new capabilities
5. No breaking changes from Milestone 1

### Milestone 3 Deployment
1. Add torrent/metalink support (addTorrent, addMetalink)
2. Add configuration methods (changeOption, getVersion)
3. Add WebSocket client for event notifications (optional)
4. Add system methods (system.listMethods)
5. Update documentation with complete feature set
6. No breaking changes from Milestone 2

### Rollback Strategy
- Each milestone is additive, no breaking changes
- If an issue is found in a milestone, that milestone's features can be disabled without affecting earlier milestones
- Configuration file format is stable across milestones
- For critical issues, revert skill to previous milestone's implementation

### Script Implementation Language

**Decision**: Use Python 3.6+ scripts with builtin libraries. External dependency `websockets` only for Milestone 3 WebSocket support.

**Rationale**:
- Python 3.6+ provides all required builtin modules for HTTP POST JSON-RPC client:
  - `urllib.request`: HTTP POST requests (no external dependencies)
  - `json`: JSON-RPC request/response formatting
  - `base64`: Base64 encoding for torrent/metalink files
  - `os`, `sys`: Environment variable and file system operations
- Widely available on most systems with Python 3 pre-installed
- Mature error handling and debugging capabilities
- For WebSocket (Milestone 3), use `websockets` library with dependency check

**Alternatives considered**:
- **Node.js**: Requires Node.js runtime; `fetch` is builtin in Node 18+, but WebSocket needs `ws` library. Similar dependency issue.
- **Shell script**: Requires external tools (`curl`, `jq` for JSON processing). No native JSON handling, very difficult to implement JSON-RPC protocol correctly. WebSocket nearly impossible.
- **Python with full dependencies**: Would use `requests` and `websockets`. Rejected to minimize dependencies.

**Dependency strategy**:
- **Milestone 1-2**: Zero external dependencies (Python 3.6+ builtin only)
- **Milestone 3**: Optional `websockets` library for WebSocket support; HTTP POST remains fully functional without it

### Dependency Management and Error Reporting

**Decision**: Implement comprehensive dependency checks at script startup with clear error messages.

**Rationale**:
- Fail fast with actionable error messages
- Help users understand missing requirements and how to fix them
- Distinguish between mandatory (Python version) and optional (websockets) dependencies

**Implementation**:
```python
# Dependency checks at script startup
import sys

# Mandatory: Python version check
if sys.version_info < (3, 6):
    print("ERROR: Python 3.6 or higher is required")
    print(f"Current version: {sys.version}")
    print("Please install Python 3.6+ from https://www.python.org/downloads/")
    sys.exit(1)

# Optional: WebSocket library check (Milestone 3)
try:
    import websockets
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    print("WARNING: 'websockets' library not found")
    print("WebSocket features will be disabled. Install with: pip install websockets")

# Builtin modules check (should always succeed in Python 3.6+)
required_modules = ['urllib.request', 'json', 'base64', 'os']
missing_modules = []
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        missing_modules.append(module)

if missing_modules:
    print(f"ERROR: Required builtin modules missing: {', '.join(missing_modules)}")
    print("This indicates a corrupted Python installation.")
    print("Please reinstall Python 3.6+ or report this as a Python bug.")
    sys.exit(1)
```

**Error message format**:
- **Mandatory dependency missing**: "ERROR: ..." with clear description and fix instructions
- **Optional dependency missing**: "WARNING: ..." with impact description and installation command
- **Runtime dependency failure**: "ERROR: Failed to load module X: [specific error]" with context

## Open Questions

1. **WebSocket Implementation Priority**: Should WebSocket support be required in Milestone 3 or optional? (Decided: optional, HTTP POST remains primary)

2. **Command Mapping Complexity**: Is keyword-based mapping sufficient, or should we implement more sophisticated intent classification? (Current approach: simple keyword matching should work for aria2's straightforward method names)

3. **Configuration File Location**: Should we support global configuration in user home directory, or only project-local config.json? (Decided: only project-local skills/aria2-json-rpc/config.json to avoid cross-project conflicts)

4. **Error Recovery Granularity**: Should users configure retry count and backoff strategy, or use fixed defaults? (Current approach: fixed defaults, can expose configuration if needed)

5. **Batch Request Implementation**: Should we implement system.multicall or direct batch JSON-RPC array format? (Current approach: support both, multicall is more widely supported)