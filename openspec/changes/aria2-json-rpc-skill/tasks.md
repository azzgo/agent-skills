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
- [x] 1.10 Implement JSON-RPC 2.0 request formatting (jsonrpc, method, params, id)
- [x] 1.11 Implement token injection for authentication (token:<SECRET_TOKEN>)
- [x] 1.12 Implement HTTP POST client using urllib.request
- [x] 1.13 Implement JSON-RPC response parsing (result/error handling)
- [x] 1.14 Implement aria2.addUri method (single and multiple URLs)
- [x] 1.15 Implement aria2.tellStatus method (task status query)
- [x] 1.16 Implement aria2.remove method (task removal)
- [x] 1.17 Implement aria2.getGlobalStat method (global statistics)
- [x] 1.18 Implement natural language command mapping for Milestone 1 methods
- [x] 1.19 Add Python unit tests for RPC client (HTTP POST, token injection, response parsing)
- [x] 1.20 Add Python unit tests for configuration module (config.json, environment variables, validation)
- [x] 1.21 Add Python unit tests for natural language mapping (command parsing, method selection)

## 2. Milestone 2: Batch Operations and Advanced Control

- [x] 2.1 Implement aria2.pause method (pause active downloads by GID)
- [x] 2.2 Implement aria2.pauseAll method (pause all active downloads)
- [x] 2.3 Implement aria2.unpause method (resume paused downloads by GID)
- [x] 2.4 Implement aria2.unpauseAll method (resume all paused downloads)
- [x] 2.5 Implement aria2.tellActive method (list all active downloads)
- [x] 2.6 Implement aria2.tellWaiting method (list waiting downloads with pagination)
- [x] 2.7 Implement aria2.tellStopped method (list stopped downloads with pagination)
- [x] 2.8 Implement aria2.getOption method (get download options by GID)
- [x] 2.9 Implement aria2.changeOption method (modify download options by GID)
- [x] 2.10 Implement aria2.getGlobalOption method (get global aria2 options)
- [x] 2.11 Implement aria2.changeGlobalOption method (modify global aria2 options)
- [x] 2.12 Implement aria2.purgeDownloadResult method (remove completed download records)
- [x] 2.13 Implement aria2.removeDownloadResult method (remove specific download record)
- [x] 2.14 Implement aria2.getVersion method (get aria2 and aria2c version)
- [x] 2.15 Implement system.listMethods method (list all available RPC methods)
- [x] 2.16 Implement system.multicall method (execute multiple RPC calls in one request)
- [x] 2.17 Implement natural language command mapping for Milestone 2 methods
- [x] 2.18 Add Python unit tests for pause/unpause operations
- [x] 2.19 Add Python unit tests for tellActive/tellWaiting/tellStopped methods
- [x] 2.20 Add Python unit tests for option management (get/change)
- [x] 2.21 Add Python unit tests for multicall functionality
- [x] 2.22 Add Python unit tests for natural language mapping for Milestone 2
- [x] 2.23 Add example scripts for batch operations (pause-all.sh, list-downloads.py)
- [x] 2.24 Add example scripts for option management (set-options.py)
- [x] 2.25 Update SKILL.md with Milestone 2 operations documentation
- [x] 2.26 Update references/aria2-methods.md with Milestone 2 methods

## 3. Milestone 3: Advanced Features (Optional Dependencies)

- [ ] 3.1 Implement aria2.addTorrent method (add torrent file from base64 or file path)
- [ ] 3.2 Implement aria2.addTorrentByParam method (add torrent with structure parameters)
- [ ] 3.3 Implement aria2.addMetalink method (add metalink file from base64)
- [ ] 3.4 Implement aria2.addMetalinkByParam method (add metalink with structure parameters)
- [ ] 3.5 Implement WebSocket client for aria2 event notifications
- [ ] 3.6 Implement event subscription (aria2.onDownloadStart, onDownloadPause, etc.)
- [ ] 3.7 Implement WebSocket reconnection logic
- [ ] 3.8 Implement WebSocket event handler registration
- [ ] 3.9 Add optional dependency detection for websockets library
- [ ] 3.10 Add fallback for missing websockets library (HTTP polling alternative)
- [ ] 3.11 Implement natural language command mapping for Milestone 3 methods
- [ ] 3.12 Add Python unit tests for torrent/metalink operations
- [ ] 3.13 Add Python unit tests for WebSocket client
- [ ] 3.14 Add Python unit tests for event handling
- [ ] 3.15 Add example scripts for torrent downloads (add-torrent.py)
- [ ] 3.16 Add example scripts for WebSocket monitoring (monitor-downloads.py)
- [ ] 3.17 Update SKILL.md with Milestone 3 operations documentation
- [ ] 3.18 Update references/aria2-methods.md with Milestone 3 methods
- [ ] 3.19 Add WebSocket dependency check in dependency_check.py
- [ ] 3.20 Document optional dependency handling in SKILL.md

## 5. Test Infrastructure

- [x] 5.1 Create test suite directory structure: tests/unit/ and tests/integration/
- [x] 5.2 Set up Python unit test framework (unittest or pytest)
- [x] 5.3 Create test fixtures and mocks for HTTP requests (patch urllib.request)
- [x] 5.4 Create test fixtures for file system operations (config.json)
- [x] 5.5 Create test fixtures for environment variables (patch os.environ)
- [x] 5.6 Implement mock aria2 JSON-RPC server (http.server)
- [x] 5.7 Add mock server endpoints for all aria2 RPC methods (Milestones 1-3)
- [x] 5.8 Implement mock server request/response logging
- [ ] 5.9 Create integration test runner script (tests/run_integration_tests.py)
- [ ] 5.10 Implement mock server startup/shutdown logic in test runner
- [ ] 5.11 Add integration test fixtures for skill initialization
- [ ] 5.12 Create integration tests for Milestone 1 operations
- [ ] 5.13 Create integration tests for Milestone 2 operations
- [ ] 5.14 Create integration tests for Milestone 3 operations (with optional deps)
- [ ] 5.15 Implement test result aggregation and reporting
- [ ] 5.16 Create test report generation (summary, pass/fail rates, common failures)
- [ ] 5.17 Add performance metrics tracking (execution time, latency)

## 6. Test Execution and Validation

- [x] 6.1 Run Python unit tests for Milestone 1 (isolated, no external dependencies)
- [x] 6.2 Verify all unit tests pass before proceeding to integration tests
- [ ] 6.3 Run Python unit tests for Milestone 2
- [ ] 6.4 Run Python unit tests for Milestone 3
- [ ] 6.5 Start mock aria2 server for integration testing
- [ ] 6.6 Run integration tests for Milestone 1
- [ ] 6.7 Run integration tests for Milestone 2
- [ ] 6.8 Run integration tests for Milestone 3
- [ ] 6.9 Generate comprehensive test report for all milestones
- [ ] 6.10 Analyze common failure patterns across all tests
- [ ] 6.11 Verify Python 3.6+ compatibility with all tests
- [ ] 6.12 Verify zero-dependency operation for Milestones 1-2
- [ ] 6.13 Verify optional dependency handling for Milestone 3 (websockets)
- [ ] 6.14 Perform end-to-end testing with real aria2 daemon
- [ ] 6.15 Test all three milestones sequentially with real aria2

## 7. Documentation and Examples

- [ ] 7.1 Complete SKILL.md with full API reference (all milestones)
- [ ] 7.2 Add configuration examples (assets/config.json, environment variables)
- [ ] 7.3 Add usage examples for all RPC methods (Milestones 1-3)
- [ ] 7.4 Add troubleshooting section for common issues
- [ ] 7.5 Add security best practices documentation
- [ ] 7.6 Add milestone rollout guide (when to use which milestone)
- [ ] 7.7 Add examples of natural language commands (organized by milestone)
- [ ] 7.8 Add example scripts in scripts/ for common workflows
- [ ] 7.9 Document error messages and solutions
- [ ] 7.10 Add testing documentation (how to run unit tests, integration tests)
- [ ] 7.11 Document test report interpretation
- [ ] 7.12 Add contribution guidelines (if applicable)

## 8. Final Integration and Deployment

- [ ] 8.1 Register skill in OpenCode agent framework
- [ ] 8.2 Verify skill loading and initialization (SKILL.md + assets/ + scripts/ + references/)
- [ ] 8.3 Test skill integration with agent command parser
- [ ] 8.4 Run full test suite before deployment (unit + integration)
- [ ] 8.5 Run linting and code quality checks
- [ ] 8.6 Update project README with skill information
- [ ] 8.7 Create release notes for Milestone 1
- [ ] 8.8 Create release notes for Milestone 2
- [ ] 8.9 Create release notes for Milestone 3
- [ ] 8.10 Prepare deployment package and documentation
- [ ] 8.11 Verify rollback capability between milestones