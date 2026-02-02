#!/usr/bin/env python3
"""
Merge all milestone scenario files into a single scenarios file.
"""

import json
from pathlib import Path


def merge_scenarios():
    """Merge all milestone scenario files into all_scenarios.json."""
    scenarios_dir = Path(__file__).parent

    all_scenarios = []

    # Load each milestone
    for milestone in ["milestone1", "milestone2", "milestone3"]:
        scenario_file = scenarios_dir / f"{milestone}_scenarios.json"

        if scenario_file.exists():
            with open(scenario_file, "r") as f:
                scenarios = json.load(f)
                all_scenarios.extend(scenarios)
                print(f"Loaded {len(scenarios)} scenarios from {milestone}")
        else:
            print(f"Warning: {scenario_file} not found")

    # Save merged scenarios
    output_file = scenarios_dir / "all_scenarios.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_scenarios, f, indent=2)

    print(f"\nMerged {len(all_scenarios)} total scenarios to {output_file}")

    # Print summary by milestone
    from collections import Counter

    milestone_counts = Counter(s["milestone"] for s in all_scenarios)

    print("\nScenarios by milestone:")
    for milestone, count in sorted(milestone_counts.items()):
        print(f"  {milestone}: {count}")


if __name__ == "__main__":
    merge_scenarios()
