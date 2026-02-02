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
    os.path.dirname(__file__), "..", "..", "skills", "aria2-json-rpc", "scripts"
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
            "secret": "test-token",
            "secure": False,
            "timeout": 30000,
        }
        self.client = Aria2RpcClient(self.config)

    def test_client_initialization(self):
        """Test client initialization with configuration."""
        self.assertEqual(self.client.config["host"], "localhost")
        self.assertEqual(self.client.config["port"], 6800)
        self.assertEqual(self.client.config["secret"], "test-token")
        self.assertEqual(self.client.endpoint_url, "http://localhost:6800/jsonrpc")

    def test_build_endpoint_url_http(self):
        """Test HTTP endpoint URL building."""
        client = Aria2RpcClient(
            {"host": "localhost", "port": 6800, "secure": False, "secret": None}
        )
        self.assertEqual(client.endpoint_url, "http://localhost:6800/jsonrpc")

    def test_build_endpoint_url_https(self):
        """Test HTTPS endpoint URL building."""
        client = Aria2RpcClient(
            {"host": "example.com", "port": 443, "secure": True, "secret": None}
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


if __name__ == "__main__":
    unittest.main()
