#!/usr/bin/env python3
"""
OpenCode Executor wrapper for Instance 1.

This module wraps the execution of aria2-json-rpc skill commands and captures
complete LLM tracing including reasoning chain, tool calls, and decision process.

Supports two modes:
1. Simulated mode: Direct execution with simulated reasoning (fast, no external deps)
2. OpenCode mode: Real OpenCode API calls with actual LLM tracing

See design.md lines 375-464 for detailed architecture.
"""

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import uuid

from .execution_record import (
    ExecutionRecord,
    ExecutionRecordBuilder,
    ExecutorSession,
    InitialContext,
    ReasoningStep,
    ToolCall,
    RPCInteraction,
)
from .config import ExecutorConfig, get_config


class OpenCodeExecutor:
    """
    Executor wrapper that runs aria2-json-rpc skill commands and captures
    full execution traces.

    Supports two modes:
    - simulated: Direct execution with simulated reasoning (default)
    - opencode: Real OpenCode API calls with actual LLM tracing
    """

    def __init__(
        self,
        skill_path: Path,
        model: str = "simulated-llm",
        enable_tracing: bool = True,
        rpc_host: str = "localhost",
        rpc_port: int = 6800,
        mode: str = "simulated",
        config: Optional[ExecutorConfig] = None,
    ):
        """
        Initialize the executor.

        Args:
            skill_path: Path to the aria2-json-rpc skill directory
            model: LLM model identifier (for metadata)
            enable_tracing: Whether to enable full LLM tracing
            rpc_host: aria2 RPC server host
            rpc_port: aria2 RPC server port
            mode: Execution mode ('simulated' or 'opencode')
            config: Optional ExecutorConfig (for OpenCode mode)
        """
        self.skill_path = skill_path
        self.model = model
        self.enable_tracing = enable_tracing
        self.instance_id = f"executor-{uuid.uuid4().hex[:8]}"
        self.rpc_host = rpc_host
        self.rpc_port = rpc_port
        self.mode = mode
        self.config = config

        # Initialize OpenCode client if needed
        self.opencode_client = None
        if self.mode == "opencode":
            if config is None:
                raise ValueError("ExecutorConfig required for OpenCode mode")

            from .opencode_client import create_executor_client

            self.opencode_client = create_executor_client(config)
            self.model = config.model.name

            # Verify OpenCode API is available
            if not self.opencode_client.health_check():
                raise ConnectionError(
                    f"OpenCode API not available at {config.api_endpoint}. "
                    "Please ensure OpenCode is running or switch to 'simulated' mode."
                )

        # Paths to skill components (for simulated mode)
        self.rpc_client = skill_path / "scripts" / "rpc_client.py"
        self.command_mapper = skill_path / "scripts" / "command_mapper.py"

        # Validate skill exists (for simulated mode)
        if self.mode == "simulated":
            if not self.rpc_client.exists():
                raise FileNotFoundError(f"RPC client not found: {self.rpc_client}")
            if not self.command_mapper.exists():
                raise FileNotFoundError(
                    f"Command mapper not found: {self.command_mapper}"
                )

    def execute(self, command: str, test_case: Dict[str, Any]) -> ExecutionRecord:
        """
        Execute a natural language command and generate execution record.

        Args:
            command: Natural language command (e.g., "download http://example.com/file.zip")
            test_case: Test case metadata including test_id, milestone, name, expected_outcome

        Returns:
            ExecutionRecord with complete execution trace
        """
        if self.mode == "opencode":
            return self._execute_opencode(command, test_case)
        else:
            return self._execute_simulated(command, test_case)

    def _execute_opencode(
        self, command: str, test_case: Dict[str, Any]
    ) -> ExecutionRecord:
        """Execute command using real OpenCode API."""
        start_time = datetime.now()

        # Initialize record builder
        builder = ExecutionRecordBuilder(
            test_id=test_case["test_id"],
            milestone=test_case["milestone"],
            test_name=test_case["name"],
            command=command,
        )

        try:
            # Call OpenCode API
            result = self.opencode_client.execute_command(
                command=command,
                skill_path=self.skill_path,
                test_case=test_case,
                rpc_host=self.rpc_host,
                rpc_port=self.rpc_port,
            )

            # Extract data from OpenCode response
            reasoning_chain = []
            for i, step in enumerate(result.get("reasoning_chain", []), 1):
                reasoning_chain.append(
                    ReasoningStep(
                        step=i,
                        thought=step.get("thought", ""),
                        tool_called=step.get("tool_called"),
                    )
                )

            tool_calls = []
            for i, tc in enumerate(result.get("tool_calls", []), 1):
                tool_calls.append(
                    ToolCall(
                        sequence=i,
                        tool=tc.get("tool", ""),
                        command=tc.get("command", ""),
                        input=tc.get("input", ""),
                        output=tc.get("output", ""),
                        success=tc.get("success", True),
                        execution_time_ms=tc.get("execution_time_ms", 0),
                    )
                )

            rpc_interactions = []
            for i, rpc in enumerate(result.get("rpc_interactions", []), 1):
                rpc_interactions.append(
                    RPCInteraction(
                        sequence=i,
                        method=rpc.get("method", ""),
                        request=rpc.get("request", {}),
                        mock_server_response=rpc.get("response", {}),
                        latency_ms=rpc.get("latency_ms", 0),
                    )
                )

            skill_output = result.get("response", "")
            error_occurred = result.get("error") is not None
            error_details = result.get("error")

            final_response = skill_output

        except Exception as e:
            # Handle OpenCode API errors
            error_occurred = True
            error_details = {
                "type": "OpenCodeAPIError",
                "message": str(e),
                "traceback": self._get_traceback(),
            }
            skill_output = f"Error calling OpenCode API: {str(e)}"
            final_response = skill_output
            reasoning_chain = []
            tool_calls = []
            rpc_interactions = []

        # Finalize timing
        end_time = datetime.now()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)

        # Build execution record
        builder.set_executor_session(
            instance_id=self.instance_id,
            model=self.model,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            duration_ms=duration_ms,
        )

        capabilities = self._get_skill_capabilities()

        builder.set_llm_tracing(
            initial_context=InitialContext(
                user_query=command,
                available_skills=["aria2-json-rpc"],
                loaded_skill="aria2-json-rpc",
                skill_capabilities=capabilities,
            ),
            reasoning_chain=reasoning_chain,
            tool_calls=tool_calls,
            final_response=final_response,
            decision_process=self._generate_decision_summary(reasoning_chain),
        )

        for interaction in rpc_interactions:
            builder.rpc_interactions.append(interaction)

        builder.set_skill_output(skill_output)

        if error_occurred:
            builder.set_error(error_details)

        return builder.build()

    def _execute_simulated(
        self, command: str, test_case: Dict[str, Any]
    ) -> ExecutionRecord:
        """Execute command using simulated mode (original implementation)."""
        start_time = datetime.now()

        # Initialize record builder
        builder = ExecutionRecordBuilder(
            test_id=test_case["test_id"],
            milestone=test_case["milestone"],
            test_name=test_case["name"],
            command=command,
        )

        # Step 1: Parse natural language command to aria2 method
        reasoning_chain = []
        tool_calls = []
        rpc_interactions = []

        try:
            # Simulate initial reasoning
            reasoning_chain.append(
                ReasoningStep(
                    step=1,
                    thought=f"User command: '{command}'. Need to parse this to aria2 RPC method.",
                )
            )

            # Map command to aria2 method using command_mapper
            mapping_result = self._map_command(command)

            reasoning_chain.append(
                ReasoningStep(
                    step=2,
                    thought=f"Command mapped to aria2 method: {mapping_result['method']} with params: {mapping_result.get('params', [])}",
                )
            )

            # Step 2: Execute the RPC call
            reasoning_chain.append(
                ReasoningStep(
                    step=3,
                    thought=f"Executing RPC call to {self.rpc_host}:{self.rpc_port}",
                    tool_called={
                        "tool": "bash",
                        "command": f"python {self.rpc_client} {mapping_result['method']}",
                        "arguments": mapping_result.get("params", []),
                    },
                )
            )

            # Execute RPC client
            exec_start = time.time()
            rpc_result = self._execute_rpc_call(
                mapping_result["method"], mapping_result.get("params", [])
            )
            exec_duration = int((time.time() - exec_start) * 1000)

            # Record tool call
            tool_calls.append(
                ToolCall(
                    sequence=1,
                    tool="bash",
                    command=f"python {self.rpc_client} {mapping_result['method']}",
                    input=f"Method: {mapping_result['method']}, Params: {mapping_result.get('params', [])}",
                    output=json.dumps(rpc_result),
                    success=not rpc_result.get("error"),
                    execution_time_ms=exec_duration,
                )
            )

            # Record RPC interaction (extract from captured output if possible)
            if "request" in rpc_result and "response" in rpc_result:
                rpc_interactions.append(
                    RPCInteraction(
                        sequence=1,
                        method=mapping_result["method"],
                        request=rpc_result["request"],
                        mock_server_response=rpc_result["response"],
                        latency_ms=rpc_result.get("latency_ms", exec_duration),
                    )
                )

            # Step 3: Format response
            reasoning_chain.append(
                ReasoningStep(step=4, thought="Formatting result for user presentation")
            )

            final_response = self._format_response(mapping_result["method"], rpc_result)

            skill_output = final_response
            error_occurred = rpc_result.get("error") is not None
            error_details = rpc_result.get("error") if error_occurred else None

        except Exception as e:
            # Handle execution errors
            error_occurred = True
            error_details = {
                "type": type(e).__name__,
                "message": str(e),
                "traceback": self._get_traceback(),
            }
            skill_output = f"Error: {str(e)}"
            final_response = skill_output

            reasoning_chain.append(
                ReasoningStep(
                    step=len(reasoning_chain) + 1,
                    thought=f"Error occurred during execution: {str(e)}",
                )
            )

        # Finalize timing
        end_time = datetime.now()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)

        # Build execution record
        builder.set_executor_session(
            instance_id=self.instance_id,
            model=self.model,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            duration_ms=duration_ms,
        )

        # Get skill capabilities
        capabilities = self._get_skill_capabilities()

        builder.set_llm_tracing(
            initial_context=InitialContext(
                user_query=command,
                available_skills=["aria2-json-rpc"],
                loaded_skill="aria2-json-rpc",
                skill_capabilities=capabilities,
            ),
            reasoning_chain=reasoning_chain,
            tool_calls=tool_calls,
            final_response=final_response,
            decision_process=self._generate_decision_summary(reasoning_chain),
        )

        # Add RPC interactions
        for interaction in rpc_interactions:
            builder.rpc_interactions.append(interaction)

        builder.set_skill_output(skill_output)

        if error_occurred:
            builder.set_error(error_details)

        return builder.build()

    def _map_command(self, command: str) -> Dict[str, Any]:
        """
        Map natural language command to aria2 RPC method.

        Uses the command_mapper.py from the skill.
        """
        try:
            result = subprocess.run(
                [sys.executable, str(self.command_mapper), command],
                capture_output=True,
                text=True,
                timeout=5,
                env={
                    **subprocess.os.environ,
                    "ARIA2_RPC_HOST": self.rpc_host,
                    "ARIA2_RPC_PORT": str(self.rpc_port),
                },
            )

            if result.returncode != 0:
                raise Exception(f"Command mapping failed: {result.stderr}")

            # Parse output (assuming command_mapper returns JSON)
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            # Fallback: simple keyword-based mapping
            return self._simple_command_mapping(command)
        except Exception as e:
            raise Exception(f"Failed to map command: {str(e)}")

    def _simple_command_mapping(self, command: str) -> Dict[str, Any]:
        """Simple fallback command mapping."""
        command_lower = command.lower()

        # Extract URLs if present
        import re

        urls = re.findall(r"https?://[^\s]+", command)

        if "download" in command_lower and urls:
            return {"method": "aria2.addUri", "params": [urls]}
        elif "status" in command_lower or "query" in command_lower:
            # Extract GID if present
            gid_match = re.search(r"[0-9a-f]{16}", command)
            if gid_match:
                return {"method": "aria2.tellStatus", "params": [gid_match.group()]}
        elif "pause all" in command_lower:
            return {"method": "aria2.pauseAll", "params": []}
        elif "pause" in command_lower:
            gid_match = re.search(r"[0-9a-f]{16}", command)
            if gid_match:
                return {"method": "aria2.pause", "params": [gid_match.group()]}
        elif "resume all" in command_lower or "unpause all" in command_lower:
            return {"method": "aria2.unpauseAll", "params": []}
        elif "resume" in command_lower or "unpause" in command_lower:
            gid_match = re.search(r"[0-9a-f]{16}", command)
            if gid_match:
                return {"method": "aria2.unpause", "params": [gid_match.group()]}
        elif "remove" in command_lower or "delete" in command_lower:
            gid_match = re.search(r"[0-9a-f]{16}", command)
            if gid_match:
                return {"method": "aria2.remove", "params": [gid_match.group()]}
        elif "stats" in command_lower or "statistics" in command_lower:
            return {"method": "aria2.getGlobalStat", "params": []}
        elif "active" in command_lower or "downloading" in command_lower:
            return {"method": "aria2.tellActive", "params": []}

        raise Exception(f"Could not map command to aria2 method: {command}")

    def _execute_rpc_call(self, method: str, params: List[Any]) -> Dict[str, Any]:
        """
        Execute an aria2 RPC call via the rpc_client.py script.

        Returns a dict with the result or error.
        """
        try:
            # Build command arguments
            cmd_args = [sys.executable, str(self.rpc_client), method]

            # Add params as JSON string
            if params:
                cmd_args.append(json.dumps(params))

            # Execute
            result = subprocess.run(
                cmd_args,
                capture_output=True,
                text=True,
                timeout=10,
                env={
                    **subprocess.os.environ,
                    "ARIA2_RPC_HOST": self.rpc_host,
                    "ARIA2_RPC_PORT": str(self.rpc_port),
                },
            )

            # Parse output
            if result.returncode == 0:
                # Try to parse as JSON
                try:
                    output_data = json.loads(result.stdout)
                    return {"result": output_data, "error": None}
                except json.JSONDecodeError:
                    # Plain text output
                    return {"result": result.stdout.strip(), "error": None}
            else:
                return {
                    "result": None,
                    "error": {
                        "code": result.returncode,
                        "message": result.stderr.strip() or result.stdout.strip(),
                    },
                }
        except subprocess.TimeoutExpired:
            return {
                "result": None,
                "error": {"code": -1, "message": "RPC call timed out"},
            }
        except Exception as e:
            return {"result": None, "error": {"code": -1, "message": str(e)}}

    def _format_response(self, method: str, rpc_result: Dict[str, Any]) -> str:
        """Format RPC result for user-friendly response."""
        if rpc_result.get("error"):
            return f"Error: {rpc_result['error']['message']}"

        result = rpc_result.get("result")

        # Method-specific formatting
        if method == "aria2.addUri":
            return f"Download added successfully. GID: {result}"
        elif method == "aria2.tellStatus":
            if isinstance(result, dict):
                status = result.get("status", "unknown")
                completed = result.get("completedLength", "0")
                total = result.get("totalLength", "0")
                return f"Status: {status}, Downloaded: {completed}/{total} bytes"
            return f"Status: {result}"
        elif method == "aria2.remove":
            return f"Download removed. GID: {result}"
        elif method == "aria2.getGlobalStat":
            if isinstance(result, dict):
                active = result.get("numActive", "0")
                waiting = result.get("numWaiting", "0")
                stopped = result.get("numStopped", "0")
                return f"Active: {active}, Waiting: {waiting}, Stopped: {stopped}"
            return f"Global stats: {result}"
        elif method in ["aria2.pause", "aria2.unpause"]:
            return f"Operation successful. GID: {result}"
        elif method in ["aria2.pauseAll", "aria2.unpauseAll"]:
            return f"Batch operation successful: {result}"
        elif method == "aria2.tellActive":
            if isinstance(result, list):
                return f"Active downloads: {len(result)}"
            return f"Active downloads: {result}"
        else:
            return f"Result: {json.dumps(result)}"

    def _get_skill_capabilities(self) -> List[str]:
        """Get list of skill capabilities (aria2 methods supported)."""
        return [
            "addUri",
            "addTorrent",
            "addMetalink",
            "tellStatus",
            "tellActive",
            "tellWaiting",
            "tellStopped",
            "pause",
            "pauseAll",
            "unpause",
            "unpauseAll",
            "remove",
            "removeDownloadResult",
            "getGlobalStat",
            "getVersion",
            "getOption",
            "changeOption",
            "getGlobalOption",
            "changeGlobalOption",
            "purgeDownloadResult",
        ]

    def _generate_decision_summary(self, reasoning_chain: List[ReasoningStep]) -> str:
        """Generate a summary of the decision process."""
        steps = [step.thought for step in reasoning_chain]
        return " → ".join(steps)

    def _get_traceback(self) -> str:
        """Get current exception traceback."""
        import traceback

        return traceback.format_exc()


if __name__ == "__main__":
    # Example usage
    skill_path = (
        Path(__file__).parent.parent.parent.parent / "skills" / "aria2-json-rpc"
    )
    executor = OpenCodeExecutor(skill_path=skill_path)

    test_case = {
        "test_id": "milestone1_add_uri_001",
        "milestone": "Milestone 1",
        "name": "Add URI Download",
        "expected_outcome": "Download added with valid GID",
    }

    record = executor.execute("download http://example.com/file.zip", test_case)
    print(record.to_json())
