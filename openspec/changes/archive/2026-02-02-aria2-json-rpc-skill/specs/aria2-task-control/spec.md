## ADDED Requirements

### Requirement: Pause Single Task [Milestone 2]
The skill SHALL provide capability to pause a specific download task using aria2.pause method.

#### Scenario: Pause Active Download
- **WHEN** user requests to pause an actively downloading task by GID
- **THEN** the skill SHALL call aria2.pause with the GID
- **AND** the task SHALL transition to "paused" status
- **AND** the skill SHALL return success confirmation

#### Scenario: Pause Already Paused Task
- **WHEN** user requests to pause a task that is already paused
- **THEN** the skill SHALL return success (idempotent operation)
- **AND** no error SHALL be raised

#### Scenario: Pause Non-existent Task
- **WHEN** user requests to pause a GID that does not exist
- **THEN** the skill SHALL return error with code -1
- **AND** the error message SHALL indicate the GID was not found

#### Scenario: Pause Completed Task
- **WHEN** user requests to pause a completed download
- **THEN** the skill SHALL return error indicating task is already complete
- **AND** no state change SHALL occur

### Requirement: Resume Single Task [Milestone 2]
The skill SHALL provide capability to resume a paused download task using aria2.unpause method.

#### Scenario: Resume Paused Download
- **WHEN** user requests to resume a paused task by GID
- **THEN** the skill SHALL call aria2.unpause with the GID
- **AND** the task SHALL transition back to "waiting" or "active" status
- **AND** the skill SHALL return success confirmation

#### Scenario: Resume Already Active Task
- **WHEN** user requests to resume a task that is already downloading
- **THEN** the skill SHALL return success (idempotent operation)
- **AND** no error SHALL be raised

#### Scenario: Resume Completed Task
- **WHEN** user requests to resume a completed download
- **THEN** the skill SHALL return error indicating task cannot be resumed
- **AND** the skill SHALL suggest re-adding the download if needed

### Requirement: Pause All Downloads [Milestone 2]
The skill SHALL provide capability to pause all active and waiting downloads using aria2.pauseAll method.

#### Scenario: Pause All Active Downloads
- **WHEN** user requests to pause all downloads
- **THEN** the skill SHALL call aria2.pauseAll
- **AND** all active downloads SHALL transition to "paused" status
- **AND** the skill SHALL return success after all pauses are initiated

#### Scenario: No Downloads Running
- **WHEN** user requests pauseAll with no active downloads
- **THEN** the skill SHALL return success (idempotent operation)
- **AND** no errors SHALL be raised

#### Scenario: Partial Pause Failure
- **WHEN** aria2 encounters error pausing some tasks during pauseAll
- **THEN** the skill SHALL return partial success with details of failed GIDs
- **AND** the skill SHALL continue attempting to pause remaining tasks

### Requirement: Resume All Downloads [Milestone 2]
The skill SHALL provide capability to resume all paused downloads using aria2.unpauseAll method.

#### Scenario: Resume All Paused Downloads
- **WHEN** user requests to resume all downloads
- **THEN** the skill SHALL call aria2.unpauseAll
- **AND** all paused downloads SHALL transition to "waiting" or "active" status
- **AND** the skill SHALL return success after all resumes are initiated

#### Scenario: No Downloads Paused
- **WHEN** user requests unpauseAll with no paused downloads
- **THEN** the skill SHALL return success (idempotent operation)

#### Scenario: Selective Resume by Pattern
- **WHEN** user requests to resume all paused downloads matching a pattern
- **THEN** the skill SHALL filter paused downloads by pattern (e.g., by directory, URL pattern)
- **AND** only matching downloads SHALL be resumed

### Requirement: Remove Task [Milestone 1]
The skill SHALL provide capability to stop and remove a download task using aria2.remove method.

#### Scenario: Remove Active Download
- **WHEN** user requests to remove an active download by GID
- **THEN** the skill SHALL call aria2.remove with the GID
- **AND** the download SHALL be stopped and removed from the queue
- **AND** partially downloaded files SHALL be deleted unless keep-files option was set

#### Scenario: Remove Paused Download
- **WHEN** user requests to remove a paused download
- **THEN** the skill SHALL remove the task from the queue
- **AND** no files SHALL have been downloaded yet

#### Scenario: Remove Completed Download
- **WHEN** user requests to remove a completed download
- **THEN** the skill SHALL remove the completed task from history
- **AND** the downloaded files SHALL remain on disk (unless delete-file option is used)

#### Scenario: Remove Non-existent Task
- **WHEN** user requests to remove a non-existent GID
- **THEN** the skill SHALL return error with code -1

### Requirement: Force Remove Task [Milestone 2]
The skill SHALL provide capability to forcibly stop and remove a download task that may be stuck using aria2.forceRemove method.

#### Scenario: Force Remove Stuck Download
- **WHEN** normal remove fails or user requests force remove
- **THEN** the skill SHALL call aria2.forceRemove with the GID
- **AND** the download SHALL be stopped regardless of current state
- **AND** the task SHALL be removed from all queues

#### Scenario: Force Remove with Resource Cleanup
- **WHEN** force remove is called with cleanup option
- **THEN** the skill SHALL attempt to release all allocated resources
- **AND** the skill SHALL close any open file handles

### Requirement: Task State Transition Handling [Milestone 2]
The skill SHALL handle state transitions and provide feedback on task status changes.

#### Scenario: State Transition Notification
- **WHEN** a task state changes (via pause/unpause/remove)
- **THEN** the skill SHALL provide the new status to the caller
- **AND** the skill SHALL emit events for registered listeners (WebSocket mode)

#### Scenario: Concurrent State Changes
- **WHEN** multiple pause/unpause requests are made for the same GID simultaneously
- **THEN** the skill SHALL handle requests in order
- **AND** the final state SHALL reflect the last requested operation

#### Scenario: State Change During Query
- **WHEN** status is queried immediately after state change request
- **THEN** the skill SHALL return the requested state (optimistic) or actual state after propagation
