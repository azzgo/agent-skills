#!/usr/bin/env python3
"""
OpenCode API client for LLM evaluation system.

This module provides client functions to interact with real OpenCode
API endpoints for both executor and evaluator instances.
"""

import json
import requests
import time
from typing import Dict, List, Optional, Any
from pathlib import Path

from .config import ExecutorConfig, EvaluatorConfig


class OpenCodeClient:
    """Base client for OpenCode API interactions."""

    def __init__(
        self,
        api_endpoint: str,
        model_name: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        timeout: int = 60,
        auth_type: str = "none",
        auth_token: str = "",
        api_key_header: str = "X-API-Key",
    ):
        """
        Initialize OpenCode client.

        Args:
            api_endpoint: OpenCode API endpoint URL
            model_name: Model identifier
            temperature: Sampling temperature
            max_tokens: Maximum tokens for response
            timeout: Request timeout in seconds
            auth_type: Authentication type ('none', 'bearer', 'api_key')
            auth_token: Authentication token
            api_key_header: Header name for API key authentication
        """
        self.api_endpoint = api_endpoint.rstrip("/")
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.auth_type = auth_type
        self.auth_token = auth_token
        self.api_key_header = api_key_header

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers including authentication."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if self.auth_type == "bearer" and self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        elif self.auth_type == "api_key" and self.auth_token:
            headers[self.api_key_header] = self.auth_token

        return headers

    def send_message(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        enable_tracing: bool = True,
    ) -> Dict[str, Any]:
        """
        Send a message to OpenCode API and get response.

        Args:
            prompt: User prompt/message
            system_prompt: Optional system prompt
            context: Optional context information
            enable_tracing: Whether to request full LLM tracing

        Returns:
            Dictionary with response and tracing information
        """
        payload = {
            "model": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "prompt": prompt,
            "enable_tracing": enable_tracing,
        }

        if system_prompt:
            payload["system_prompt"] = system_prompt

        if context:
            payload["context"] = context

        try:
            response = requests.post(
                f"{self.api_endpoint}/v1/execute",
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            raise Exception(f"OpenCode API request timed out after {self.timeout}s")
        except requests.exceptions.ConnectionError as e:
            raise Exception(
                f"Failed to connect to OpenCode API at {self.api_endpoint}: {e}"
            )
        except requests.exceptions.HTTPError as e:
            raise Exception(f"OpenCode API returned error: {e}")
        except Exception as e:
            raise Exception(f"OpenCode API call failed: {e}")

    def health_check(self) -> bool:
        """
        Check if OpenCode API is available.

        Returns:
            True if API is healthy, False otherwise
        """
        try:
            response = requests.get(
                f"{self.api_endpoint}/health",
                headers=self._get_headers(),
                timeout=5,
            )
            return response.status_code == 200
        except:
            return False


class OpenCodeExecutorClient(OpenCodeClient):
    """Client for OpenCode executor instance (Instance 1)."""

    def __init__(self, config: ExecutorConfig):
        """
        Initialize executor client from configuration.

        Args:
            config: Executor configuration
        """
        super().__init__(
            api_endpoint=config.api_endpoint,
            model_name=config.model.name,
            temperature=config.model.temperature,
            max_tokens=config.model.max_tokens,
            timeout=config.timeout,
            auth_type=config.auth.type,
            auth_token=config.auth.token,
            api_key_header=config.auth.api_key_header,
        )
        self.enable_tracing = config.enable_tracing

    def execute_command(
        self,
        command: str,
        skill_path: Path,
        test_case: Dict[str, Any],
        rpc_host: str = "localhost",
        rpc_port: int = 6800,
    ) -> Dict[str, Any]:
        """
        Execute a natural language command with aria2-json-rpc skill.

        Args:
            command: Natural language command
            skill_path: Path to aria2-json-rpc skill
            test_case: Test case metadata
            rpc_host: aria2 RPC server host
            rpc_port: aria2 RPC server port

        Returns:
            Dictionary with execution result and tracing
        """
        # Build system prompt with skill context
        system_prompt = f"""You are an AI assistant with access to the aria2-json-rpc skill.
The skill allows you to control aria2 download manager through JSON-RPC.

Skill location: {skill_path}
RPC server: {rpc_host}:{rpc_port}

Available aria2 methods:
- aria2.addUri: Add HTTP/FTP download
- aria2.addTorrent: Add torrent download
- aria2.tellStatus: Get download status
- aria2.tellActive: Get active downloads
- aria2.pause/unpause: Pause/resume downloads
- aria2.remove: Remove download
- aria2.getGlobalStat: Get global statistics
- And more...

When the user asks you to perform download-related tasks, use the aria2-json-rpc skill
to execute the appropriate RPC methods.
"""

        # Build context
        context = {
            "test_id": test_case["test_id"],
            "milestone": test_case["milestone"],
            "test_name": test_case["name"],
            "expected_outcome": test_case.get("expected_outcome", ""),
            "skill_path": str(skill_path),
            "rpc_config": {"host": rpc_host, "port": rpc_port},
        }

        # Execute via OpenCode API
        start_time = time.time()
        response = self.send_message(
            prompt=command,
            system_prompt=system_prompt,
            context=context,
            enable_tracing=self.enable_tracing,
        )
        duration_ms = int((time.time() - start_time) * 1000)

        # Extract execution information
        result = {
            "duration_ms": duration_ms,
            "response": response.get("response", ""),
            "reasoning_chain": response.get("tracing", {}).get("reasoning_chain", []),
            "tool_calls": response.get("tracing", {}).get("tool_calls", []),
            "rpc_interactions": response.get("tracing", {}).get("rpc_interactions", []),
            "error": response.get("error"),
            "raw_response": response,
        }

        return result


class OpenCodeEvaluatorClient(OpenCodeClient):
    """Client for OpenCode evaluator instance (Instance 2)."""

    def __init__(self, config: EvaluatorConfig):
        """
        Initialize evaluator client from configuration.

        Args:
            config: Evaluator configuration
        """
        super().__init__(
            api_endpoint=config.api_endpoint,
            model_name=config.model.name,
            temperature=config.model.temperature,
            max_tokens=config.model.max_tokens,
            timeout=config.timeout,
            auth_type=config.auth.type,
            auth_token=config.auth.token,
            api_key_header=config.auth.api_key_header,
        )
        self.criteria_weights = config.criteria_weights
        self.pass_threshold = config.pass_threshold

    def evaluate_execution(
        self,
        execution_record: Dict[str, Any],
        test_case: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Evaluate an execution record.

        Args:
            execution_record: Execution record from Instance 1
            test_case: Original test case

        Returns:
            Dictionary with evaluation result
        """
        # Build evaluation prompt
        prompt = f"""You are an expert evaluator analyzing the execution of an aria2-json-rpc skill command.

TEST CASE:
- Test ID: {test_case["test_id"]}
- Milestone: {test_case["milestone"]}
- Test Name: {test_case["name"]}
- Command: {test_case["command"]}
- Expected Outcome: {test_case.get("expected_outcome", "Successful completion")}

EXECUTION RECORD:
```json
{json.dumps(execution_record, indent=2)}
```

Please evaluate this execution based on the following criteria:

1. **Task Completion** (weight: {self.criteria_weights["task_completion"]}): Did the skill complete what the user requested?
2. **RPC Correctness** (weight: {self.criteria_weights["rpc_correctness"]}): Were correct aria2 methods called with correct parameters?
3. **Reasoning Quality** (weight: {self.criteria_weights["reasoning_quality"]}): Was the LLM's decision process logical and efficient?
4. **Error Handling** (weight: {self.criteria_weights["error_handling"]}): Were errors handled appropriately?
5. **Response Quality** (weight: {self.criteria_weights["response_quality"]}): Was the final response clear and helpful?

For each criterion, provide:
- A score from 0.0 to 1.0
- Brief explanation

Then provide:
- Overall judgment: PASS or FAIL (pass threshold: {self.pass_threshold})
- Overall score (weighted average)
- Confidence level (0.0-1.0)
- List of strengths
- List of weaknesses
- If failed: root cause analysis and improvement suggestions

Please respond in the following JSON format:
```json
{{
  "judgment": {{
    "status": "PASS" or "FAIL",
    "confidence": 0.95,
    "overall_score": 0.87
  }},
  "criteria_scores": {{
    "task_completion": 0.9,
    "rpc_correctness": 0.85,
    "reasoning_quality": 0.88,
    "error_handling": 0.90,
    "response_quality": 0.85
  }},
  "criteria_explanations": {{
    "task_completion": "Explanation...",
    ...
  }},
  "strengths": ["strength 1", "strength 2"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "failure_analysis": {{
    "root_cause": "...",
    "expected_behavior": "...",
    "actual_behavior": "..."
  }},
  "improvement_suggestions": ["suggestion 1", "suggestion 2"]
}}
```
"""

        # Send evaluation request
        start_time = time.time()
        response = self.send_message(
            prompt=prompt,
            enable_tracing=False,  # Don't need tracing for evaluation
        )
        duration_ms = int((time.time() - start_time) * 1000)

        # Parse evaluation result
        try:
            # Try to extract JSON from response
            response_text = response.get("response", "")

            # Look for JSON in code blocks
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            else:
                json_text = response_text

            evaluation = json.loads(json_text)
            evaluation["duration_ms"] = duration_ms
            evaluation["raw_response"] = response

            return evaluation

        except json.JSONDecodeError as e:
            # Fallback: return error
            return {
                "error": f"Failed to parse evaluation response: {e}",
                "raw_response": response,
                "duration_ms": duration_ms,
                "judgment": {
                    "status": "FAIL",
                    "confidence": 0.0,
                    "overall_score": 0.0,
                },
            }


def create_executor_client(config: ExecutorConfig) -> OpenCodeExecutorClient:
    """
    Create executor client from configuration.

    Args:
        config: Executor configuration

    Returns:
        OpenCodeExecutorClient instance
    """
    return OpenCodeExecutorClient(config)


def create_evaluator_client(config: EvaluatorConfig) -> OpenCodeEvaluatorClient:
    """
    Create evaluator client from configuration.

    Args:
        config: Evaluator configuration

    Returns:
        OpenCodeEvaluatorClient instance
    """
    return OpenCodeEvaluatorClient(config)


if __name__ == "__main__":
    # Test client initialization
    from .config import get_config

    config = get_config()

    print("Testing OpenCode clients...")
    print(f"\nExecutor mode: {config.executor.mode}")
    print(f"Executor endpoint: {config.executor.api_endpoint}")

    if config.executor.mode == "opencode":
        executor_client = create_executor_client(config.executor)
        print(f"Executor client created")
        print(f"Health check: {executor_client.health_check()}")

    print(f"\nEvaluator mode: {config.evaluator.mode}")
    print(f"Evaluator endpoint: {config.evaluator.api_endpoint}")

    if config.evaluator.mode == "opencode":
        evaluator_client = create_evaluator_client(config.evaluator)
        print(f"Evaluator client created")
        print(f"Health check: {evaluator_client.health_check()}")
