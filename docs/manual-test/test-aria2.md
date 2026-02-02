---
description: Run manual tests for aria2-json-rpc skill
---

Run the manual test suite for aria2-json-rpc skill.

**⚠️ CRITICAL**: This command MUST be executed from the `.manual-test/` directory!

**Test Objective:**
This test validates the complete user interaction flow - when users give natural language commands, the AI agent should understand the intent, execute the appropriate Python scripts from the skill, and format responses in a user-friendly way.

**Execution Environment:**
- **Working Directory**: `.manual-test/` (MUST be current directory)
- **Skill Location**: `.opencode/skills/aria2-json-rpc/` (relative to `.manual-test/`)
- **Configuration**: `.opencode/skills/aria2-json-rpc/config.json` (relative to `.manual-test/`)

**Prerequisites:**
1. You are currently in `.manual-test/` directory
2. aria2 daemon is running on localhost:6800
3. aria2-json-rpc skill is loaded from `.opencode/skills/aria2-json-rpc/` (relative path)
4. Configuration file `config.json` exists at `.opencode/skills/aria2-json-rpc/config.json` (relative path)

**Steps:**

1. **Verify test environment**
   - Confirm current directory is `.manual-test/`
   - Check that aria2 daemon is running on port 6800
   - Verify skill is loaded from `.opencode/skills/aria2-json-rpc/` (relative to current directory)
   - Verify configuration exists at `.opencode/skills/aria2-json-rpc/config.json` (relative to current directory)
   - **CRITICAL**: Confirm `python3` is available (not `python`) - required on macOS

2. **Read test instructions**
   - Load and read `instruct.md` for complete test instructions
   - Understand test configuration, objectives, and coverage

3. **Execute tests milestone by milestone**
   - Start with Milestone 1: Core Operations
   - For each test:
     * Receive natural language command from test instructions
     * Identify the user's intent
     * Execute the appropriate Python script using **`python3`** command (see "What Agent Should Do" in each test)
     * Format the output in a user-friendly way (convert bytes, speeds, percentages per execution-guide.md)
     * Verify results against expected outcomes
   - Proceed to Milestone 2 and 3 if Milestone 1 passes

4. **Record test results**
   - Create a timestamped result file in `results/` directory
   - Format: `timestamped_run_YYYYMMDD_HHMMSS.md`
   - For each test, record:
     * User command
     * Agent actions (which script was called with `python3`)
     * Script output (raw)
     * Agent's user-friendly response (formatted with human-readable sizes/speeds)
     * Verification results

5. **Provide summary**
   - Generate pass/fail summary per milestone
   - List critical issues encountered
   - Note any cases where agent didn't choose the right script
   - Note any cases where agent used `python` instead of `python3`
   - Check if agent properly formatted data (bytes → human-readable)
   - Provide recommendations for improvement

**Test Configuration:**
- **Working Directory**: `.manual-test/` (current directory - CRITICAL)
- **Skill Path**: `.opencode/skills/aria2-json-rpc/` (relative to `.manual-test/`)
- **Config File**: `.opencode/skills/aria2-json-rpc/config.json` (relative to `.manual-test/`)
- **Instructions**: `instruct.md` (in current directory)
- **Results Directory**: `results/` (in current directory)

**Output:**
- Test run report in `results/`
- Pass/fail summary per milestone
- Issues and recommendations
- Next steps for follow-up

**Important:**
- Test against real aria2 daemon (port 6800, secret: test-secret)
- Agent should ALWAYS use Python scripts with **`python3`** command (NOT `python`)
- Agent should NEVER manually construct JSON-RPC requests
- Agent should format data for users (bytes → KB/MB/GB, speeds with units, percentages)
- Verify each step as instructed
- Record detailed results including tool calls, script output, and formatted responses
- Don't skip verification steps
- Pause and report if any test fails