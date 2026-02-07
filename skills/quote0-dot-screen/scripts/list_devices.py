#!/usr/bin/env python3
"""
Get Quote/0 device list.

Usage:
    python list_devices.py [--format json|markdown]
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.error


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

    url = "https://dot.mindreset.tech/api/authV2/open/devices"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            status_code = response.status
            body = response.read().decode("utf-8")
            
            if status_code == 200:
                return json.loads(body)
            elif status_code == 401:
                print("Error: Invalid or expired API key. Please check your DOT_API_KEY.", file=sys.stderr)
                sys.exit(1)
            elif status_code == 500:
                print("Error: Internal server error. Please try again later.", file=sys.stderr)
                sys.exit(1)
            else:
                print(f"Error: Unexpected status code {status_code}. Response: {body}", file=sys.stderr)
                sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP error occurred. {e}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Failed to connect to API. {e}", file=sys.stderr)
        sys.exit(1)


def format_as_markdown(devices):
    """
    Format devices list as markdown list.
    
    Args:
        devices: List of device dictionaries
        
    Returns:
        Markdown formatted string
    """
    if not devices:
        return "No devices found."
    
    output = []
    
    for i, device in enumerate(devices):
        output.append(f"Serial Number: {device.get('id', 'N/A')}")
        output.append(f"Series: {device.get('series', 'N/A')}")
        output.append(f"Model: {device.get('model', 'N/A')}")
        output.append(f"Edition: {device.get('edition', 'N/A')}")
        if i < len(devices) - 1:
            output.append("")
    
    return "\n".join(output)


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
