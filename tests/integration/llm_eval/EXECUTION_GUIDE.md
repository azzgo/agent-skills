# LLM Evaluation System - Execution Guide

Quick start guide for running LLM-as-judgment tests on the aria2-json-rpc skill.

## Table of Contents

1. [Quick Start](#quick-start-5-minutes)
2. [Configuration](#configuration)
3. [Running Tests](#running-full-test-suite)
4. [Understanding Output](#understanding-the-output)
5. [OpenCode Integration](#opencode-integration)
6. [Troubleshooting](#troubleshooting)

## Quick Start (5 minutes)

### 1. Run the Example

The fastest way to see the system in action:

```bash
cd tests/integration/llm_eval
python3 example.py
```

**Expected output:**
```
============================================================
LLM Evaluation System - Example Run
============================================================
Skill Path: /path/to/skills/aria2-json-rpc
Output Dir: /path/to/results_example
Test Cases: 2

Starting mock aria2 server...
Mock aria2 server started on port 6800 (PID: 12345)
Running test suite...

============================================================
Running test: Add URI Download Example
Milestone: Milestone 1
Command: download http://example.com/file.zip
============================================================

[Executor] Executing command...
[Executor] Execution record saved: example_add_uri_20250202_120000.json
[Executor] Duration: 150ms

[Evaluator] Analyzing execution...
[Evaluator] Evaluation record saved: example_add_uri_evaluation_20250202_120000.json
[Evaluator] Duration: 200ms

============================================================
Result: PASS
Overall Score: 0.97
Confidence: 0.95
============================================================

[... test 2 output ...]

############################################################
TEST SUMMARY
############################################################
Total Tests:     2
Passed:          2 (100.0%)
Failed:          0
Avg Score:       0.96
Avg Exec Time:   160ms
Avg Eval Time:   210ms

Example run completed successfully!
============================================================

Check the results in: /path/to/results_example

Generated files:
  - /path/to/results_example/reports/analysis_report.json
  - /path/to/results_example/reports/analysis_report.yaml
  - /path/to/results_example/reports/test_report.txt
```

**Results location:** `../results_example/`

**Note:** By default, the system runs in **simulated mode** (no external dependencies). To use real OpenCode API, see [OpenCode Integration](#opencode-integration).

### 2. View the Results

```bash
# View concise text report (optimized for LLM reading)
cat ../results_example/reports/test_report.txt

# View structured JSON report
cat ../results_example/reports/analysis_report.json

# View execution record for first test
cat ../results_example/execution_records/example_add_uri_*.json
```

## Configuration

### Configuration File

The system uses `config.yaml` to manage settings for executor, evaluator, and other components.

**Location:** `tests/integration/llm_eval/config.yaml`

**Key settings:**

```yaml
# Execution mode: 'simulated' or 'opencode'
execution_mode: simulated

# Executor (Instance 1) configuration
executor:
  mode: simulated  # or 'opencode' for real OpenCode API
  api_endpoint: http://localhost:8080  # OpenCode API URL
  model:
    name: claude-3-5-sonnet-20241022
    temperature: 0.7
    max_tokens: 4096
  timeout: 60
  enable_tracing: true
  auth:
    type: none  # or 'bearer', 'api_key'
    token: ""

# Evaluator (Instance 2) configuration
evaluator:
  mode: simulated  # or 'opencode' for real OpenCode API
  api_endpoint: http://localhost:8081  # Can be different from executor
  model:
    name: claude-3-5-sonnet-20241022
    temperature: 0.3  # Lower for consistent evaluation
    max_tokens: 4096
  timeout: 60
  criteria_weights:
    task_completion: 0.30
    rpc_correctness: 0.25
    reasoning_quality: 0.20
    error_handling: 0.15
    response_quality: 0.10
  pass_threshold: 0.7
```

### Using Custom Config

Specify a custom config file:

```bash
python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --config /path/to/custom_config.yaml
```

### Configuration Modes

**Simulated Mode** (Default):
- No external dependencies
- Fast execution
- Rule-based evaluation
- Good for development and CI/CD

**OpenCode Mode**:
- Requires running OpenCode instance
- Real LLM reasoning and evaluation
- More accurate but slower
- Good for production validation

## Running Full Test Suite

### Basic Command

Run all 30 tests across all milestones:

```bash
cd tests/integration
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json
```

**Time estimate:** ~30-60 seconds for full suite  
**Token estimate:** ~15K-36K tokens (simulated LLM calls)

### Test Specific Milestone

Test only Milestone 1 (7 tests):
```bash
python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --milestone "Milestone 1"
```

Test only Milestone 2 (16 tests):
```bash
python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --milestone "Milestone 2"
```

Test only Milestone 3 (7 tests):
```bash
python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --milestone "Milestone 3"
```

### Custom Output Directory

Save results to a specific location:
```bash
python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --output-dir /path/to/custom/results
```

### Use Custom Mock Server Port

If port 6800 is in use:
```bash
python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --port 6801
```

### Use Existing Mock Server

Run mock server separately (useful for debugging):

**Terminal 1 - Start mock server:**
```bash
cd tests/integration
python3 mock_aria2_server.py --port 6800 --verbose
```

**Terminal 2 - Run tests:**
```bash
cd tests/integration
python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --no-server \
  --port 6800
```

## Understanding the Output

### Console Output During Test

```
============================================================
Running test: Add URI Download - Single URL
Milestone: Milestone 1
Command: download http://example.com/file.zip
============================================================

[Executor] Executing command...
  → Executor captures full LLM reasoning trace
[Executor] Execution record saved: milestone1_add_uri_001_20250202_120000.json
[Executor] Duration: 150ms

[Evaluator] Analyzing execution...
  → Evaluator judges quality using 5 criteria
[Evaluator] Evaluation record saved: milestone1_add_uri_001_evaluation_20250202_120000.json
[Evaluator] Duration: 200ms

============================================================
Result: PASS          ← Overall judgment
Overall Score: 0.97   ← Weighted score (0.0-1.0)
Confidence: 0.95      ← Evaluator confidence
============================================================
```

### Final Summary

```
############################################################
TEST SUMMARY
############################################################
Total Tests:     30
Passed:          28 (93.3%)  ← Pass rate
Failed:          2
Avg Score:       0.94        ← Average across all tests
Avg Exec Time:   175ms       ← Executor performance
Avg Eval Time:   220ms       ← Evaluator performance

============================================================
BY MILESTONE
============================================================

Milestone 1:
  Total:   7
  Passed:  7 (100.0%)
  Failed:  0
  Avg Score: 0.96

Milestone 2:
  Total:   16
  Passed:  15 (93.8%)
  Failed:  1
  Avg Score: 0.93

Milestone 3:
  Total:   7
  Passed:  6 (85.7%)
  Failed:  1
  Avg Score: 0.91
############################################################

Test results saved to: results/reports/test_results.json

Generated reports:
  JSON: results/reports/analysis_report.json
  YAML: results/reports/analysis_report.yaml
  TEXT: results/reports/test_report.txt
```

## Generated Files Explained

After running tests, you'll find:

```
results/
├── execution_records/           # One per test
│   ├── milestone1_add_uri_001_20250202_120000.json
│   └── ...
├── evaluation_records/          # One per test
│   ├── milestone1_add_uri_001_evaluation_20250202_120000.json
│   └── ...
└── reports/
    ├── test_results.json        # Raw test data
    ├── analysis_report.json     # Structured analysis (for programs)
    ├── analysis_report.yaml     # Structured analysis (human-readable)
    └── test_report.txt          # Concise text (LLM-optimized)
```

### Execution Record Format

Each execution record captures:
- Complete LLM reasoning chain (step by step)
- All tool calls made during execution
- RPC interactions with mock server
- Final output and any errors

**Example excerpt:**
```json
{
  "test_id": "milestone1_add_uri_001",
  "command": "download http://example.com/file.zip",
  "llm_tracing": {
    "reasoning_chain": [
      {
        "step": 1,
        "thought": "User wants to download a file. Need to check aria2-json-rpc skill."
      },
      {
        "step": 2,
        "thought": "aria2-json-rpc supports addUri method for HTTP downloads."
      }
    ],
    "tool_calls": [...],
    "final_response": "Download added successfully. GID: 2089b05ecca3d829"
  },
  "skill_output": "Download added successfully. GID: 2089b05ecca3d829",
  "error_occurred": false
}
```

### Evaluation Record Format

Each evaluation record provides:
- Pass/fail judgment
- Scores for 5 criteria (0.0-1.0 each)
- Overall weighted score
- Strengths and weaknesses analysis
- Improvement suggestions (if failed)

**Example excerpt:**
```json
{
  "test_id": "milestone1_add_uri_001",
  "judgment": {
    "status": "PASS",
    "confidence": 0.95,
    "criteria_scores": {
      "task_completion": 1.0,
      "rpc_correctness": 1.0,
      "reasoning_quality": 0.9,
      "error_handling": 1.0,
      "response_quality": 0.95
    },
    "overall_score": 0.97
  },
  "analysis": {
    "strengths": [
      "Correctly identified user intent (download file)",
      "Matched intent to appropriate aria2 method (addUri)"
    ],
    "weaknesses": []
  }
}
```

### Report Formats

**1. JSON Report** (`analysis_report.json`)
- Machine-readable
- Complete structured data
- For programmatic access

**2. YAML Report** (`analysis_report.yaml`)
- Human-readable structure
- Same data as JSON
- Easier to read in text editor

**3. Text Report** (`test_report.txt`)
- Concise, no formatting overhead
- Optimized for LLM consumption
- Key metrics only

**Example text report:**
```
=== LLM EVALUATION TEST REPORT ===
Generated: 2025-02-02T12:00:00Z
Total Tests: 30

SUMMARY
Tests: 30 total, 28 passed, 2 failed
Success Rate: 93.3%
Average Score: 0.94
Average Execution Time: 175ms
Average Evaluation Time: 220ms

CRITERIA SCORES (Average)
  Task Completion: 0.95
  Rpc Correctness: 0.93
  Reasoning Quality: 0.88
  Error Handling: 0.96
  Response Quality: 0.91

RESULTS BY MILESTONE
Milestone 1:
  Tests: 7 (7 passed, 0 failed)
  Success Rate: 100.0%
  Average Score: 0.96
  ...

FAILURE PATTERNS
RPC Method Errors:
  Frequency: 2 occurrences (100.0%)
  Description: Tests failed due to incorrect RPC method usage
  Examples: milestone2_changeoption_001, milestone3_addtorrent_002

TOP PRIORITY ISSUES
1. [HIGH] RPC Method Errors
   Description: 2 tests with incorrect RPC calls
   Recommendation: Review parameter construction for changeOption and addTorrent
   Affected: milestone2_changeoption_001, milestone3_addtorrent_002
```

## Evaluation Criteria

Each test is scored on 5 criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Task Completion | 30% | Did the skill complete what the user requested? |
| RPC Correctness | 25% | Were correct aria2 methods called with correct parameters? |
| Reasoning Quality | 20% | Was the LLM's decision process logical and efficient? |
| Error Handling | 15% | Were errors handled appropriately? |
| Response Quality | 10% | Was the final response clear and helpful? |

**Pass threshold:** Overall score ≥ 0.7

**Score ranges:**
- 0.9-1.0: Excellent
- 0.7-0.89: Good (passes)
- 0.5-0.69: Fair (fails)
- 0.0-0.49: Poor (fails)

## Token Cost Estimates

**Per test execution:**
- Executor: ~200-500 tokens (simulated)
- Evaluator: ~300-700 tokens (simulated)
- Total per test: ~500-1200 tokens

**Full test suite (30 tests):**
- Estimated: 15,000-36,000 tokens
- With real LLM: actual costs vary by model

**Cost control strategies:**
1. Test one milestone at a time
2. Run failed tests only (after fixing issues)
3. Use example.py for quick validation (only 2 tests)

## Generating Reports Only

If you already ran tests and just want to regenerate reports:

```bash
cd tests/integration
python3 -m llm_eval.report_generator results/
```

Generate specific format only:
```bash
# JSON only
python3 -m llm_eval.report_generator results/ --format json

# YAML only
python3 -m llm_eval.report_generator results/ --format yaml

# Text only
python3 -m llm_eval.report_generator results/ --format text
```

## Analyzing Results

### View Test Summary
```bash
cat results/reports/test_report.txt
```

### Find Failed Tests
```bash
# From JSON
jq '.tests[] | select(.status == "FAIL") | .test_id' results/reports/test_results.json

# From text report
grep -A 5 "FAILURE PATTERNS" results/reports/test_report.txt
```

### Check Specific Test Details
```bash
# Execution record
cat results/execution_records/milestone1_add_uri_001_*.json | jq '.llm_tracing'

# Evaluation record
cat results/evaluation_records/milestone1_add_uri_001_evaluation_*.json | jq '.judgment'
```

### Get Top Priorities
```bash
cat results/reports/analysis_report.json | jq '.top_priorities'
```

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'llm_eval'"

**Solution:** Run from the correct directory:
```bash
cd tests/integration  # Must be in this directory
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json
```

### Problem: "Mock server failed to start"

**Cause:** Port 6800 already in use

**Solution 1:** Use different port:
```bash
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json --port 6801
```

**Solution 2:** Kill existing process:
```bash
lsof -ti:6800 | xargs kill -9
```

### Problem: "scenarios file not found"

**Solution:** Check you're in `tests/integration/`:
```bash
pwd  # Should show: .../tests/integration
ls scenarios/all_scenarios.json  # Should exist
```

### Problem: Tests pass but score is low

**Cause:** Evaluation criteria are strict

**Review:**
1. Check execution record reasoning chain
2. Review RPC interactions
3. Verify skill output format
4. Adjust evaluator weights if needed (in `evaluator.py`)

### Problem: All tests fail

**Possible causes:**
1. Skill not properly installed at `skills/aria2-json-rpc/`
2. RPC client script missing or not executable
3. Python version < 3.6

**Check:**
```bash
# Verify skill exists
ls skills/aria2-json-rpc/scripts/rpc_client.py

# Check Python version
python3 --version  # Should be 3.6+

# Test skill directly
python3 skills/aria2-json-rpc/scripts/rpc_client.py --help
```

## Next Steps After Running Tests

### If all tests pass (success rate ≥ 90%):
1. Review the text report: `cat results/reports/test_report.txt`
2. Check any warnings or low-score criteria
3. Consider the skill validated for use

### If some tests fail (success rate < 90%):
1. Review failure patterns in the report
2. Check top priority issues
3. Examine failed test execution records
4. Fix issues in the skill code
5. Re-run failed tests to verify fixes

### Iterative testing workflow:
```bash
# 1. Run all tests
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json

# 2. Review failures
cat results/reports/test_report.txt | grep -A 10 "FAILURE PATTERNS"

# 3. Fix issues in skill code

# 4. Test specific milestone again
python3 -m llm_eval.test_runner \
  --scenarios scenarios/milestone2_scenarios.json \
  --milestone "Milestone 2"

# 5. Repeat until all pass
```

## OpenCode Integration

### Prerequisites

To use real OpenCode API integration:

1. **Running OpenCode Instance(s)**:
   - Executor instance (Instance 1) running on configured endpoint
   - Evaluator instance (Instance 2) running on configured endpoint
   - Can be same or different instances

2. **Network Access**:
   - Test runner must be able to reach OpenCode API endpoints
   - Firewall rules configured if needed

3. **Authentication** (if required):
   - API tokens or keys configured in `config.yaml`

### Setup for OpenCode Mode

**1. Configure `config.yaml`:**

```yaml
execution_mode: opencode

executor:
  mode: opencode
  api_endpoint: http://your-opencode-instance:8080
  model:
    name: claude-3-5-sonnet-20241022
  auth:
    type: bearer  # or 'api_key'
    token: "your-token-here"

evaluator:
  mode: opencode
  api_endpoint: http://your-opencode-instance:8081  # Can be same endpoint
  model:
    name: claude-3-5-sonnet-20241022
  auth:
    type: bearer
    token: "your-token-here"
```

**2. Verify OpenCode Connectivity:**

```bash
# Test configuration
cd tests/integration/llm_eval
python3 -c "from config import get_config; from opencode_client import create_executor_client, create_evaluator_client; c = get_config(); print('Executor health:', create_executor_client(c.executor).health_check()); print('Evaluator health:', create_evaluator_client(c.evaluator).health_check())"
```

**3. Run Tests with OpenCode:**

```bash
cd tests/integration
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json
```

The system will automatically use OpenCode mode based on `config.yaml`.

### Mixed Mode

You can mix modes (e.g., OpenCode executor + simulated evaluator):

```yaml
executor:
  mode: opencode
  api_endpoint: http://localhost:8080
  # ... other config

evaluator:
  mode: simulated  # Use rule-based evaluation
```

This is useful for:
- Testing executor with real LLM but fast evaluation
- Cost optimization (only executor uses LLM tokens)
- Development and debugging

### OpenCode API Specification

The system expects OpenCode API endpoints to support:

**Executor Endpoint:** `POST /v1/execute`
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "temperature": 0.7,
  "max_tokens": 4096,
  "prompt": "user command here",
  "system_prompt": "system instructions",
  "context": {"test_id": "...", "skill_path": "..."},
  "enable_tracing": true
}
```

**Expected Response:**
```json
{
  "response": "execution output",
  "tracing": {
    "reasoning_chain": [...],
    "tool_calls": [...],
    "rpc_interactions": [...]
  },
  "error": null
}
```

**Evaluator Endpoint:** `POST /v1/execute`
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "prompt": "evaluation prompt with execution record",
  "enable_tracing": false
}
```

**Expected Response:**
```json
{
  "response": "{\n  \"judgment\": {...},\n  \"criteria_scores\": {...},\n  ...\n}"
}
```

### Token Usage Tracking

When using OpenCode mode with real LLM:

**Estimated token usage per test:**
- Executor: 500-2000 tokens
- Evaluator: 800-3000 tokens
- **Total per test: ~1500-5000 tokens**

**Full test suite (30 tests):**
- Estimated: 45,000-150,000 tokens
- Cost depends on model pricing

**Tips to reduce costs:**
- Use simulated mode for development
- Test specific milestones only
- Use mixed mode (OpenCode executor + simulated evaluator)
- Run failed tests only after fixes

## Command Reference

```bash
# Quick test (2 tests, simulated mode)
cd tests/integration/llm_eval && python3 example.py

# Full suite (30 tests, uses config.yaml mode)
cd tests/integration
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json

# With custom config (OpenCode mode)
python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --config /path/to/opencode_config.yaml

# Single milestone
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json --milestone "Milestone 1"

# Custom output
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json --output-dir /tmp/results

# Use existing mock server
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json --no-server --port 6800

# Generate reports only
python3 -m llm_eval.report_generator results/

# View results
cat results/reports/test_report.txt              # Concise summary
cat results/reports/analysis_report.json | jq . # Full analysis
```

## Getting Help

- **Comprehensive reference**: See `README.md` in this directory
- **Architecture details**: See `IMPLEMENTATION_SUMMARY.md`
- **Test scenarios**: See `scenarios/*.json` files
- **Code examples**: See `example.py`
- **Configuration reference**: See `config.yaml` with inline comments
