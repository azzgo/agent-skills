#!/usr/bin/env python3
"""
Result aggregation and analysis for LLM evaluation tests.

Provides tools to analyze test results across multiple runs, identify patterns,
and generate insights for improvement.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from collections import defaultdict, Counter

from .execution_record import ExecutionRecord, load_all_records
from .evaluation_record import EvaluationRecord, TestResult, load_all_evaluations


class ResultAggregator:
    """Aggregates and analyzes test results across multiple runs."""

    def __init__(self, results_dir: Path):
        """
        Initialize the aggregator.

        Args:
            results_dir: Directory containing test results
        """
        self.results_dir = results_dir
        self.execution_records_dir = results_dir / "execution_records"
        self.evaluation_records_dir = results_dir / "evaluation_records"
        self.reports_dir = results_dir / "reports"

    def load_all_results(self) -> List[Dict[str, Any]]:
        """
        Load all test results from the results directory.

        Returns:
            List of test result dictionaries (combined exec + eval data)
        """
        # Load execution records
        execution_records = load_all_records(self.execution_records_dir)

        # Load evaluation records
        evaluation_records = load_all_evaluations(self.evaluation_records_dir)

        # Match execution and evaluation records by test_id
        results = []
        exec_by_id = {r.test_id: r for r in execution_records}
        eval_by_id = {r.test_id: r for r in evaluation_records}

        # Get all test IDs
        all_test_ids = set(exec_by_id.keys()) | set(eval_by_id.keys())

        for test_id in all_test_ids:
            exec_rec = exec_by_id.get(test_id)
            eval_rec = eval_by_id.get(test_id)

            if exec_rec and eval_rec:
                # Combine into TestResult
                result = {
                    "test_id": test_id,
                    "milestone": exec_rec.milestone,
                    "test_name": exec_rec.test_name,
                    "command": exec_rec.command,
                    "status": eval_rec.judgment.status,
                    "overall_score": eval_rec.judgment.overall_score,
                    "criteria_scores": {
                        "task_completion": eval_rec.judgment.criteria_scores.task_completion,
                        "rpc_correctness": eval_rec.judgment.criteria_scores.rpc_correctness,
                        "reasoning_quality": eval_rec.judgment.criteria_scores.reasoning_quality,
                        "error_handling": eval_rec.judgment.criteria_scores.error_handling,
                        "response_quality": eval_rec.judgment.criteria_scores.response_quality,
                    },
                    "execution_duration_ms": exec_rec.executor_session.duration_ms,
                    "evaluation_duration_ms": eval_rec.evaluator_session.duration_ms,
                    "timestamp": exec_rec.timestamp,
                }
                results.append(result)

        return results

    def aggregate_by_milestone(
        self, results: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Aggregate results by milestone.

        Returns:
            Dictionary mapping milestone to aggregated stats
        """
        milestones = defaultdict(
            lambda: {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "scores": [],
                "criteria_scores": defaultdict(list),
            }
        )

        for result in results:
            milestone = result["milestone"]
            milestones[milestone]["total"] += 1

            if result["status"] == "PASS":
                milestones[milestone]["passed"] += 1
            else:
                milestones[milestone]["failed"] += 1

            milestones[milestone]["scores"].append(result["overall_score"])

            # Collect criterion scores
            for criterion, score in result["criteria_scores"].items():
                milestones[milestone]["criteria_scores"][criterion].append(score)

        # Calculate averages
        summary = {}
        for milestone, data in milestones.items():
            avg_score = (
                sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0.0
            )

            criteria_avg = {}
            for criterion, scores in data["criteria_scores"].items():
                criteria_avg[criterion] = sum(scores) / len(scores) if scores else 0.0

            summary[milestone] = {
                "total": data["total"],
                "passed": data["passed"],
                "failed": data["failed"],
                "success_rate": (data["passed"] / data["total"] * 100)
                if data["total"] > 0
                else 0.0,
                "avg_overall_score": avg_score,
                "avg_criteria_scores": criteria_avg,
            }

        return summary

    def identify_failure_patterns(
        self, results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Identify common failure patterns across tests.

        Returns:
            List of failure patterns with frequency and examples
        """
        failed_results = [r for r in results if r["status"] == "FAIL"]

        if not failed_results:
            return []

        # Analyze failure patterns
        patterns = []

        # Pattern 1: Low task completion
        low_completion = [
            r for r in failed_results if r["criteria_scores"]["task_completion"] < 0.5
        ]
        if low_completion:
            patterns.append(
                {
                    "pattern": "Low Task Completion",
                    "count": len(low_completion),
                    "frequency": len(low_completion) / len(failed_results) * 100,
                    "description": "Tests failed due to incomplete task execution",
                    "examples": [r["test_id"] for r in low_completion[:3]],
                }
            )

        # Pattern 2: RPC incorrectness
        rpc_errors = [
            r for r in failed_results if r["criteria_scores"]["rpc_correctness"] < 0.5
        ]
        if rpc_errors:
            patterns.append(
                {
                    "pattern": "RPC Method Errors",
                    "count": len(rpc_errors),
                    "frequency": len(rpc_errors) / len(failed_results) * 100,
                    "description": "Tests failed due to incorrect RPC method usage or parameters",
                    "examples": [r["test_id"] for r in rpc_errors[:3]],
                }
            )

        # Pattern 3: Poor reasoning quality
        reasoning_issues = [
            r for r in failed_results if r["criteria_scores"]["reasoning_quality"] < 0.5
        ]
        if reasoning_issues:
            patterns.append(
                {
                    "pattern": "Poor Reasoning Quality",
                    "count": len(reasoning_issues),
                    "frequency": len(reasoning_issues) / len(failed_results) * 100,
                    "description": "Tests failed due to unclear or illogical reasoning process",
                    "examples": [r["test_id"] for r in reasoning_issues[:3]],
                }
            )

        # Sort by frequency
        patterns.sort(key=lambda p: p["frequency"], reverse=True)

        return patterns

    def identify_top_priorities(
        self, results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Identify top priority issues to fix.

        Returns:
            List of priority issues with recommendations
        """
        failed_results = [r for r in results if r["status"] == "FAIL"]

        if not failed_results:
            return []

        priorities = []

        # Priority 1: High-frequency failures in a specific milestone
        milestone_failures = defaultdict(list)
        for result in failed_results:
            milestone_failures[result["milestone"]].append(result)

        for milestone, failures in milestone_failures.items():
            if len(failures) >= 3:  # At least 3 failures in same milestone
                avg_score = sum(f["overall_score"] for f in failures) / len(failures)
                priorities.append(
                    {
                        "priority": "HIGH",
                        "category": "Milestone Failures",
                        "description": f"{milestone}: {len(failures)} tests failing (avg score: {avg_score:.2f})",
                        "recommendation": f"Review {milestone} implementation and fix systematic issues",
                        "affected_tests": [f["test_id"] for f in failures],
                    }
                )

        # Priority 2: Critical criterion failures (< 0.3)
        for criterion in ["task_completion", "rpc_correctness"]:
            critical_fails = [
                r for r in failed_results if r["criteria_scores"][criterion] < 0.3
            ]
            if critical_fails:
                priorities.append(
                    {
                        "priority": "HIGH",
                        "category": f"Critical {criterion.replace('_', ' ').title()} Failures",
                        "description": f"{len(critical_fails)} tests with very low {criterion} scores",
                        "recommendation": f"Fix fundamental issues with {criterion}",
                        "affected_tests": [f["test_id"] for f in critical_fails[:5]],
                    }
                )

        return priorities

    def generate_summary_stats(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate overall summary statistics.

        Returns:
            Dictionary with summary statistics
        """
        if not results:
            return {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "success_rate": 0.0,
                "avg_overall_score": 0.0,
                "avg_execution_time_ms": 0,
                "avg_evaluation_time_ms": 0,
            }

        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = total - passed

        avg_score = sum(r["overall_score"] for r in results) / total
        avg_exec_time = sum(r["execution_duration_ms"] for r in results) / total
        avg_eval_time = sum(r["evaluation_duration_ms"] for r in results) / total

        # Calculate criterion-specific averages
        criteria_avgs = {}
        for criterion in [
            "task_completion",
            "rpc_correctness",
            "reasoning_quality",
            "error_handling",
            "response_quality",
        ]:
            scores = [r["criteria_scores"][criterion] for r in results]
            criteria_avgs[criterion] = sum(scores) / len(scores)

        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "success_rate": (passed / total * 100) if total > 0 else 0.0,
            "avg_overall_score": avg_score,
            "avg_execution_time_ms": int(avg_exec_time),
            "avg_evaluation_time_ms": int(avg_eval_time),
            "avg_criteria_scores": criteria_avgs,
        }

    def generate_analysis_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive analysis report.

        Returns:
            Complete analysis report dictionary
        """
        results = self.load_all_results()

        return {
            "timestamp": datetime.now().isoformat(),
            "total_tests_analyzed": len(results),
            "summary": self.generate_summary_stats(results),
            "by_milestone": self.aggregate_by_milestone(results),
            "failure_patterns": self.identify_failure_patterns(results),
            "top_priorities": self.identify_top_priorities(results),
        }

    def save_analysis_report(self, filename: str = "analysis_report.json") -> Path:
        """Save analysis report to file."""
        report = self.generate_analysis_report()

        self.reports_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.reports_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        return filepath


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python aggregator.py <results_dir>")
        sys.exit(1)

    results_dir = Path(sys.argv[1])

    if not results_dir.exists():
        print(f"Error: Directory not found: {results_dir}")
        sys.exit(1)

    aggregator = ResultAggregator(results_dir)
    report_path = aggregator.save_analysis_report()

    print(f"Analysis report saved to: {report_path}")

    # Print summary
    report = aggregator.generate_analysis_report()
    summary = report["summary"]

    print(f"\nSummary:")
    print(f"  Total Tests: {summary['total_tests']}")
    print(f"  Success Rate: {summary['success_rate']:.1f}%")
    print(f"  Avg Score: {summary['avg_overall_score']:.2f}")
