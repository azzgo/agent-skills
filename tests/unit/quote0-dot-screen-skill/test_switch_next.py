#!/usr/bin/env python3
"""
Unit tests for switch_next script.

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


class TestSwitchNext(unittest.TestCase):
    """Test switch_next functionality."""

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    def test_switch_next_success(self, mock_urlopen):
        """Test successful content switch."""
        from switch_next import switch_next

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Device ABCD1234ABCD successfully switched to next content","result":{"message":"Device ABCD1234ABCD successfully switched to next content"}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = switch_next("ABCD1234ABCD")

        self.assertEqual(result["code"], 200)
        self.assertIn("successfully switched", result["message"])


class TestFormatAsMarkdown(unittest.TestCase):
    """Test markdown formatting."""

    def test_format_as_markdown_simple_response(self):
        """Test formatting simple response."""
        from switch_next import format_as_markdown

        response = {
            "code": 200,
            "message": "Device ABCD1234ABCD successfully switched to next content",
            "result": {
                "message": "Device ABCD1234ABCD successfully switched to next content"
            }
        }

        result = format_as_markdown(response)

        self.assertIn("successfully switched", result)

    def test_format_as_markdown_without_result(self):
        """Test formatting response without result."""
        from switch_next import format_as_markdown

        response = {
            "code": 200,
            "message": "Success"
        }

        result = format_as_markdown(response)

        self.assertEqual(result, "Success")


class TestMain(unittest.TestCase):
    """Test main function."""

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["switch_next.py", "ABCD1234ABCD", "--format", "json"])
    def test_main_json_format(self, mock_urlopen):
        """Test main with JSON format."""
        from switch_next import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Success","result":{}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        parsed = json.loads(output)

        self.assertEqual(parsed["code"], 200)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["switch_next.py", "ABCD1234ABCD"])
    def test_main_default_format(self, mock_urlopen):
        """Test main with default format (markdown)."""
        from switch_next import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Success","result":{}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        self.assertIn("Success", output)


if __name__ == "__main__":
    unittest.main()
