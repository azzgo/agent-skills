## ADDED Requirements

### Requirement: Client Initialization and Configuration [Milestone 1]
The skill SHALL establish a JSON-RPC 2.0 client connection to an aria2 RPC endpoint. The skill SHALL support configuration from two sources: JSON config file (config.json in skill directory) and environment variables (ARIA2_RPC_*). The skill SHALL provide interactive configuration guidance on first use when no configuration is found. Configuration options include: endpoint URL (HTTP or WebSocket), port number, secret token for authentication, and connection timeout. The client SHALL handle both HTTP POST and WebSocket transport protocols. The skill SHALL validate configuration legality before each RPC call.

#### Scenario: HTTP Client Initialization
- **WHEN** skill is loaded with valid configuration from any source
- **THEN** the skill creates an HTTP client capable of sending JSON-RPC 2.0 POST requests to the specified endpoint
- **AND** the client prepends the secret token to the params array for all requests when authentication is configured

#### Scenario: Load Configuration from Skill Config File
- **WHEN** config.json file exists in skills/aria2-json-rpc/ directory with valid JSON configuration
- **THEN** the skill SHALL load configuration from the file
- **AND** the skill SHALL parse the JSON structure: {"host": "...", "port": ..., "secret": "...", "secure": false, "timeout": ...}

#### Scenario: Load Configuration from Environment Variables
- **WHEN** environment variables ARIA2_RPC_HOST, ARIA2_RPC_PORT, ARIA2_RPC_SECRET, ARIA2_RPC_SECURE are set
- **THEN** the skill SHALL use environment variable values
- **AND** environment variables SHALL override config.json settings

#### Scenario: Interactive Configuration on First Use
- **WHEN** no configuration is found from any source (no config.json, no environment variables)
- **THEN** the skill SHALL prompt the user for configuration interactively
- **AND** the skill SHALL ask for: host address (default: localhost), port number (default: 6800), secret token (optional), secure mode (default: false)
- **AND** the skill SHALL save the configuration to skills/aria2-json-rpc/config.json for future use

#### Scenario: Configuration Priority Resolution
- **WHEN** both environment variables and config.json provide values for the same parameter
- **THEN** the skill SHALL use environment variable values with higher priority
- **AND** config.json values SHALL be used as fallback when environment variables are not set

#### Scenario: Configuration Validation Before RPC Call
- **WHEN** the skill attempts to make an RPC call
- **THEN** the skill SHALL validate configuration legality before making the call
- **AND** the skill SHALL check required fields (host, port) are present and valid
- **AND** the skill SHALL test connection to aria2 endpoint
- **AND** the skill SHALL only proceed with RPC call if validation passes
- **AND** the skill SHALL throw error if validation fails

#### Scenario: WebSocket Client Initialization
- **WHEN** skill is loaded with WebSocket transport configuration (secure=true or ws:// prefix in host)
- **THEN** the skill establishes a persistent WebSocket connection to the aria2 endpoint
- **AND** the client supports server-side notifications (onDownloadStart, onDownloadComplete, onDownloadError, onBtDownloadComplete)

#### Scenario: Missing Configuration with Defaults
- **WHEN** no configuration source provides values
- **THEN** the skill SHALL use default value "localhost" for host
- **AND** the skill SHALL use default value "6800" for port
- **AND** the skill SHALL use default value "false" for secure
- **AND** the skill SHALL use default value "null" for secret (no authentication)

### Requirement: JSON-RPC 2.0 Request Formatting [Milestone 1]
The skill SHALL format all requests according to JSON-RPC 2.0 specification. Each request SHALL include jsonrpc: "2.0" field, a unique string id for request-response correlation, the method name prefixed with "aria2." for aria2 methods, and a params array with token injection when authentication is configured.

#### Scenario: Request Without Authentication
- **WHEN** no secret token is configured
- **THEN** the skill SHALL send requests with params array containing only user-provided parameters

#### Scenario: Request With Token Authentication
- **WHEN** aria2.rpc.secret is configured
- **THEN** the skill SHALL inject the token as the first element of params array in format "token:{secret}"
- **AND** the token injection SHALL apply to all aria2.* methods except system.* methods

#### Scenario: Method Name Prefix
- **WHEN** calling addUri method
- **THEN** the skill SHALL invoke the remote method as "aria2.addUri" in the JSON-RPC request

### Requirement: Configuration File Structure [Milestone 1]
The skill SHALL support JSON configuration file located exclusively in the skill directory (skills/aria2-json-rpc/config.json). The skill SHALL validate configuration file format and provide helpful error messages for invalid configurations. The skill SHALL NOT support any other configuration file formats (INI, YAML, TOML, .env) or configuration locations outside the skill directory.

#### Scenario: Valid JSON Configuration File
- **WHEN** skills/aria2-json-rpc/config.json file contains valid JSON configuration
- **THEN** the skill SHALL parse and apply configuration successfully
- **AND** supported structure: {"host": "string", "port": number, "secret": "string|null", "secure": boolean, "timeout": number}

#### Scenario: Invalid JSON Configuration File
- **WHEN** skills/aria2-json-rpc/config.json file contains malformed JSON
- **THEN** the skill SHALL throw error indicating JSON parse failure
- **AND** the skill SHALL include the specific parse error and line number
- **AND** the skill SHALL suggest the file location and provide example valid JSON structure

#### Scenario: Missing Required Configuration Fields
- **WHEN** configuration file is missing required fields (host, port)
- **THEN** the skill SHALL throw error indicating which fields are missing
- **AND** the skill SHALL provide example configuration structure in error message

#### Scenario: Configuration File Permissions
- **WHEN** skills/aria2-json-rpc/config.json file has restrictive permissions (not readable by skill)
- **THEN** the skill SHALL throw permission error
- **AND** the skill SHALL suggest checking file permissions: chmod 644 skills/aria2-json-rpc/config.json

#### Scenario: Configuration File in Wrong Location
- **WHEN** config.json exists in project root or user home directory instead of skill directory
- **THEN** the skill SHALL ignore the file
- **AND** the skill SHALL only look for configuration in skills/aria2-json-rpc/config.json
- **AND** the skill SHALL provide error message indicating the correct location if user accidentally places config.json elsewhere

### Requirement: Configuration Reload [Milestone 1]
The skill SHALL support dynamic configuration reload without requiring skill restart. The skill SHALL provide mechanism to reload configuration from config.json when changed.

#### Scenario: Reload Configuration on File Change
- **WHEN** skills/aria2-json-rpc/config.json file is modified after initial load
- **THEN** the skill SHALL detect file change and reload configuration
- **AND** the skill SHALL apply new configuration without disconnecting if possible

#### Scenario: Manual Configuration Reload
- **WHEN** user requests configuration reload
- **THEN** the skill SHALL re-read config.json and environment variables
- **AND** the skill SHALL validate new configuration before applying
- **AND** the skill SHALL report success or error of reload operation

#### Scenario: Configuration Reload Error
- **WHEN** configuration reload encounters invalid configuration in config.json
- **THEN** the skill SHALL keep previous valid configuration
- **AND** the skill SHALL throw error indicating why reload failed
- **AND** the skill SHALL provide details for fixing invalid configuration

### Requirement: Response Handling [Milestone 1]
The skill SHALL parse JSON-RPC 2.0 responses and handle success, error, and batch responses appropriately. The skill SHALL preserve error context including code, message, and data for debugging purposes.

#### Scenario: Successful Response
- **WHEN** the aria2 server returns a valid JSON-RPC response with result field
- **THEN** the skill SHALL return the result to the calling function as a parsed JavaScript object

#### Scenario: JSON-RPC Error Response
- **WHEN** the aria2 server returns an error response with error field
- **THEN** the skill SHALL throw an error with the code, message, and optional data from the response
- **AND** the skill SHALL include the request id in the error context for debugging

#### Scenario: Parse Error Handling
- **WHEN** the response cannot be parsed as valid JSON
- **THEN** the skill SHALL throw a parse error with descriptive message
- **AND** the skill SHALL log the raw response for debugging

### Requirement: Configuration File Structure [Milestone 1]
The skill SHALL support structured configuration files with clear schema definition. The skill SHALL validate configuration file format and provide helpful error messages for invalid configurations.

#### Scenario: Valid JSON Configuration File
- **WHEN** .aria2rc file contains valid JSON configuration
- **THEN** the skill SHALL parse and apply configuration successfully
- **AND** supported structure: {"aria2": {"rpc": {"host": "string", "port": number, "secret": "string|null", "secure": boolean}, "timeout": number}}

#### Scenario: Invalid JSON Configuration File
- **WHEN** .aria2rc file contains malformed JSON
- **THEN** the skill SHALL throw error indicating JSON parse failure
- **AND** the skill SHALL include the specific parse error and line number

#### Scenario: Missing Required Configuration Fields
- **WHEN** configuration file is missing required fields (host, port)
- **THEN** the skill SHALL throw error indicating which fields are missing
- **AND** the skill SHALL provide example configuration structure in error message

#### Scenario: Configuration File Permissions
- **WHEN** .aria2rc file has restrictive permissions (not readable by skill)
- **THEN** the skill SHALL throw permission error
- **AND** the skill SHALL suggest checking file permissions

#### Scenario: Multiple Configuration Formats
- **WHEN** .aria2rc (JSON), .aria2.conf (INI), and .env files all exist
- **THEN** the skill SHALL load .aria2rc with highest priority
- **AND** the skill SHALL ignore .aria2.conf and .env files when .aria2rc exists
The skill SHALL implement configurable timeout handling for all RPC calls with optional automatic retry for idempotent methods.

#### Scenario: Request Timeout
- **WHEN** a request exceeds the configured timeout duration (default 30 seconds)
- **THEN** the skill SHALL abort the request and throw a timeout error
- **AND** the skill SHALL provide clear error message indicating timeout occurred

#### Scenario: Automatic Retry on Network Error
- **WHEN** a network error occurs and the method is idempotent (GET-like operations)
- **THEN** the skill SHALL retry the request up to configured retry count (default 3)
- **AND** the skill SHALL implement exponential backoff between retries

### Requirement: Batch Request Support [Milestone 2]
The skill SHALL support batch requests for multiple operations in a single HTTP request using system.multicall or direct batch formatting.

#### Scenario: Batch Request via Multicall
- **WHEN** multiple method calls are needed in a single request
- **THEN** the skill SHALL format requests using system.multicall with array of method calls
- **AND** the skill SHALL parse the nested response array and return results in corresponding order

#### Scenario: Batch Request Without Multicall
- **WHEN** batch operations do not use system.multicall
- **THEN** the skill SHALL format multiple JSON-RPC request objects in an array
- **AND** the skill SHALL handle responses by correlating with request ids

### Requirement: WebSocket Event Handling [Milestone 3]
The skill SHALL subscribe to and handle aria2 server notifications when using WebSocket transport, enabling real-time status updates.

#### Scenario: Subscribe to Download Events
- **WHEN** WebSocket connection is established
- **THEN** the skill SHALL register handlers for aria2.onDownloadStart, aria2.onDownloadComplete, aria2.onDownloadError, and aria2.onBtDownloadComplete
- **AND** the skill SHALL emit corresponding events to registered listeners

#### Scenario: Event Listener Registration
- **WHEN** user registers a callback for download complete events
- **THEN** the skill SHALL call the callback with the gid when aria2.onDownloadComplete is received
