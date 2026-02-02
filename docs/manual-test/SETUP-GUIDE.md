# Manual Testing Setup Guide (For Developers)

This guide is for **developers** who want to set up the manual testing environment using the project's `just` commands.

> **Note**: This file is NOT copied to `.manual-test/`. It's only for developers working in the project repository.

## Overview

The manual testing system provides an isolated environment for testing the aria2-json-rpc skill with OpenCode against a real aria2 daemon.

### Files in this Directory

- **SETUP-GUIDE.md** (this file) - Setup instructions for developers (NOT copied to `.manual-test/`)
- **README.md** - User guide copied to `.manual-test/` (independent of project structure)
- **instruct.md** - Detailed test instructions for OpenCode to execute
- **test-aria2.md** - OpenCode command definition for running tests

### Key Features

- **Isolated environment**: `.manual-test/` directory is gitignored
- **Independent operation**: Test environment only depends on python3 (via `python3` command), aria2 daemon, and skills
- **No project dependency**: Once set up, tests don't require `just` commands or project directory
- **Real aria2 daemon**: Tests against actual aria2 RPC server
- **Natural language testing**: Tests use human-readable commands
- **Data formatting validation**: Tests verify agent formats bytes/speeds/percentages for users
- **Timestamped results**: Each test run generates a timestamped report

## Developer Setup (Using `just` commands)

```bash
# 1. Set up the test environment
just manual-test-setup

# 2. Start aria2 daemon
just manual-test-start-aria2 6800 test-secret

# 3. Check status
just manual-test-status

# 4. The test environment is now ready for use
#    See .manual-test/README.md for user instructions

# 5. Clean up when done
just manual-test-clean
```

## Test Coverage

### Milestone 1: Core Operations
- Download files (single/multiple URLs with fallback handling)
- Query download status (with data formatting)
- Get global statistics (with speed formatting)
- Remove downloads (active vs completed)

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

## Test Coverage

Tests are organized into milestones:

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
docs/manual-test/          (Source documentation - for developers)
  ├── SETUP-GUIDE.md       (this file - NOT copied)
  ├── README.md            (copied to .manual-test/)
  ├── instruct.md          (copied to .manual-test/)
  └── test-aria2.md        (copied to .manual-test/.opencode/command/)
          ↓ (copied by just manual-test-setup)
.manual-test/              (Independent test environment - WORK FROM HERE)
  ├── .opencode/
  │   ├── skills/
  │   │   └── aria2-json-rpc/  (full copy of skills/aria2-json-rpc/)
  │   │       ├── scripts/
  │   │       ├── references/
  │   │       ├── SKILL.md
  │   │       └── config.json  (aria2 connection config - CRITICAL)
  │   └── command/
  │       └── test-aria2.md    (copy)
  ├── instruct.md            (test instructions - copy)
  ├── README.md              (user guide - copy)
  └── results/               (test results - generated)
      └── timestamped_run_*.md
```

**Key Points:**
- All test operations must be performed from `.manual-test/` directory
- The `.opencode/` directory is INSIDE `.manual-test/`
- Skills are loaded from `.manual-test/.opencode/skills/`
- Configuration is at `.manual-test/.opencode/skills/aria2-json-rpc/config.json`

## What Gets Copied

- **Full copy**: `.opencode/skills/aria2-json-rpc/` (isolated from source, changes require re-running setup)
- **Copied**: `README.md`, `instruct.md`, `test-aria2.md` (independent copies)
- **Created**: `config.json` in `.manual-test/.opencode/skills/aria2-json-rpc/` directory
- **Not copied**: `SETUP-GUIDE.md` (developer-only documentation)

**Important**: The config file is created at `.manual-test/.opencode/skills/aria2-json-rpc/config.json`

## Available `just` Commands

```bash
# Setup and status
just manual-test-setup        # Create test environment
just manual-test-status       # Check environment status

# aria2 daemon management
just manual-test-start-aria2  # Start aria2 daemon
just manual-test-stop-aria2   # Stop aria2 daemon

# Cleanup
just manual-test-clean        # Remove test environment and stop daemon
```

## Manual Testing Workflow (Without `just`)

Once the environment is set up, you can run tests independently:

1. **Start aria2** (if not already running):
   ```bash
   aria2c --enable-rpc --rpc-listen-all=true \
     --rpc-listen-port=6800 --rpc-secret=test-secret \
     --rpc-allow-origin-all --dir=/tmp/aria2-test-downloads \
     --log=/tmp/aria2-test.log -D
   ```

2. **Navigate to test directory**:
   ```bash
   cd .manual-test
   ```

3. **Follow README.md instructions** in that directory

4. **Tests are independent** - no need for `just` commands or project directory

## Configuration

Default test configuration created at `.manual-test/.opencode/skills/aria2-json-rpc/config.json`:

```json
{
  "host": "localhost",
  "port": 6800,
  "path": null,
  "secret": "test-secret",
  "secure": false,
  "timeout": 30000
}
```

**Note**: The `path` field is optional:
- Set to `null` for standard aria2 on localhost (default)
- Set to `"/jsonrpc"` or custom path for reverse proxy setups
- See skill documentation for reverse proxy configuration examples

## Maintenance

- **Edit source files** in `docs/manual-test/` or `skills/aria2-json-rpc/` directories
- **Run setup** with `just manual-test-setup` to update `.manual-test/` copies
- **Skill changes** require re-running `just manual-test-setup` to copy updated files
- **Test results** are generated locally in `.manual-test/results/`

## Notes

- `.manual-test/` is gitignored
- Test downloads go to `/tmp/aria2-test-downloads/`
- aria2 logs saved to `/tmp/aria2-test.log`
- Once set up, tests only depend on: python3 (via `python3` command), aria2 daemon, and the skill

## Related Documentation

- User guide: `.manual-test/README.md` (after setup)
- Test instructions: `.manual-test/instruct.md` (after setup)
- Skill documentation: `../../skills/aria2-json-rpc/SKILL.md`
- Main project README: `../../README.md`
