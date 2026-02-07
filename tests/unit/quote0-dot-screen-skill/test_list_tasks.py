#!/usr/bin/env python3
"""
Unit tests for list_tasks script.

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


class TestListTasks(unittest.TestCase):
    """Test list_tasks functionality."""

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    def test_list_tasks_success(self, mock_urlopen):
        """Test successful task list retrieval."""
        from list_tasks import list_tasks

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'[{"type":"TEXT_API","key":"task1","refreshNow":true,"title":"Hello","message":"World"}]'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = list_tasks("ABCD1234ABCD", "loop")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "TEXT_API")
        self.assertEqual(result[0]["key"], "task1")

    @patch.dict(os.environ, {"DOT_API_KEY": ""})
    @patch("sys.exit")
    def test_list_tasks_missing_api_key(self, mock_exit):
        """Test missing API key error."""
        from list_tasks import list_tasks

        list_tasks("ABCD1234ABCD")
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_list_tasks_unauthorized(self, mock_exit, mock_urlopen):
        """Test 401 unauthorized error."""
        from list_tasks import list_tasks

        mock_response = Mock()
        mock_response.status = 401
        mock_urlopen.return_value.__enter__.return_value = mock_response

        list_tasks("ABCD1234ABCD")
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_list_tasks_server_error(self, mock_exit, mock_urlopen):
        """Test 500 server error."""
        from list_tasks import list_tasks

        mock_response = Mock()
        mock_response.status = 500
        mock_urlopen.return_value.__enter__.return_value = mock_response

        list_tasks("ABCD1234ABCD")
        mock_exit.assert_called_with(1)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.exit")
    def test_list_tasks_connection_error(self, mock_exit, mock_urlopen):
        """Test connection error."""
        from list_tasks import list_tasks
        import urllib.error

        mock_urlopen.side_effect = urllib.error.URLError("Connection failed")

        list_tasks("ABCD1234ABCD")
        mock_exit.assert_called_with(1)


class TestFormatTaskMarkdown(unittest.TestCase):
    """Test task markdown formatting."""

    def test_format_text_api_task(self):
        """Test formatting TEXT_API task."""
        from list_tasks import format_task_markdown

        task = {
            "type": "TEXT_API",
            "key": "task1",
            "refreshNow": True,
            "title": "Hello",
            "message": "World",
            "icon": "👋",
            "signature": "AI"
        }

        result = format_task_markdown(task)

        self.assertIn("**Type**: TEXT_API", result)
        self.assertIn("**Key**: task1", result)
        self.assertIn("**Refresh Now**: True", result)
        self.assertIn("**Title**:\nHello", result)
        self.assertIn("**Message**:\nWorld", result)
        self.assertIn("**Icon**: 👋", result)
        self.assertIn("**Signature**: AI", result)

    def test_format_image_api_task(self):
        """Test formatting IMAGE_API task."""
        from list_tasks import format_task_markdown

        task = {
            "type": "IMAGE_API",
            "key": "task2",
            "refreshNow": False,
            "border": 1,
            "ditherType": "DIFFUSION",
            "ditherKernel": "FLOYD_STEINBERG"
        }

        result = format_task_markdown(task)

        self.assertIn("**Type**: IMAGE_API", result)
        self.assertIn("**Key**: task2", result)
        self.assertIn("**Refresh Now**: False", result)
        self.assertIn("**Border**: 1", result)
        self.assertIn("**Dither Type**: DIFFUSION", result)
        self.assertIn("**Dither Kernel**: FLOYD_STEINBERG", result)

    def test_format_task_with_link(self):
        """Test formatting task with NFC link."""
        from list_tasks import format_task_markdown

        task = {
            "type": "TEXT_API",
            "key": "task1",
            "link": "https://example.com"
        }

        result = format_task_markdown(task)

        self.assertIn("**Link**: https://example.com", result)

    def test_format_task_minimal(self):
        """Test formatting task with minimal fields."""
        from list_tasks import format_task_markdown

        task = {"type": "TEXT_API"}

        result = format_task_markdown(task)

        self.assertIn("**Type**: TEXT_API", result)


class TestFormatAsMarkdown(unittest.TestCase):
    """Test markdown formatting for task list."""

    def test_format_single_task(self):
        """Test formatting single task."""
        from list_tasks import format_as_markdown

        tasks = [
            {
                "type": "TEXT_API",
                "key": "task1",
                "title": "Hello",
                "message": "World"
            }
        ]

        result = format_as_markdown(tasks)

        self.assertIn("### Task 1", result)
        self.assertIn("**Type**: TEXT_API", result)
        self.assertIn("**Title**:\nHello", result)

    def test_format_multiple_tasks(self):
        """Test formatting multiple tasks."""
        from list_tasks import format_as_markdown

        tasks = [
            {"type": "TEXT_API", "key": "task1"},
            {"type": "IMAGE_API", "key": "task2"}
        ]

        result = format_as_markdown(tasks)

        self.assertIn("### Task 1", result)
        self.assertIn("### Task 2", result)
        self.assertIn("---", result)
        self.assertIn("TEXT_API", result)
        self.assertIn("IMAGE_API", result)

    def test_format_empty_list(self):
        """Test formatting empty task list."""
        from list_tasks import format_as_markdown

        result = format_as_markdown([])

        self.assertEqual(result, "No tasks found.")


class TestMain(unittest.TestCase):
    """Test main function."""

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["list_tasks.py", "ABCD1234ABCD", "--format", "json"])
    def test_main_json_format(self, mock_urlopen):
        """Test main with JSON format."""
        from list_tasks import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'[{"type":"TEXT_API","key":"task1"}]'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        parsed = json.loads(output)

        self.assertEqual(parsed[0]["type"], "TEXT_API")
        self.assertEqual(parsed[0]["key"], "task1")

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["list_tasks.py", "ABCD1234ABCD", "--format", "markdown"])
    def test_main_markdown_format(self, mock_urlopen):
        """Test main with markdown format."""
        from list_tasks import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'[{"type":"TEXT_API","key":"task1"}]'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        self.assertIn("### Task 1", output)
        self.assertIn("**Type**: TEXT_API", output)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["list_tasks.py", "ABCD1234ABCD"])
    def test_main_default_format(self, mock_urlopen):
        """Test main with default format (markdown)."""
        from list_tasks import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'[{"type":"TEXT_API","key":"task1"}]'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        self.assertIn("### Task 1", output)
        self.assertIn("**Type**: TEXT_API", output)

    @patch.dict(os.environ, {"DOT_API_KEY": "test-api-key"})
    @patch("urllib.request.urlopen")
    @patch("sys.argv", ["list_tasks.py", "ABCD1234ABCD", "loop"])
    def test_main_with_task_type(self, mock_urlopen):
        """Test main with explicit task type."""
        from list_tasks import main

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'[]'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        self.assertEqual(captured_output.getvalue(), "No tasks found.\n")


if __name__ == "__main__":
    unittest.main()
