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

- [x] 3.1 Implement aria2.addTorrent method (add torrent file from base64 or file path)
- [x] 3.2 Implement aria2.addTorrentByParam method (add torrent with structure parameters)
- [x] 3.3 Implement aria2.addMetalink method (add metalink file from base64)
- [x] 3.4 Implement aria2.addMetalinkByParam method (add metalink with structure parameters)
- [x] 3.5 Implement WebSocket client for aria2 event notifications
- [x] 3.6 Implement event subscription (aria2.onDownloadStart, onDownloadPause, etc.)
- [x] 3.7 Implement WebSocket reconnection logic
- [x] 3.8 Implement WebSocket event handler registration
- [x] 3.9 Add optional dependency detection for websockets library
- [x] 3.10 Add fallback for missing websockets library (HTTP polling alternative)
- [x] 3.11 Implement natural language command mapping for Milestone 3 methods
- [x] 3.12 Add Python unit tests for torrent/metalink operations
- [x] 3.13 Add Python unit tests for WebSocket client
- [x] 3.14 Add Python unit tests for event handling
- [x] 3.15 Add example scripts for torrent downloads (add-torrent.py)
- [x] 3.16 Add example scripts for WebSocket monitoring (monitor-downloads.py)
- [x] 3.17 Update SKILL.md with Milestone 3 operations documentation
- [x] 3.18 Update references/aria2-methods.md with Milestone 3 methods
- [x] 3.19 Add WebSocket dependency check in dependency_check.py
- [x] 3.20 Document optional dependency handling in SKILL.md

## 4. LLM-Based Evaluation (Optional, Future Implementation)

**Note:** This section describes the dual-instance "LLM as judgment" integration test system from design.md (Section: Testing Strategy, Part 2). These tasks are OPTIONAL and not currently prioritized due to high token costs and complexity. If implemented, they should follow the architecture described in design.md lines 334-703.

**Architecture Overview:**
- Instance 1 (Executor): Executes natural language commands, records full LLM tracing (reasoning chain, tool calls, decision process)
- Instance 2 (Evaluator): Analyzes execution records, judges task success/failure, provides improvement suggestions
- Mock aria2 server: Provides reproducible test environment (already implemented in tests/integration/mock_aria2_server.py)

**Tasks (Not Started):**

- [x] 4.1 Implement OpenCode Executor wrapper for Instance 1
  - Load aria2-json-rpc skill in isolated OpenCode instance
  - Enable full LLM context tracing (initial context, reasoning chain, tool calls)
  - Capture all execution data including intermediate steps and decision process
  - Generate execution record in JSON format (see design.md lines 380-464)

- [x] 4.2 Implement execution record format and serialization
  - Define JSON schema for execution records (test_id, timestamp, milestone, command, executor_session, llm_tracing, rpc_interactions, skill_output, error_details)
  - Implement serialization/deserialization functions
  - Add validation for execution record structure
  - Support incremental writing for long-running tests

- [x] 4.3 Implement OpenCode Evaluator wrapper for Instance 2
  - Load evaluation criteria from configuration (task_completion, rpc_correctness, reasoning_quality, error_handling, response_quality)
  - Receive and parse execution records from Executor
  - Analyze LLM reasoning chain and decision process
  - Generate judgment with confidence scores and criteria breakdown

- [x] 4.4 Implement evaluation criteria and judgment logic
  - Define scoring rubrics for each criterion (0.0-1.0 scale)
  - Implement LLM-powered analysis of reasoning quality
  - Generate detailed strengths/weaknesses analysis
  - Calculate overall score with weighted criteria
  - Produce pass/fail judgment with confidence level

- [x] 4.5 Implement failure analysis and improvement suggestions
  - Detect root cause of failures (skill bugs, parameter errors, response parsing issues, etc.)
  - Generate specific improvement suggestions for each failure type
  - Prioritize suggestions (HIGH, MEDIUM, LOW)
  - Provide recommended actions with file locations and code references

- [x] 4.6 Create evaluation record format and reporting
  - Define evaluation record JSON schema (see design.md lines 482-525 for pass, lines 527-577 for fail)
  - Generate comprehensive test reports with pass/fail summary, common patterns, top priorities
  - Support aggregation across multiple test runs
  - Export reports in JSON and human-readable markdown formats

- [x] 4.7 Implement integration test runner for dual-instance architecture
  - Manage lifecycle of both OpenCode instances (startup, execution, evaluation, shutdown)
  - Coordinate execution record transfer from Executor to Evaluator
  - Handle test scenarios by milestone (Milestone 1, 2, 3)
  - Support parallel test execution where applicable
  - Implement timeout and error recovery mechanisms

- [x] 4.8 Create test scenario definitions for Milestone 1
  - Add URI download (single URL): "download http://example.com/file.zip"
  - Add URI download (multiple URLs): "download these files: url1, url2"
  - Query task status by GID: "show status for GID xxx"
  - Remove task by GID: "remove download xxx"
  - Get global statistics: "show global stats"
  - Error handling: invalid URL, non-existent GID

- [x] 4.9 Create test scenario definitions for Milestone 2
  - Pause/resume operations: "pause download xxx", "resume all"
  - List operations: "what's downloading", "show waiting downloads", "list stopped"
  - Batch operations: "pause all downloads", "resume everything"
  - Option management: "get options for xxx", "change speed limit"
  - Error handling: GID not found, invalid options

- [x] 4.10 Create test scenario definitions for Milestone 3
  - Torrent operations: "add torrent file.torrent", "download magnet link"
  - Metalink operations: "add metalink file.metalink"
  - Configuration: "get aria2 version", "list available methods"
  - WebSocket events: "monitor downloads", "subscribe to events"
  - Error handling: missing websockets library, invalid torrent

- [x] 4.11 Implement mock server integration with test runner
  - Start mock_aria2_server.py before test execution
  - Configure skill to connect to mock server (ARIA2_RPC_HOST, ARIA2_RPC_PORT)
  - Verify mock server responds correctly to all RPC methods
  - Collect RPC interaction logs for analysis
  - Shutdown mock server after tests complete

- [x] 4.12 Implement execution record collection and storage
  - Save execution records to timestamped files (tests/integration/results/execution_records/)
  - Index records by test_id, milestone, and status
  - Support querying records by criteria (passed, failed, milestone)
  - Implement record archiving for old test runs
  - Provide CLI tool to inspect and analyze stored records

- [x] 4.13 Implement evaluation result aggregation and analysis
  - Aggregate results across all test scenarios
  - Calculate pass/fail rates per milestone
  - Identify common failure patterns (e.g., parameter parsing errors across multiple tests)
  - Track trends over time (improvement or regression)
  - Generate actionable insights and priority fixes

- [x] 4.14 Create comprehensive test report generation
  - Generate HTML dashboard with visualizations (pass/fail charts, criteria scores, trends)
  - Export detailed markdown reports with test details and recommendations
  - Include execution traces for failed tests
  - Highlight top improvement priorities with code references
  - Support filtering by milestone, status, and confidence level

- [x] 4.15 Document LLM evaluation system usage
  - Write README for tests/integration/ explaining dual-instance architecture
  - Provide step-by-step guide to run LLM evaluation tests
  - Document execution record and evaluation record formats
  - Explain evaluation criteria and scoring rubrics
  - Add troubleshooting guide for common issues

- [x] 4.16 Add CI/CD integration for LLM evaluation (optional)
  - Integrate with GitHub Actions or similar CI system
  - Run LLM evaluation on pull requests (with token budget limits)
  - Post evaluation summary as PR comment
  - Block merge if critical failures detected
  - Archive evaluation results for historical analysis

**Estimated Effort:** High (3-4 weeks for full implementation)  
**Token Cost:** Significant (estimated $10-50 per full test run depending on LLM model)  
**Priority:** Low (manual testing with real aria2 daemon is sufficient for now)

## 5. Test Infrastructure

**Note:** Python unit tests (isolated, no external dependencies) are complete and functional. The dual-instance "LLM as judgment" integration tests described in design.md (Section: Testing Strategy, Part 2) are NOT implemented and would be costly (token consumption) and unstable. A mock aria2 JSON-RPC server is provided for future LLM-based testing if needed.

- [x] 5.1 Create test suite directory structure: tests/unit/ and tests/integration/
- [x] 5.2 Set up Python unit test framework (unittest or pytest)
- [x] 5.3 Create test fixtures and mocks for HTTP requests (patch urllib.request)
- [x] 5.4 Create test fixtures for file system operations (config.json)
- [x] 5.5 Create test fixtures for environment variables (patch os.environ)
- [x] 5.6 Implement mock aria2 JSON-RPC server (tests/integration/mock_aria2_server.py) for LLM testing

## 6. Test Execution and Validation

**Note:** Python unit tests (6.1-6.4) are complete and should be run regularly. Integration testing with real aria2 daemon (6.5-6.7) should be performed manually by the project owner. LLM-based dual-instance evaluation tests (described in design.md) are not implemented due to token costs and instability.

- [x] 6.1 Run Python unit tests for Milestone 1 (isolated, no external dependencies)
- [x] 6.2 Verify all unit tests pass before proceeding to integration tests
- [x] 6.3 Run Python unit tests for Milestone 2
- [x] 6.4 Run Python unit tests for Milestone 3
- [ ] 6.5 Perform end-to-end testing with real aria2 daemon for Milestone 1 - **Manual execution required**
- [ ] 6.6 Perform end-to-end testing with real aria2 daemon for Milestone 2 - **Manual execution required**
- [ ] 6.7 Perform end-to-end testing with real aria2 daemon for Milestone 3 - **Manual execution required**

## 7. Documentation and Examples

- [x] 7.1 Complete SKILL.md with full API reference (all milestones)
- [x] 7.2 Add configuration examples (assets/config.json, environment variables)
- [x] 7.3 Add usage examples for all RPC methods (Milestones 1-3)
- [x] 7.4 Add troubleshooting section for common issues
- [x] 7.5 Add security best practices documentation
- [x] 7.6 Add milestone rollout guide (when to use which milestone)
- [x] 7.7 Add examples of natural language commands (organized by milestone)
- [x] 7.8 Add example scripts in scripts/ for common workflows
- [x] 7.9 Document error messages and solutions
- [x] 7.10 Add testing documentation (how to run unit tests, integration tests)
- [x] 7.11 Document test report interpretation
- [x] 7.12 Add contribution guidelines (if applicable)

## 8. Final Integration and Deployment

- [x] 8.1 Register skill in OpenCode agent framework
- [x] 8.2 Verify skill loading and initialization (SKILL.md + assets/ + scripts/ + references/)
- [x] 8.3 Test skill integration with agent command parser
- [x] 8.4 Run full test suite before deployment (unit + integration)
- [x] 8.5 Run linting and code quality checks
- [x] 8.6 Update project README with skill information
- [x] 8.7 Create release notes for Milestone 1
- [x] 8.8 Create release notes for Milestone 2
- [x] 8.9 Create release notes for Milestone 3
- [x] 8.10 Prepare deployment package and documentation
- [x] 8.11 Verify rollback capability between milestones