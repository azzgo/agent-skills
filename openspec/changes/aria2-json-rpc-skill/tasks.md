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
- [x] 1.16 Add Python unit tests for RPC client (HTTP POST, token injection, response parsing)
- [x] 1.17 Add Python unit tests for configuration module (config.json, environment variables, validation)
- [x] 1.18 Add Python unit tests for natural language mapping (command parsing, method selection)
- [x] 5.1 Create test suite directory structure: tests/unit/ and tests/integration/
- [x] 5.2 Set up Python unit test framework (unittest or pytest)
- [x] 5.3 Create test fixtures and mocks for HTTP requests (patch urllib.request)
- [x] 5.4 Create test fixtures for file system operations (config.json)
- [x] 5.5 Create test fixtures for environment variables (patch os.environ)
- [x] 5.6 Implement mock aria2 JSON-RPC server (http.server or Flask)
- [x] 5.7 Add mock server endpoints for all aria2 RPC methods (Milestones 1-3)
- [x] 5.8 Implement mock server request/response logging
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

- [x] 6.1 Run Python unit tests for Milestone 1 (isolated, no external dependencies)
- [x] 6.2 Verify all unit tests pass before proceeding to integration tests
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