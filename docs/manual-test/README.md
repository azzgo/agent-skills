# Manual Testing for aria2-json-rpc Skill

This directory provides an isolated environment for manually testing the aria2-json-rpc skill with OpenCode.

## Quick Start

```bash
# 1. Set up the test environment
just manual-test-setup

# 2. Start aria2 daemon for testing
just manual-test-start-aria2 6800 test-secret

# 3. Load the skill in OpenCode from:
#    .manual-test/.opencode/skills/aria2-json-rpc/

# 4. Run tests following instructions in:
#    .manual-test/instruct.md
```

## Available Commands

### Setup Commands

```bash
# Initialize test environment
just manual-test-setup

# Check environment status
just manual-test-status
```

### aria2 Server Commands

```bash
# Start aria2 daemon (port, secret)
just manual-test-start-aria2 6800 test-secret

# Stop aria2 daemon
just manual-test-stop-aria2
```

### Running Tests

```bash
# Show testing instructions
cat .manual-test/instruct.md

# Test results will be saved to:
# .manual-test/results/timestamped_run_*.md
```

### Cleanup

```bash
# Stop aria2 and clean test environment
just manual-test-clean
```

## Test Environment

### Directory Structure

```
.manual-test/
├── .opencode/
│   └── skills/
│       └── aria2-json-rpc/  (symlink to actual skill)
├── config.json              (aria2 connection config)
├── instruct.md              (test instructions - copy from docs/manual-test/)
├── .opencode/
│   └── command/
│       └── test-aria2.md    (copy from docs/manual-test/)
└── results/                 (test execution results)
```

### Configuration

- **RPC Host**: localhost
- **RPC Port**: 6800 (configurable)
- **RPC Secret**: test-secret (configurable)
- **Download Dir**: /tmp/aria2-test-downloads
- **Log File**: /tmp/aria2-test.log

## Test Coverage

### Milestone 1: Core Operations
- Download files (single and multiple URLs)
- Query download status by GID
- Get global statistics
- Remove downloads

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

1. **Load the skill** from `.manual-test/.opencode/skills/aria2-json-rpc/`

2. **Configuration** is automatically loaded from `.manual-test/config.json`:
   ```json
   {
     "host": "localhost",
     "port": 6800,
     "secret": "test-secret",
     "secure": false,
     "timeout": 30000
   }
   ```

3. **Execute tests** following the instructions in `.manual-test/instruct.md`

4. **Record results** in `.manual-test/results/` with timestamps

## Result Format

Each test run should create a result file: `results/timestamped_run_YYYYMMDD_HHMMSS.md`

Include:
- Test run metadata (timestamp, server type)
- Test results per milestone
- Pass/fail summary
- Issues encountered
- Recommendations

## Notes

- The `.manual-test` directory is gitignored
- Test artifacts are local and not committed
- Skill files are symlinked from the main project
- aria2 downloads go to `/tmp/aria2-test-downloads`
- Logs are saved to `/tmp/aria2-test.log`
- Source documentation maintained in `docs/manual-test/`

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
- Verify aria2 daemon is running: `just manual-test-status`
- Check configuration in `.manual-test/config.json`
- Review aria2 logs: `cat /tmp/aria2-test.log`
- Ensure skill is loaded from correct path

## Cleanup

To completely remove the test environment:

```bash
just manual-test-clean
```

This will:
- Stop aria2 daemon
- Remove `.manual-test/` directory
- Remove test downloads from `/tmp/aria2-test-downloads/`