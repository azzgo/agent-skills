#!/usr/bin/env python3
"""
Dot API client library for Quote/0 device control.

Provides common HTTP request functionality and API key validation.
"""

import sys
import os
import json
import urllib.request
import urllib.error


BASE_URL = "https://dot.mindreset.tech/api/authV2"


def get_api_key():
    """
    Get API key from environment variable.

    Returns:
        str: API key

    Exits:
        If DOT_API_KEY is not set
    """
    api_key = os.environ.get("DOT_API_KEY")
    if not api_key:
        print("Error: DOT_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it with: export DOT_API_KEY=your_api_key", file=sys.stderr)
        sys.exit(1)
    return api_key


def api_request(endpoint, data=None):
    """
    Make authenticated API request to Dot API.

    Args:
        endpoint: API endpoint path (e.g., '/open/devices')
        data: Optional data to send in request body (for POST requests)

    Returns:
        dict: JSON response data

    Exits:
        On HTTP error, connection error, or non-200 status code
    """
    api_key = get_api_key()
    url = f"{BASE_URL}{endpoint}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        if data is not None:
            body = json.dumps(data).encode("utf-8")
            req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        else:
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


def format_as_markdown_list(items, field_names, field_labels=None, empty_message="No items found."):
    """
    Format list of dictionaries as markdown list.

    Args:
        items: List of dictionaries
        field_names: List of field names to include, in order
        field_labels: Optional list of display labels (default: field_names with underscores replaced and title-cased)
        empty_message: Message to display when list is empty

    Returns:
        str: Markdown formatted string
    """
    if not items:
        return empty_message

    output = []

    for i, item in enumerate(items):
        for j, field_name in enumerate(field_names):
            value = item.get(field_name, "N/A")
            if field_labels and j < len(field_labels):
                label = field_labels[j]
            else:
                label = field_name.replace("_", " ").title()
            output.append(f"{label}: {value}")
        if i < len(items) - 1:
            output.append("")

    return "\n".join(output)
