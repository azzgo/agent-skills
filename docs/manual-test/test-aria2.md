---
description: Run manual tests for aria2-json-rpc skill
---

Run the manual test suite for aria2-json-rpc skill.

**Prerequisites:**
1. aria2 daemon is running (check: `just manual-test-status`)
2. Test environment is set up (run: `just manual-test-setup`)
3. aria2-json-rpc skill is loaded from `.manual-test/.opencode/skills/aria2-json-rpc/`

**Steps:**

1. **Verify test environment**
   - Check that aria2 daemon is running on port 6800
   - Verify configuration is loaded from `.manual-test/config.json`

2. **Read test instructions**
   - Load and read `.manual-test/instruct.md` for complete test instructions
   - Understand test configuration and coverage

3. **Execute tests milestone by milestone**
   - Start with Milestone 1: Core Operations
   - Execute each natural language command as specified
   - Verify results against expected outcomes
   - Proceed to Milestone 2 and 3 if Milestone 1 passes

4. **Record test results**
   - Create a timestamped result file in `.manual-test/results/`
   - Format: `timestamped_run_YYYYMMDD_HHMMSS.md`
   - Include: test status, tool calls, responses, verification results

5. **Provide summary**
   - Generate pass/fail summary per milestone
   - List critical issues encountered
   - Provide recommendations for improvement

**Test Configuration:**
- Skill path: `.manual-test/.opencode/skills/aria2-json-rpc/`
- Config file: `.manual-test/config.json`
- Instructions: `.manual-test/instruct.md`
- Results directory: `.manual-test/results/`

**Output:**
- Test run report in `.manual-test/results/`
- Pass/fail summary per milestone
- Issues and recommendations
- Next steps for follow-up

**Important:**
- Test against real aria2 daemon (port 6800, secret: test-secret)
- Verify each step as instructed
- Record detailed results including tool calls and responses
- Don't skip verification steps
- Pause and report if any test fails