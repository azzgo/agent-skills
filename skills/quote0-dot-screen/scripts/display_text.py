#!/usr/bin/env python3
"""
Display text on Quote/0 device.

Usage:
    python display_text.py <device_id> <message> [--title <title>] [--signature <signature>] [--icon <icon>] [--link <link>] [--task-key <task_key>] [--no-refresh]
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))
from api_client import api_request


def display_text(
    device_id: str,
    message: str,
    title: str | None = None,
    signature: str | None = None,
    icon: str | None = None,
    link: str | None = None,
    task_key: str | None = None,
    refresh_now: bool = True,
):
    """
    Display text on a Quote/0 device.

    Args:
        device_id: The device serial number
        message: The text content to display
        title: Optional title to display
        signature: Optional signature to display
        icon: Optional base64-encoded PNG icon data (40px×40px)
        link: Optional NFC redirect link
        task_key: Optional task key for specific Text API content
        refresh_now: Whether to display content immediately (default: True)

    Returns:
        dict: API response
    """
    endpoint = f"/open/device/{device_id}/text"
    
    data: dict[str, str | bool] = {"refreshNow": refresh_now, "message": message}
    if title:
        data["title"] = title
    if signature:
        data["signature"] = signature
    if icon:
        data["icon"] = icon
    if link:
        data["link"] = link
    if task_key:
        data["taskKey"] = task_key
    
    return api_request(endpoint, data)


def main():
    parser = argparse.ArgumentParser(description="Display text on Quote/0 device")
    parser.add_argument("device_id", help="Device serial number")
    parser.add_argument("message", help="Text content to display")
    parser.add_argument("--title", help="Title to display")
    parser.add_argument("--signature", help="Signature to display")
    parser.add_argument("--icon", help="Base64-encoded PNG icon data (40px×40px)")
    parser.add_argument("--link", help="NFC redirect link")
    parser.add_argument("--task-key", help="Task key for specific Text API content")
    parser.add_argument("--no-refresh", action="store_true", help="Do not display immediately")

    args = parser.parse_args()

    result = display_text(
        args.device_id,
        args.message,
        args.title,
        args.signature,
        args.icon,
        args.link,
        args.task_key,
        not args.no_refresh,
    )
    print(result.get("message", "Sent successfully"))


if __name__ == "__main__":
    main()
