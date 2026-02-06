#!/usr/bin/env python3
"""
Switch Quote/0 device to next content.

Usage:
    python switch_next.py <device_id>
"""

import sys
import os
import requests
import argparse


def switch_next(device_id: str):
    """
    Switch device to next content item.

    Args:
        device_id: The device serial number
    """
    api_key = os.environ.get("DOT_API_KEY")
    if not api_key:
        print("Error: DOT_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it with: export DOT_API_KEY=your_api_key", file=sys.stderr)
        sys.exit(1)

    url = f"https://api.mindreset.tech/api/quotes/{device_id}/next"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Switch Quote/0 device to next content"
    )
    parser.add_argument("device_id", help="Device serial number")

    args = parser.parse_args()

    result = switch_next(args.device_id)
    print("Switch: {}".format(result.get("message", "Switched successfully")))


if __name__ == "__main__":
    main()
