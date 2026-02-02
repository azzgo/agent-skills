---
description: Run manual tests for aria2-json-rpc skill
---

Run the manual test suite for aria2-json-rpc skill.

**Test Objective:**
This test validates the complete user interaction flow - when users give natural language commands, the AI agent should understand the intent, execute the appropriate Python scripts from the skill, and format responses in a user-friendly way.

**Prerequisites:**
1. aria2 daemon is running on localhost:6800
2. aria2-json-rpc skill is loaded from `.opencode/skills/aria2-json-rpc/`
3. Configuration file `config.json` exists in the skill directory (`.opencode/skills/aria2-json-rpc/config.json`)

**Steps:**

1. **Verify test environment**
   - Check that aria2 daemon is running on port 6800
   - Verify configuration is loaded from `config.json` in skill directory

2. **Read test instructions**
   - Load and read `instruct.md` for complete test instructions
   - Understand test configuration, objectives, and coverage

3. **Execute tests milestone by milestone**
   - Start with Milestone 1: Core Operations
   - For each test:
     * Receive natural language command from test instructions
     * Identify the user's intent
     * Execute the appropriate Python script (see "What Agent Should Do" in each test)
     * Format the output in a user-friendly way
     * Verify results against expected outcomes
   - Proceed to Milestone 2 and 3 if Milestone 1 passes

4. **Record test results**
   - Create a timestamped result file in `results/` directory
   - Format: `timestamped_run_YYYYMMDD_HHMMSS.md`
   - For each test, record:
     * User command
     * Agent actions (which script was called)
     * Script output
     * Agent's user-friendly response
     * Verification results

5. **Provide summary**
   - Generate pass/fail summary per milestone
   - List critical issues encountered
   - Note any cases where agent didn't choose the right script
   - Provide recommendations for improvement

**Test Configuration:**
- Skill path: `.opencode/skills/aria2-json-rpc/`
- Config file: `.opencode/skills/aria2-json-rpc/config.json`
- Instructions: `instruct.md` (in current directory)
- Results directory: `results/` (in current directory)

**Output:**
- Test run report in `results/`
- Pass/fail summary per milestone
- Issues and recommendations
- Next steps for follow-up

**Important:**
- Test against real aria2 daemon (port 6800, secret: test-secret)
- Agent should ALWAYS use Python scripts, NEVER manually construct JSON-RPC
- Verify each step as instructed
- Record detailed results including tool calls, script output, and formatted responses
- Don't skip verification steps
- Pause and report if any test fails