#!/usr/bin/env python3
"""
Configuration loader for aria2-json-rpc skill.

Supports three-tier configuration priority:
1. Environment variables (highest priority)
2. config.json file in skill directory
3. Interactive defaults (fallback)

Configuration schema:
{
    "host": "localhost",
    "port": 6800,
    "secret": null,
    "secure": false,
    "timeout": 30000
}
"""

import json
import os
import sys
import urllib.request
import urllib.error


class ConfigurationError(Exception):
    """Raised when configuration is invalid or cannot be loaded."""

    pass


class Aria2Config:
    """
    Manages aria2 RPC configuration with multi-source loading.
    """

    DEFAULT_CONFIG = {
        "host": "localhost",
        "port": 6800,
        "secret": None,
        "secure": False,
        "timeout": 30000,
    }

    # Environment variable names
    ENV_PREFIX = "ARIA2_RPC_"
    ENV_VARS = {
        "host": "ARIA2_RPC_HOST",
        "port": "ARIA2_RPC_PORT",
        "secret": "ARIA2_RPC_SECRET",
        "secure": "ARIA2_RPC_SECURE",
        "timeout": "ARIA2_RPC_TIMEOUT",
    }

    def __init__(self, config_path=None):
        """
        Initialize configuration loader.

        Args:
            config_path (str, optional): Path to config.json file.
                                        Defaults to skills/aria2-json-rpc/config.json
        """
        self.config_path = config_path or self._get_default_config_path()
        self.config = self.DEFAULT_CONFIG.copy()
        self._loaded = False

    def _get_default_config_path(self):
        """Get the default path to config.json in the skill directory."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        skill_dir = os.path.dirname(script_dir)
        return os.path.join(skill_dir, "config.json")

    def load(self):
        """
        Load configuration from all sources with priority resolution.

        Priority: Environment Variables > config.json > Defaults

        Returns:
            dict: Loaded configuration

        Raises:
            ConfigurationError: If configuration is invalid
        """
        # Start with defaults
        config = self.DEFAULT_CONFIG.copy()

        # Load from config.json if it exists
        if os.path.exists(self.config_path):
            try:
                file_config = self._load_from_file(self.config_path)
                config.update(file_config)
            except Exception as e:
                raise ConfigurationError(
                    f"Failed to load config from {self.config_path}: {e}"
                )

        # Override with environment variables
        env_config = self._load_from_env()
        config.update(env_config)

        # Validate configuration
        self._validate_config(config)

        self.config = config
        self._loaded = True
        return config

    def _load_from_file(self, path):
        """
        Load configuration from JSON file.

        Args:
            path (str): Path to config.json

        Returns:
            dict: Configuration from file

        Raises:
            ConfigurationError: If file is invalid JSON or unreadable
        """
        try:
            with open(path, "r") as f:
                file_config = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigurationError(
                f"Invalid JSON in config file: {path}\n"
                f"Error at line {e.lineno}, column {e.colno}: {e.msg}\n"
                f"Example valid structure:\n"
                f"{json.dumps(self.DEFAULT_CONFIG, indent=2)}"
            )
        except PermissionError:
            raise ConfigurationError(
                f"Permission denied reading config file: {path}\n"
                f"Please check file permissions: chmod 644 {path}"
            )
        except Exception as e:
            raise ConfigurationError(f"Error reading config file: {e}")

        return file_config

    def _load_from_env(self):
        """
        Load configuration from environment variables.

        Returns:
            dict: Configuration from environment variables
        """
        env_config = {}

        for key, env_var in self.ENV_VARS.items():
            value = os.environ.get(env_var)
            if value is not None:
                # Type conversion based on expected type
                if key == "port" or key == "timeout":
                    try:
                        env_config[key] = int(value)
                    except ValueError:
                        print(
                            f"WARNING: Invalid {env_var}={value}, expected integer. Ignoring."
                        )
                elif key == "secure":
                    env_config[key] = value.lower() in ("true", "1", "yes")
                elif key == "secret":
                    # Empty string means no secret
                    env_config[key] = value if value else None
                else:
                    env_config[key] = value

        return env_config

    def _validate_config(self, config):
        """
        Validate configuration values.

        Args:
            config (dict): Configuration to validate

        Raises:
            ConfigurationError: If configuration is invalid
        """
        # Validate required fields
        if not config.get("host"):
            raise ConfigurationError(
                "Missing required field: 'host'\n"
                f"Example configuration:\n{json.dumps(self.DEFAULT_CONFIG, indent=2)}"
            )

        if (
            not isinstance(config.get("port"), int)
            or config["port"] <= 0
            or config["port"] > 65535
        ):
            raise ConfigurationError(
                f"Invalid port: {config.get('port')}. Must be integer between 1-65535."
            )

        if not isinstance(config.get("timeout"), int) or config["timeout"] <= 0:
            raise ConfigurationError(
                f"Invalid timeout: {config.get('timeout')}. Must be positive integer (milliseconds)."
            )

        # Validate optional fields
        if config.get("secret") is not None and not isinstance(config["secret"], str):
            raise ConfigurationError("Secret must be a string or null")

        if not isinstance(config.get("secure"), bool):
            raise ConfigurationError("Secure must be a boolean (true/false)")

    def test_connection(self):
        """
        Test connection to aria2 RPC endpoint.

        Returns:
            bool: True if connection successful, False otherwise
        """
        if not self._loaded:
            self.load()

        # Build URL
        protocol = "https" if self.config["secure"] else "http"
        url = f"{protocol}://{self.config['host']}:{self.config['port']}/jsonrpc"

        # Create a simple test request (aria2.getVersion)
        request_data = {
            "jsonrpc": "2.0",
            "id": "test-connection",
            "method": "aria2.getVersion",
            "params": [],
        }

        # Add token if configured
        if self.config.get("secret"):
            request_data["params"].insert(0, f"token:{self.config['secret']}")

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(request_data).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )

            timeout_sec = self.config["timeout"] / 1000.0
            response = urllib.request.urlopen(req, timeout=timeout_sec)
            result = json.loads(response.read().decode("utf-8"))

            # Check for valid JSON-RPC response
            if "result" in result or "error" in result:
                return True
            else:
                return False

        except urllib.error.URLError as e:
            print(f"Connection test failed: {e}")
            return False
        except Exception as e:
            print(f"Connection test error: {e}")
            return False

    def get(self, key, default=None):
        """Get configuration value."""
        if not self._loaded:
            self.load()
        return self.config.get(key, default)

    def get_all(self):
        """Get all configuration values."""
        if not self._loaded:
            self.load()
        return self.config.copy()

    def reload(self):
        """
        Reload configuration from all sources.

        Returns:
            dict: Reloaded configuration

        Note: If reload fails, previous configuration is preserved.
        """
        try:
            old_config = self.config.copy()
            self.config = self.DEFAULT_CONFIG.copy()
            self._loaded = False
            return self.load()
        except Exception as e:
            # Restore previous configuration on error
            self.config = old_config
            self._loaded = True
            raise ConfigurationError(
                f"Configuration reload failed: {e}\nPrevious configuration preserved."
            )

    def get_endpoint_url(self):
        """Get the full RPC endpoint URL."""
        if not self._loaded:
            self.load()

        protocol = "https" if self.config["secure"] else "http"
        return f"{protocol}://{self.config['host']}:{self.config['port']}/jsonrpc"


if __name__ == "__main__":
    # Test configuration loading
    print("Testing aria2 configuration loader...")
    print()

    try:
        config = Aria2Config()
        config.load()

        print("✓ Configuration loaded successfully")
        print()
        print("Configuration:")
        for key, value in config.get_all().items():
            if key == "secret" and value:
                print(f"  {key}: ****** (hidden)")
            else:
                print(f"  {key}: {value}")

        print()
        print(f"Endpoint URL: {config.get_endpoint_url()}")

        # Test connection
        print()
        print("Testing connection to aria2 RPC endpoint...")
        if config.test_connection():
            print("✓ Connection successful")
        else:
            print("✗ Connection failed (aria2 daemon may not be running)")

    except ConfigurationError as e:
        print(f"✗ Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)
