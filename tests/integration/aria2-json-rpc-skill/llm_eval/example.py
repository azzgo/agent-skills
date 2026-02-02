#!/usr/bin/env python3
"""
Example: Running LLM evaluation tests

This script demonstrates how to use the LLM evaluation system
to test the aria2-json-rpc skill.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_eval.test_runner import IntegrationTestRunner, MockServerManager


def main():
    """Run a simple evaluation test example."""

    # Define test cases
    test_cases = [
        {
            "test_id": "example_add_uri",
            "milestone": "Milestone 1",
            "name": "Add URI Download Example",
            "command": "download http://example.com/file.zip",
            "expected_outcome": "Download added with valid GID",
        },
        {
            "test_id": "example_global_stat",
            "milestone": "Milestone 1",
            "name": "Get Global Stats Example",
            "command": "show global stats",
            "expected_outcome": "Global statistics displayed",
        },
    ]

    # Setup paths
    skill_path = (
        Path(__file__).parent.parent.parent.parent / "skills" / "aria2-json-rpc"
    )
    output_dir = Path(__file__).parent.parent / "results_example"

    print("=" * 60)
    print("LLM Evaluation System - Example Run")
    print("=" * 60)
    print(f"Skill Path: {skill_path}")
    print(f"Output Dir: {output_dir}")
    print(f"Test Cases: {len(test_cases)}")
    print("")

    # Create test runner
    runner = IntegrationTestRunner(
        skill_path=skill_path, output_dir=output_dir, rpc_port=6800
    )

    # Run tests with mock server
    try:
        print("Starting mock aria2 server...")
        with MockServerManager(port=6800, verbose=False):
            print("Running test suite...")
            results = runner.run_test_suite(test_cases)

            print("\n")
            runner.print_summary()

            print("\nSaving results and generating reports...")
            runner.save_results()

            print(f"\n{'=' * 60}")
            print("Example run completed successfully!")
            print(f"{'=' * 60}")
            print(f"\nCheck the results in: {output_dir}")
            print("\nGenerated files:")
            print(f"  - {output_dir}/reports/analysis_report.json")
            print(f"  - {output_dir}/reports/analysis_report.yaml")
            print(f"  - {output_dir}/reports/test_report.txt")

    except KeyboardInterrupt:
        print("\n\nExample run interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
