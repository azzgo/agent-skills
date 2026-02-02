#!/usr/bin/env python3
"""
Unit tests for aria2 JSON-RPC client.

Tests HTTP POST, token injection, and response parsing.
"""

import unittest
import json
from unittest.mock import patch, MagicMock, Mock
import sys
import os

# Add scripts directory to path
script_dir = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "skills", "aria2-json-rpc", "scripts"
)
sys.path.insert(0, script_dir)
from rpc_client import Aria2RpcClient, Aria2RpcError


class TestAria2RpcClient(unittest.TestCase):
    """Test JSON-RPC client implementation."""

    def setUp(self):
        """Set up test configuration."""
        self.config = {
            "host": "localhost",
            "port": 6800,
            "path": None,
            "secret": "test-token",
            "secure": False,
            "timeout": 30000,
        }
        self.client = Aria2RpcClient(self.config)

    def test_client_initialization(self):
        """Test client initialization with configuration."""
        self.assertEqual(self.client.config["host"], "localhost")
        self.assertEqual(self.client.config["port"], 6800)
        self.assertIsNone(self.client.config["path"])
        self.assertEqual(self.client.config["secret"], "test-token")
        self.assertEqual(self.client.endpoint_url, "http://localhost:6800")

    def test_build_endpoint_url_http(self):
        """Test HTTP endpoint URL building."""
        client = Aria2RpcClient(
            {
                "host": "localhost",
                "port": 6800,
                "path": "/jsonrpc",
                "secure": False,
                "secret": None,
            }
        )
        self.assertEqual(client.endpoint_url, "http://localhost:6800/jsonrpc")

    def test_build_endpoint_url_https(self):
        """Test HTTPS endpoint URL building."""
        client = Aria2RpcClient(
            {
                "host": "example.com",
                "port": 443,
                "path": "/jsonrpc",
                "secure": True,
                "secret": None,
            }
        )
        self.assertEqual(client.endpoint_url, "https://example.com:443/jsonrpc")

    def test_build_endpoint_url_no_path(self):
        """Test endpoint URL building without path."""
        client = Aria2RpcClient(
            {
                "host": "localhost",
                "port": 6800,
                "path": None,
                "secure": False,
                "secret": None,
            }
        )
        self.assertEqual(client.endpoint_url, "http://localhost:6800")

    def test_build_endpoint_url_reverse_proxy(self):
        """Test endpoint URL building for reverse proxy."""
        client = Aria2RpcClient(
            {
                "host": "example.com",
                "port": 443,
                "path": "/jsonrpc",
                "secure": True,
                "secret": None,
            }
        )
        self.assertEqual(client.endpoint_url, "https://example.com:443/jsonrpc")

    def test_generate_request_id(self):
        """Test request ID generation."""
        id1 = self.client._generate_request_id()
        id2 = self.client._generate_request_id()

        self.assertNotEqual(id1, id2)
        self.assertTrue(id1.startswith("aria2-rpc-"))
        self.assertTrue(id2.startswith("aria2-rpc-"))

    def test_inject_token_with_secret(self):
        """Test token injection when secret is configured."""
        params = ["uri1", "uri2"]
        result = self.client._inject_token(params)

        self.assertEqual(result[0], "token:test-token")
        self.assertEqual(result[1], "uri1")
        self.assertEqual(result[2], "uri2")

    def test_inject_token_without_secret(self):
        """Test no token injection when secret is not configured."""
        client = Aria2RpcClient(
            {"host": "localhost", "port": 6800, "secret": None, "secure": False}
        )
        params = ["uri1", "uri2"]
        result = client._inject_token(params)

        self.assertEqual(result, params)

    def test_format_request_with_aria2_method(self):
        """Test request formatting for aria2.* methods."""
        request = self.client._format_request(
            "aria2.addUri", [["http://example.com/file.zip"]]
        )

        self.assertEqual(request["jsonrpc"], "2.0")
        self.assertEqual(request["method"], "aria2.addUri")
        self.assertEqual(request["params"][0], "token:test-token")
        self.assertEqual(request["params"][1][0], "http://example.com/file.zip")
        self.assertIn("id", request)

    def test_format_request_with_system_method(self):
        """Test request formatting for system.* methods (no token)."""
        request = self.client._format_request("system.listMethods", [])

        self.assertEqual(request["jsonrpc"], "2.0")
        self.assertEqual(request["method"], "system.listMethods")
        self.assertEqual(len(request["params"]), 0)  # No token
        self.assertIn("id", request)

    def test_parse_response_success(self):
        """Test parsing successful response."""
        response = {"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": "2089b05ecca3d829"}

        result = self.client._parse_response(response, "aria2-rpc-1")

        self.assertEqual(result, "2089b05ecca3d829")

    def test_parse_response_error(self):
        """Test parsing error response."""
        response = {
            "jsonrpc": "2.0",
            "id": "aria2-rpc-1",
            "error": {
                "code": 1,
                "message": "GID not found",
                "data": "2089b05ecca3d829",
            },
        }

        with self.assertRaises(Aria2RpcError) as context:
            self.client._parse_response(response, "aria2-rpc-1")

        error = context.exception
        self.assertEqual(error.code, 1)
        self.assertEqual(error.message, "GID not found")
        self.assertEqual(error.data, "2089b05ecca3d829")

    def test_parse_response_missing_jsonrpc(self):
        """Test parsing response with missing jsonrpc field."""
        response = {"id": "aria2-rpc-1", "result": "test"}

        with self.assertRaises(Exception) as context:
            self.client._parse_response(response, "aria2-rpc-1")

        self.assertIn("jsonrpc", str(context.exception))

    def test_parse_response_id_mismatch(self):
        """Test parsing response with ID mismatch."""
        response = {
            "jsonrpc": "2.0",
            "id": "aria2-rpc-2",  # Wrong ID
            "result": "test",
        }

        with self.assertRaises(Exception) as context:
            self.client._parse_response(response, "aria2-rpc-1")

        self.assertIn("ID mismatch", str(context.exception))

    @patch("urllib.request.urlopen")
    def test_send_request_success(self, mock_urlopen):
        """Test sending HTTP request successfully."""
        # Mock response
        mock_response = Mock()
        mock_response.read.return_value = (
            b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": "success"}'
        )
        mock_urlopen.return_value = mock_response

        request = self.client._format_request("aria2.getVersion", [])
        response = self.client._send_request(request)

        self.assertEqual(response["result"], "success")

    @patch("urllib.request.urlopen")
    def test_call_method_success(self, mock_urlopen):
        """Test calling a method successfully."""
        # Mock response
        mock_response = Mock()
        mock_response.read.return_value = (
            b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": "2089b05ecca3d829"}'
        )
        mock_urlopen.return_value = mock_response

        gid = self.client.call("aria2.addUri", [["http://example.com/file.zip"]])

        self.assertEqual(gid, "2089b05ecca3d829")

    @patch("urllib.request.urlopen")
    def test_call_method_with_error(self, mock_urlopen):
        """Test calling a method that returns an error."""
        # Mock error response
        mock_response = Mock()
        mock_response.read.return_value = b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "error": {"code": 1, "message": "GID not found"}}'
        mock_urlopen.return_value = mock_response

        with self.assertRaises(Aria2RpcError) as context:
            self.client.call("aria2.tellStatus", ["invalid-gid"])

        self.assertEqual(context.exception.code, 1)

    # Milestone 2 method tests

    @patch("urllib.request.urlopen")
    def test_pause_method(self, mock_urlopen):
        """Test pause method."""
        mock_response = Mock()
        mock_response.read.return_value = (
            b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": "2089b05ecca3d829"}'
        )
        mock_urlopen.return_value = mock_response

        gid = self.client.pause("2089b05ecca3d829")
        self.assertEqual(gid, "2089b05ecca3d829")

    @patch("urllib.request.urlopen")
    def test_pause_all_method(self, mock_urlopen):
        """Test pauseAll method."""
        mock_response = Mock()
        mock_response.read.return_value = (
            b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": "OK"}'
        )
        mock_urlopen.return_value = mock_response

        result = self.client.pause_all()
        self.assertEqual(result, "OK")

    @patch("urllib.request.urlopen")
    def test_unpause_method(self, mock_urlopen):
        """Test unpause method."""
        mock_response = Mock()
        mock_response.read.return_value = (
            b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": "2089b05ecca3d829"}'
        )
        mock_urlopen.return_value = mock_response

        gid = self.client.unpause("2089b05ecca3d829")
        self.assertEqual(gid, "2089b05ecca3d829")

    @patch("urllib.request.urlopen")
    def test_unpause_all_method(self, mock_urlopen):
        """Test unpauseAll method."""
        mock_response = Mock()
        mock_response.read.return_value = (
            b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": "OK"}'
        )
        mock_urlopen.return_value = mock_response

        result = self.client.unpause_all()
        self.assertEqual(result, "OK")

    @patch("urllib.request.urlopen")
    def test_tell_active_method(self, mock_urlopen):
        """Test tellActive method."""
        mock_response = Mock()
        mock_response.read.return_value = b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": [{"gid": "2089b05ecca3d829", "status": "active"}]}'
        mock_urlopen.return_value = mock_response

        result = self.client.tell_active()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["gid"], "2089b05ecca3d829")

    @patch("urllib.request.urlopen")
    def test_tell_waiting_method(self, mock_urlopen):
        """Test tellWaiting method."""
        mock_response = Mock()
        mock_response.read.return_value = b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": [{"gid": "abc123def456", "status": "waiting"}]}'
        mock_urlopen.return_value = mock_response

        result = self.client.tell_waiting(0, 100)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["gid"], "abc123def456")

    @patch("urllib.request.urlopen")
    def test_tell_stopped_method(self, mock_urlopen):
        """Test tellStopped method."""
        mock_response = Mock()
        mock_response.read.return_value = b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": [{"gid": "123456789012", "status": "complete"}]}'
        mock_urlopen.return_value = mock_response

        result = self.client.tell_stopped(0, 50)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["status"], "complete")

    @patch("urllib.request.urlopen")
    def test_get_option_method(self, mock_urlopen):
        """Test getOption method."""
        mock_response = Mock()
        mock_response.read.return_value = b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": {"max-download-limit": "0"}}'
        mock_urlopen.return_value = mock_response

        result = self.client.get_option("2089b05ecca3d829")
        self.assertIn("max-download-limit", result)

    @patch("urllib.request.urlopen")
    def test_change_option_method(self, mock_urlopen):
        """Test changeOption method."""
        mock_response = Mock()
        mock_response.read.return_value = (
            b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": "OK"}'
        )
        mock_urlopen.return_value = mock_response

        result = self.client.change_option(
            "2089b05ecca3d829", {"max-download-limit": "1M"}
        )
        self.assertEqual(result, "OK")

    @patch("urllib.request.urlopen")
    def test_get_global_option_method(self, mock_urlopen):
        """Test getGlobalOption method."""
        mock_response = Mock()
        mock_response.read.return_value = b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": {"max-concurrent-downloads": "5"}}'
        mock_urlopen.return_value = mock_response

        result = self.client.get_global_option()
        self.assertIn("max-concurrent-downloads", result)

    @patch("urllib.request.urlopen")
    def test_change_global_option_method(self, mock_urlopen):
        """Test changeGlobalOption method."""
        mock_response = Mock()
        mock_response.read.return_value = (
            b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": "OK"}'
        )
        mock_urlopen.return_value = mock_response

        result = self.client.change_global_option({"max-concurrent-downloads": "10"})
        self.assertEqual(result, "OK")

    @patch("urllib.request.urlopen")
    def test_purge_download_result_method(self, mock_urlopen):
        """Test purgeDownloadResult method."""
        mock_response = Mock()
        mock_response.read.return_value = (
            b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": "OK"}'
        )
        mock_urlopen.return_value = mock_response

        result = self.client.purge_download_result()
        self.assertEqual(result, "OK")

    @patch("urllib.request.urlopen")
    def test_remove_download_result_method(self, mock_urlopen):
        """Test removeDownloadResult method."""
        mock_response = Mock()
        mock_response.read.return_value = (
            b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": "OK"}'
        )
        mock_urlopen.return_value = mock_response

        result = self.client.remove_download_result("2089b05ecca3d829")
        self.assertEqual(result, "OK")

    @patch("urllib.request.urlopen")
    def test_get_version_method(self, mock_urlopen):
        """Test getVersion method."""
        mock_response = Mock()
        mock_response.read.return_value = (
            b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": {"version": "1.36.0"}}'
        )
        mock_urlopen.return_value = mock_response

        result = self.client.get_version()
        self.assertIn("version", result)

    @patch("urllib.request.urlopen")
    def test_list_methods_method(self, mock_urlopen):
        """Test system.listMethods method."""
        mock_response = Mock()
        mock_response.read.return_value = b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": ["aria2.addUri", "aria2.pause"]}'
        mock_urlopen.return_value = mock_response

        result = self.client.list_methods()
        self.assertIn("aria2.addUri", result)
        self.assertIn("aria2.pause", result)

    @patch("urllib.request.urlopen")
    def test_multicall_method(self, mock_urlopen):
        """Test system.multicall method."""
        mock_response = Mock()
        mock_response.read.return_value = b'{"jsonrpc": "2.0", "id": "aria2-rpc-1", "result": [["2089b05ecca3d829"], ["OK"]]}'
        mock_urlopen.return_value = mock_response

        calls = [
            {"methodName": "aria2.tellStatus", "params": ["2089b05ecca3d829"]},
            {"methodName": "aria2.pause", "params": ["2089b05ecca3d829"]},
        ]
        result = self.client.multicall(calls)
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
