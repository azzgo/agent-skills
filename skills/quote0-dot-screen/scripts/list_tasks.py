#!/usr/bin/env python3
"""
List tasks on a Quote/0 device.

Usage:
    python list_tasks.py <device_id> <task_type>

Valid task types:
    - loop (default)

Output formats:
    - json (default)
    - markdown
"""

import sys
import os
import argparse
import json

sys.path.insert(0, os.path.dirname(__file__))
from api_client import api_request, format_as_markdown_list


def list_tasks(device_id: str, task_type: str = "loop"):
    """
    Get list of content tasks on a Quote/0 device.

    Args:
        device_id: The device serial number
        task_type: Task type (default: "loop")

    Returns:
        List of device tasks
    """
    endpoint = f"/open/device/{device_id}/{task_type}/list"
    return api_request(endpoint)


def format_task_markdown(task):
    """Format a single task as markdown."""
    lines = [f"**Type**: {task.get('type', 'N/A')}"]
    
    if task.get('key'):
        lines.append(f"**Key**: {task['key']}")
    
    if task.get('type') == 'TEXT_API':
        if task.get('title'):
            lines.append(f"**Title**:\n{task['title']}")
        if task.get('message'):
            lines.append(f"**Message**:\n{task['message']}")
        if task.get('icon'):
            lines.append(f"**Icon**: {task['icon']}")
        if task.get('signature'):
            lines.append(f"**Signature**: {task['signature']}")
    elif task.get('type') == 'IMAGE_API':
        if task.get('border') is not None:
            lines.append(f"**Border**: {task['border']}")
        if task.get('ditherType'):
            lines.append(f"**Dither Type**: {task['ditherType']}")
        if task.get('ditherKernel'):
            lines.append(f"**Dither Kernel**: {task['ditherKernel']}")
    
    if task.get('refreshNow') is not None:
        lines.append(f"**Refresh Now**: {task['refreshNow']}")
    if task.get('link'):
        lines.append(f"**Link**: {task['link']}")
    
    return "\n".join(lines)


def format_as_markdown(tasks):
    """Format list of tasks as markdown."""
    if not tasks:
        return "No tasks found."
    
    output = []
    for i, task in enumerate(tasks):
        output.append(f"### Task {i + 1}")
        output.append(format_task_markdown(task))
        if i < len(tasks) - 1:
            output.append("---")
    
    return "\n\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="List tasks on Quote/0 device")
    parser.add_argument("device_id", help="Device serial number")
    parser.add_argument("task_type", nargs="?", default="loop", help="Task type (default: loop)")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown", help="Output format (default: markdown)")

    args = parser.parse_args()

    result = list_tasks(args.device_id, args.task_type)
    
    if args.format == "markdown":
        print(format_as_markdown(result))
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
