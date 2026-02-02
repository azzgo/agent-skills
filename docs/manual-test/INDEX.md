# Manual Testing Documentation

This directory contains documentation for manually testing the aria2-json-rpc skill.

## Files

- **README.md** - User guide for the manual testing environment
- **instruct.md** - Detailed test instructions for OpenCode to execute
- **test-aria2.md** - OpenCode command definition for running tests

## Overview

The manual testing system provides an isolated environment for testing the aria2-json-rpc skill with OpenCode against a real aria2 daemon.

### Key Features

- **Isolated environment**: `.manual-test/` directory is gitignored
- **Real aria2 daemon**: Tests against actual aria2 RPC server
- **Natural language testing**: Tests use human-readable commands
- **Timestamped results**: Each test run generates a timestamped report
- **Source managed**: Documentation maintained here, copied during setup

## Usage

```bash
# 1. Set up the test environment
just manual-test-setup

# 2. Start aria2 daemon
just manual-test-start-aria2 6800 test-secret

# 3. Run tests in OpenCode
#    - Load skill from .manual-test/.opencode/skills/aria2-json-rpc/
#    - Follow instructions in .manual-test/instruct.md
#    - Or use command: /test-aria2

# 4. View results
#    Results saved to .manual-test/results/timestamped_run_*.md

# 5. Clean up when done
just manual-test-clean
```

## Test Coverage

### Milestone 1: Core Operations
- Download files (single/multiple URLs)
- Query download status
- Get global statistics
- Remove downloads

### Milestone 2: Batch Operations
- List downloads (active/waiting/stopped)
- Pause/resume operations
- Get options (download/global)
- Purge download results

### Milestone 3: Advanced Features
- Get aria2 version
- List available methods
- Add torrent/metalink (optional)

### Error Handling
- Invalid inputs
- Non-existent GIDs
- Edge cases

## Architecture

```
docs/manual-test/          (Source documentation)
  ├── README.md
  ├── instruct.md
  └── test-aria2.md
          ↓ (copied by just manual-test-setup)
.manual-test/              (Test environment)
  ├── .opencode/
  │   ├── skills/
  │   │   └── aria2-json-rpc/  (symlink)
  │   └── command/
  │       └── test-aria2.md    (copy)
  ├── config.json
  ├── instruct.md            (copy)
  ├── README.md              (copy)
  └── results/               (generated)
      └── timestamped_run_*.md
```

## Configuration

Default test configuration (in `.manual-test/config.json`):

```json
{
  "host": "localhost",
  "port": 6800,
  "secret": "test-secret",
  "secure": false,
  "timeout": 30000
}
```

## Maintenance

- Edit documentation files in this directory (`docs/manual-test/`)
- Run `just manual-test-setup` to update `.manual-test/` with changes
- Changes to skill files automatically reflected via symlink
- Test results are generated and stored locally

## Notes

- `.manual-test/` is gitignored (see `.gitignore`)
- Test downloads go to `/tmp/aria2-test-downloads/`
- aria2 logs saved to `/tmp/aria2-test.log`
- Use real aria2 daemon for integration testing (Option B)

## Related Documentation

- Main project README: `../README.md`
- Skill documentation: `../../skills/aria2-json-rpc/SKILL.md`
- Testing tasks: `../../openspec/changes/aria2-json-rpc-skill/tasks.md`
- Agent documentation: `../../AGENTS.md`