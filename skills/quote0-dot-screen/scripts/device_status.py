#!/usr/bin/env python3
"""
Get Quote/0 device status.

Usage:
    python device_status.py <device_id>
"""

import sys
import os
import requests
import argparse
import json


def get_device_status(device_id: str):
    """
    Get status of a specific Quote/0 device.

    Args:
        device_id: The device serial number

    Returns:
        Device status information
    """
    api_key = os.environ.get("DOT_API_KEY")
    if not api_key:
        print("Error: DOT_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it with: export DOT_API_KEY=your_api_key", file=sys.stderr)
        sys.exit(1)

    url = f"https://api.mindreset.tech/api/quotes/{device_id}/status"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Get Quote/0 fancvice status")
    parser.add_argument("device_id", help="Device serial number")

    args = parser.parse_args()

    result = get_device_status(args.device_id)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
