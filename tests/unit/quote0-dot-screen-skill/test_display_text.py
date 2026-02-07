#!/usr/bin/env python3
"""
Unit tests for display_text script.

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


class TestDisplayText(unittest.TestCase):
    """Test display_text functionality."""

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    def test_display_text_success(self, mock_urlopen):
        """Test successful text display."""
        from display_text import display_text

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Device Text API content switched","result":{"message":"Device ABCD1234ABCD Text API content switched"}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = display_text("ABCD1234ABCD", "Hello World")

        self.assertEqual(result["code"], 200)
        self.assertIn("content switched", result["message"])

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    def test_display_text_with_all_params(self, mock_urlopen):
        """Test text display with all optional parameters."""
        from display_text import display_text

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Device Text API content switched"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = display_text(
            device_id="ABCD1234ABCD",
            message="Test message",
            title="Test Title",
            signature="Test Signature",
            icon="base64icon",
            link="https://example.com",
            task_key="task1",
            refresh_now=False,
        )

        self.assertEqual(result["code"], 200)

    @patch.dict(os.environ, {"DOT_API_KEY": ""})
    @patch("sys.exit")
    def test_display_text_missing_api_key(self, mock_exit):
        """Test missing API key error."""
        from display_text import display_text

        display_text("ABCD1234ABCD", "Hello")
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_display_text_unauthorized(self, mock_exit, mock_urlopen):
        """Test 403 forbidden error."""
        from display_text import display_text

        mock_response = Mock()
        mock_response.status = 403
        mock_urlopen.return_value.__enter__.return_value = mock_response

        display_text("ABCD1234ABCD", "Hello")
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_display_text_not_found(self, mock_exit, mock_urlopen):
        """Test 404 not found error."""
        from display_text import display_text

        mock_response = Mock()
        mock_response.status = 404
        mock_urlopen.return_value.__enter__.return_value = mock_response

        display_text("ABCD1234ABCD", "Hello")
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_display_text_device_error(self, mock_exit, mock_urlopen):
        """Test 500 device response failure."""
        from display_text import display_text

        mock_response = Mock()
        mock_response.status = 500
        mock_urlopen.return_value.__enter__.return_value = mock_response

        display_text("ABCD1234ABCD", "Hello")
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_display_text_connection_error(self, mock_exit, mock_urlopen):
        """Test connection error."""
        from display_text import display_text
        import urllib.error

        mock_urlopen.side_effect = urllib.error.URLError("Connection failed")

        display_text("ABCD1234ABCD", "Hello")
        mock_exit.assert_called_with(1)


class TestMain(unittest.TestCase):
    """Test main function."""

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["display_text.py", "ABCD1234ABCD", "Hello World"])
    def test_main_basic(self, mock_urlopen):
        """Test main with basic arguments."""
        from display_text import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Device Text API content switched"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("content switched", output)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["display_text.py", "ABCD1234ABCD", "Hello", "--title", "Test", "--signature", "AI", "--no-refresh"])
    def test_main_with_options(self, mock_urlopen):
        """Test main with all options."""
        from display_text import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Device Text API content switched"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("content switched", output)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["display_text.py", "ABCD1234ABCD", "Hello", "--icon", "base64", "--link", "https://example.com", "--task-key", "task1"])
    def test_main_with_new_params(self, mock_urlopen):
        """Test main with new parameters."""
        from display_text import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Device Text API content switched"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("content switched", output)


if __name__ == "__main__":
    unittest.main()
