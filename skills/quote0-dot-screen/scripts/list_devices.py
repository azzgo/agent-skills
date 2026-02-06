#!/usr/bin/env python3
"""
Get Quote/0 device list.

Usage:
    python list_devices.py
"""

import sys
import os
import requests
import json


def list_devices():
    """
    Get list of all Quote/0 devices.

    Returns:
        List of devices with their information
    """
    api_key = os.environ.get("DOT_API_KEY")
    if not api_key:
        print("Error: DOT_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it with: export DOT_API_KEY=your_api_key", file=sys.stderr)
        sys.exit(1)

    url = "https://api.mindreset.tech/api/quotes"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    result = list_devices()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
