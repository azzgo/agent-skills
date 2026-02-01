## ADDED Requirements

### Requirement: Query Task Status [Milestone 1]
The skill SHALL provide capability to query detailed status and progress of a specific download task using aria2.tellStatus method.

#### Scenario: Query Active Download Status
- **WHEN** user requests status for a GID of an actively downloading task
- **THEN** the skill SHALL return complete status information including: gid, status (active), totalLength, completedLength, uploadLength, downloadSpeed, uploadSpeed, numSeeders, peers information
- **AND** the skill SHALL calculate and include progress percentage when requested

#### Scenario: Query Paused Download Status
- **WHEN** user requests status for a paused task
- **THEN** the skill SHALL return status with status field set to "paused"
- **AND** the skill SHALL include completeLength showing progress at pause time

#### Scenario: Query Completed Download Status
- **WHEN** user requests status for a completed download
- **THEN** the skill SHALL return status with status field set to "complete"
- **AND** the skill SHALL include completedLength equal to totalLength
- **AND** the skill SHALL include files array with verification status

#### Scenario: Query Non-existent GID
- **WHEN** user requests status for a GID that does not exist
- **THEN** the skill SHALL return error with code -1 and message indicating GID not found
- **AND** the skill SHALL distinguish between never-existing and expired/completed downloads

### Requirement: List Active Downloads [Milestone 2]
The skill SHALL provide capability to list all currently active (downloading) tasks using aria2.tellActive method.

#### Scenario: No Active Downloads
- **WHEN** aria2 has no active downloads
- **THEN** the skill SHALL return an empty array

#### Scenario: Single Active Download
- **WHEN** aria2 has one active download
- **THEN** the skill SHALL return an array with one status object containing all active task details

#### Scenario: Multiple Active Downloads
- **WHEN** aria2 has multiple active downloads
- **THEN** the skill SHALL return an array with status objects for all active tasks
- **AND** each status object SHALL contain gid, status, downloadSpeed, completedLength, totalLength, and files

#### Scenario: Filter Active by Type
- **WHEN** user requests active downloads filtered by type (http/ftp, bt, metalink)
- **THEN** the skill SHALL filter results to only matching download types
- **AND** the skill SHALL return empty array if no matching type exists

### Requirement: List Waiting Downloads [Milestone 2]
The skill SHALL provide capability to list tasks that are waiting in queue or currently paused using aria2.tellWaiting method.

#### Scenario: Query Waiting Queue
- **WHEN** user requests list of waiting downloads
- **THEN** the skill SHALL return array of status objects for tasks in "waiting" state
- **AND** the skill SHALL support offset and num parameters for pagination

#### Scenario: Query Paused Tasks
- **WHEN** user requests list of paused downloads
- **THEN** the skill SHALL return array of status objects with status "paused"
- **AND** the skill SHALL include the reason for pause if available

#### Scenario: Empty Waiting Queue
- **WHEN** no downloads are waiting or paused
- **THEN** the skill SHALL return an empty array

#### Scenario: Pagination
- **WHEN** user requests waiting list with offset and num parameters
- **THEN** the skill SHALL return only the specified slice of waiting tasks
- **AND** the skill SHALL support getting total count separately

### Requirement: List Stopped Downloads [Milestone 2]
The skill SHALL provide capability to list completed, removed, or stopped tasks using aria2.tellStopped method.

#### Scenario: Query Completed Downloads
- **WHEN** user requests list of stopped/completed downloads
- **THEN** the skill SHALL return array of status objects with status "complete"
- **AND** the skill SHALL include numConsecutiveHiccups, verifyIntegrityResult, and other completion metadata

#### Scenario: Query Removed Downloads
- **WHEN** user requests list of removed downloads
- **THEN** the skill SHALL return array of status objects with status "removed"
- **AND** the skill SHALL include the reason for removal when available

#### Scenario: Expired Downloads
- **WHEN** download history is purged due to max-download-result setting
- **THEN** the skill SHALL exclude purged downloads from tellStopped results
- **AND** the skill SHALL inform user about potential missing history

#### Scenario: Limit Results
- **WHEN** user specifies num parameter to limit results
- **THEN** the skill SHALL return at most the specified number of stopped downloads
- **AND** the skill SHALL order results by stop time (most recent first)

### Requirement: Global Statistics [Milestone 1]
The skill SHALL provide capability to retrieve global download statistics using aria2.getGlobalStat method.

#### Scenario: Overall Statistics
- **WHEN** user requests global statistics
- **THEN** the skill SHALL return: numActive, numWaiting, numStopped, numStoppedTotal, uploadSpeed, downloadSpeed
- **AND** the skill SHALL provide real-time aggregate values from aria2

#### Scenario: High Activity Detection
- **WHEN** user requests global statistics and numActive exceeds threshold
- **THEN** the skill SHALL provide option to return true if activity level is high
- **AND** the skill SHALL include upload and download speeds in bytes per second

#### Scenario: Idle State
- **WHEN** there are no active or waiting downloads
- **THEN** the skill SHALL return numActive: 0, numWaiting: 0, downloadSpeed: 0, uploadSpeed: 0

#### Scenario: Historical Data
- **WHEN** user requests historical download statistics
- **THEN** the skill SHALL return numStoppedTotal showing total downloads ever completed
- **AND** the skill SHALL provide running totals for tracking purposes

### Requirement: Status Field Mapping [Milestone 1]
The skill SHALL map aria2 status fields to human-readable formats and provide derived calculations.

#### Scenario: Status String Mapping
- **WHEN** aria2 returns status code
- **THEN** the skill SHALL map to human-readable strings: "active", "waiting", "paused", "complete", "removed", "error"

#### Scenario: Speed Unit Conversion
- **WHEN** aria2 returns speeds in bytes per second
- **THEN** the skill SHALL provide option to display in KB/s, MB/s, GB/s as appropriate

#### Scenario: Progress Calculation
- **WHEN** user requests progress percentage
- **THEN** the skill SHALL calculate (completedLength / totalLength * 100)
- **AND** the skill SHALL handle zero totalLength (live stream case) gracefully

#### Scenario: ETA Calculation
- **WHEN** user requests estimated time to completion
- **THEN** the skill SHALL calculate ETA based on downloadSpeed and remaining bytes
- **AND** the skill SHALL return null if downloadSpeed is zero or negative
