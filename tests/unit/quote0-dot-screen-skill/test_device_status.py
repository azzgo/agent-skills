#!/usr/bin/env python3
"""
Unit tests for device_status script.

Tests API response parsing, error handling, and output formatting.
"""

import unittest
import json
from unittest.mock import patch, Mock
import sys
import os
import io

script_dir = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "skills", "quote0-dot-screen", "scripts"
)
sys.path.insert(0, script_dir)


class TestGetDeviceStatus(unittest.TestCase):
    """Test get_device_status functionality."""

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    def test_get_device_status_success(self, mock_urlopen):
        """Test successful device status retrieval."""
        from device_status import get_device_status

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"deviceId":"ABCD1234ABCD","alias":"My Device","location":"Living Room","status":{"version":"1.0.0","current":"Power Active","description":"The device is power active and ready to use","battery":"Charging","wifi":"-62 dBm"},"renderInfo":{"last":"12/18/2025 14:11","current":{"rotated":false,"border":0,"image":["https://example.com/render/0.png"]},"next":{"battery":"12/18/2025 17:11","power":"12/18/2025 14:16"}}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = get_device_status("ABCD1234ABCD")

        self.assertEqual(result["deviceId"], "ABCD1234ABCD")
        self.assertEqual(result["alias"], "My Device")


    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    def test_get_device_status_without_alias_location(self, mock_urlopen):
        """Test device status with null alias and location."""
        from device_status import get_device_status

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"deviceId":"ABCD1234ABCD","alias":null,"location":null,"status":{"version":"1.0.0","current":"Power Active","description":"Active","battery":"Charging","wifi":"-62 dBm"},"renderInfo":{"last":"12/18/2025 14:11","current":{"rotated":false,"border":0,"image":null},"next":{"battery":"12/18/2025 17:11","power":"12/18/2025 14:16"}}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = get_device_status("ABCD1234ABCD")

        self.assertIsNone(result["alias"])
        self.assertIsNone(result["location"])


class TestFormatAsMarkdown(unittest.TestCase):
    """Test markdown formatting."""

    def test_format_as_markdown_complete_status(self):
        """Test formatting complete device status."""
        from device_status import format_as_markdown

        status = {
            "deviceId": "ABCD1234ABCD",
            "alias": "My Device",
            "location": "Living Room",
            "status": {
                "version": "1.0.0",
                "current": "Power Active",
                "description": "Active",
                "battery": "Charging",
                "wifi": "-62 dBm"
            },
            "renderInfo": {
                "last": "12/18/2025 14:11",
                "current": {
                    "rotated": False,
                    "border": 0,
                    "image": ["https://example.com/render/0.png", "https://example.com/render/1.png"]
                },
                "next": {
                    "battery": "12/18/2025 17:11",
                    "power": "12/18/2025 14:16"
                }
            }
        }

        result = format_as_markdown(status)

        self.assertIn("## Device Information", result)
        self.assertIn("Device ID: ABCD1234ABCD", result)
        self.assertIn("Alias: My Device", result)
        self.assertIn("Location: Living Room", result)
        self.assertIn("## Status", result)
        self.assertIn("Version: 1.0.0", result)
        self.assertIn("Current: Power Active", result)
        self.assertIn("Battery: Charging", result)
        self.assertIn("WiFi: -62 dBm", result)
        self.assertIn("## Render Info", result)
        self.assertIn("Last Render: 12/18/2025 14:11", result)
        self.assertIn("Rotated: False", result)
        self.assertIn("Border: 0", result)
        self.assertIn("Battery Mode: 12/18/2025 17:11", result)

    def test_format_as_markdown_with_null_values(self):
        """Test formatting status with null values."""
        from device_status import format_as_markdown

        status = {
            "deviceId": "ABCD1234ABCD",
            "alias": None,
            "location": None,
            "status": {
                "version": "1.0.0",
                "current": "Active",
                "description": "Active",
                "battery": "Charging",
                "wifi": "-62 dBm"
            },
            "renderInfo": {
                "last": "12/18/2025 14:11",
                "current": {
                    "rotated": False,
                    "border": 0,
                    "image": None
                },
                "next": {
                    "battery": "12/18/2025 17:11",
                    "power": "12/18/2025 14:16"
                }
            }
        }

        result = format_as_markdown(status)

        self.assertIn("Alias: N/A", result)
        self.assertIn("Location: N/A", result)
        self.assertIn("Images: N/A", result)


class TestMain(unittest.TestCase):
    """Test main function."""

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["device_status.py", "ABCD1234ABCD", "--format", "json"])
    def test_main_json_format(self, mock_urlopen):
        """Test main with JSON format."""
        from device_status import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"deviceId":"ABCD1234ABCD","alias":"My Device","status":{"version":"1.0.0","current":"Active"},"renderInfo":{"last":"12/18/2025 14:11","current":{},"next":{}}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        parsed = json.loads(output)

        self.assertEqual(parsed["deviceId"], "ABCD1234ABCD")

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["device_status.py", "ABCD1234ABCD", "--format", "markdown"])
    def test_main_markdown_format(self, mock_urlopen):
        """Test main with markdown format."""
        from device_status import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"deviceId":"ABCD1234ABCD","alias":null,"status":{"version":"1.0.0","current":"Active","description":"Active","battery":"Charging","wifi":"-62 dBm"},"renderInfo":{"last":"12/18/2025 14:11","current":{"rotated":false,"border":0,"image":null},"next":{"battery":"12/18/2025 17:11","power":"12/18/2025 14:16"}}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        self.assertIn("## Device Information", output)
        self.assertIn("Device ID: ABCD1234ABCD", output)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["device_status.py", "ABCD1234ABCD"])
    def test_main_default_format(self, mock_urlopen):
        """Test main with default format (markdown)."""
        from device_status import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"deviceId":"ABCD1234ABCD","alias":"My Device","status":{"version":"1.0.0","current":"Active"},"renderInfo":{"last":"12/18/2025 14:11","current":{},"next":{}}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        self.assertIn("## Device Information", output)


if __name__ == "__main__":
    unittest.main()
