## ADDED Requirements

### Requirement: Change Task Options [Milestone 3]
The skill SHALL provide capability to dynamically modify options for a specific download task using aria2.changeOption method.

#### Scenario: Modify Download Speed Limit
- **WHEN** user requests to change download speed limit for a specific GID
- **THEN** the skill SHALL call aria2.changeOption with the GID and new options
- **AND** the skill SHALL support: max-download-limit, max-upload-limit, max-concurrent-downloads

#### Scenario: Modify File Allocation
- **WHEN** user changes file allocation method for active download
- **THEN** the skill SHALL update file allocation to: none, prealloc, trunc
- **AND** the skill SHALL note that allocation method cannot be changed mid-download for some filesystems

#### Scenario: Add HTTP Headers
- **WHEN** user adds or modifies HTTP headers for a download
- **THEN** the skill SHALL update the header options using header parameter
- **AND** the skill SHALL append new headers to existing headers

#### Scenario: Invalid Option Change
- **WHEN** user attempts to change an immutable option for an active download
- **THEN** the skill SHALL return error if the option cannot be changed
- **AND** the error message SHALL indicate which option is immutable

#### Scenario: Batch Option Update
- **WHEN** user provides multiple options to change at once
- **THEN** the skill SHALL pass all options in a single changeOption call
- **AND** the skill SHALL validate all options before sending

### Requirement: Get Version Information [Milestone 3]
The skill SHALL provide capability to retrieve aria2 version and enabled features using aria2.getVersion method.

#### Scenario: Query Version
- **WHEN** user requests aria2 version information
- **THEN** the skill SHALL call aria2.getVersion
- **AND** the skill SHALL return: version string, enabled features (bittorrent, checksum, gzip, HTTPS, message-digest, rar, torrent, zip)

#### Scenario: Feature Availability Check
- **WHEN** user checks for specific feature availability
- **THEN** the skill SHALL return boolean for each feature in the enabledFeatures array
- **AND** the skill SHALL clearly indicate if requested feature is not available

#### Scenario: Protocol Version
- **WHEN** user requests protocol version information
- **THEN** the skill SHALL return the JSON-RPC protocol version supported by aria2

### Requirement: System Method Introspection [Milestone 3]
The skill SHALL provide capability to list all available RPC methods using system.listMethods method.

#### Scenario: List All Methods
- **WHEN** user requests list of all available aria2 RPC methods
- **THEN** the skill SHALL call system.listMethods
- **AND** the skill SHALL return array of method descriptions with name and parameters

#### Scenario: Method Signature Discovery
- **WHEN** user inspects a specific method signature
- **THEN** the skill SHALL return the method's parameter names and types
- **AND** the skill SHALL indicate which parameters are required vs optional

#### Scenario: Extension Method Detection
- **WHEN** user checks for extension methods beyond standard aria2
- **THEN** the skill SHALL return all available methods including any extensions
- **AND** the skill SHALL categorize methods by functionality (download, torrent, system)

### Requirement: Get URI [Milestone 1/2/3]
The skill SHALL provide capability to query URIs associated with a specific download using aria2.getUris method.

#### Scenario: Get Download URIs
- **WHEN** user requests URIs for a specific GID
- **THEN** the skill SHALL call aria2.getUris with the GID
- **AND** the skill SHALL return array of URI objects with: uri, status, downloading (boolean), remaining content length

#### Scenario: URI Status Tracking
- **WHEN** user checks which URIs are actively downloading
- **THEN** the skill SHALL return uri objects with downloading: true for active sources
- **AND** the skill SHALL indicate which URIs have been exhausted

#### Scenario: Multiple Sources
- **WHEN** download has multiple source URIs (mirrors, web seeds)
- **THEN** the skill SHALL return all URI objects in the response
- **AND** the skill SHALL indicate the current downloading source if any

### Requirement: Get Files [Milestone 1/2/3]
The skill SHALL provide capability to query file information for a specific download using aria2.getFiles method.

#### Scenario: List Download Files
- **WHEN** user requests file list for a specific GID
- **THEN** the skill SHALL call aria2.getFiles with the GID
- **AND** the skill SHALL return array of file objects with: index, path, length, completedLength, selected (boolean), uris

#### Scenario: File Selection State
- **WHEN** user checks which files are selected for download (torrent/metalink)
- **THEN** the skill SHALL return selected: true for files queued to download
- **AND** the skill SHALL return selected: false for deselected files

#### Scenario: File Download Progress
- **WHEN** user checks progress for individual files in a multi-file download
- **THEN** the skill SHALL return completedLength for each file
- **AND** the skill SHALL allow identifying partially downloaded files

### Requirement: Change Global Options [Milestone 3]
The skill SHALL provide capability to modify global options that affect all downloads using aria2.changeGlobalOption method.

#### Scenario: Global Download Limit
- **WHEN** user changes global download speed limit
- **THEN** the skill SHALL call aria2.changeGlobalOption with global scope
- **AND** the setting SHALL apply to all current and future downloads

#### Scenario: Global Configuration Update
- **WHEN** user updates global configuration (save session, force save)
- **THEN** the skill SHALL update the corresponding global option
- **AND** the skill SHALL confirm the global option was applied

#### Scenario: Global Option Query
- **WHEN** user requests current global options
- **THEN** the skill SHALL return all configurable global options
- **AND** the skill SHALL indicate which options differ from defaults

### Requirement: Option Schema Validation [Milestone 1/2/3]
The skill SHALL validate options against aria2's option schema before sending changes.

#### Scenario: Valid Option Names
- **WHEN** user provides an option name that aria2 does not recognize
- **THEN** the skill SHALL return error indicating unknown option
- **AND** the skill SHALL suggest similar valid option names if available

#### Scenario: Valid Option Values
- **WHEN** user provides an invalid value for a known option
- **THEN** the skill SHALL return error indicating invalid value
- **AND** the error message SHALL describe the expected value type or range

#### Scenario: Option Deprecation Warning
- **WHEN** user uses a deprecated option
- **THEN** the skill SHALL return warning along with the result
- **AND** the skill SHALL suggest the modern equivalent if available
