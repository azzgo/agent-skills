#!/usr/bin/env python3
"""
Get Quote/0 device list.

Usage:
    python list_devices.py [--format json|markdown]
"""

import json
import argparse
from api_client import api_request, format_as_markdown_list


DEVICE_FIELDS = ["id", "series", "model", "edition"]
DEVICE_FIELD_LABELS = ["Serial Number", "Series", "Model", "Edition"]


def list_devices():
    """
    Get list of all Quote/0 devices.

    Returns:
        List of devices with their information
    """
    return api_request("/open/devices")


def format_as_markdown(devices):
    """
    Format devices list as markdown list.

    Args:
        devices: List list of device dictionaries

    Returns:
        Markdown formatted string
    """
    return format_as_markdown_list(
        devices,
        DEVICE_FIELDS,
        field_labels=DEVICE_FIELD_LABELS,
        empty_message="No devices found."
    )


def main():
    parser = argparse.ArgumentParser(description="Get Quote/0 device list")
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    args = parser.parse_args()

    result = list_devices()

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(format_as_markdown(result))


if __name__ == "__main__":
    main()
