# Manual Testing Instructions for aria2-json-rpc Skill

**⚠️ EXECUTION ENVIRONMENT**: This test MUST be executed from the `.manual-test/` directory.

## Testing Objective

**This test validates the complete user interaction flow:**

When a user gives natural language commands (e.g., "download http://example.com/file.zip"), the AI agent should:
1. **Understand** the user's intent from natural language
2. **Execute** the appropriate Python script from the skill's `scripts/` directory using **`python3`** (NOT `python`)
3. **Format** the script output into a user-friendly response with:
   - Human-readable file sizes (KB, MB, GB instead of bytes)
   - Formatted speeds (KB/s, MB/s instead of bytes/sec)
   - Progress percentages (e.g., "45.2%" instead of raw completedLength/totalLength)
   - Clear status messages

The aria2-json-rpc skill is **agent-facing** - it instructs agents to use Python scripts (via `python3`) rather than manually constructing JSON-RPC requests. These tests verify that agents correctly interpret user commands and call the right scripts.

**What we're testing:**
- ✅ Agent's ability to map user requests to script calls
- ✅ Correct script execution with proper parameters using `python3` (not `python`)
- ✅ User-friendly response formatting (human-readable sizes, speeds, percentages)
- ❌ NOT testing: Manual JSON-RPC construction (agents should never do this)

## Prerequisites

Before running tests, ensure:
1. **Working Directory**: You are in `.manual-test/` directory
2. **aria2 daemon** is running on localhost:6800 with secret "test-secret"
3. **aria2-json-rpc skill** is loaded from `.opencode/skills/aria2-json-rpc/` (relative to `.manual-test/`)
4. **Configuration file** exists at `.opencode/skills/aria2-json-rpc/config.json` (relative to `.manual-test/`)
5. **Python 3** is available via `python3` command (NOT `python` - critical on macOS)

## Test Configuration

- **Working Directory**: `.manual-test/`
- **Skill Location**: `.manual-test/.opencode/skills/aria2-json-rpc/`
- **Config File**: `.manual-test/.opencode/skills/aria2-json-rpc/config.json`
- **RPC Host**: localhost
- **RPC Port**: 6800
- **RPC Secret**: test-secret
- **Download Dir**: /tmp/aria2-test-downloads
- **Log File**: /tmp/aria2-test.log

---

## Milestone 1: Core Operations

### Test 1.1: Download a file from URL

**User Command**: `download http://example.com/test-file.zip`

**What Agent Should Do**:
- Identify intent: Add a new download
- Execute: `python3 scripts/rpc_client.py aria2.addUri '["http://example.com/test-file.zip"]'`
- Parse the returned GID and format a user-friendly response

**Expected Results**:
- A new GID is returned
- Download is created with status "active"
- Download appears in active downloads list

**Verification Steps**:
1. Check that GID is returned in response
2. Run `show status for GID <gid>` to verify download exists
3. Run `show active downloads` to confirm it's active

---

### Test 1.2: Download multiple URLs (Fallback Sources)

**User Command**: `download http://example.com/file.zip with fallback http://mirror.com/file.zip`

**What Agent Should Do**:
- Identify intent: Add download with fallback/mirror sources
- Execute: `python3 scripts/rpc_client.py aria2.addUri '["http://example.com/file.zip","http://mirror.com/file.zip"]'`
- Parse GID and explain that URLs are fallback sources

**Expected Results**:
- **ONE GID is returned** (not multiple - this is important!)
- aria2 treats multiple URLs as backup sources for the SAME download
- If first URL fails, aria2 will try the second URL automatically

**Verification Steps**:
1. Check that **1 GID** is returned (not 2)
2. Verify download exists using the single GID
3. Run `show status for GID <gid>` - should show multiple URIs in the files list
4. Confirm this creates ONE download with multiple sources, not separate downloads

**Note**: This behavior is documented in aria2-methods.md - multiple URIs in one `aria2.addUri` call create a single download with mirror/fallback sources. To download multiple **separate** files, call `aria2.addUri` once per file with a single URL each.

---

### Test 1.2b: Download multiple separate files

**User Command**: `download http://example.com/file1.zip and http://example.com/file2.zip as separate downloads`

**What Agent Should Do**:
- Identify intent: Add multiple **separate** downloads
- Execute **two separate calls**:
  - `python3 scripts/rpc_client.py aria2.addUri '["http://example.com/file1.zip"]'`
  - `python3 scripts/rpc_client.py aria2.addUri '["http://example.com/file2.zip"]'`
- Parse both GIDs and report to user

**Expected Results**:
- Two GIDs are returned (one per command)
- Two separate downloads are created
- Both downloads have status "active"

**Verification Steps**:
1. Check that 2 GIDs are returned
2. Verify both downloads exist using their GIDs
3. Confirm both appear in active downloads list as separate entries

---

### Test 1.3: Query download status

**User Command**: `show status for GID <gid>`

**What Agent Should Do**:
- Identify intent: Query download status
- Execute: `python3 scripts/rpc_client.py aria2.tellStatus '<gid>'`
- Parse status information and format in a readable way:
  - Convert bytes to human-readable sizes (e.g., "10.5 MB" instead of "11010048")
  - Convert speeds to KB/s or MB/s (e.g., "2.5 MB/s" instead of "2621440")
  - Calculate and display progress percentage (e.g., "45.2%")
  - Format status clearly (Active, Paused, Complete, etc.)

**Expected Results**:
- Download details returned (status, progress, speed, etc.)
- All expected fields present (gid, status, totalLength, completedLength, downloadSpeed)
- Data is formatted in user-friendly way (NOT raw bytes)

**Verification Steps**:
1. Verify response contains download information
2. Check that status field is present and valid
3. Confirm GID matches the one provided
4. **Verify data formatting**: Check that agent converted bytes to KB/MB/GB and speeds to KB/s or MB/s

---

### Test 1.4: Query global statistics

**User Command**: `show global stats`

**What Agent Should Do**:
- Identify intent: Get global statistics
- Execute: `python3 scripts/rpc_client.py aria2.getGlobalStat`
- Parse statistics and present in a readable format:
  - Convert download/upload speeds to human-readable format (KB/s, MB/s)
  - Display counts clearly (number of active/waiting/stopped downloads)

**Expected Results**:
- Global statistics returned
- Fields like numActive, numWaiting, numStopped, downloadSpeed, uploadSpeed present
- Speeds formatted as KB/s or MB/s (not raw bytes/sec)

**Verification Steps**:
1. Verify response contains all expected statistics
2. Check that values are numeric and non-negative
3. Confirm numActive reflects current downloads
4. **Verify data formatting**: Check that speeds are displayed with units (not raw bytes)

---

### Test 1.5: Remove active download

**User Command**: `remove GID <gid>` (where <gid> is an **active** download)

**What Agent Should Do**:
- Identify intent: Remove an active download
- Check download status first (should be active, waiting, or paused)
- Execute: `python3 scripts/rpc_client.py aria2.remove '<gid>'`
- Confirm removal to the user

**Expected Results**:
- Active download is stopped and removed from aria2
- GID no longer appears in active downloads list
- Download may appear in stopped list briefly

**Verification Steps**:
1. Start with an active download
2. Check that removal command succeeds
3. Run `show active downloads` - removed GID should not appear
4. GID may appear in `show stopped downloads` with status "removed"

**Note**: Use `aria2.remove` for active/waiting/paused downloads. For completed downloads, see Test 2.11.

---

### Test 1.5b: Remove completed download result

**User Command**: `remove completed download GID <gid>` (where <gid> is a **completed** download)

**What Agent Should Do**:
- Identify intent: Remove a completed download record
- Check download status (should be complete, error, or removed)
- Execute: `python3 scripts/rpc_client.py aria2.removeDownloadResult '<gid>'`
- Confirm removal to the user

**Expected Results**:
- Download record is cleared from memory
- GID no longer appears in stopped downloads list
- Downloaded files remain on disk (not deleted)

**Verification Steps**:
1. Complete a download first or let one finish
2. Check that command succeeds
3. Run `show stopped downloads` - removed GID should not appear
4. Verify downloaded file still exists in download directory

**Important** (documented in aria2-methods.md): 
- `aria2.remove` → for active/waiting/paused downloads (stops and removes)
- `aria2.removeDownloadResult` → for complete/error/removed downloads (clears from memory)
- Neither method deletes downloaded files from disk

---

## Milestone 2: Batch Operations

### Test 2.1: List active downloads

**User Command**: `show active downloads`

**What Agent Should Do**:
- Identify intent: List active downloads
- Execute: `python3 scripts/examples/list-downloads.py` or `python scripts/rpc_client.py aria2.tellActive`
- Format the list in a user-friendly table or list format

**Expected Results**:
- List of all active downloads returned
- Each download contains status, progress, and details

**Verification Steps**:
1. Verify list format is correct
2. Check that all downloads have status "active"
3. Confirm count matches expected

---

### Test 2.2: List waiting downloads

**Command**: `show waiting downloads`

**Expected Results**:
- List of waiting downloads returned (or empty if none)
- Format matches expected structure

**Verification Steps**:
1. Verify list format is correct
2. Check that all downloads have status "waiting"
3. Confirm pagination works if there are many

---

### Test 2.3: List stopped downloads

**Command**: `show stopped downloads`

**What Agent Should Do**:
- Execute: `python3 scripts/rpc_client.py aria2.tellStopped 0 100`
- Format the list with human-readable data

**Expected Results**:
- List of stopped downloads returned (completed, error, removed)
- Format matches expected structure
- Uses pagination (offset=0, num=100 as documented in aria2-methods.md)

**Verification Steps**:
1. Verify list format is correct
2. Check that downloads have status "complete", "error", or "removed"
3. Confirm pagination works if there are many (first 100 items returned)
4. **Note**: To get recent items, can use negative offset: `python3 scripts/rpc_client.py aria2.tellStopped -1 10` (last 10)

---

### Test 2.4: Pause a specific download

**User Command**: `pause GID <gid>`

**What Agent Should Do**:
- Identify intent: Pause a specific download
- Execute: `python3 scripts/rpc_client.py aria2.pause '<gid>'`
- Confirm pause action to the user

**Expected Results**:
- Download status changes to "paused"
- Download still exists but not downloading
- Appears in active downloads with paused status

**Verification Steps**:
1. Check that pause command succeeds
2. Run `show status for GID <gid>` - status should be "paused"
3. Verify downloadSpeed is 0

---

### Test 2.5: Pause all downloads

**User Command**: `pause all downloads`

**What Agent Should Do**:
- Identify intent: Pause all active downloads
- Execute: `python3 scripts/examples/pause-all.py` or `python scripts/rpc_client.py aria2.pauseAll`
- Report number of downloads paused

**Expected Results**:
- All active downloads are paused
- Return value indicates number of paused downloads

**Verification Steps**:
1. Check that command succeeds
2. Run `show active downloads` - all should be paused
3. Verify no downloads have active download speed

---

### Test 2.6: Resume a paused download

**Command**: `resume GID <gid>`

**Expected Results**:
- Download status changes back to "active"
- Download resumes with download speed > 0

**Verification Steps**:
1. Check that resume command succeeds
2. Run `show status for GID <gid>` - status should be "active"
3. Verify downloadSpeed > 0

---

### Test 2.7: Resume all downloads

**Command**: `resume all downloads`

**Expected Results**:
- All paused downloads are resumed
- Return value indicates number of resumed downloads

**Verification Steps**:
1. Check that command succeeds
2. Run `show active downloads` - paused ones should be active
3. Verify downloads have download speed > 0

---

### Test 2.8: Get download options

**Command**: `show options for GID <gid>`

**Expected Results**:
- Download options returned (dir, out, max-connection, etc.)
- All expected option fields present

**Verification Steps**:
1. Verify response contains option fields
2. Check that values match expected (dir=/tmp/aria2-test-downloads)
3. Confirm format is correct

---

### Test 2.9: Get global options

**Command**: `show global options`

**Expected Results**:
- Global aria2 options returned
- Fields like max-concurrent-downloads, download-timeout present

**Verification Steps**:
1. Verify response contains global option fields
2. Check that values are valid
3. Confirm format matches aria2 RPC spec

---

### Test 2.10: Purge download results

**Command**: `purge download results`

**Expected Results**:
- Completed/removed download records are cleared
- Return value indicates number of purged records

**Verification Steps**:
1. Complete a download first (or remove one)
2. Run purge command
3. Run `show stopped downloads` - purged records should be gone

---

### Test 2.11: Remove download result (alternative test)

**Note**: This test is similar to Test 1.5b but tests with different download states and error handling.

**Command**: `clear download result GID <gid>`

**What Agent Should Do**:
- Identify intent: Remove a download result
- Verify download is in stopped state (complete, error, or removed)
- Execute: `python3 scripts/rpc_client.py aria2.removeDownloadResult '<gid>'`
- Confirm removal to the user

**Expected Results**:
- Specific download record is removed from memory
- GID no longer appears in stopped downloads
- Downloaded files (if any) remain on disk

**Verification Steps**:
1. Complete a download or let one fail (appears in stopped list)
2. Run remove download result command
3. Verify GID no longer appears in `show stopped downloads`
4. If download completed, verify files still exist in download directory

**Error Scenario** (documented in aria2-methods.md):
- If GID is still active/waiting/paused, this command should fail with error
- Agent should recognize the error and suggest using `aria2.remove` instead
- This tests the removal method selection logic documented in the "Download Removal Guide"

---

## Milestone 3: Advanced Features

### Test 3.1: Get aria2 version

**Command**: `show aria2 version`

**Expected Results**:
- aria2 version and features returned
- Fields: enabledFeatures, version

**Verification Steps**:
1. Verify version is returned
2. Check that enabledFeatures list is present
3. Confirm format matches expected

---

### Test 3.2: List available methods

**Command**: `list available methods`

**Expected Results**:
- List of all available RPC methods returned
- Methods include aria2.*, system.*, etc.

**Verification Steps**:
1. Verify list format is correct
2. Check that core methods (addUri, tellStatus, etc.) are present
3. Confirm no duplicate entries

---

### Test 3.3: Add torrent file (Optional - requires torrent file)

**Command**: `add torrent /path/to/test.torrent`

**Expected Results**:
- Torrent is added successfully
- GID is returned
- Download appears in appropriate list

**Verification Steps**:
1. Check that GID is returned
2. Run `show status for GID <gid>` to verify
3. Confirm download type is torrent

---

### Test 3.4: Add metalink file (Optional - requires metalink file)

**Command**: `add metalink /path/to/test.metalink`

**Expected Results**:
- Metalink is added successfully
- GIDs returned (one per file in metalink)
- Downloads appear in appropriate list

**Verification Steps**:
1. Check that GIDs are returned
2. Verify downloads exist
3. Confirm download type is metalink

---

## Error Handling Tests

### Test E.1: Invalid URL format

**Command**: `download invalid-url-without-protocol`

**Expected Results**:
- Appropriate error message returned
- No download is created
- Error indicates invalid URL format

**Verification Steps**:
1. Check that error message is clear
2. Verify no GID is returned
3. Confirm no new downloads appear

---

### Test E.2: Non-existent GID

**Command**: `show status for GID nonexistent123`

**Expected Results**:
- Error message about GID not found
- No status returned
- Error is specific about missing GID

**Verification Steps**:
1. Check that error message is clear
2. Verify no status data returned
3. Confirm error mentions GID

---

### Test E.3: Empty command

**Command**: `download` (without URL)

**Expected Results**:
- Error message or prompt for URL
- No download created

**Verification Steps**:
1. Check that OpenCode handles empty input gracefully
2. Verify helpful error or prompt
3. Confirm no side effects

---

### Test E.4: Pause non-existent download

**Command**: `pause GID nonexistent123`

**Expected Results**:
- Error message about GID not found
- No state changes

**Verification Steps**:
1. Check that error message is clear
2. Verify no downloads are affected
3. Confirm error is specific

---

## Test Results Format

For each test, record:

### Test: [Test Number] - [Test Name]

**Status**: PASS / FAIL

**User Command**: [natural language command]

**Agent Actions**:
- Tool Call: Bash
- Command Executed: [python3 scripts/... command]
- Description: [what the agent did]

**Script Output**:
```json
[raw output from Python script]
```

**Agent Response to User**:
[The formatted, user-friendly response the agent gave]
**Note**: Response should include human-readable data (KB/MB/GB for sizes, KB/s or MB/s for speeds, percentages for progress)

**Verification Results**:
- [Verification step 1]: PASS / FAIL
- [Verification step 2]: PASS / FAIL
- [Verification step 3]: PASS / FAIL
- **Data Formatting Check**: PASS / FAIL (Did agent format bytes/speeds/percentages?)

**Issues / Notes**:
- [Any issues encountered]
- [Did the agent choose the correct script?]
- [Did the agent use `python3` instead of `python`?]
- [Was the response user-friendly with proper data formatting?]
- [Additional observations]

---

## Completion

After completing all tests:

1. **Summary Statistics**:
   - Total tests: [N]
   - Passed: [N]
   - Failed: [N]
   - Pass rate: [X%]

2. **Milestone Breakdown**:
   - Milestone 1: [X]/[Y] tests passed
   - Milestone 2: [X]/[Y] tests passed
   - Milestone 3: [X]/[Y] tests passed
   - Error Handling: [X]/[Y] tests passed

3. **Critical Issues**:
   - List any critical failures that need fixing
   - Note any instances where `python` was used instead of `python3`

4. **Recommendations**:
   - Suggestions for improvement
   - Areas that need more testing
   - Data formatting quality assessment

5. **Next Steps**:
   - What to do with the results
   - Any follow-up actions needed
