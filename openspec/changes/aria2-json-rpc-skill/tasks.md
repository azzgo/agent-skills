## 1. Milestone 1: Core Setup and Basic Operations

- [x] 1.1 Create skill directory structure: skills/aria2-json-rpc/
- [x] 1.2 Create SKILL.md with skill metadata and usage instructions
- [x] 1.3 Create assets/ directory for templates and resources
- [x] 1.4 Create scripts/ directory for executable scripts
- [x] 1.5 Create references/ directory for documentation
- [x] 1.6 Implement dependency check module (Python version, builtin modules)
- [x] 1.7 Implement configuration loading from assets/config.json or root config.json
- [x] 1.8 Implement configuration loading from environment variables (ARIA2_RPC_*)
- [x] 1.9 Implement configuration validation and connection testing
- [x] 1.7 Implement JSON-RPC 2.0 request formatting (jsonrpc, method, params, id)
- [x] 1.8 Implement token injection for authentication (token:<SECRET_TOKEN>)
- [x] 1.9 Implement HTTP POST client using urllib.request
- [x] 1.10 Implement JSON-RPC response parsing (result/error handling)
- [x] 1.11 Implement aria2.addUri method (single and multiple URLs)
- [x] 1.12 Implement aria2.tellStatus method (task status query)
- [x] 1.13 Implement aria2.remove method (task removal)
- [x] 1.14 Implement aria2.getGlobalStat method (global statistics)
- [x] 1.15 Implement natural language command mapping for Milestone 1 methods
- [ ] 1.16 Add Python unit tests for RPC client (HTTP POST, token injection, response parsing)
- [ ] 1.17 Add Python unit tests for configuration module (config.json, environment variables, validation)
- [ ] 1.18 Add Python unit tests for natural language mapping (command parsing, method selection)
- [ ] 1.19 Create mock aria2 JSON-RPC server for integration testing
- [ ] 1.20 Implement OpenCode Executor instance for Milestone 1 testing
- [ ] 1.21 Implement OpenCode Evaluator instance for Milestone 1 testing
- [ ] 1.22 Run dual-instance integration tests for Milestone 1 methods (Executor + Evaluator)
- [ ] 1.23 Analyze execution records and LLM tracing from integration tests
- [ ] 1.24 Generate evaluation reports with success/failure analysis and improvement suggestions
- [ ] 1.25 Fix any issues identified in integration tests
- [ ] 1.26 Update SKILL.md with Milestone 1 capabilities and examples

## 2. Milestone 2: Advanced Task Control and Batch Operations

- [ ] 2.1 Implement aria2.pause method (pause single task)
- [ ] 2.2 Implement aria2.unpause method (resume single task)
- [ ] 2.3 Implement aria2.pauseAll method (pause all downloads)
- [ ] 2.4 Implement aria2.unpauseAll method (resume all downloads)
- [ ] 2.5 Implement aria2.forceRemove method (force remove stuck task)
- [ ] 2.6 Implement aria2.tellActive method (list active downloads)
- [ ] 2.7 Implement aria2.tellWaiting method (list waiting/paused downloads with pagination)
- [ ] 2.8 Implement aria2.tellStopped method (list completed/removed downloads)
- [ ] 2.9 Implement aria2.getUris method (query URIs for a task)
- [ ] 2.10 Implement aria2.getFiles method (query file information for a task)
- [ ] 2.11 Implement status field mapping (status codes to readable strings)
- [ ] 2.12 Implement speed unit conversion (bytes/s to KB/s, MB/s, GB/s)
- [ ] 2.13 Implement progress percentage calculation
- [ ] 2.14 Implement ETA calculation (estimated time to completion)
- [ ] 2.15 Extend natural language mapping for Milestone 2 methods
- [ ] 2.16 Add Python unit tests for batch operations (pauseAll/unpauseAll, forceRemove)
- [ ] 2.17 Add Python unit tests for list methods (tellActive/tellWaiting/tellStopped)
- [ ] 2.18 Add Python unit tests for status calculations (progress, ETA, speed conversion)
- [ ] 2.19 Extend mock aria2 server responses for Milestone 2 methods
- [ ] 2.20 Run dual-instance integration tests for Milestone 2 methods
- [ ] 2.21 Analyze execution records and LLM reasoning chain for batch operations
- [ ] 2.22 Generate evaluation reports with detailed failure analysis
- [ ] 2.23 Fix any issues identified in Milestone 2 integration tests
- [ ] 2.24 Update SKILL.md with Milestone 2 capabilities and examples

## 3. Milestone 3: Complete Protocol Support

- [ ] 3.1 Implement Base64 encoding module for binary files
- [ ] 3.2 Implement aria2.addTorrent method (torrent file download)
- [ ] 3.3 Implement aria2.addMetalink method (metalink file download)
- [ ] 3.4 Implement aria2.changeOption method (modify task options)
- [ ] 3.5 Implement aria2.changeGlobalOption method (modify global options)
- [ ] 3.6 Implement aria2.getVersion method (version and features)
- [ ] 3.7 Implement aria2.getOption method (get task options)
- [ ] 3.8 Implement aria2.getGlobalOption method (get global options)
- [ ] 3.9 Implement system.listMethods method (list all RPC methods)
- [ ] 3.10 Implement option schema validation (valid option names and values)
- [ ] 3.11 Implement dependency check for websockets library (optional)
- [ ] 3.12 Implement WebSocket client connection (if websockets available)
- [ ] 3.13 Implement WebSocket event subscription (onDownloadStart, onDownloadComplete, onDownloadError, onBtDownloadComplete)
- [ ] 3.14 Implement WebSocket event handlers and callbacks
- [ ] 3.15 Extend natural language mapping for Milestone 3 methods
- [ ] 3.16 Add Python unit tests for torrent/metalink operations (Base64 encoding, file handling)
- [ ] 3.17 Add Python unit tests for configuration methods (changeOption, getVersion)
- [ ] 3.18 Add Python unit tests for option schema validation
- [ ] 3.19 Add Python unit tests for WebSocket event handlers (if implemented)
- [ ] 3.20 Extend mock aria2 server responses for Milestone 3 methods
- [ ] 3.21 Run dual-instance integration tests for Milestone 3 methods
- [ ] 3.22 Analyze LLM tracing for complex operations (torrent/metalink, configuration changes)
- [ ] 3.23 Generate evaluation reports for WebSocket event tests (if applicable)
- [ ] 3.24 Fix any issues identified in Milestone 3 integration tests
- [ ] 3.25 Update SKILL.md with Milestone 3 capabilities and examples
- [ ] 3.26 Update SKILL.md with complete feature documentation

## 4. Error Handling and Robustness

- [ ] 4.1 Implement network error handling with retry logic (idempotent methods only)
- [ ] 4.2 Implement exponential backoff for retries
- [ ] 4.3 Implement JSON parse error handling with line/column information
- [ ] 4.4 Implement aria2 error handling with code/message/data preservation
- [ ] 4.5 Implement timeout handling for all RPC calls
- [ ] 4.6 Implement graceful error messages for missing dependencies
- [ ] 4.7 Add error context logging for debugging (request ID, raw response)
- [ ] 4.8 Implement configuration reload error handling (keep previous config on error)
- [ ] 4.9 Add Python unit tests for error handling (network errors, parse errors, aria2 errors)
- [ ] 4.10 Add integration tests for error scenarios (invalid GID, connection failures, timeouts)
- [ ] 4.11 Verify Evaluator correctly analyzes error handling failures
- [ ] 4.12 Document error codes and troubleshooting guide

## 5. Testing Infrastructure and Framework

- [ ] 5.1 Create test suite directory structure: tests/unit/ and tests/integration/
- [ ] 5.2 Set up Python unit test framework (unittest or pytest)
- [ ] 5.3 Create test fixtures and mocks for HTTP requests (patch urllib.request)
- [ ] 5.4 Create test fixtures for file system operations (config.json)
- [ ] 5.5 Create test fixtures for environment variables (patch os.environ)
- [ ] 5.6 Implement mock aria2 JSON-RPC server (http.server or Flask)
- [ ] 5.7 Add mock server endpoints for all aria2 RPC methods (Milestones 1-3)
- [ ] 5.8 Implement mock server request/response logging
- [ ] 5.9 Implement OpenCode Executor class (loads skill, executes commands, records tracing)
- [ ] 5.10 Implement LLM context tracing in Executor (reasoning chain, tool calls, decisions)
- [ ] 5.11 Implement OpenCode Evaluator class (analyzes execution, judges success/failure)
- [ ] 5.12 Define evaluation criteria (task completion, RPC correctness, reasoning quality, error handling, response quality)
- [ ] 5.13 Implement failure analysis in Evaluator (root cause, location, expected vs actual behavior)
- [ ] 5.14 Implement improvement suggestion generation in Evaluator (code fixes, priorities, action items)
- [ ] 5.15 Create integration test runner script (orchestrates Executor and Evaluator)
- [ ] 5.16 Implement test result aggregation and reporting
- [ ] 5.17 Create test execution record JSON schema and validation
- [ ] 5.18 Create evaluation result JSON schema and validation
- [ ] 5.19 Implement test report generation (summary, pass/fail rates, common failures, priorities)
- [ ] 5.20 Add performance metrics tracking (execution time, latency, throughput)

## 6. Test Execution and Validation

- [ ] 6.1 Run Python unit tests for Milestone 1 (isolated, no external dependencies)
- [ ] 6.2 Verify all unit tests pass before proceeding to integration tests
- [ ] 6.3 Start mock aria2 server for integration testing
- [ ] 6.4 Configure skill to connect to mock server (environment variables or config.json)
- [ ] 6.5 Run dual-instance integration tests for Milestone 1
- [ ] 6.6 Analyze LLM tracing from Executor for Milestone 1 tests
- [ ] 6.7 Review Evaluator judgments and failure analysis for Milestone 1
- [ ] 6.8 Fix any issues identified in Milestone 1 integration tests
- [ ] 6.9 Re-run integration tests to verify fixes
- [ ] 6.10 Run Python unit tests for Milestone 2
- [ ] 6.11 Run dual-instance integration tests for Milestone 2
- [ ] 6.12 Analyze LLM reasoning chain for batch operations
- [ ] 6.13 Review Evaluator feedback on complex scenarios
- [ ] 6.14 Fix any issues identified in Milestone 2 integration tests
- [ ] 6.15 Re-run integration tests to verify fixes
- [ ] 6.16 Run Python unit tests for Milestone 3
- [ ] 6.17 Run dual-instance integration tests for Milestone 3
- [ ] 6.18 Analyze LLM tracing for advanced operations (torrent/metalink)
- [ ] 6.19 Review Evaluator analysis of WebSocket tests (if applicable)
- [ ] 6.20 Fix any issues identified in Milestone 3 integration tests
- [ ] 6.21 Re-run integration tests to verify fixes
- [ ] 6.22 Generate comprehensive test report for all milestones
- [ ] 6.23 Analyze common failure patterns across all tests
- [ ] 6.24 Generate improvement recommendations report
- [ ] 6.25 Verify Python 3.6+ compatibility with all tests
- [ ] 6.26 Verify zero-dependency operation for Milestones 1-2
- [ ] 6.27 Verify optional dependency handling for Milestone 3 (websockets)

## 7. Documentation and Examples

- [ ] 7.1 Complete SKILL.md with full API reference
- [ ] 7.2 Add configuration examples (assets/config.json, environment variables)
- [ ] 7.3 Add usage examples for all RPC methods
- [ ] 7.4 Add troubleshooting section for common issues
- [ ] 7.5 Add security best practices documentation
- [ ] 7.6 Add milestone rollout guide
- [ ] 7.7 Add examples of natural language commands
- [ ] 7.8 Add example scripts in scripts/ for common workflows
- [ ] 7.9 Document error messages and solutions
- [ ] 7.10 Add testing documentation (how to run unit tests, integration tests)
- [ ] 7.11 Document test report interpretation
- [ ] 7.12 Add contribution guidelines (if applicable)

## 8. Final Integration and Deployment

- [ ] 8.1 Register skill in OpenCode agent framework
- [ ] 8.2 Verify skill loading and initialization (SKILL.md + assets/ + scripts/ + references/)
- [ ] 8.3 Test skill integration with agent command parser
- [ ] 8.4 Perform end-to-end testing with real aria2 daemon
- [ ] 8.5 Test all three milestones sequentially with real aria2
- [ ] 8.6 Verify rollback capability between milestones
- [ ] 8.7 Run full test suite before deployment (unit + integration)
- [ ] 8.8 Review all Evaluator improvement suggestions
- [ ] 8.9 Address any high-priority issues identified in testing
- [ ] 8.10 Run linting and code quality checks
- [ ] 8.11 Update project README with skill information
- [ ] 8.12 Create release notes for Milestone 1
- [ ] 8.13 Create release notes for Milestone 2
- [ ] 8.14 Create release notes for Milestone 3
- [ ] 8.15 Prepare deployment package and documentation