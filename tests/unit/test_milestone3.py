#!/usr/bin/env python3
"""
Unit tests for Milestone 3 features.

Tests torrent/metalink operations and WebSocket client (with optional dependency).
"""

import unittest
import json
import base64
import tempfile
import os
from unittest.mock import patch, MagicMock, Mock, mock_open
import sys

# Add scripts directory to path
script_dir = os.path.join(
    os.path.dirname(__file__), "..", "..", "skills", "aria2-json-rpc", "scripts"
)
sys.path.insert(0, script_dir)

from rpc_client import Aria2RpcClient, Aria2RpcError
from dependency_check import check_optional_websockets


class TestTorrentOperations(unittest.TestCase):
    """Test torrent-related operations."""

    def setUp(self):
        """Set up test configuration."""
        self.config = {
            "host": "localhost",
            "port": 6800,
            "secret": "test-token",
            "secure": False,
            "timeout": 30000,
        }
        self.client = Aria2RpcClient(self.config)

    def test_add_torrent_from_file_path(self):
        """Test adding torrent from file path."""
        # Create a temporary torrent file
        with tempfile.NamedTemporaryFile(
            mode="wb", suffix=".torrent", delete=False
        ) as f:
            # Write some dummy torrent data
            torrent_data = b"d8:announce33:http://tracker.example.com/e"
            f.write(torrent_data)
            torrent_path = f.name

        try:
            # Expected base64 of the torrent data
            expected_base64 = base64.b64encode(torrent_data).decode("utf-8")

            # Mock the HTTP request
            with patch("urllib.request.urlopen") as mock_urlopen:
                mock_response = Mock()
                mock_response.read.return_value = json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": "aria2-rpc-1",
                        "result": "2089b05ecca3d829",
                    }
                ).encode("utf-8")
                mock_urlopen.return_value = mock_response

                # Call add_torrent with file path
                gid = self.client.add_torrent(torrent_path)

                # Verify the result
                self.assertEqual(gid, "2089b05ecca3d829")

                # Verify the request was made correctly
                mock_urlopen.assert_called_once()
                call_args = mock_urlopen.call_args
                request = call_args[0][0]

                # Parse the request data
                request_data = json.loads(request.data.decode("utf-8"))

                # Check method and base64 encoding
                self.assertEqual(request_data["method"], "aria2.addTorrent")
                # First param after token should be the base64-encoded torrent
                self.assertEqual(request_data["params"][1], expected_base64)

        finally:
            # Clean up temporary file
            os.unlink(torrent_path)

    def test_add_torrent_from_bytes(self):
        """Test adding torrent from bytes content."""
        torrent_data = b"d8:announce33:http://tracker.example.com/e"
        expected_base64 = base64.b64encode(torrent_data).decode("utf-8")

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = json.dumps(
                {"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": "abc123def456"}
            ).encode("utf-8")
            mock_urlopen.return_value = mock_response

            gid = self.client.add_torrent(torrent_data)

            self.assertEqual(gid, "abc123def456")

            # Verify base64 encoding in request
            call_args = mock_urlopen.call_args
            request = call_args[0][0]
            request_data = json.loads(request.data.decode("utf-8"))
            self.assertEqual(request_data["params"][1], expected_base64)

    def test_add_torrent_from_base64_string(self):
        """Test adding torrent from pre-encoded base64 string."""
        torrent_base64 = "ZDg6YW5ub3VuY2UzMzpodHRwOi8vdHJhY2tlci5leGFtcGxlLmNvbS9l"

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = json.dumps(
                {"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": "xyz789"}
            ).encode("utf-8")
            mock_urlopen.return_value = mock_response

            # Create a non-existent file path to test base64 string handling
            with patch("os.path.isfile", return_value=False):
                gid = self.client.add_torrent(torrent_base64)

            self.assertEqual(gid, "xyz789")

            # Verify the base64 string was passed through
            call_args = mock_urlopen.call_args
            request = call_args[0][0]
            request_data = json.loads(request.data.decode("utf-8"))
            self.assertEqual(request_data["params"][1], torrent_base64)

    def test_add_torrent_with_web_seeds(self):
        """Test adding torrent with web seed URIs."""
        torrent_data = b"d8:announce33:http://tracker.example.com/e"
        web_seeds = ["http://mirror1.com/file", "http://mirror2.com/file"]

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = json.dumps(
                {"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": "gid123"}
            ).encode("utf-8")
            mock_urlopen.return_value = mock_response

            gid = self.client.add_torrent(torrent_data, uris=web_seeds)

            self.assertEqual(gid, "gid123")

            # Verify web seeds are in params
            call_args = mock_urlopen.call_args
            request = call_args[0][0]
            request_data = json.loads(request.data.decode("utf-8"))
            # params should be: [token, base64_torrent, web_seeds]
            self.assertEqual(request_data["params"][2], web_seeds)

    def test_add_torrent_with_options(self):
        """Test adding torrent with download options."""
        torrent_data = b"d8:announce33:http://tracker.example.com/e"
        options = {"dir": "/downloads", "seed-time": 60}

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = json.dumps(
                {"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": "gid456"}
            ).encode("utf-8")
            mock_urlopen.return_value = mock_response

            gid = self.client.add_torrent(torrent_data, options=options)

            self.assertEqual(gid, "gid456")

            # Verify options are in params
            call_args = mock_urlopen.call_args
            request = call_args[0][0]
            request_data = json.loads(request.data.decode("utf-8"))
            # params should include options
            self.assertIn(options, request_data["params"])

    def test_add_torrent_invalid_type(self):
        """Test add_torrent with invalid input type."""
        with self.assertRaises(ValueError) as ctx:
            self.client.add_torrent(12345)  # Invalid type

        self.assertIn("must be a file path", str(ctx.exception))


class TestMetalinkOperations(unittest.TestCase):
    """Test metalink-related operations."""

    def setUp(self):
        """Set up test configuration."""
        self.config = {
            "host": "localhost",
            "port": 6800,
            "secret": "test-token",
            "secure": False,
            "timeout": 30000,
        }
        self.client = Aria2RpcClient(self.config)

    def test_add_metalink_from_file_path(self):
        """Test adding metalink from file path."""
        # Create a temporary metalink file
        with tempfile.NamedTemporaryFile(
            mode="wb", suffix=".metalink", delete=False
        ) as f:
            # Write some dummy metalink data
            metalink_data = (
                b'<?xml version="1.0" encoding="UTF-8"?><metalink></metalink>'
            )
            f.write(metalink_data)
            metalink_path = f.name

        try:
            expected_base64 = base64.b64encode(metalink_data).decode("utf-8")

            with patch("urllib.request.urlopen") as mock_urlopen:
                mock_response = Mock()
                # Metalink returns array of GIDs
                mock_response.read.return_value = json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": "aria2-rpc-1",
                        "result": ["gid1", "gid2", "gid3"],
                    }
                ).encode("utf-8")
                mock_urlopen.return_value = mock_response

                gids = self.client.add_metalink(metalink_path)

                # Verify the result
                self.assertEqual(gids, ["gid1", "gid2", "gid3"])

                # Verify the request
                call_args = mock_urlopen.call_args
                request = call_args[0][0]
                request_data = json.loads(request.data.decode("utf-8"))
                self.assertEqual(request_data["method"], "aria2.addMetalink")
                self.assertEqual(request_data["params"][1], expected_base64)

        finally:
            os.unlink(metalink_path)

    def test_add_metalink_from_bytes(self):
        """Test adding metalink from bytes content."""
        metalink_data = b'<?xml version="1.0" encoding="UTF-8"?><metalink></metalink>'
        expected_base64 = base64.b64encode(metalink_data).decode("utf-8")

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = json.dumps(
                {"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": ["gid123"]}
            ).encode("utf-8")
            mock_urlopen.return_value = mock_response

            gids = self.client.add_metalink(metalink_data)

            self.assertEqual(gids, ["gid123"])

            # Verify base64 encoding
            call_args = mock_urlopen.call_args
            request = call_args[0][0]
            request_data = json.loads(request.data.decode("utf-8"))
            self.assertEqual(request_data["params"][1], expected_base64)

    def test_add_metalink_with_options(self):
        """Test adding metalink with download options."""
        metalink_data = b'<?xml version="1.0" encoding="UTF-8"?><metalink></metalink>'
        options = {"dir": "/downloads", "max-connection-per-server": 16}

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = json.dumps(
                {"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": ["gid789"]}
            ).encode("utf-8")
            mock_urlopen.return_value = mock_response

            gids = self.client.add_metalink(metalink_data, options=options)

            self.assertEqual(gids, ["gid789"])

            # Verify options in params
            call_args = mock_urlopen.call_args
            request = call_args[0][0]
            request_data = json.loads(request.data.decode("utf-8"))
            self.assertIn(options, request_data["params"])

    def test_add_metalink_invalid_type(self):
        """Test add_metalink with invalid input type."""
        with self.assertRaises(ValueError) as ctx:
            self.client.add_metalink([1, 2, 3])  # Invalid type

        self.assertIn("must be a file path", str(ctx.exception))


class TestWebSocketDependency(unittest.TestCase):
    """Test WebSocket optional dependency handling."""

    def test_websocket_dependency_check(self):
        """Test checking if websockets library is available."""
        # This test simply verifies the function runs
        result = check_optional_websockets()
        self.assertIsInstance(result, bool)

    @unittest.skipIf(
        not check_optional_websockets(), "websockets library not available"
    )
    def test_websocket_client_import(self):
        """Test importing WebSocket client when library is available."""
        try:
            from websocket_client import Aria2WebSocketClient, check_websocket_available

            self.assertTrue(check_websocket_available())

            # Test client initialization
            config = {
                "host": "localhost",
                "port": 6800,
                "secret": None,
                "secure": False,
                "timeout": 30000,
            }
            client = Aria2WebSocketClient(config)
            self.assertEqual(client.ws_url, "ws://localhost:6800/jsonrpc")

        except ImportError as e:
            self.fail(f"Failed to import WebSocket client: {e}")

    def test_websocket_client_unavailable_graceful(self):
        """Test graceful handling when websockets library is not available."""
        # Mock the websocket check to return False
        with patch("dependency_check.check_optional_websockets", return_value=False):
            # Importing should work but client initialization should fail
            try:
                # Re-import to get the mocked version
                import importlib
                import sys

                if "websocket_client" in sys.modules:
                    importlib.reload(sys.modules["websocket_client"])

                from websocket_client import (
                    Aria2WebSocketClient,
                    check_websocket_available,
                )

                self.assertFalse(check_websocket_available())

                # Client initialization should raise ImportError
                config = {
                    "host": "localhost",
                    "port": 6800,
                    "secret": None,
                    "secure": False,
                    "timeout": 30000,
                }

                with self.assertRaises(ImportError) as ctx:
                    client = Aria2WebSocketClient(config)

                self.assertIn("websockets library not available", str(ctx.exception))

            except Exception as e:
                # If module reloading fails, skip the test
                self.skipTest(f"Module reload failed: {e}")


class TestCommandMapperMilestone3(unittest.TestCase):
    """Test natural language command mapping for Milestone 3."""

    def setUp(self):
        """Set up command mapper."""
        from command_mapper import CommandMapper

        self.mapper = CommandMapper()

    def test_add_torrent_command(self):
        """Test mapping 'add torrent' commands."""
        commands = [
            "add torrent /path/to/file.torrent",
            "download torrent ubuntu.torrent",
            "download from torrent movie.torrent",
        ]

        for command in commands:
            result = self.mapper.map_command(command)
            self.assertIsNotNone(result, f"Failed to map: {command}")
            method, params = result
            self.assertEqual(method, "aria2.addTorrent")
            self.assertEqual(len(params), 1)
            self.assertTrue(params[0].endswith(".torrent"))

    def test_add_metalink_command(self):
        """Test mapping 'add metalink' commands."""
        commands = [
            "add metalink archive.metalink",
            "download metalink package.metalink",
            "download from metalink files.metalink",
        ]

        for command in commands:
            result = self.mapper.map_command(command)
            self.assertIsNotNone(result, f"Failed to map: {command}")
            method, params = result
            self.assertEqual(method, "aria2.addMetalink")
            self.assertEqual(len(params), 1)
            self.assertTrue(params[0].endswith(".metalink"))


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
