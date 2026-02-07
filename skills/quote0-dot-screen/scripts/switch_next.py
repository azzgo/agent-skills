#!/usr/bin/env python3
"""
Switch Quote/0 device to next content.

Usage:
    python switch_next.py <device_id> [--format json|markdown]
"""

import json
import argparse
from api_client import api_request, format_as_markdown_dict


def switch_next(device_id: str):
    """
    Switch device to next content item.

    Args:
        device_id: The device serial number

    Returns:
        Switch response data
    """
    return api_request(f"/open/device/{device_id}/next", data={})


def format_as_markdown(response):
    """
    Format switch response as markdown.

    Args:
        response: Response dictionary

    Returns:
        Markdown formatted string
    """
    message = response.get('message', 'Switched successfully')
    return message


def main():
    parser = argparse.ArgumentParser(
        description="Switch Quote/0 device to next content"
    )
    parser.add_argument("device_id", help="Device serial number")
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="markdown",
        help="Output format (default: markdown)"
    )

    args = parser.parse_args()

    result = switch_next(args.device_id)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(format_as_markdown(result))


if __name__ == "__main__":
    main()
