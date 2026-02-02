# LLM Evaluation System Documentation

Complete guide for using the dual-instance LLM evaluation system for the aria2-json-rpc skill.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Setup](#setup)
4. [Running Tests](#running-tests)
5. [Understanding Results](#understanding-results)
6. [Test Scenarios](#test-scenarios)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Usage](#advanced-usage)

---

## Overview

The LLM evaluation system provides comprehensive testing and analysis of the aria2-json-rpc skill using a dual-instance architecture:

- **Instance 1 (Executor)**: Executes natural language commands and captures full LLM reasoning traces
- **Instance 2 (Evaluator)**: Analyzes executions and provides judgment, scoring, and improvement suggestions

This system enables:
- Automated evaluation of skill functionality across all milestones
- Deep insights into LLM decision-making processes
- Identification of failure patterns and improvement priorities
- Comprehensive reporting with actionable recommendations

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Integration Test Framework                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │   Mock JSON-RPC  │────────▶│  OpenCode        │             │
│  │   Server         │  HTTP   │  Instance 1      │             │
│  │  (Port 6800)     │◀────────│  (Executor)      │             │
│  └──────────────────┘         │  - aria2 skill   │             │
│                               │  - executes cmd  │             │
│                               └────────┬─────────┘             │
│                                        │                        │
│                                        │ Execution Record      │
│                                        │ (full tracing)        │
│                                        ▼                        │
│                               ┌──────────────────┐             │
│                               │  OpenCode        │             │
│                               │  Instance 2      │             │
│                               │  (Evaluator)     │             │
│                               │  - analyzes      │             │
│                               │  - judges        │             │
│                               │  - suggests      │             │
│                               └──────────────────┘             │
│                                        │                        │
│                                        ▼                        │
│                               ┌──────────────────┐             │
│                               │  Test Reports    │             │
│                               └──────────────────┘             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Executor** (`executor.py`): Executes skill commands with full tracing
2. **Evaluator** (`evaluator.py`): Analyzes execution and generates judgments
3. **Test Runner** (`test_runner.py`): Orchestrates execution and evaluation
4. **Mock Server** (`mock_aria2_server.py`): Provides reproducible test environment
5. **Aggregator** (`aggregator.py`): Analyzes results across test runs
6. **Report Generator** (`report_generator.py`): Creates comprehensive reports

## Setup

### Prerequisites

- Python 3.6 or higher
- aria2-json-rpc skill installed in `skills/aria2-json-rpc/`
- All skill dependencies installed

### Directory Structure

```
tests/integration/
├── llm_eval/
│   ├── __init__.py
│   ├── execution_record.py      # Execution record format
│   ├── evaluation_record.py     # Evaluation record format
│   ├── executor.py              # Executor wrapper
│   ├── evaluator.py             # Evaluator wrapper
│   ├── test_runner.py           # Test orchestration
│   ├── aggregator.py            # Result aggregation
│   └── report_generator.py      # Report generation
├── scenarios/
│   ├── milestone1_scenarios.json
│   ├── milestone2_scenarios.json
│   ├── milestone3_scenarios.json
│   ├── all_scenarios.json
│   └── merge_scenarios.py
├── results/                     # Generated test results
│   ├── execution_records/
│   ├── evaluation_records/
│   └── reports/
└── mock_aria2_server.py         # Mock aria2 RPC server
```

### Installation

No additional installation required beyond the skill dependencies.

## Running Tests

### Basic Usage

Run all tests for all milestones:

```bash
cd tests/integration
python3 -m llm_eval.test_runner --scenarios scenarios/all_scenarios.json
```

### Filter by Milestone

Run tests for a specific milestone:

```bash
python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --milestone "Milestone 1"
```

### Use Existing Mock Server

If you have the mock server already running:

```bash
# Terminal 1: Start mock server
python3 mock_aria2_server.py --port 6800 --verbose

# Terminal 2: Run tests
python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --no-server \
  --port 6800
```

### Custom Output Directory

Specify a custom output directory for results:

```bash
python3 -m llm_eval.test_runner \
  --scenarios scenarios/all_scenarios.json \
  --output-dir /path/to/results
```

### Full Command Options

```bash
python3 -m llm_eval.test_runner --help

Options:
  --skill-path PATH       Path to aria2-json-rpc skill directory
  --output-dir PATH       Output directory for test results
  --port INT              Mock server port (default: 6800)
  --milestone STR         Filter tests by milestone
  --scenarios PATH        Path to test scenarios JSON file
  --no-server             Don't start mock server
  --verbose               Verbose output
```

## Understanding Results

### Test Output

During test execution, you'll see:

```
============================================================
Running test: Add URI Download - Single URL
Milestone: Milestone 1
Command: download http://example.com/file.zip
============================================================

[Executor] Executing command...
[Executor] Execution record saved: milestone1_add_uri_001_20250202_120000.json
[Executor] Duration: 150ms

[Evaluator] Analyzing execution...
[Evaluator] Evaluation record saved: milestone1_add_uri_001_evaluation_20250202_120000.json
[Evaluator] Duration: 200ms

============================================================
Result: PASS
Overall Score: 0.97
Confidence: 0.95
============================================================
```

### Summary Statistics

At the end of a test run:

```
############################################################
TEST SUMMARY
############################################################
Total Tests:     30
Passed:          28 (93.3%)
Failed:          2
Avg Score:       0.94
Avg Exec Time:   175ms
Avg Eval Time:   220ms

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
```

### Execution Records

Execution records capture complete execution traces:

```json
{
  "test_id": "milestone1_add_uri_001",
  "timestamp": "2025-02-02T12:00:00Z",
  "milestone": "Milestone 1",
  "test_name": "Add URI Download",
  "command": "download http://example.com/file.zip",
  "executor_session": {
    "instance_id": "executor-abc123",
    "model": "simulated-llm",
    "start_time": "2025-02-02T12:00:00Z",
    "end_time": "2025-02-02T12:00:03Z",
    "duration_ms": 3000
  },
  "llm_tracing": {
    "initial_context": { ... },
    "reasoning_chain": [ ... ],
    "tool_calls": [ ... ],
    "final_response": "Download added successfully. GID: 2089b05ecca3d829",
    "decision_process": "..."
  },
  "rpc_interactions": [ ... ],
  "skill_output": "Download added successfully. GID: 2089b05ecca3d829",
  "error_occurred": false
}
```

### Evaluation Records

Evaluation records provide judgment and analysis:

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
    "strengths": [ ... ],
    "weaknesses": [ ... ],
    "decision_process_assessment": { ... }
  }
}
```

### Evaluation Criteria

Each test is scored on five criteria (0.0-1.0 scale):

1. **Task Completion** (30% weight): Did the skill complete the requested task?
2. **RPC Correctness** (25% weight): Were the correct aria2 methods called with correct parameters?
3. **Reasoning Quality** (20% weight): Was the LLM's decision process logical and efficient?
4. **Error Handling** (15% weight): Were errors handled appropriately?
5. **Response Quality** (10% weight): Was the response clear and helpful?

Overall score is a weighted average. Tests pass if score ≥ 0.7.

## Test Scenarios

### Creating Custom Scenarios

Test scenarios are defined in JSON format:

```json
[
  {
    "test_id": "custom_test_001",
    "milestone": "Milestone 1",
    "name": "Custom Test Name",
    "command": "download http://example.com/file.zip",
    "expected_outcome": "Download added with valid GID",
    "description": "Test description for documentation"
  }
]
```

### Merging Scenario Files

Use the merge script to combine multiple scenario files:

```bash
cd tests/integration/scenarios
python3 merge_scenarios.py
```

This creates `all_scenarios.json` with all milestone scenarios.

## Generating Reports

### Generate All Reports

Generate all report formats (JSON, YAML, Text):

```bash
python3 -m llm_eval.report_generator results/
```

This creates:
- `reports/analysis_report.json`: Structured data (for programmatic access)
- `reports/analysis_report.yaml`: Structured data (human-readable)
- `reports/test_report.txt`: Concise text (optimized for LLM evaluators)

### Generate Specific Format

Generate only one format:

```bash
# JSON only (structured)
python3 -m llm_eval.report_generator results/ --format json

# YAML only (structured, human-readable)
python3 -m llm_eval.report_generator results/ --format yaml

# Text only (concise, for LLM consumption)
python3 -m llm_eval.report_generator results/ --format text
```

### Report Formats

**1. Structured Formats (JSON/YAML)**
- Complete analysis data
- Machine-readable
- Suitable for further processing or integration

**2. Concise Text Format**
- Optimized for LLM evaluator consumption
- Minimal formatting overhead
- Focuses on essential information
- No redundant visual elements

### Report Contents

All formats include:
- **Summary Statistics**: Overall pass/fail rates, scores, timing
- **Results by Milestone**: Breakdown for each milestone
- **Failure Patterns**: Common patterns in failed tests
- **Top Priorities**: High-priority issues with recommendations
- **Criteria Analysis**: Scores for each evaluation criterion

### Viewing Reports

View text report directly:

```bash
cat results/reports/test_report.txt
```

Or process structured data:

```bash
# JSON
jq '.summary' results/reports/analysis_report.json

# YAML
cat results/reports/analysis_report.yaml
```

## Troubleshooting

### Mock Server Won't Start

**Problem**: Mock server fails to start

**Solutions**:
1. Check if port 6800 is already in use: `lsof -i :6800`
2. Use a different port: `--port 6801`
3. Ensure `mock_aria2_server.py` has execute permissions

### No Test Results

**Problem**: Tests run but no results are saved

**Solutions**:
1. Check `--output-dir` path is writable
2. Ensure sufficient disk space
3. Check for Python exceptions in test output

### Command Mapping Failures

**Problem**: Natural language commands fail to map to aria2 methods

**Solutions**:
1. Check `command_mapper.py` is functioning
2. Review command syntax in scenario files
3. Add fallback mappings in `executor.py::_simple_command_mapping()`

### Evaluation Scores Too Low

**Problem**: Tests pass functionally but get low scores

**Solutions**:
1. Review evaluation criteria in `evaluator.py`
2. Adjust criteria weights if needed
3. Check if execution records contain complete tracing

### Import Errors

**Problem**: `ModuleNotFoundError` when running tests

**Solutions**:
1. Run from `tests/integration/` directory
2. Use `-m` flag: `python3 -m llm_eval.test_runner`
3. Check all files in `llm_eval/` have `__init__.py`

## Advanced Usage

### Custom Evaluation Criteria

Modify `evaluator.py` to adjust evaluation logic:

```python
# In OpenCodeEvaluator.__init__()
self.criteria_weights = {
    "task_completion": 0.4,      # Increase weight
    "rpc_correctness": 0.3,      # Increase weight
    "reasoning_quality": 0.15,   # Decrease weight
    "error_handling": 0.1,
    "response_quality": 0.05
}
```

### Programmatic Usage

Use the evaluation system programmatically:

```python
from pathlib import Path
from llm_eval.test_runner import IntegrationTestRunner, MockServerManager

# Initialize
runner = IntegrationTestRunner(
    skill_path=Path("skills/aria2-json-rpc"),
    output_dir=Path("results")
)

# Load test cases
test_cases = [...]

# Run with mock server
with MockServerManager(port=6800):
    results = runner.run_test_suite(test_cases)

# Generate reports
runner.print_summary()
runner.save_results()
```

### Analyzing Historical Results

Analyze results from previous runs:

```python
from pathlib import Path
from llm_eval.aggregator import ResultAggregator

aggregator = ResultAggregator(Path("results"))
analysis = aggregator.generate_analysis_report()

print(f"Success Rate: {analysis['summary']['success_rate']:.1f}%")
print(f"Top Priorities: {len(analysis['top_priorities'])}")
```

### CI/CD Integration

Integrate into continuous integration:

```yaml
# Example GitHub Actions workflow
name: LLM Evaluation Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Run LLM Evaluation Tests
        run: |
          cd tests/integration
          python3 -m llm_eval.test_runner \
            --scenarios scenarios/milestone1_scenarios.json \
            --output-dir results
      
      - name: Generate Reports
        run: |
          python3 -m llm_eval.report_generator results/
      
      - name: Upload Reports
        uses: actions/upload-artifact@v2
        with:
          name: test-reports
          path: results/reports/
```

## Additional Resources

- **Design Document**: See `openspec/changes/aria2-json-rpc-skill/design.md` lines 334-703 for architectural details
- **Skill Documentation**: See `skills/aria2-json-rpc/SKILL.md` for skill usage
- **Test Scenarios**: See `tests/integration/scenarios/` for example test cases

## Support

For issues or questions:
1. Check this documentation
2. Review error messages and logs
3. Inspect execution and evaluation records
4. Check the design document for architectural details
