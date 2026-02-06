#!/usr/bin/env python3
"""
Display image on Quote/0 device.

Usage:
    python display_image.py <device_id> <image_url>
"""

import sys
import os
import requests
import argparse


def display_image(device_id: str, image_url: str):
    """
    Display an image on a Quote/0 device.

    Args:
        device_id: The device serial number
        image_url: URL of the image to display
    """
    api_key = os.environ.get("DOT_API_KEY")
    if not api_key:
        print("Error: DOT_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it with: export DOT_API_KEY=your_api_key", file=sys.stderr)
        sys.exit(1)

    url = f"https://api.mindreset.tech/api/quotes/{device_id}/image"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    data = {"image_url": image_url}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Display image on Quote/0 device")
    parser.add_argument("device_id", help="Device serial number")
    parser.add_argument("image_url", help="URL of the image to display")

    args = parser.parse_args()

    result = display_image(args.device_id, args.image_url)
    print("Image: {}".format(result.get("message", "Sent successfully")))


if __name__ == "__main__":
    main()
