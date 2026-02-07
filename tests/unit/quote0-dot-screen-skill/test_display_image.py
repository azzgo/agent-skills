#!/usr/bin/env python3
"""
Unit tests for display_image script.

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


class TestDisplayImage(unittest.TestCase):
    """Test display_image functionality."""

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    def test_display_image_success(self, mock_urlopen):
        """Test successful image display."""
        from display_image import display_image

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Device Image API content switched","result":{"message":"Device ABCD1234ABCD Image API content switched"}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = display_image("ABCD1234ABCD", "base64imagedata")

        self.assertEqual(result["code"], 200)
        self.assertIn("content switched", result["message"])

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    def test_display_image_with_all_params(self, mock_urlopen):
        """Test image display with all optional parameters."""
        from display_image import display_image

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Device Image API content switched"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = display_image(
            device_id="ABCD1234ABCD",
            image="base64imagedata",
            link="https://example.com",
            border=1,
            dither_type="DIFFUSION",
            dither_kernel="FLOYD_STEINBERG",
            task_key="task1",
            refresh_now=False,
        )

        self.assertEqual(result["code"], 200)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    def test_display_image_with_ordered_dither(self, mock_urlopen):
        """Test image display with ordered dithering."""
        from display_image import display_image

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Device Image API content switched"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = display_image(
            device_id="ABCD1234ABCD",
            image="base64imagedata",
            dither_type="ORDERED",
            dither_kernel="SIERRA2",
        )

        self.assertEqual(result["code"], 200)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    def test_display_image_no_dither(self, mock_urlopen):
        """Test image display with dithering disabled."""
        from display_image import display_image

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Device Image API content switched"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = display_image(
            device_id="ABCD1234ABCD",
            image="base64imagedata",
            dither_type="NONE",
        )

        self.assertEqual(result["code"], 200)

    @patch.dict(os.environ, {"DOT_API_KEY": ""})
    @patch("sys.exit")
    def test_display_image_missing_api_key(self, mock_exit):
        """Test missing API key error."""
        from display_image import display_image

        display_image("ABCD1234ABCD", "base64imagedata")
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_display_image_forbidden(self, mock_exit, mock_urlopen):
        """Test 403 forbidden error."""
        from display_image import display_image

        mock_response = Mock()
        mock_response.status = 403
        mock_urlopen.return_value.__enter__.return_value = mock_response

        display_image("ABCD1234ABCD", "base64imagedata")
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_display_image_not_found(self, mock_exit, mock_urlopen):
        """Test 404 not found error."""
        from display_image import display_image

        mock_response = Mock()
        mock_response.status = 404
        mock_urlopen.return_value.__enter__.return_value = mock_response

        display_image("ABCD1234ABCD", "base64imagedata")
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_display_image_invalid_params(self, mock_exit, mock_urlopen):
        """Test 400 invalid parameters error."""
        from display_image import display_image

        mock_response = Mock()
        mock_response.status = 400
        mock_urlopen.return_value.__enter__.return_value = mock_response

        display_image("ABCD1234ABCD", "base64imagedata")
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_display_image_device_error(self, mock_exit, mock_urlopen):
        """Test 500 device response failure."""
        from display_image import display_image

        mock_response = Mock()
        mock_response.status = 500
        mock_urlopen.return_value.__enter__.return_value = mock_response

        display_image("ABCD1234ABCD", "base64imagedata")
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_display_image_connection_error(self, mock_exit, mock_urlopen):
        """Test connection error."""
        from display_image import display_image
        import urllib.error

        mock_urlopen.side_effect = urllib.error.URLError("Connection failed")

        display_image("ABCD1234ABCD", "base64imagedata")
        mock_exit.assert_called_with(1)


class TestMain(unittest.TestCase):
    """Test main function."""

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["display_image.py", "ABCD1234ABCD", "base64imagedata"])
    def test_main_basic(self, mock_urlopen):
        """Test main with basic arguments."""
        from display_image import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Device Image API content switched"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("content switched", output)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["display_image.py", "ABCD1234ABCD", "base64imagedata", "--link", "https://example.com", "--border", "1"])
    def test_main_with_options(self, mock_urlopen):
        """Test main with link and border options."""
        from display_image import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Device Image API content switched"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("content switched", output)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["display_image.py", "ABCD1234ABCD", "base64imagedata", "--dither-type", "ORDERED", "--dither-kernel", "SIERRA2"])
    def test_main_with_dither(self, mock_urlopen):
        """Test main with dithering options."""
        from display_image import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Device Image API content switched"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("content switched", output)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["display_image.py", "ABCD1234ABCD", "base64imagedata", "--task-key", "task1", "--no-refresh"])
    def test_main_with_task_key(self, mock_urlopen):
        """Test main with task key and no refresh."""
        from display_image import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"code":200,"message":"Device Image API content switched"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("content switched", output)


if __name__ == "__main__":
    unittest.main()
