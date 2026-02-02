#!/usr/bin/env python3
"""
Integration test runner for dual-instance LLM evaluation architecture.

This module coordinates the execution and evaluation of test scenarios:
1. Start mock aria2 server
2. Run Executor (Instance 1) to execute commands
3. Run Evaluator (Instance 2) to analyze execution
4. Collect and aggregate results
5. Generate comprehensive reports

See design.md lines 579-703 for workflow details.
"""

import json
import subprocess
import sys
import time
import signal
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import threading

from .executor import OpenCodeExecutor
from .evaluator import OpenCodeEvaluator
from .execution_record import ExecutionRecord, load_all_records
from .evaluation_record import EvaluationRecord, TestResult, load_all_evaluations
from .config import get_config, Config


class MockServerManager:
    """Manages the lifecycle of the mock aria2 server."""

    def __init__(self, port: int = 6800, verbose: bool = False):
        self.port = port
        self.verbose = verbose
        self.process: Optional[subprocess.Popen] = None
        self.server_script = Path(__file__).parent.parent / "mock_aria2_server.py"

    def start(self) -> bool:
        """
        Start the mock server.

        Returns:
            True if server started successfully, False otherwise
        """
        if not self.server_script.exists():
            print(f"Error: Mock server script not found: {self.server_script}")
            return False

        try:
            args = [sys.executable, str(self.server_script), "--port", str(self.port)]
            if self.verbose:
                args.append("--verbose")

            self.process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE if not self.verbose else None,
                stderr=subprocess.PIPE if not self.verbose else None,
            )

            # Wait for server to be ready
            time.sleep(1)

            # Check if process is still running
            if self.process.poll() is not None:
                print(
                    f"Error: Mock server failed to start (exit code: {self.process.returncode})"
                )
                return False

            print(
                f"Mock aria2 server started on port {self.port} (PID: {self.process.pid})"
            )
            return True

        except Exception as e:
            print(f"Error starting mock server: {e}")
            return False

    def stop(self):
        """Stop the mock server."""
        if self.process:
            print(f"Stopping mock aria2 server (PID: {self.process.pid})")
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Server did not terminate gracefully, forcing shutdown")
                self.process.kill()
                self.process.wait()

            self.process = None

    def is_running(self) -> bool:
        """Check if the server is running."""
        return self.process is not None and self.process.poll() is None

    def __enter__(self):
        """Context manager entry."""
        if not self.start():
            raise RuntimeError("Failed to start mock server")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


class IntegrationTestRunner:
    """
    Runs integration tests using dual-instance architecture.

    Coordinates Executor and Evaluator to test the aria2-json-rpc skill
    with comprehensive LLM tracing and evaluation.
    """

    def __init__(
        self,
        skill_path: Path,
        output_dir: Path,
        rpc_host: str = "localhost",
        rpc_port: int = 6800,
        executor_model: str = "simulated-executor",
        evaluator_model: str = "simulated-evaluator",
        config: Optional[Config] = None,
    ):
        """
        Initialize the test runner.

        Args:
            skill_path: Path to aria2-json-rpc skill directory
            output_dir: Directory for test results
            rpc_host: Mock server host
            rpc_port: Mock server port
            executor_model: Model identifier for executor
            evaluator_model: Model identifier for evaluator
            config: Optional Config object (loads from config.yaml if not provided)
        """
        self.skill_path = skill_path
        self.output_dir = output_dir
        self.rpc_host = rpc_host
        self.rpc_port = rpc_port

        # Load configuration if not provided
        if config is None:
            config = get_config()
        self.config = config

        # Create output directories
        self.execution_records_dir = output_dir / "execution_records"
        self.evaluation_records_dir = output_dir / "evaluation_records"
        self.reports_dir = output_dir / "reports"

        for directory in [
            self.execution_records_dir,
            self.evaluation_records_dir,
            self.reports_dir,
        ]:
            directory.mkdir(parents=True, exist_ok=True)

        # Determine execution modes from config
        executor_mode = config.executor.mode
        evaluator_mode = config.evaluator.mode

        # Initialize executor
        if executor_mode == "opencode":
            print(
                f"Initializing executor in OpenCode mode: {config.executor.api_endpoint}"
            )
            print(f"  Model: {config.executor.model.name}")
            self.executor = OpenCodeExecutor(
                skill_path=skill_path,
                model=config.executor.model.name,
                enable_tracing=config.executor.enable_tracing,
                rpc_host=rpc_host,
                rpc_port=rpc_port,
                mode="opencode",
                config=config.executor,
            )
        else:
            print(f"Initializing executor in simulated mode")
            self.executor = OpenCodeExecutor(
                skill_path=skill_path,
                model=executor_model,
                enable_tracing=True,
                rpc_host=rpc_host,
                rpc_port=rpc_port,
                mode="simulated",
            )

        # Initialize evaluator
        if evaluator_mode == "opencode":
            print(
                f"Initializing evaluator in OpenCode mode: {config.evaluator.api_endpoint}"
            )
            print(f"  Model: {config.evaluator.model.name}")
            self.evaluator = OpenCodeEvaluator(
                model=config.evaluator.model.name,
                mode="opencode",
                config=config.evaluator,
            )
        else:
            print(f"Initializing evaluator in simulated mode")
            self.evaluator = OpenCodeEvaluator(
                model=evaluator_model,
                mode="simulated",
            )

        # Test results
        self.test_results: List[TestResult] = []

    def run_test(self, test_case: Dict[str, Any]) -> TestResult:
        """
        Run a single test case.

        Args:
            test_case: Test case definition with test_id, milestone, name,
                      command, and expected_outcome

        Returns:
            TestResult with execution and evaluation data
        """
        print(f"\n{'=' * 60}")
        print(f"Running test: {test_case['name']}")
        print(f"Milestone: {test_case['milestone']}")
        print(f"Command: {test_case['command']}")
        print(f"{'=' * 60}")

        # Step 1: Execute with Executor (Instance 1)
        print("\n[Executor] Executing command...")
        execution_record = self.executor.execute(test_case["command"], test_case)

        # Save execution record
        exec_path = execution_record.save(self.execution_records_dir)
        print(f"[Executor] Execution record saved: {exec_path.name}")
        print(f"[Executor] Duration: {execution_record.executor_session.duration_ms}ms")

        # Step 2: Evaluate with Evaluator (Instance 2)
        print("\n[Evaluator] Analyzing execution...")
        evaluation_record = self.evaluator.evaluate(execution_record, test_case)

        # Save evaluation record
        eval_path = evaluation_record.save(self.evaluation_records_dir)
        print(f"[Evaluator] Evaluation record saved: {eval_path.name}")
        print(
            f"[Evaluator] Duration: {evaluation_record.evaluator_session.duration_ms}ms"
        )

        # Display results
        print(f"\n{'=' * 60}")
        print(f"Result: {evaluation_record.judgment.status}")
        print(f"Overall Score: {evaluation_record.judgment.overall_score:.2f}")
        print(f"Confidence: {evaluation_record.judgment.confidence:.2f}")
        print(f"{'=' * 60}")

        # Create combined test result
        test_result = TestResult(
            test_id=test_case["test_id"],
            milestone=test_case["milestone"],
            test_name=test_case["name"],
            command=test_case["command"],
            execution_duration_ms=execution_record.executor_session.duration_ms,
            evaluation_duration_ms=evaluation_record.evaluator_session.duration_ms,
            status=evaluation_record.judgment.status,
            overall_score=evaluation_record.judgment.overall_score,
            criteria_scores=evaluation_record.judgment.criteria_scores,
            strengths=evaluation_record.analysis.strengths,
            weaknesses=evaluation_record.analysis.weaknesses,
            improvement_suggestions=evaluation_record.improvement_suggestions,
            failure_analysis=evaluation_record.failure_analysis,
            execution_record_path=str(exec_path),
            evaluation_record_path=str(eval_path),
        )

        self.test_results.append(test_result)
        return test_result

    def run_test_suite(
        self, test_cases: List[Dict[str, Any]], milestone_filter: Optional[str] = None
    ) -> List[TestResult]:
        """
        Run a suite of test cases.

        Args:
            test_cases: List of test case definitions
            milestone_filter: Optional milestone filter (e.g., "Milestone 1")

        Returns:
            List of TestResult instances
        """
        # Filter test cases if needed
        if milestone_filter:
            test_cases = [
                tc for tc in test_cases if tc.get("milestone") == milestone_filter
            ]

        print(f"\n{'#' * 60}")
        print(f"Starting test suite: {len(test_cases)} tests")
        if milestone_filter:
            print(f"Filter: {milestone_filter}")
        print(f"{'#' * 60}")

        # Run each test
        results = []
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest {i}/{len(test_cases)}")
            try:
                result = self.run_test(test_case)
                results.append(result)
            except Exception as e:
                print(f"ERROR: Test failed with exception: {e}")
                import traceback

                traceback.print_exc()

        return results

    def generate_summary(self) -> Dict[str, Any]:
        """
        Generate summary statistics from test results.

        Returns:
            Dictionary with summary statistics
        """
        if not self.test_results:
            return {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "success_rate": 0.0,
                "avg_score": 0.0,
                "avg_execution_time_ms": 0,
                "avg_evaluation_time_ms": 0,
            }

        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r.status == "PASS")
        failed = total - passed

        avg_score = sum(r.overall_score for r in self.test_results) / total
        avg_exec_time = sum(r.execution_duration_ms for r in self.test_results) / total
        avg_eval_time = sum(r.evaluation_duration_ms for r in self.test_results) / total

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "success_rate": (passed / total * 100) if total > 0 else 0.0,
            "avg_score": avg_score,
            "avg_execution_time_ms": int(avg_exec_time),
            "avg_evaluation_time_ms": int(avg_eval_time),
            "by_milestone": self._group_by_milestone(),
        }

    def _group_by_milestone(self) -> Dict[str, Dict[str, Any]]:
        """Group test results by milestone."""
        milestones = {}

        for result in self.test_results:
            milestone = result.milestone
            if milestone not in milestones:
                milestones[milestone] = {
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "avg_score": 0.0,
                }

            milestones[milestone]["total"] += 1
            if result.status == "PASS":
                milestones[milestone]["passed"] += 1
            else:
                milestones[milestone]["failed"] += 1

        # Calculate averages
        for milestone, stats in milestones.items():
            milestone_results = [
                r for r in self.test_results if r.milestone == milestone
            ]
            stats["avg_score"] = sum(r.overall_score for r in milestone_results) / len(
                milestone_results
            )
            stats["success_rate"] = (
                (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0.0
            )

        return milestones

    def save_results(self, filename: str = "test_results.json"):
        """Save all test results to a JSON file."""
        output_path = self.reports_dir / filename

        results_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": self.generate_summary(),
            "tests": [result.to_dict() for result in self.test_results],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results_data, f, indent=2)

        print(f"\nTest results saved to: {output_path}")

        # Also generate reports
        from .report_generator import ReportGenerator

        generator = ReportGenerator(self.output_dir)
        reports = generator.generate_reports()

        print("\nGenerated reports:")
        for fmt, path in reports.items():
            print(f"  {fmt.upper()}: {path}")

        return output_path

    def print_summary(self):
        """Print test summary to console."""
        summary = self.generate_summary()

        print(f"\n{'#' * 60}")
        print("TEST SUMMARY")
        print(f"{'#' * 60}")
        print(f"Total Tests:     {summary['total']}")
        print(f"Passed:          {summary['passed']} ({summary['success_rate']:.1f}%)")
        print(f"Failed:          {summary['failed']}")
        print(f"Avg Score:       {summary['avg_score']:.2f}")
        print(f"Avg Exec Time:   {summary['avg_execution_time_ms']}ms")
        print(f"Avg Eval Time:   {summary['avg_evaluation_time_ms']}ms")

        if summary["by_milestone"]:
            print(f"\n{'=' * 60}")
            print("BY MILESTONE")
            print(f"{'=' * 60}")
            for milestone, stats in summary["by_milestone"].items():
                print(f"\n{milestone}:")
                print(f"  Total:   {stats['total']}")
                print(f"  Passed:  {stats['passed']} ({stats['success_rate']:.1f}%)")
                print(f"  Failed:  {stats['failed']}")
                print(f"  Avg Score: {stats['avg_score']:.2f}")

        print(f"\n{'#' * 60}")


def main():
    """Main entry point for running integration tests."""
    import argparse

    parser = argparse.ArgumentParser(description="Run LLM evaluation integration tests")
    parser.add_argument(
        "--skill-path",
        type=Path,
        default=Path(__file__).parent.parent.parent.parent
        / "skills"
        / "aria2-json-rpc",
        help="Path to aria2-json-rpc skill directory",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory for test results (overrides config)",
    )
    parser.add_argument("--port", type=int, help="Mock server port (overrides config)")
    parser.add_argument(
        "--milestone", type=str, help="Filter tests by milestone (e.g., 'Milestone 1')"
    )
    parser.add_argument(
        "--scenarios", type=Path, help="Path to test scenarios JSON file"
    )
    parser.add_argument(
        "--no-server",
        action="store_true",
        help="Don't start mock server (assume it's already running)",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to config file (default: config.yaml in module directory)",
    )

    args = parser.parse_args()

    # Load configuration
    try:
        config = get_config(args.config)
        print(f"Configuration loaded successfully")
        print(f"  Executor mode: {config.executor.mode}")
        print(f"  Evaluator mode: {config.evaluator.mode}")
    except Exception as e:
        print(f"Warning: Failed to load config: {e}")
        print("Using default configuration")
        config = get_config()

    # Override config with command line args if provided
    output_dir = args.output_dir if args.output_dir else Path(config.output.base_dir)
    rpc_port = args.port if args.port else config.mock_server.port

    # Load test scenarios
    if args.scenarios:
        with open(args.scenarios, "r") as f:
            test_cases = json.load(f)
    else:
        # Use default scenarios (will be created by tasks 4.8-4.10)
        print(
            "Error: No test scenarios provided. Use --scenarios to specify test cases."
        )
        return 1

    # Create test runner
    runner = IntegrationTestRunner(
        skill_path=args.skill_path,
        output_dir=output_dir,
        rpc_port=rpc_port,
        config=config,
    )

    # Run tests with or without mock server
    try:
        if args.no_server:
            print("Using existing mock server")
            runner.run_test_suite(test_cases, milestone_filter=args.milestone)
        else:
            verbose = args.verbose or config.mock_server.verbose
            with MockServerManager(port=rpc_port, verbose=verbose):
                runner.run_test_suite(test_cases, milestone_filter=args.milestone)

        # Generate and print summary
        runner.print_summary()

        # Save results
        runner.save_results()

        return 0

    except KeyboardInterrupt:
        print("\n\nTest run interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
