#!/usr/bin/env python3
"""
Comprehensive test report generation for LLM evaluation.

Generates reports in two formats:
1. Structured format (JSON/YAML) for programmatic access
2. Concise text format optimized for LLM evaluator consumption
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from .aggregator import ResultAggregator


class ReportGenerator:
    """Generates comprehensive test reports in structured and text formats."""

    def __init__(self, results_dir: Path):
        """
        Initialize the report generator.

        Args:
            results_dir: Directory containing test results
        """
        self.results_dir = results_dir
        self.reports_dir = results_dir / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        self.aggregator = ResultAggregator(results_dir)

    def generate_concise_text_report(self, analysis: Dict[str, Any]) -> str:
        """
        Generate a concise text report optimized for LLM evaluator consumption.

        Focuses on essential information without redundant formatting.

        Args:
            analysis: Analysis report from aggregator

        Returns:
            Concise text formatted report string
        """
        lines = []

        # Header
        lines.append("=== LLM EVALUATION TEST REPORT ===")
        lines.append(f"Generated: {analysis['timestamp']}")
        lines.append(f"Total Tests: {analysis['total_tests_analyzed']}")
        lines.append("")

        # Summary
        summary = analysis["summary"]
        lines.append("SUMMARY")
        lines.append(
            f"Tests: {summary['total_tests']} total, {summary['passed']} passed, {summary['failed']} failed"
        )
        lines.append(f"Success Rate: {summary['success_rate']:.1f}%")
        lines.append(f"Average Score: {summary['avg_overall_score']:.2f}")
        lines.append(f"Average Execution Time: {summary['avg_execution_time_ms']}ms")
        lines.append(f"Average Evaluation Time: {summary['avg_evaluation_time_ms']}ms")
        lines.append("")

        # Criteria scores
        lines.append("CRITERIA SCORES (Average)")
        for criterion, score in summary["avg_criteria_scores"].items():
            criterion_name = criterion.replace("_", " ").title()
            lines.append(f"  {criterion_name}: {score:.2f}")
        lines.append("")

        # By milestone
        lines.append("RESULTS BY MILESTONE")
        for milestone, stats in analysis["by_milestone"].items():
            lines.append(f"{milestone}:")
            lines.append(
                f"  Tests: {stats['total']} ({stats['passed']} passed, {stats['failed']} failed)"
            )
            lines.append(f"  Success Rate: {stats['success_rate']:.1f}%")
            lines.append(f"  Average Score: {stats['avg_overall_score']:.2f}")
            lines.append(f"  Criteria:")
            for criterion, score in stats["avg_criteria_scores"].items():
                criterion_name = criterion.replace("_", " ").title()
                lines.append(f"    {criterion_name}: {score:.2f}")
        lines.append("")

        # Failure patterns
        if analysis["failure_patterns"]:
            lines.append("FAILURE PATTERNS")
            for pattern in analysis["failure_patterns"]:
                lines.append(f"{pattern['pattern']}:")
                lines.append(
                    f"  Frequency: {pattern['count']} occurrences ({pattern['frequency']:.1f}%)"
                )
                lines.append(f"  Description: {pattern['description']}")
                lines.append(f"  Examples: {', '.join(pattern['examples'])}")
        else:
            lines.append("FAILURE PATTERNS")
            lines.append("No failures detected.")
        lines.append("")

        # Top priorities
        if analysis["top_priorities"]:
            lines.append("TOP PRIORITY ISSUES")
            for i, priority in enumerate(analysis["top_priorities"], 1):
                lines.append(f"{i}. [{priority['priority']}] {priority['category']}")
                lines.append(f"   Description: {priority['description']}")
                lines.append(f"   Recommendation: {priority['recommendation']}")
                lines.append(
                    f"   Affected: {', '.join(priority['affected_tests'][:3])}"
                )
                if len(priority["affected_tests"]) > 3:
                    lines.append(
                        f"   ... and {len(priority['affected_tests']) - 3} more"
                    )
        else:
            lines.append("TOP PRIORITY ISSUES")
            lines.append("No high-priority issues identified.")
        lines.append("")

        lines.append("=== END OF REPORT ===")

        return "\n".join(lines)

    def generate_yaml_report(self, analysis: Dict[str, Any]) -> str:
        """
        Generate a YAML format report.

        Args:
            analysis: Analysis report from aggregator

        Returns:
            YAML formatted report string
        """
        try:
            import yaml

            return yaml.dump(analysis, default_flow_style=False, sort_keys=False)
        except ImportError:
            # Fallback to simple YAML-like format if pyyaml not installed
            return self._simple_yaml_format(analysis)

    def _simple_yaml_format(self, data: Any, indent: int = 0) -> str:
        """Simple YAML-like formatting without pyyaml dependency."""
        lines = []
        prefix = "  " * indent

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"{prefix}{key}:")
                    lines.append(self._simple_yaml_format(value, indent + 1))
                else:
                    lines.append(f"{prefix}{key}: {value}")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    lines.append(f"{prefix}-")
                    lines.append(self._simple_yaml_format(item, indent + 1))
                else:
                    lines.append(f"{prefix}- {item}")
        else:
            return str(data)

        return "\n".join(lines)

    def generate_reports(self, formats: List[str] = None) -> Dict[str, Path]:
        """
        Generate reports in specified formats.

        Args:
            formats: List of formats to generate. Options: 'json', 'yaml', 'text'
                    If None, generates all formats.

        Returns:
            Dictionary mapping format to file path
        """
        if formats is None:
            formats = ["json", "yaml", "text"]

        # Get analysis
        analysis = self.aggregator.generate_analysis_report()

        # Generate reports
        reports = {}

        # JSON report (structured)
        if "json" in formats:
            json_path = self.reports_dir / "analysis_report.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(analysis, f, indent=2)
            reports["json"] = json_path

        # YAML report (structured)
        if "yaml" in formats:
            yaml_content = self.generate_yaml_report(analysis)
            yaml_path = self.reports_dir / "analysis_report.yaml"
            with open(yaml_path, "w", encoding="utf-8") as f:
                f.write(yaml_content)
            reports["yaml"] = yaml_path

        # Text report (concise)
        if "text" in formats:
            text_content = self.generate_concise_text_report(analysis)
            text_path = self.reports_dir / "test_report.txt"
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(text_content)
            reports["text"] = text_path

        return reports


def main():
    """CLI entry point for report generation."""
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate test reports from LLM evaluation results"
    )
    parser.add_argument(
        "results_dir", type=Path, help="Directory containing test results"
    )
    parser.add_argument(
        "--format",
        choices=["json", "yaml", "text", "all"],
        default="all",
        help="Report format (default: all)",
    )

    args = parser.parse_args()

    if not args.results_dir.exists():
        print(f"Error: Directory not found: {args.results_dir}")
        sys.exit(1)

    generator = ReportGenerator(args.results_dir)

    if args.format == "all":
        reports = generator.generate_reports()
        print("Reports generated:")
        for fmt, path in reports.items():
            print(f"  {fmt.upper()}: {path}")
    else:
        # Generate specific format
        reports = generator.generate_reports(formats=[args.format])
        path = reports[args.format]
        print(f"Report generated: {path}")


if __name__ == "__main__":
    main()
