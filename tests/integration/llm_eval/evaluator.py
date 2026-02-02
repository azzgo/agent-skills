#!/usr/bin/env python3
"""
OpenCode Evaluator wrapper for Instance 2.

This module implements the evaluator that analyzes execution records and provides
judgment, analysis, and improvement suggestions.

Supports two modes:
1. Simulated mode: Rule-based evaluation logic (fast, no external deps)
2. OpenCode mode: Real OpenCode API calls with actual LLM evaluation

See design.md lines 466-577 for detailed architecture.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import time

from .execution_record import ExecutionRecord
from .evaluation_record import (
    EvaluationRecord,
    EvaluatorSession,
    Judgment,
    CriteriaScores,
    Analysis,
    DecisionProcessAssessment,
    FailureAnalysis,
)
from .config import EvaluatorConfig, get_config


class OpenCodeEvaluator:
    """
    Evaluator wrapper that analyzes execution records and generates judgments.

    Supports two modes:
    - simulated: Rule-based evaluation logic (default)
    - opencode: Real OpenCode API calls with actual LLM evaluation
    """

    def __init__(
        self,
        criteria_config: Optional[Dict[str, Any]] = None,
        model: str = "simulated-evaluator",
        mode: str = "simulated",
        config: Optional[EvaluatorConfig] = None,
    ):
        """
        Initialize the evaluator.

        Args:
            criteria_config: Configuration for evaluation criteria and weights
            model: LLM model identifier (for metadata)
            mode: Evaluation mode ('simulated' or 'opencode')
            config: Optional EvaluatorConfig (for OpenCode mode)
        """
        self.model = model
        self.instance_id = f"evaluator-{uuid.uuid4().hex[:8]}"
        self.mode = mode
        self.config = config

        # Default criteria weights
        self.criteria_weights = {
            "task_completion": 0.3,
            "rpc_correctness": 0.25,
            "reasoning_quality": 0.2,
            "error_handling": 0.15,
            "response_quality": 0.1,
        }

        if criteria_config:
            self.criteria_weights.update(criteria_config.get("weights", {}))

        # Initialize OpenCode client if needed
        self.opencode_client = None
        self.pass_threshold = 0.7

        if self.mode == "opencode":
            if config is None:
                raise ValueError("EvaluatorConfig required for OpenCode mode")

            from .opencode_client import create_evaluator_client

            self.opencode_client = create_evaluator_client(config)
            self.model = config.model.name
            self.criteria_weights = config.criteria_weights
            self.pass_threshold = config.pass_threshold

            # Verify OpenCode API is available
            if not self.opencode_client.health_check():
                raise ConnectionError(
                    f"OpenCode API not available at {config.api_endpoint}. "
                    "Please ensure OpenCode is running or switch to 'simulated' mode."
                )

    def evaluate(
        self, execution_record: ExecutionRecord, test_case: Dict[str, Any]
    ) -> EvaluationRecord:
        """
        Evaluate an execution record and generate evaluation.

        Args:
            execution_record: The execution record to evaluate
            test_case: Original test case with expected outcomes

        Returns:
            EvaluationRecord with judgment and analysis
        """
        if self.mode == "opencode":
            return self._evaluate_opencode(execution_record, test_case)
        else:
            return self._evaluate_simulated(execution_record, test_case)

    def _evaluate_opencode(
        self, execution_record: ExecutionRecord, test_case: Dict[str, Any]
    ) -> EvaluationRecord:
        """Evaluate using real OpenCode API."""
        start_time = datetime.now()

        try:
            # Convert execution record to dict for OpenCode API
            exec_dict = execution_record.to_dict()

            # Call OpenCode evaluator API
            result = self.opencode_client.evaluate_execution(
                execution_record=exec_dict,
                test_case=test_case,
            )

            # Parse response from OpenCode
            judgment_data = result.get("judgment", {})
            criteria_data = result.get("criteria_scores", {})

            criteria_scores = CriteriaScores(
                task_completion=criteria_data.get("task_completion", 0.0),
                rpc_correctness=criteria_data.get("rpc_correctness", 0.0),
                reasoning_quality=criteria_data.get("reasoning_quality", 0.0),
                error_handling=criteria_data.get("error_handling", 0.0),
                response_quality=criteria_data.get("response_quality", 0.0),
            )

            judgment = Judgment(
                status=judgment_data.get("status", "FAIL"),
                confidence=judgment_data.get("confidence", 0.0),
                criteria_scores=criteria_scores,
                overall_score=judgment_data.get("overall_score", 0.0),
            )

            # Extract analysis
            strengths = result.get("strengths", [])
            weaknesses = result.get("weaknesses", [])

            decision_assessment = DecisionProcessAssessment(
                logical_flow=result.get("decision_process_assessment", {}).get(
                    "logical_flow", "N/A"
                ),
                tool_usage=result.get("decision_process_assessment", {}).get(
                    "tool_usage", "N/A"
                ),
                parameter_construction=result.get(
                    "decision_process_assessment", {}
                ).get("parameter_construction", "N/A"),
                error_handling=result.get("decision_process_assessment", {}).get(
                    "error_handling", "N/A"
                ),
            )

            analysis = Analysis(
                strengths=strengths,
                weaknesses=weaknesses,
                decision_process_assessment=decision_assessment,
            )

            # Extract failure analysis if present
            failure_analysis = None
            if "failure_analysis" in result and result["failure_analysis"]:
                fa_data = result["failure_analysis"]
                failure_analysis = FailureAnalysis(
                    root_cause=fa_data.get("root_cause", "Unknown"),
                    location=fa_data.get("location"),
                    error_trace=fa_data.get("error_trace"),
                    llm_context=fa_data.get("llm_context", ""),
                    expected_behavior=fa_data.get("expected_behavior", ""),
                    actual_behavior=fa_data.get("actual_behavior", ""),
                )

            improvement_suggestions = result.get("improvement_suggestions", [])
            priority = result.get("priority")
            recommended_actions = result.get("recommended_actions")

        except Exception as e:
            # Fallback to simulated evaluation if OpenCode API fails
            print(
                f"Warning: OpenCode evaluation failed: {e}, falling back to simulated mode"
            )
            return self._evaluate_simulated(execution_record, test_case)

        # Finalize timing
        end_time = datetime.now()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)

        # Create evaluation record
        return EvaluationRecord(
            test_id=execution_record.test_id,
            evaluator_session=EvaluatorSession(
                instance_id=self.instance_id,
                model=self.model,
                evaluation_time=end_time.isoformat(),
                duration_ms=duration_ms,
            ),
            judgment=judgment,
            analysis=analysis,
            improvement_suggestions=improvement_suggestions,
            failure_analysis=failure_analysis,
            priority=priority,
            recommended_actions=recommended_actions,
        )

    def _evaluate_simulated(
        self, execution_record: ExecutionRecord, test_case: Dict[str, Any]
    ) -> EvaluationRecord:
        """Evaluate using simulated mode (original implementation)."""
        start_time = datetime.now()

        # Evaluate each criterion
        task_completion = self._evaluate_task_completion(execution_record, test_case)
        rpc_correctness = self._evaluate_rpc_correctness(execution_record, test_case)
        reasoning_quality = self._evaluate_reasoning_quality(execution_record)
        error_handling = self._evaluate_error_handling(execution_record)
        response_quality = self._evaluate_response_quality(execution_record)

        # Create criteria scores
        criteria_scores = CriteriaScores(
            task_completion=task_completion,
            rpc_correctness=rpc_correctness,
            reasoning_quality=reasoning_quality,
            error_handling=error_handling,
            response_quality=response_quality,
        )

        # Calculate overall score (weighted average)
        overall_score = (
            task_completion * self.criteria_weights["task_completion"]
            + rpc_correctness * self.criteria_weights["rpc_correctness"]
            + reasoning_quality * self.criteria_weights["reasoning_quality"]
            + error_handling * self.criteria_weights["error_handling"]
            + response_quality * self.criteria_weights["response_quality"]
        )

        # Determine pass/fail (threshold: 0.7)
        status = "PASS" if overall_score >= 0.7 else "FAIL"

        # Calculate confidence based on score distribution
        score_variance = self._calculate_score_variance(criteria_scores)
        confidence = max(0.5, min(0.99, 1.0 - score_variance))

        # Generate judgment
        judgment = Judgment(
            status=status,
            confidence=confidence,
            criteria_scores=criteria_scores,
            overall_score=overall_score,
        )

        # Analyze strengths and weaknesses
        strengths = self._identify_strengths(execution_record, criteria_scores)
        weaknesses = self._identify_weaknesses(execution_record, criteria_scores)

        # Assess decision process
        decision_assessment = self._assess_decision_process(
            execution_record, criteria_scores
        )

        # Create analysis
        analysis = Analysis(
            strengths=strengths,
            weaknesses=weaknesses,
            decision_process_assessment=decision_assessment,
        )

        # Generate failure analysis if failed
        failure_analysis = None
        improvement_suggestions = None
        priority = None
        recommended_actions = None

        if status == "FAIL":
            failure_analysis = self._analyze_failure(execution_record, test_case)
            improvement_suggestions = self._generate_improvements(
                execution_record, criteria_scores, failure_analysis
            )
            priority = self._determine_priority(criteria_scores)
            recommended_actions = self._generate_recommended_actions(
                failure_analysis, improvement_suggestions
            )

        # Finalize timing
        end_time = datetime.now()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)

        # Create evaluation record
        return EvaluationRecord(
            test_id=execution_record.test_id,
            evaluator_session=EvaluatorSession(
                instance_id=self.instance_id,
                model=self.model,
                evaluation_time=end_time.isoformat(),
                duration_ms=duration_ms,
            ),
            judgment=judgment,
            analysis=analysis,
            improvement_suggestions=improvement_suggestions,
            failure_analysis=failure_analysis,
            priority=priority,
            recommended_actions=recommended_actions,
        )

    def _evaluate_task_completion(
        self, record: ExecutionRecord, test_case: Dict[str, Any]
    ) -> float:
        """Evaluate if the task was completed successfully."""
        # If error occurred, task likely not completed
        if record.error_occurred:
            return 0.0

        # Check if output matches expected outcome pattern
        expected = test_case.get("expected_outcome", "")
        output = record.skill_output

        # Simple pattern matching
        if "valid GID" in expected.lower():
            # Check if output contains a GID (16 hex characters)
            import re

            if re.search(r"[0-9a-f]{16}", output):
                return 1.0
            return 0.3

        if "status" in expected.lower():
            if "status" in output.lower():
                return 1.0
            return 0.2

        if "success" in expected.lower():
            if "success" in output.lower() or "ok" in output.lower():
                return 1.0
            return 0.2

        # If no specific expectation, check for non-error output
        if output and "error" not in output.lower():
            return 0.8

        return 0.5

    def _evaluate_rpc_correctness(
        self, record: ExecutionRecord, test_case: Dict[str, Any]
    ) -> float:
        """Evaluate if the correct RPC methods were called with correct parameters."""
        # Check if any RPC interactions occurred
        if not record.rpc_interactions:
            # Check tool calls as fallback
            rpc_tool_calls = [
                tc for tc in record.llm_tracing.tool_calls if "rpc_client" in tc.command
            ]
            if not rpc_tool_calls:
                return 0.0

            # At least tool was called correctly
            if all(tc.success for tc in rpc_tool_calls):
                return 0.7
            return 0.3

        # Analyze RPC interactions
        score = 1.0

        for interaction in record.rpc_interactions:
            # Check if method is valid
            if not interaction.method.startswith(
                "aria2."
            ) and not interaction.method.startswith("system."):
                score *= 0.5

            # Check if response was successful
            response = interaction.mock_server_response
            if "error" in response:
                score *= 0.6
            elif "result" not in response:
                score *= 0.8

        return max(0.0, min(1.0, score))

    def _evaluate_reasoning_quality(self, record: ExecutionRecord) -> float:
        """Evaluate the quality of LLM reasoning process."""
        reasoning = record.llm_tracing.reasoning_chain

        if not reasoning:
            return 0.0

        score = 0.0

        # Check for logical progression (at least 3 steps)
        if len(reasoning) >= 3:
            score += 0.4
        elif len(reasoning) >= 2:
            score += 0.2

        # Check if reasoning mentions key concepts
        reasoning_text = " ".join([step.thought for step in reasoning])

        if "aria2" in reasoning_text.lower():
            score += 0.2

        if "rpc" in reasoning_text.lower() or "method" in reasoning_text.lower():
            score += 0.2

        # Check if tool calls align with reasoning
        tool_calls = record.llm_tracing.tool_calls
        if tool_calls and len(tool_calls) == len(
            [r for r in reasoning if r.tool_called]
        ):
            score += 0.2

        return min(1.0, score)

    def _evaluate_error_handling(self, record: ExecutionRecord) -> float:
        """Evaluate how well errors were handled."""
        # If no error occurred, check if error handling was needed
        if not record.error_occurred:
            # Check if any RPC errors occurred but were handled
            rpc_errors = [
                i for i in record.rpc_interactions if "error" in i.mock_server_response
            ]
            if not rpc_errors:
                return 1.0  # No errors, excellent

            # Errors occurred in RPC but were handled gracefully
            if "error" not in record.skill_output.lower():
                return 0.7  # Handled but not ideal
            return 0.9  # Handled and reported

        # Error occurred, check if it was handled appropriately
        if record.error_details:
            # Error was captured with details
            if "message" in record.error_details:
                return 0.6  # Captured and reported
            return 0.4  # Captured but incomplete

        return 0.2  # Error occurred but not well handled

    def _evaluate_response_quality(self, record: ExecutionRecord) -> float:
        """Evaluate the quality of the final response to the user."""
        response = record.llm_tracing.final_response

        if not response:
            return 0.0

        score = 0.5  # Base score for having a response

        # Check for clarity
        if len(response) > 10:  # Not too short
            score += 0.2

        # Check for informative content
        if any(
            keyword in response.lower()
            for keyword in ["gid", "status", "success", "active", "download"]
        ):
            score += 0.2

        # Check for error communication
        if record.error_occurred:
            if "error" in response.lower():
                score += 0.1  # Communicated error
        else:
            if "error" not in response.lower():
                score += 0.1  # No false error messages

        return min(1.0, score)

    def _calculate_score_variance(self, scores: CriteriaScores) -> float:
        """Calculate variance in criteria scores (lower = more consistent)."""
        score_list = [
            scores.task_completion,
            scores.rpc_correctness,
            scores.reasoning_quality,
            scores.error_handling,
            scores.response_quality,
        ]

        mean = sum(score_list) / len(score_list)
        variance = sum((s - mean) ** 2 for s in score_list) / len(score_list)

        return variance

    def _identify_strengths(
        self, record: ExecutionRecord, scores: CriteriaScores
    ) -> List[str]:
        """Identify strengths in the execution."""
        strengths = []

        if scores.task_completion >= 0.9:
            strengths.append("Successfully completed the requested task")

        if scores.rpc_correctness >= 0.9:
            strengths.append("Correct aria2 RPC method selection and invocation")

        if scores.reasoning_quality >= 0.8:
            strengths.append("Clear and logical reasoning process")

        if scores.response_quality >= 0.8:
            strengths.append("Provided clear and informative response")

        if not record.error_occurred:
            strengths.append("Executed without errors")

        # Check for efficient tool usage
        if len(record.llm_tracing.tool_calls) <= 2:
            strengths.append("Efficient tool usage with minimal calls")

        return strengths if strengths else ["Execution completed"]

    def _identify_weaknesses(
        self, record: ExecutionRecord, scores: CriteriaScores
    ) -> List[str]:
        """Identify weaknesses in the execution."""
        weaknesses = []

        if scores.task_completion < 0.7:
            weaknesses.append("Task was not fully completed")

        if scores.rpc_correctness < 0.7:
            weaknesses.append("Incorrect or inappropriate RPC method usage")

        if scores.reasoning_quality < 0.6:
            weaknesses.append("Reasoning process could be more structured")

        if scores.error_handling < 0.6 and record.error_occurred:
            weaknesses.append("Error handling could be improved")

        if scores.response_quality < 0.6:
            weaknesses.append("Response lacks clarity or detail")

        # Check for excessive tool calls
        if len(record.llm_tracing.tool_calls) > 5:
            weaknesses.append("Too many tool calls, could be more efficient")

        return weaknesses if weaknesses else []

    def _assess_decision_process(
        self, record: ExecutionRecord, scores: CriteriaScores
    ) -> DecisionProcessAssessment:
        """Assess the quality of decision-making process."""
        # Assess logical flow
        if scores.reasoning_quality >= 0.9:
            logical_flow = "Excellent"
        elif scores.reasoning_quality >= 0.7:
            logical_flow = "Good"
        elif scores.reasoning_quality >= 0.5:
            logical_flow = "Fair"
        else:
            logical_flow = "Poor"

        # Assess tool usage efficiency
        num_tools = len(record.llm_tracing.tool_calls)
        if num_tools <= 2:
            tool_usage = "Efficient"
        elif num_tools <= 4:
            tool_usage = "Acceptable"
        else:
            tool_usage = "Inefficient"

        # Assess parameter construction
        if scores.rpc_correctness >= 0.9:
            param_construction = "Correct"
        elif scores.rpc_correctness >= 0.6:
            param_construction = "Partial"
        else:
            param_construction = "Incorrect"

        # Assess error handling
        if not record.error_occurred:
            error_handling_assessment = "N/A"
        elif scores.error_handling >= 0.8:
            error_handling_assessment = "Excellent"
        elif scores.error_handling >= 0.6:
            error_handling_assessment = "Good"
        elif scores.error_handling >= 0.4:
            error_handling_assessment = "Fair"
        else:
            error_handling_assessment = "Poor"

        return DecisionProcessAssessment(
            logical_flow=logical_flow,
            tool_usage=tool_usage,
            parameter_construction=param_construction,
            error_handling=error_handling_assessment,
        )

    def _analyze_failure(
        self, record: ExecutionRecord, test_case: Dict[str, Any]
    ) -> FailureAnalysis:
        """Analyze why a test failed."""
        if record.error_occurred and record.error_details:
            root_cause = record.error_details.get("message", "Unknown error")
            error_trace = record.error_details.get("traceback", "")
            location = self._extract_location_from_trace(error_trace)
        else:
            root_cause = "Task not completed successfully"
            error_trace = None
            location = None

        # Determine expected vs actual behavior
        expected = test_case.get("expected_outcome", "Successful completion")
        actual = record.skill_output if record.skill_output else "No output generated"

        # Analyze LLM context
        llm_context = self._summarize_llm_context(record)

        return FailureAnalysis(
            root_cause=root_cause,
            location=location,
            error_trace=error_trace,
            llm_context=llm_context,
            expected_behavior=expected,
            actual_behavior=actual,
        )

    def _extract_location_from_trace(self, trace: Optional[str]) -> Optional[str]:
        """Extract file location from error traceback."""
        if not trace:
            return None

        import re

        # Look for file paths and line numbers in trace
        match = re.search(r'File "([^"]+)", line (\d+)', trace)
        if match:
            return f"{match.group(1)}:{match.group(2)}"

        return None

    def _summarize_llm_context(self, record: ExecutionRecord) -> str:
        """Summarize LLM decision context."""
        reasoning = record.llm_tracing.reasoning_chain
        if not reasoning:
            return "No reasoning information available"

        summary_parts = []
        summary_parts.append(f"Reasoning steps: {len(reasoning)}")
        summary_parts.append(f"Tool calls: {len(record.llm_tracing.tool_calls)}")

        if record.error_occurred:
            summary_parts.append("Error occurred during execution")

        return ", ".join(summary_parts)

    def _generate_improvements(
        self, record: ExecutionRecord, scores: CriteriaScores, failure: FailureAnalysis
    ) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []

        if scores.task_completion < 0.7:
            suggestions.append(
                "Review task completion logic and ensure all steps are executed"
            )

        if scores.rpc_correctness < 0.7:
            suggestions.append("Verify aria2 RPC method selection matches user intent")
            suggestions.append("Check parameter format and types for RPC calls")

        if scores.reasoning_quality < 0.6:
            suggestions.append("Add more structured reasoning steps before execution")

        if scores.error_handling < 0.6:
            suggestions.append("Implement better error handling and user feedback")

        if record.error_occurred:
            suggestions.append(f"Fix error: {failure.root_cause}")
            if failure.location:
                suggestions.append(f"Check code at {failure.location}")

        return suggestions

    def _determine_priority(self, scores: CriteriaScores) -> str:
        """Determine priority level for fixes."""
        if scores.task_completion < 0.3 or scores.rpc_correctness < 0.3:
            return "HIGH"
        elif scores.task_completion < 0.7 or scores.rpc_correctness < 0.7:
            return "MEDIUM"
        else:
            return "LOW"

    def _generate_recommended_actions(
        self, failure: FailureAnalysis, suggestions: List[str]
    ) -> List[str]:
        """Generate specific recommended actions."""
        actions = []

        if failure.location:
            actions.append(f"Review and fix code at {failure.location}")

        if "parameter" in failure.root_cause.lower():
            actions.append("Update parameter construction logic")

        if "method not found" in failure.root_cause.lower():
            actions.append("Verify aria2 method name spelling and availability")

        # Add test-related actions
        actions.append("Add or update unit tests for this scenario")
        actions.append("Verify with integration test before merging")

        return actions


if __name__ == "__main__":
    # Example usage
    from .execution_record import (
        ExecutionRecordBuilder,
        InitialContext,
        ReasoningStep,
        ToolCall,
    )

    # Create a sample execution record
    builder = ExecutionRecordBuilder(
        test_id="milestone1_add_uri_001",
        milestone="Milestone 1",
        test_name="Add URI Download",
        command="download http://example.com/file.zip",
    )

    # ... (build execution record)

    evaluator = OpenCodeEvaluator()
    test_case = {
        "test_id": "milestone1_add_uri_001",
        "milestone": "Milestone 1",
        "name": "Add URI Download",
        "expected_outcome": "Download added with valid GID",
    }

    # evaluation = evaluator.evaluate(execution_record, test_case)
    # print(evaluation.to_json())
