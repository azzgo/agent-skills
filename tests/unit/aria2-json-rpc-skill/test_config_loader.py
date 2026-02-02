#!/usr/bin/env python3
"""
Unit tests for aria2 configuration loader.

Tests config.json loading, environment variables, and validation.
"""

import unittest
import json
import os
import sys
import tempfile
from unittest.mock import patch

# Add scripts directory to path
script_dir = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "skills", "aria2-json-rpc", "scripts"
)
sys.path.insert(0, script_dir)
from config_loader import Aria2Config, ConfigurationError


class TestAria2Config(unittest.TestCase):
    """Test configuration loading and validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "config.json")

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)

    def test_default_config(self):
        """Test default configuration values."""
        config = Aria2Config(self.config_path)
        config.load()

        self.assertEqual(config.get("host"), "localhost")
        self.assertEqual(config.get("port"), 6800)
        self.assertIsNone(config.get("path"))
        self.assertIsNone(config.get("secret"))
        self.assertFalse(config.get("secure"))
        self.assertEqual(config.get("timeout"), 30000)

    def test_load_from_file(self):
        """Test loading configuration from file."""
        test_config = {
            "host": "192.168.1.1",
            "port": 7000,
            "path": "/api/jsonrpc",
            "secret": "my-secret",
            "secure": True,
            "timeout": 60000,
        }

        with open(self.config_path, "w") as f:
            json.dump(test_config, f)

        config = Aria2Config(self.config_path)
        config.load()

        self.assertEqual(config.get("host"), "192.168.1.1")
        self.assertEqual(config.get("port"), 7000)
        self.assertEqual(config.get("path"), "/api/jsonrpc")
        self.assertEqual(config.get("secret"), "my-secret")
        self.assertTrue(config.get("secure"))
        self.assertEqual(config.get("timeout"), 60000)

    def test_load_from_env_vars(self):
        """Test loading configuration from environment variables."""
        env_vars = {
            "ARIA2_RPC_HOST": "env-host",
            "ARIA2_RPC_PORT": "9000",
            "ARIA2_RPC_PATH": "/custom/path",
            "ARIA2_RPC_SECRET": "env-secret",
            "ARIA2_RPC_SECURE": "true",
            "ARIA2_RPC_TIMEOUT": "45000",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = Aria2Config(self.config_path)
            config.load()

            self.assertEqual(config.get("host"), "env-host")
            self.assertEqual(config.get("port"), 9000)
            self.assertEqual(config.get("path"), "/custom/path")
            self.assertEqual(config.get("secret"), "env-secret")
            self.assertTrue(config.get("secure"))
            self.assertEqual(config.get("timeout"), 45000)

    def test_env_vars_override_file(self):
        """Test environment variables override file configuration."""
        test_config = {
            "host": "file-host",
            "port": 6000,
            "path": "/file/path",
            "secret": "file-secret",
        }

        with open(self.config_path, "w") as f:
            json.dump(test_config, f)

        env_vars = {
            "ARIA2_RPC_HOST": "env-host",
            "ARIA2_RPC_PORT": "7000",
            "ARIA2_RPC_PATH": "/env/path",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = Aria2Config(self.config_path)
            config.load()

            # Environment variables should override
            self.assertEqual(config.get("host"), "env-host")
            self.assertEqual(config.get("port"), 7000)
            self.assertEqual(config.get("path"), "/env/path")
            # File values should be used for non-env vars
            self.assertEqual(config.get("secret"), "file-secret")

    def test_invalid_json_in_file(self):
        """Test error handling for invalid JSON in config file."""
        with open(self.config_path, "w") as f:
            f.write('{"host": "test", invalid}')

        config = Aria2Config(self.config_path)

        with self.assertRaises(ConfigurationError) as context:
            config.load()

        self.assertIn("Invalid JSON", str(context.exception))

    def test_missing_required_fields(self):
        """Test error handling for missing required fields."""
        # The config loader has defaults, so we need to explicitly set invalid values
        invalid_configs = [
            {"host": "", "port": 6800},  # Empty host
            {"host": "localhost", "port": 0},  # Invalid port
        ]

        for invalid_config in invalid_configs:
            with open(self.config_path, "w") as f:
                json.dump(invalid_config, f)

            config = Aria2Config(self.config_path)

            with self.assertRaises(ConfigurationError):
                config.load()

    def test_invalid_port_value(self):
        """Test validation of port value."""
        invalid_configs = [
            {"host": "localhost", "port": -1},
            {"host": "localhost", "port": 70000},
            {"host": "localhost", "port": "invalid"},
        ]

        for invalid_config in invalid_configs:
            with open(self.config_path, "w") as f:
                json.dump(invalid_config, f)

            config = Aria2Config(self.config_path)

            with self.assertRaises(ConfigurationError):
                config.load()

    def test_invalid_timeout_value(self):
        """Test validation of timeout value."""
        invalid_configs = [
            {"host": "localhost", "port": 6800, "timeout": -100},
            {"host": "localhost", "port": 6800, "timeout": "invalid"},
        ]

        for invalid_config in invalid_configs:
            with open(self.config_path, "w") as f:
                json.dump(invalid_config, f)

            config = Aria2Config(self.config_path)

            with self.assertRaises(ConfigurationError):
                config.load()

    def test_empty_secret_string(self):
        """Test empty string for secret becomes None."""
        env_vars = {"ARIA2_RPC_SECRET": ""}

        with patch.dict(os.environ, env_vars, clear=True):
            config = Aria2Config(self.config_path)
            config.load()

            self.assertIsNone(config.get("secret"))

    def test_get_endpoint_url(self):
        """Test endpoint URL generation."""
        # HTTP with default path (null)
        config = Aria2Config(self.config_path)
        config.config = {
            "host": "localhost",
            "port": 6800,
            "path": None,
            "secure": False,
        }
        config._loaded = True
        self.assertEqual(config.get_endpoint_url(), "http://localhost:6800")

        # HTTP with custom path
        config.config = {
            "host": "localhost",
            "port": 6800,
            "path": "/jsonrpc",
            "secure": False,
        }
        self.assertEqual(config.get_endpoint_url(), "http://localhost:6800/jsonrpc")

        # HTTPS with custom path
        config.config = {
            "host": "example.com",
            "port": 443,
            "path": "/api/rpc",
            "secure": True,
        }
        self.assertEqual(config.get_endpoint_url(), "https://example.com:443/api/rpc")

        # HTTPS reverse proxy
        config.config = {
            "host": "example.com",
            "port": 443,
            "path": "/jsonrpc",
            "secure": True,
        }
        self.assertEqual(config.get_endpoint_url(), "https://example.com:443/jsonrpc")

    def test_reload_preserves_on_error(self):
        """Test configuration reload preserves previous config on error."""
        valid_config = {"host": "localhost", "port": 6800}

        with open(self.config_path, "w") as f:
            json.dump(valid_config, f)

        config = Aria2Config(self.config_path)
        config.load()

        # Save current config
        old_host = config.get("host")

        # Write invalid config
        with open(self.config_path, "w") as f:
            f.write("invalid json")

        # Reload should preserve old config
        try:
            config.reload()
        except ConfigurationError:
            pass

        # Config should be unchanged
        self.assertEqual(config.get("host"), old_host)

    def test_get_all_returns_copy(self):
        """Test that get_all returns a copy, not reference."""
        config = Aria2Config(self.config_path)
        config.load()

        config_dict = config.get_all()
        config_dict["host"] = "modified"

        # Original should be unchanged
        self.assertNotEqual(config.get("host"), "modified")

    def test_path_null_or_empty(self):
        """Test path can be null or empty string."""
        # Null path
        test_config = {"host": "localhost", "port": 6800, "path": None}
        with open(self.config_path, "w") as f:
            json.dump(test_config, f)

        config = Aria2Config(self.config_path)
        config.load()
        self.assertIsNone(config.get("path"))
        self.assertEqual(config.get_endpoint_url(), "http://localhost:6800")

        # Empty string path via env var
        env_vars = {"ARIA2_RPC_PATH": ""}
        with patch.dict(os.environ, env_vars, clear=True):
            config = Aria2Config(self.config_path)
            config.load()
            self.assertIsNone(config.get("path"))

    def test_path_without_leading_slash(self):
        """Test path without leading slash is automatically prefixed."""
        env_vars = {"ARIA2_RPC_PATH": "jsonrpc"}
        with patch.dict(os.environ, env_vars, clear=True):
            config = Aria2Config(self.config_path)
            config.load()
            self.assertEqual(config.get("path"), "/jsonrpc")

    def test_path_invalid_type(self):
        """Test path must be string or null."""
        test_config = {"host": "localhost", "port": 6800, "path": 123}
        with open(self.config_path, "w") as f:
            json.dump(test_config, f)

        config = Aria2Config(self.config_path)
        with self.assertRaises(ConfigurationError) as context:
            config.load()
        self.assertIn("Path must be a string or null", str(context.exception))


if __name__ == "__main__":
    unittest.main()
