#!/usr/bin/env python3
"""
Display image on Quote/0 device.

Usage:
    python display_image.py <device_id> <base64_image> [--link <link>] [--border <0|1>] [--dither-type <type>] [--dither-kernel <kernel>] [--task-key <task_key>] [--no-refresh]
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))
from api_client import api_request


def display_image(
    device_id: str,
    image: str,
    link: str | None = None,
    border: int = 0,
    dither_type: str | None = None,
    dither_kernel: str | None = None,
    task_key: str | None = None,
    refresh_now: bool = True,
):
    """
    Display an image on a Quote/0 device.

    Args:
        device_id: The device serial number
        image: Base64-encoded PNG image data (296px×152px)
        link: Optional NFC redirect link
        border: Border color (0=white, 1=black, default: 0)
        dither_type: Optional dither type (DIFFUSION, ORDERED, NONE)
        dither_kernel: Optional dither kernel (FLOYD_STEINBERG, ATKINSON, etc.)
        task_key: Optional task key for specific Image API content
        refresh_now: Whether to display immediately (default: True)

    Returns:
        dict: API response
    """
    endpoint = f"/open/device/{device_id}/image"
    
    data: dict[str, str | int | bool] = {"refreshNow": refresh_now, "image": image}
    
    if border in (0, 1):
        data["border"] = border
    
    if link:
        data["link"] = link
    if dither_type:
        data["ditherType"] = dither_type
    if dither_kernel:
        data["ditherKernel"] = dither_kernel
    if task_key:
        data["taskKey"] = task_key
    
    return api_request(endpoint, data)


def main():
    parser = argparse.ArgumentParser(description="Display image on Quote/0 device")
    parser.add_argument("device_id", help="Device serial number")
    parser.add_argument("image", help="Base64-encoded PNG image data (296px×152px)")
    parser.add_argument("--link", help="NFC redirect link")
    parser.add_argument("--border", type=int, choices=[0, 1], default=0, help="Border color (0=white, 1=black, default: 0)")
    parser.add_argument("--dither-type", choices=["DIFFUSION", "ORDERED", "NONE"], help="Dither type (DIFFUSION, ORDERED, NONE)")
    parser.add_argument("--dither-kernel", help="Dither kernel (FLOYD_STEINBERG, ATKINSON, BURKES, etc.)")
    parser.add_argument("--task-key", help="Task key for specific Image API content")
    parser.add_argument("--no-refresh", action="store_true", help="Do not display immediately")

    args = parser.parse_args()

    result = display_image(
        args.device_id,
        args.image,
        args.link,
        args.border,
        args.dither_type,
        args.dither_kernel,
        args.task_key,
        not args.no_refresh,
    )
    print(result.get("message", "Sent successfully"))


if __name__ == "__main__":
    main()
