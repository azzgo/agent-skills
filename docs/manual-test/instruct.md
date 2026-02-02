# Manual Testing Instructions for aria2-json-rpc Skill

## Prerequisites

Before running tests, ensure:
1. aria2 daemon is running (use: `just manual-test-start-aria2 6800 test-secret`)
2. aria2-json-rpc skill is loaded from `.manual-test/.opencode/skills/aria2-json-rpc/`
3. Configuration is loaded from `.manual-test/config.json`

## Test Configuration

- **RPC Host**: localhost
- **RPC Port**: 6800
- **RPC Secret**: test-secret
- **Download Dir**: /tmp/aria2-test-downloads
- **Log File**: /tmp/aria2-test.log

---

## Milestone 1: Core Operations

### Test 1.1: Download a file from URL

**Command**: `download http://example.com/test-file.zip`

**Expected Results**:
- A new GID is returned
- Download is created with status "active"
- Download appears in active downloads list

**Verification Steps**:
1. Check that GID is returned in response
2. Run `show status for GID <gid>` to verify download exists
3. Run `show active downloads` to confirm it's active

---

### Test 1.2: Download multiple files

**Command**: `download http://example.com/file1.zip http://example.com/file2.zip`

**Expected Results**:
- Multiple GIDs are returned (one per URL)
- Both downloads are created with status "active"

**Verification Steps**:
1. Check that 2 GIDs are returned
2. Verify both downloads exist using their GIDs
3. Confirm both appear in active downloads list

---

### Test 1.3: Query download status

**Command**: `show status for GID <gid>`

**Expected Results**:
- Download details returned (status, progress, speed, etc.)
- All expected fields present (gid, status, totalLength, completedLength, downloadSpeed)

**Verification Steps**:
1. Verify response contains download information
2. Check that status field is present and valid
3. Confirm GID matches the one provided

---

### Test 1.4: Query global statistics

**Command**: `show global stats`

**Expected Results**:
- Global statistics returned
- Fields like numActive, numWaiting, numStopped, downloadSpeed, uploadSpeed present

**Verification Steps**:
1. Verify response contains all expected statistics
2. Check that values are numeric and non-negative
3. Confirm numActive reflects current downloads

---

### Test 1.5: Remove download

**Command**: `remove GID <gid>`

**Expected Results**:
- Download is removed from aria2
- GID no longer exists
- Removed from active downloads list

**Verification Steps**:
1. Check that removal command succeeds
2. Run `show status for GID <gid>` - should return error
3. Run `show active downloads` - removed GID should not appear

---

## Milestone 2: Batch Operations

### Test 2.1: List active downloads

**Command**: `show active downloads`

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

**Expected Results**:
- List of stopped downloads returned (completed, error, removed)
- Format matches expected structure

**Verification Steps**:
1. Verify list format is correct
2. Check that downloads have status "complete", "error", or "removed"
3. Confirm pagination works if there are many

---

### Test 2.4: Pause a specific download

**Command**: `pause GID <gid>`

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

**Command**: `pause all downloads`

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

### Test 2.11: Remove download result

**Command**: `remove download result GID <gid>`

**Expected Results**:
- Specific download record is removed
- GID no longer appears in stopped downloads

**Verification Steps**:
1. Remove a download (let it appear in stopped)
2. Run remove download result command
3. Verify GID no longer appears in stopped downloads

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

**Command Executed**: [command]

**Tool Calls Made**:
- [Tool name]: [parameters]
- [Tool name]: [parameters]

**Response from aria2**:
```json
[response data]
```

**Verification Results**:
- [Verification step 1]: PASS / FAIL
- [Verification step 2]: PASS / FAIL
- [Verification step 3]: PASS / FAIL

**Issues / Notes**:
- [Any issues encountered]
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

4. **Recommendations**:
   - Suggestions for improvement
   - Areas that need more testing

5. **Next Steps**:
   - What to do with the results
   - Any follow-up actions needed