#!/usr/bin/env python3
"""
Get Quote/0 device status.

Usage:
    python device_status.py <device_id> [--format json|markdown]
"""

import json
import argparse
from api_client import api_request


def get_device_status(device_id: str):
    """
    Get status of a specific Quote/0 device.

    Args:
        device_id: The device serial number

    Returns:
        Device status information
    """
    return api_request(f"/open/device/{device_id}/status")


def format_as_markdown(status):
    """
    Format device status as markdown.

    Args:
        status: Device status dictionary

    Returns:
        Markdown formatted string
    """
    output = []

    output.append("## Device Information")
    output.append(f"Device ID: {status.get('deviceId', 'N/A')}")
    output.append(f"Alias: {status.get('alias') or 'N/A'}")
    output.append(f"Location: {status.get('location') or 'N/A'}")
    output.append("")

    status_obj = status.get('status', {})
    output.append("## Status")
    output.append(f"Version: {status_obj.get('version', 'N/A')}")
    output.append(f"Current: {status_obj.get('current', 'N/A')}")
    output.append(f"Description: {status_obj.get('description', 'N/A')}")
    output.append(f"Battery: {status_obj.get('battery', 'N/A')}")
    output.append(f"WiFi: {status_obj.get('wifi', 'N/A')}")
    output.append("")

    render_info = status.get('renderInfo', {})
    output.append("## Render Info")
    output.append(f"Last Render: {render_info.get('last', 'N/A')}")

    current_render = render_info.get('current', {})
    output.append("Current Render:")
    output.append(f"  Rotated: {current_render.get('rotated', 'N/A')}")
    output.append(f"  Border: {current_render.get('border', 'N/A')}")
    images = current_render.get('image') or []
    if images:
        for i, img in enumerate(images):
            output.append(f"  Image {i+1}: {img}")
    else:
        output.append("  Images: N/A")

    next_render = render_info.get('next', {})
    output.append("Next Scheduled Render:")
    output.append(f"  Battery Mode: {next_render.get('battery', 'N/A')}")
    output.append(f"  Power Mode: {next_render.get('power', 'N/A')}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="Get Quote/0 device status")
    parser.add_argument("device_id", help="Device serial number")
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="markdown",
        help="Output format (default: markdown)"
    )

    args = parser.parse_args()

    result = get_device_status(args.device_id)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(format_as_markdown(result))


if __name__ == "__main__":
    main()
