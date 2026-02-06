#!/usr/bin/env python3
"""
Display text on Quote/0 device.

Usage:
    python display_text.py <device_id> <message> [--title <title>] [--signature <signature>] [--refresh-now]
"""

import sys
import os
import requests
import argparse


def display_text(
    device_id: str,
    message: str,
    title: str | None = None,
    signature: str | None = None,
    refresh_now: bool = True,
):
    """
    Display text on a Quote/0 device.

    Args:
        device_id: The device serial number
        message: The text content to display
        title: Optional title to display
        signature: Optional signature to display
        refresh_now: Whether to display content immediately (default: True)
    """
    api_key = os.environ.get("DOT_API_KEY")
    if not api_key:
        print("Error: DOT_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it with: export DOT_API_KEY=your_api_key", file=sys.stderr)
        sys.exit(1)

    url = f"https://dot.mindreset.tech/api/authV2/open/device/{device_id}/text"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    data: dict[str, str | bool] = {"refreshNow": refresh_now, "message": message}
    if title:
        data["title"] = title
    if signature:
        data["signature"] = signature

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Display text on Quote/0 device")
    parser.add_argument("device_id", help="Device serial number")
    parser.add_argument("message", help="Text content to display")
    parser.add_argument("--title", help="Title to display")
    parser.add_argument("--signature", help="Signature to display")
    parser.add_argument(
        "--refresh-now", action="store_true", help="Display content immediately"
    )
    parser.add_argument(
        "--no-refresh", action="store_true", help="Do not display immediately"
    )

    args = parser.parse_args()

    refresh_now = args.refresh_now and not args.no_refresh
    result = display_text(
        args.device_id, args.message, args.title, args.signature, refresh_now
    )
    print("Text: {}".format(result.get("message", "Sent successfully")))


if __name__ == "__main__":
    main()
