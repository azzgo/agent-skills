#!/usr/bin/env python3
"""
List tasks on a Quote/0 device.

Usage:
    python list_tasks.py <device_id>
"""

import sys
import os
import requests
import argparse
import json


def list_tasks(device_id: str):
    """
    Get list of content tasks on a Quote/0 device.

    Args:
        device_id: The device serial number

    Returns:
        List of device tasks
    """
    api_key = os.environ.get("DOT_API_KEY")
    if not api_key:
        print("Error: DOT_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it with: export DOT_API_KEY=your_api_key", file=sys.stderr)
        sys.exit(1)

    url = f"https://api.mindreset.tech/api/quotes/{device_id}/tasks"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="List tasks on Quote/0 device")
    parser.add_argument("device_id", help="Device serial number")

    args = parser.parse_args()

    result = list_tasks(args.device_id)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
