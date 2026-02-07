#!/usr/bin/env python3
"""
Unit tests for list_devices script.

Tests API response parsing, error handling, and output formatting.
"""

import unittest
import json
from unittest.mock import patch, MagicMock, Mock
import sys
import os
import io

script_dir = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "skills", "quote0-dot-screen", "scripts"
)
sys.path.insert(0, script_dir)


class TestListDevices(unittest.TestCase):
    """Test list_devices functionality."""

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    def test_list_devices_success(self, mock_urlopen):
        """Test successful device list retrieval."""
        from list_devices import list_devices

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'[{"series":"quote","model":"quote_0","edition":1,"id":"ABCD1234ABCD"}]'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = list_devices()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "ABCD1234ABCD")
        self.assertEqual(result[0]["series"], "quote")

    @patch.dict(os.environ, {})
    @patch("sys.exit")
    def test_list_devices_missing_api_key(self, mock_exit):
        """Test missing API key error."""
        from list_devices import list_devices

        list_devices()
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_list_devices_unauthorized(self, mock_exit, mock_urlopen):
        """Test 401 unauthorized error."""
        from list_devices import list_devices

        mock_response = Mock()
        mock_response.status = 401
        mock_urlopen.return_value.__enter__.return_value = mock_response

        list_devices()
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_list_devices_server_error(self, mock_exit, mock_urlopen):
        """Test 500 server error."""
        from list_devices import list_devices

        mock_response = Mock()
        mock_response.status = 500
        mock_urlopen.return_value.__enter__.return_value = mock_response

        list_devices()
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_list_devices_unexpected_status(self, mock_exit, mock_urlopen):
        """Test unexpected status code."""
        from list_devices import list_devices

        mock_response = Mock()
        mock_response.status = 404
        mock_response.read.return_value = b"Not found"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        list_devices()
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_list_devices_connection_error(self, mock_exit, mock_urlopen):
        """Test connection error."""
        from list_devices import list_devices
        import urllib.error

        mock_urlopen.side_effect = urllib.error.URLError("Connection failed")

        list_devices()
        mock_exit.assert_called_with(1)


class TestFormatAsMarkdown(unittest.TestCase):
    """Test markdown formatting."""

    def test_format_as_markdown_single_device(self):
        """Test formatting single device."""
        from list_devices import format_as_markdown

        devices = [
            {
                "series": "quote",
                "model": "quote_0",
                "edition": 1,
                "id": "ABCD1234ABCD"
            }
        ]

        result = format_as_markdown(devices)

        self.assertIn("Serial Number: ABCD1234ABCD", result)
        self.assertIn("Series: quote", result)
        self.assertIn("Model: quote_0", result)
        self.assertIn("Edition: 1", result)
        self.assertFalse(result.endswith("\n"))

    def test_format_as_markdown_multiple_devices(self):
        """Test formatting multiple devices."""
        from list_devices import format_as_markdown

        devices = [
            {
                "series": "quote",
                "model": "quote_0",
                "edition": 1,
                "id": "ABCD1234ABCD"
            },
            {
                "series": "quote",
                "model": "quote_0",
                "edition": 2,
                "id": "ABCD5112ABCD"
            }
        ]

        result = format_as_markdown(devices)

        self.assertIn("Serial Number: ABCD1234ABCD", result)
        self.assertIn("Serial Number: ABCD5112ABCD", result)
        self.assertIn("\n\n", result)

    def test_format_as_markdown_empty_list(self):
        """Test formatting empty device list."""
        from list_devices import format_as_markdown

        result = format_as_markdown([])

        self.assertEqual(result, "No devices found.")

    def test_format_as_markdown_missing_fields(self):
        """Test formatting device with missing fields."""
        from list_devices import format_as_markdown

        devices = [{"id": "ABCD1234ABCD"}]

        result = format_as_markdown(devices)

        self.assertIn("N/A", result)
        self.assertIn("ABCD1234ABCD", result)


class TestMain(unittest.TestCase):
    """Test main function."""

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["list_devices.py", "--format", "json"])
    def test_main_json_format(self, mock_urlopen):
        """Test main with JSON format."""
        from list_devices import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'[{"series":"quote","model":"quote_0","edition":1,"id":"ABCD1234ABCD"}]'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        parsed = json.loads(output)

        self.assertEqual(parsed[0]["id"], "ABCD1234ABCD")

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["list_devices.py", "--format", "markdown"])
    def test_main_markdown_format(self, mock_urlopen):
        """Test main with markdown format."""
        from list_devices import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'[{"series":"quote","model":"quote_0","edition":1,"id":"ABCD1234ABCD"}]'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        self.assertIn("Serial Number: ABCD1234ABCD", output)
        self.assertIn("Model: quote_0", output)
        self.assertIn("ABCD1234ABCD", output)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["list_devices.py"])
    def test_main_default_format(self, mock_urlopen):
        """Test main with default format (markdown)."""
        from list_devices import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'[{"series":"quote","model":"quote_0","edition":1,"id":"ABCD1234ABCD"}]'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        self.assertIn("Serial Number: ABCD1234ABCD", output)
        self.assertIn("Model: quote_0", output)


if __name__ == "__main__":
    unittest.main()
