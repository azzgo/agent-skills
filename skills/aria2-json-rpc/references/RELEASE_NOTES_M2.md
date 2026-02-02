# Milestone 2 Release Notes

## Version 2.0.0 - Batch Operations and Advanced Control

### Overview
Milestone 2 adds comprehensive batch operations and fine-grained control capabilities. This release enables managing multiple downloads simultaneously, listing downloads by state, and dynamically modifying download options.

### New Features

#### Batch Control Methods
- **aria2.pause** / **aria2.pauseAll** - Pause individual or all active downloads
- **aria2.unpause** / **aria2.unpauseAll** - Resume individual or all paused downloads
- **aria2.tellActive** - List all currently downloading files
- **aria2.tellWaiting** - List queued/waiting downloads with pagination
- **aria2.tellStopped** - List stopped/completed downloads with pagination

#### Option Management
- **aria2.getOption** - Retrieve download-specific options
- **aria2.changeOption** - Modify download options dynamically (speed limits, etc.)
- **aria2.getGlobalOption** - View global aria2 configuration
- **aria2.changeGlobalOption** - Modify global settings (concurrent downloads, etc.)

#### Maintenance Operations
- **aria2.purgeDownloadResult** - Clear completed download history
- **aria2.removeDownloadResult** - Remove specific download record
- **aria2.getVersion** - Get aria2 version and enabled features
- **system.listMethods** - List all available RPC methods

#### Natural Language Commands
- "pause all downloads" / "resume all downloads"
- "list active downloads" / "list waiting downloads" / "list stopped downloads"
- "show options for GID X" / "set speed limit for GID X to 1M"
- "show global options" / "purge completed downloads"

#### Example Scripts
- **pause-all.py** - Pause all active downloads at once
- **list-downloads.py** - List all downloads across all states
- **set-options.py** - Interactive option modification

### API Additions

All new methods follow the same JSON-RPC 2.0 format:

```python
# Pause and resume
client.pause(gid)
client.pause_all()
client.unpause(gid)
client.unpause_all()

# List operations
active = client.tell_active()
waiting = client.tell_waiting(offset=0, num=100)
stopped = client.tell_stopped(offset=0, num=100)

# Options
options = client.get_option(gid)
client.change_option(gid, {"max-download-limit": "1M"})
global_opts = client.get_global_option()
client.change_global_option({"max-concurrent-downloads": "3"})

# Maintenance
client.purge_download_result()
client.remove_download_result(gid)
version = client.get_version()
methods = client.list_methods()
```

### Testing

#### Unit Tests Added
- Unit tests for pause/unpause operations
- Unit tests for tellActive/tellWaiting/tellStopped
- Unit tests for option management (get/change)
- Unit tests for multicall functionality
- Unit tests for natural language mapping (Milestone 2)

#### Example Usage
```bash
# Run Milestone 2 specific tests
python -m unittest tests.unit.test_milestone2 -v

# Use example scripts
python scripts/examples/pause-all.py
python scripts/examples/list-downloads.py
python scripts/examples/set-options.py --gid GID --max-download-limit 2M
```

### Dependencies
- No new dependencies (continues zero-dependency policy)
- Compatible with Milestone 1 configuration
- Python 3.6+ required

### Documentation Updates
- Updated SKILL.md with Milestone 2 operations
- Updated references/aria2-methods.md with new methods
- Added troubleshooting for batch operations
- Added security best practices for global option changes

### Migration from Milestone 1
**No breaking changes** - Milestone 2 is fully backward compatible with Milestone 1.

All Milestone 1 code continues to work without modification. Simply upgrade the skill files to gain new capabilities.

### Rollback
If issues are encountered:
1. Milestone 2 features can be disabled by reverting to Milestone 1 scripts
2. Configuration format remains unchanged
3. Core Milestone 1 functionality remains unaffected

### Known Limitations
- No BitTorrent/metalink support (Milestone 3)
- No WebSocket event notifications (Milestone 3)
- HTTP POST transport only

---

**Release Date**: 2026-02-02
**Status**: Stable
**Dependencies**: Milestone 1, Python 3.6+, aria2 daemon
**Breaking Changes**: None
