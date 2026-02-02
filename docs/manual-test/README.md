# Manual Testing for aria2-json-rpc Skill

This is an independent test environment for the aria2-json-rpc skill with OpenCode.

**⚠️ IMPORTANT: This document is located in the `.manual-test/` directory. All commands and paths are relative to `.manual-test/` unless otherwise specified.**

**Test Objective**: Validate complete user interaction flow - when users give natural language commands (e.g., "download this file"), the AI agent should:
1. Understand the intent
2. Call the appropriate Python scripts using **`python3`** (NOT `python`)
3. Format responses in a user-friendly way with:
   - Human-readable file sizes (KB, MB, GB)
   - Formatted speeds (KB/s, MB/s)
   - Progress percentages

**Test Environment**: 
- **Working Directory**: `.manual-test/` (in the project root)
- **Skill Location**: `.manual-test/.opencode/skills/aria2-json-rpc/`
- **Configuration**: `.manual-test/.opencode/skills/aria2-json-rpc/config.json`

**Dependencies**: python3 (via `python3` command), aria2 daemon, and the aria2-json-rpc skill.

## Quick Start

**IMPORTANT**: All operations should be performed from the `.manual-test/` directory.

**CRITICAL**: Tests require `python3` command (NOT `python`) - especially important on macOS where `python` symlink doesn't exist.

1. **Navigate to test environment**:
   ```bash
   cd .manual-test
   ```

2. **Start aria2 daemon** (if not already running):
   ```bash
   aria2c --enable-rpc --rpc-listen-all=true \
     --rpc-listen-port=6800 --rpc-secret=test-secret \
     --rpc-allow-origin-all --dir=/tmp/aria2-test-downloads \
     --log=/tmp/aria2-test.log -D
   ```

3. **Load the skill in OpenCode**:
   - **Working Directory**: `.manual-test/` (current directory)
   - **Skill Location**: `.opencode/skills/aria2-json-rpc/` (relative to `.manual-test/`)
   - **Config File**: `.opencode/skills/aria2-json-rpc/config.json` (relative to `.manual-test/`)

4. **Run tests**:
   - Follow instructions in `instruct.md` (in current directory)
   - Or use OpenCode command: `/test-aria2`

5. **View results**:
   - Results saved to `results/timestamped_run_*.md` (relative to `.manual-test/`)

## Check aria2 Status

```bash
# Check if aria2 is running
ps aux | grep aria2c

# Check if port 6800 is in use
lsof -i :6800

# View aria2 logs
tail -f /tmp/aria2-test.log
```

## Stop aria2

```bash
# Stop aria2 daemon
pkill -f "aria2c.*--enable-rpc"
```

## Directory Structure

```
.manual-test/                (Test environment root - WORK FROM HERE)
├── .opencode/
│   ├── skills/
│   │   └── aria2-json-rpc/  (full copy of skill files)
│   │       ├── scripts/
│   │       ├── references/
│   │       ├── SKILL.md
│   │       └── config.json  (aria2 connection config - CRITICAL)
│   └── command/
│       └── test-aria2.md    (OpenCode command)
├── instruct.md              (test instructions)
├── README.md                (this file)
└── results/                 (test execution results)
```

**Key Points**:
- All paths are relative to `.manual-test/` directory
- The `.opencode/` config directory is inside `.manual-test/`
- Skills are loaded from `.manual-test/.opencode/skills/`
- Configuration file is at `.manual-test/.opencode/skills/aria2-json-rpc/config.json`

## Configuration

**⚠️ Configuration File Location**: `.manual-test/.opencode/skills/aria2-json-rpc/config.json`

The `config.json` file contains aria2 connection settings:

```json
{
  "host": "localhost",
  "port": 6800,
  "secret": "test-secret",
  "secure": false,
  "timeout": 30000
}
```

**Important**: Make sure the port and secret match your aria2 daemon settings.

## Test Coverage

### Milestone 1: Core Operations
- Download files (single and multiple URLs)
- Query download status by GID (with formatted output)
- Get global statistics (with formatted speeds)
- Remove downloads (active vs completed)

### Milestone 2: Batch Operations
- List active/waiting/stopped downloads
- Pause and resume downloads (individual and batch)
- Get download and global options
- Purge download results

### Milestone 3: Advanced Features
- Get aria2 version
- List available RPC methods
- Add torrent/metalink files (optional)

### Error Handling
- Invalid URL format
- Non-existent GID
- Empty commands
- Invalid operations

## Using with OpenCode

**CRITICAL**: Make sure you're working from the `.manual-test/` directory!

```bash
# First, navigate to the test environment
cd .manual-test
```

1. **Ensure aria2 daemon is running** (see Quick Start section above)

2. **Load the skill**:
   - Path: `.opencode/skills/aria2-json-rpc/` (relative to `.manual-test/`)
   - OpenCode will read the skill from this location

3. **Configuration**:
   - File: `.opencode/skills/aria2-json-rpc/config.json` (relative to `.manual-test/`)
   - Scripts automatically load from this config file

4. **Execute tests**:
   - Follow instructions in `instruct.md` (in current directory)
   - All script paths are relative to the skill directory

5. **Record results**:
   - Save to `results/` directory (relative to `.manual-test/`)
   - Use timestamped filenames

## Test Results

Each test run should create a result file: `results/timestamped_run_YYYYMMDD_HHMMSS.md`

Include:
- Test run metadata (timestamp, aria2 version)
- Test results per milestone
- Pass/fail summary
- Issues encountered
- Recommendations

## Troubleshooting

### aria2 daemon won't start

```bash
# Check if already running
ps aux | grep aria2c

# Check if port is in use
lsof -i :6800

# View aria2 logs
tail -f /tmp/aria2-test.log
```

### Tests failing

- Verify aria2 daemon is running (see "Check aria2 Status" above)
- Check configuration file: `.manual-test/.opencode/skills/aria2-json-rpc/config.json` matches aria2 daemon settings
- Review aria2 logs: `cat /tmp/aria2-test.log`
- Ensure you're in `.manual-test/` directory when running OpenCode
- Ensure skill is loaded from `.opencode/skills/aria2-json-rpc/` (relative to `.manual-test/`)

## Notes

- **Working Directory**: Always work from `.manual-test/` directory
- **Skill Path**: `.manual-test/.opencode/skills/aria2-json-rpc/`
- **Config Path**: `.manual-test/.opencode/skills/aria2-json-rpc/config.json`
- **Python**: Must use `python3` command (NOT `python`) - critical on macOS
- Test downloads go to `/tmp/aria2-test-downloads/`
- aria2 logs are saved to `/tmp/aria2-test.log`
- This environment only depends on: python3, aria2 daemon, and the skill
- The skill directory is a full copy - to update the skill, re-run the setup command from the project root
- No external project dependencies required during test execution