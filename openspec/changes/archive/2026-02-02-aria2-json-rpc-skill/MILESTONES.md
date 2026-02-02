# Milestone Summary - aria2 JSON-RPC Skill

## Overview
This document summarizes all requirements by milestone for the aria2 JSON-RPC skill implementation.

---

## Milestone 1 (Core / MVP)
**Goal**: Basic "download and monitor" functionality - minimum viable product.

### aria2-rpc-client
- [x] Client Initialization and Configuration [Milestone 1]
  - HTTP client initialization
  - WebSocket client initialization (for future use)
  - Configuration defaults (localhost:6800)
- [x] JSON-RPC 2.0 Request Formatting [Milestone 1]
  - Proper JSON-RPC 2.0 specification compliance
  - Token authentication injection
  - Method name prefixing
- [x] Response Handling [Milestone 1]
  - Success response parsing
  - Error response handling
  - Parse error handling
- [x] Request Timeout and Retry [Milestone 1]
  - Configurable timeout (default 30s)
  - Automatic retry for idempotent methods

### aria2-task-creation
- [x] Add URI Download Task [Milestone 1]
  - Single HTTP/HTTPS/FTP URL
  - Multiple URLs
  - Magnet URIs
  - Download with options
- [x] Options Specification [Milestone 1]
  - Download directory (dir)
  - Output filename (out)
  - Connection settings (split, max-concurrent-downloads, lowest-speed-limit)
- [x] Task Creation Response Handling [Milestone 1]
  - GID extraction
  - Duplicate detection
  - Invalid URI handling

### aria2-task-monitoring
- [x] Query Task Status [Milestone 1]
  - Active download status
  - Paused download status
  - Completed download status
  - Non-existent GID handling
- [x] Global Statistics [Milestone 1]
  - Overall statistics (numActive, numWaiting, numStopped, numStoppedTotal)
  - High activity detection
  - Idle state handling
  - Historical data tracking
- [x] Status Field Mapping [Milestone 1]
  - Status string mapping
  - Speed unit conversion
  - Progress calculation
  - ETA calculation

### aria2-task-control
- [x] Remove Task [Milestone 1]
  - Remove active download
  - Remove paused download
  - Remove completed download
  - Remove non-existent task handling

### aria2-configuration
- [x] Get URI [Milestone 1/2/3]
  - Get download URIs
  - URI status tracking
  - Multiple sources handling
- [x] Get Files [Milestone 1/2/3]
  - List download files
  - File selection state
  - File download progress
- [x] Option Schema Validation [Milestone 1/2/3]
  - Valid option names
  - Valid option values
  - Option deprecation warning

**Milestone 1 RPC Methods**:
- `aria2.addUri` - Add URI download
- `aria2.tellStatus` - Query task status
- `aria2.remove` - Remove task
- `aria2.getGlobalStat` - Get global statistics
- `aria2.getUris` - Get task URIs (optional for MVP)
- `aria2.getFiles` - Get task files (optional for MVP)

---

## Milestone 2 (Advanced)
**Goal**: Enhanced control and batch management - like real download client.

### aria2-rpc-client
- [x] Batch Request Support [Milestone 2]
  - Batch via system.multicall
  - Batch without multicall
  - Correlating request IDs

### aria2-task-monitoring
- [x] List Active Downloads [Milestone 2]
  - No active downloads
  - Single/multiple active downloads
  - Filter by type (http/ftp, bt, metalink)
- [x] List Waiting Downloads [Milestone 2]
  - Query waiting queue
  - Query paused tasks
  - Empty waiting queue
  - Pagination support
- [x] List Stopped Downloads [Milestone 2]
  - Query completed downloads
  - Query removed downloads
  - Expired downloads handling
  - Limit results

### aria2-task-control
- [x] Pause Single Task [Milestone 2]
  - Pause active download
  - Pause already paused (idempotent)
  - Pause non-existent task
  - Pause completed task
- [x] Resume Single Task [Milestone 2]
  - Resume paused download
  - Resume already active (idempotent)
  - Resume completed task
- [x] Pause All Downloads [Milestone 2]
  - Pause all active downloads
  - No downloads running (idempotent)
  - Partial pause failure handling
- [x] Resume All Downloads [Milestone 2]
  - Resume all paused downloads
  - No downloads paused (idempotent)
  - Selective resume by pattern
- [x] Force Remove Task [Milestone 2]
  - Force remove stuck download
  - Force remove with resource cleanup
- [x] Task State Transition Handling [Milestone 2]
  - State transition notification
  - Concurrent state changes
  - State change during query

**Milestone 2 RPC Methods** (additional to Milestone 1):
- `aria2.pause` - Pause single task
- `aria2.unpause` - Resume single task
- `aria2.pauseAll` - Pause all tasks
- `aria2.unpauseAll` - Resume all tasks
- `aria2.forceRemove` - Force remove task
- `aria2.tellActive` - List active downloads
- `aria2.tellWaiting` - List waiting downloads
- `aria2.tellStopped` - List stopped downloads
- `system.multicall` - Batch requests

---

## Milestone 3 (Complete)
**Goal**: Full protocol support with torrent/metalink and dynamic configuration.

### aria2-rpc-client
- [x] WebSocket Event Handling [Milestone 3]
  - Subscribe to download events
  - Event listener registration

### aria2-task-creation
- [x] Add Torrent Download Task [Milestone 3]
  - Add torrent file
  - Torrent with web seeds
  - Torrent with options
  - Invalid torrent file handling
- [x] Add Metalink Download Task [Milestone 3]
  - Add metalink file
  - Metalink with options
  - Invalid metalink file handling

### aria2-configuration
- [x] Change Task Options [Milestone 3]
  - Modify download speed limit
  - Modify file allocation
  - Add HTTP headers
  - Invalid option change handling
  - Batch option update
- [x] Get Version Information [Milestone 3]
  - Query version
  - Feature availability check
  - Protocol version
- [x] System Method Introspection [Milestone 3]
  - List all methods
  - Method signature discovery
  - Extension method detection
- [x] Change Global Options [Milestone 3]
  - Global download limit
  - Global configuration update
  - Global option query

**Milestone 3 RPC Methods** (additional to Milestone 1+2):
- `aria2.addTorrent` - Add torrent download
- `aria2.addMetalink` - Add metalink download
- `aria2.changeOption` - Change task options
- `aria2.changeGlobalOption` - Change global options
- `aria2.getVersion` - Get version information
- `system.listMethods` - List all methods
- WebSocket notifications (onDownloadStart, onDownloadComplete, onDownloadError, onBtDownloadComplete)

---

## Implementation Priority

### Phase 1: MVP (Milestone 1)
Implement all [Milestone 1] requirements. This provides:
- Download files from HTTP/FTP URLs and magnet links
- Query download status and progress
- Remove downloads
- Get global statistics
- Basic error handling and timeout/retry

**RPC Methods**: 6 methods (addUri, tellStatus, remove, getGlobalStat, getUris, getFiles)

### Phase 2: Enhanced (Milestone 2)
Add all [Milestone 2] requirements. This provides:
- Pause/resume individual downloads
- Batch pause/resume all downloads
- List active/waiting/stopped downloads
- Better task control

**RPC Methods**: +9 methods (total 15)

### Phase 3: Complete (Milestone 3)
Add all [Milestone 3] requirements. This provides:
- Full BitTorrent support (torrent files)
- Metalink support
- Dynamic configuration
- WebSocket real-time notifications
- System introspection

**RPC Methods**: +8 methods (total 23)

---

## Configuration Requirements (All Milestones)

All milestones require:
- `aria2.rpc.host`: Aria2 RPC host (default: localhost)
- `aria2.rpc.port`: Aria2 RPC port (default: 6800)
- `aria2.rpc.secret`: RPC secret token (optional)
- `aria2.rpc.secure`: Use HTTPS (default: false)
- Transport protocol: HTTP (Milestone 1-2), WebSocket (Milestone 3 optional)

---

## Testing Strategy

### Milestone 1 Tests
- Add download from URL and verify GID returned
- Query status and verify progress tracking
- Remove download and verify cleanup
- Test error handling (invalid URL, non-existent GID)
- Test timeout and retry behavior

### Milestone 2 Tests
- Pause/resume download and verify state changes
- Batch pause/resume all downloads
- List and filter active/waiting/stopped downloads
- Test concurrent state changes

### Milestone 3 Tests
- Add torrent from Base64 and verify download
- Add metalink from Base64 and verify multiple downloads
- Change task options and verify applied
- WebSocket event subscription and notification receipt
- System method introspection