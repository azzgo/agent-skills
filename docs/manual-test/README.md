# Manual Testing for aria2-json-rpc Skill

This is an independent test environment for the aria2-json-rpc skill with OpenCode.

**Dependencies**: python3, aria2 daemon, and the aria2-json-rpc skill.

## Quick Start

1. **Start aria2 daemon** (if not already running):
   ```bash
   aria2c --enable-rpc --rpc-listen-all=true \
     --rpc-listen-port=6800 --rpc-secret=test-secret \
     --rpc-allow-origin-all --dir=/tmp/aria2-test-downloads \
     --log=/tmp/aria2-test.log -D
   ```

2. **Load the skill in OpenCode**:
   - Skill location: `.opencode/skills/aria2-json-rpc/`
   - Config file: `config.json` (in this directory)

3. **Run tests**:
   - Follow instructions in `instruct.md`
   - Or use OpenCode command: `/test-aria2`

4. **View results**:
   - Results saved to `results/timestamped_run_*.md`

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
./                           (Test environment root)
├── .opencode/
│   ├── skills/
│   │   └── aria2-json-rpc/  (skill files)
│   └── command/
│       └── test-aria2.md    (OpenCode command)
├── config.json              (aria2 connection config)
├── instruct.md              (test instructions)
├── README.md                (this file)
└── results/                 (test execution results)
```

## Configuration

The `config.json` file in this directory contains aria2 connection settings:

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

1. **Ensure aria2 daemon is running** (see Quick Start section above)

2. **Load the skill** from `.opencode/skills/aria2-json-rpc/`

3. **Configuration** is automatically loaded from `config.json` in this directory

4. **Execute tests** following the instructions in `instruct.md`

5. **Record results** in `results/` directory with timestamps

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
- Check configuration in `config.json` matches aria2 daemon settings
- Review aria2 logs: `cat /tmp/aria2-test.log`
- Ensure skill is loaded from `.opencode/skills/aria2-json-rpc/`

## Notes

- Test downloads go to `/tmp/aria2-test-downloads/`
- aria2 logs are saved to `/tmp/aria2-test.log`
- This environment only depends on: python3, aria2 daemon, and the skill
- No external project dependencies required during test execution