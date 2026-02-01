## ADDED Requirements

### Requirement: Add URI Download Task [Milestone 1]
The skill SHALL provide capability to add download tasks from URIs including HTTP/HTTPS/FTP URLs and Magnet URIs using aria2.addUri method.

#### Scenario: Add Single HTTP URL
- **WHEN** user requests to download a single HTTP/HTTPS/FTP URL
- **THEN** the skill SHALL call aria2.addUri with the URL as first parameter in options array
- **AND** the skill SHALL return the assigned GID (Global ID) for the new download task

#### Scenario: Add Multiple URLs
- **WHEN** user provides an array of URLs to download
- **THEN** the skill SHALL call aria2.addUri with all URLs in the uris array
- **AND** the skill SHALL return a single GID for the batch download session

#### Scenario: Add Magnet URI
- **WHEN** user provides a magnet: URI
- **THEN** the skill SHALL call aria2.addUri with the magnet URI in the uris array
- **AND** the skill SHALL initiate BitTorrent download with the provided magnet link

#### Scenario: Download with Options
- **WHEN** user specifies download options (dir, out, split, max-concurrent-downloads)
- **THEN** the skill SHALL pass options as second parameter to aria2.addUri
- **AND** the skill SHALL validate options against aria2 supported parameters

### Requirement: Add Torrent Download Task [Milestone 3]
The skill SHALL provide capability to add BitTorrent download tasks from Base64-encoded torrent files using aria2.addTorrent method.

#### Scenario: Add Torrent File
- **WHEN** user provides a torrent file path or content
- **THEN** the skill SHALL convert the file to Base64 encoding
- **AND** the skill SHALL call aria2.addTorrent with the Base64 string as first parameter
- **AND** the skill SHALL return the assigned GID for the torrent download

#### Scenario: Torrent with Web Seeds
- **WHEN** user provides torrent file and additional HTTP/FTP URLs (web seeds)
- **THEN** the skill SHALL pass the URLs as second parameter (uris array) to aria2.addTorrent
- **AND** the skill SHALL support hybrid download from both torrent peers and HTTP sources

#### Scenario: Torrent with Options
- **WHEN** user specifies torrent-specific options (seed-time, ratio, bt-exclude-ut)
- **THEN** the skill SHALL pass options as third parameter to aria2.addTorrent
- **AND** the skill SHALL validate torrent-specific parameters (bt-hash-check-seed, bt.save-files)

#### Scenario: Invalid Torrent File
- **WHEN** user provides an invalid or corrupted torrent file
- **THEN** the skill SHALL return an error indicating torrent parsing failed
- **AND** the skill SHALL NOT attempt to send invalid Base64 to aria2

### Requirement: Add Metalink Download Task [Milestone 3]
The skill SHALL provide capability to add Metalink download tasks from Base64-encoded Metalink files using aria2.addMetalink method.

#### Scenario: Add Metalink File
- **WHEN** user provides a Metalink file (.metalink)
- **THEN** the skill SHALL convert the file to Base64 encoding
- **AND** the skill SHALL call aria2.addMetalink with the Base64 string as first parameter
- **AND** the skill SHALL return an array of GIDs for each download defined in the Metalink

#### Scenario: Metalink with Options
- **WHEN** user specifies Metalink download options
- **THEN** the skill SHALL pass options as second parameter to aria2.addMetalink
- **AND** the skill SHALL support all Metalink version 4 features

#### Scenario: Invalid Metalink File
- **WHEN** user provides an invalid Metalink file
- **THEN** the skill SHALL return an error indicating Metalink parsing failed

### Requirement: Options Specification [Milestone 1]
The skill SHALL support comprehensive options for all task creation methods, including download location, file naming, bandwidth limits, and connection settings.

#### Scenario: Specify Download Directory
- **WHEN** user sets option "dir" to a valid filesystem path
- **THEN** the skill SHALL pass the path to aria2 for file storage location
- **AND** the skill SHALL create the directory if it does not exist (aria2 creates automatically)

#### Scenario: Specify Output Filename
- **WHEN** user sets option "out" to a filename
- **THEN** the skill SHALL use the specified filename for the downloaded file
- **AND** the skill SHALL apply to single-file downloads only (ignored for torrents/metalinks with multiple files)

#### Scenario: Configure Connection Settings
- **WHEN** user configures options: split (default 16), max-concurrent-downloads, lowest-speed-limit
- **THEN** the skill SHALL pass these to aria2 for connection management
- **AND** the skill SHALL validate values are within aria2 supported ranges

### Requirement: Task Creation Response Handling [Milestone 1]
The skill SHALL properly handle responses from task creation methods including GID extraction and error conditions.

#### Scenario: Successful Task Creation
- **WHEN** aria2.addUri, addTorrent, or addMetalink returns a GID or array of GIDs
- **THEN** the skill SHALL return the GID(s) to the caller for task tracking
- **AND** the skill SHALL allow immediate status queries using the returned GID

#### Scenario: Duplicate Download Detection
- **WHEN** user attempts to add the same URI that is already downloading
- **THEN** the skill SHALL return the existing GID if aria2 supports duplicate detection
- **AND** the skill SHALL inform the user the download may already be in progress

#### Scenario: Invalid URI
- **WHEN** user provides a malformed or unreachable URI
- **THEN** the skill SHALL return an error from aria2 indicating the URI is invalid
- **AND** the error SHALL include the problematic URI in the message
