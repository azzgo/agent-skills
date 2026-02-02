#!/usr/bin/env python3
"""
Configuration management for LLM evaluation system.

This module loads and validates configuration from config.yaml,
providing a centralized way to access settings for executor,
evaluator, and other components.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ModelConfig:
    """Model configuration."""

    name: str = "claude-3-5-sonnet-20241022"
    temperature: float = 0.7
    max_tokens: int = 4096


@dataclass
class AuthConfig:
    """Authentication configuration."""

    type: str = "none"  # 'none', 'bearer', 'api_key'
    token: str = ""
    api_key_header: str = "X-API-Key"


@dataclass
class ExecutorConfig:
    """Executor (Instance 1) configuration."""

    mode: str = "simulated"  # 'simulated' or 'opencode'
    api_endpoint: str = "http://localhost:8080"
    model: ModelConfig = field(default_factory=ModelConfig)
    timeout: int = 60
    enable_tracing: bool = True
    auth: AuthConfig = field(default_factory=AuthConfig)


@dataclass
class EvaluatorConfig:
    """Evaluator (Instance 2) configuration."""

    mode: str = "simulated"  # 'simulated' or 'opencode'
    api_endpoint: str = "http://localhost:8081"
    model: ModelConfig = field(default_factory=ModelConfig)
    timeout: int = 60
    criteria_weights: Dict[str, float] = field(
        default_factory=lambda: {
            "task_completion": 0.30,
            "rpc_correctness": 0.25,
            "reasoning_quality": 0.20,
            "error_handling": 0.15,
            "response_quality": 0.10,
        }
    )
    pass_threshold: float = 0.7
    auth: AuthConfig = field(default_factory=AuthConfig)


@dataclass
class MockServerConfig:
    """Mock server configuration."""

    port: int = 6800
    host: str = "localhost"
    verbose: bool = False


@dataclass
class OutputConfig:
    """Output configuration."""

    base_dir: str = "../results"
    generate_reports: bool = True
    report_formats: list = field(default_factory=lambda: ["json", "yaml", "text"])
    pretty_json: bool = True
    include_traces: bool = True


@dataclass
class LoggingConfig:
    """Logging configuration."""

    level: str = "INFO"
    log_to_file: bool = False
    log_file: str = "llm_eval.log"


@dataclass
class Config:
    """Main configuration container."""

    execution_mode: str = "simulated"
    executor: ExecutorConfig = field(default_factory=ExecutorConfig)
    evaluator: EvaluatorConfig = field(default_factory=EvaluatorConfig)
    mock_server: MockServerConfig = field(default_factory=MockServerConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)


class ConfigLoader:
    """Configuration loader with validation."""

    DEFAULT_CONFIG_FILE = "config.yaml"

    @staticmethod
    def load(config_path: Optional[Path] = None) -> Config:
        """
        Load configuration from YAML file.

        Args:
            config_path: Optional path to config file. If not provided,
                        looks for config.yaml in the module directory.

        Returns:
            Config object with loaded settings
        """
        # Determine config file path
        if config_path is None:
            config_path = Path(__file__).parent / ConfigLoader.DEFAULT_CONFIG_FILE

        # Check if config file exists
        if not config_path.exists():
            print(f"Warning: Config file not found at {config_path}, using defaults")
            return Config()

        # Load YAML
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config file: {e}, using defaults")
            return Config()

        # Parse configuration
        return ConfigLoader._parse_config(data)

    @staticmethod
    def _parse_config(data: Dict[str, Any]) -> Config:
        """Parse configuration data into Config object."""
        if not data:
            return Config()

        config = Config()

        # Global execution mode
        config.execution_mode = data.get("execution_mode", "simulated")

        # Parse executor config
        if "executor" in data:
            executor_data = data["executor"]
            config.executor = ExecutorConfig(
                mode=executor_data.get("mode", config.execution_mode),
                api_endpoint=executor_data.get("api_endpoint", "http://localhost:8080"),
                model=ConfigLoader._parse_model_config(executor_data.get("model", {})),
                timeout=executor_data.get("timeout", 60),
                enable_tracing=executor_data.get("enable_tracing", True),
                auth=ConfigLoader._parse_auth_config(executor_data.get("auth", {})),
            )

        # Parse evaluator config
        if "evaluator" in data:
            evaluator_data = data["evaluator"]
            config.evaluator = EvaluatorConfig(
                mode=evaluator_data.get("mode", config.execution_mode),
                api_endpoint=evaluator_data.get(
                    "api_endpoint", "http://localhost:8081"
                ),
                model=ConfigLoader._parse_model_config(evaluator_data.get("model", {})),
                timeout=evaluator_data.get("timeout", 60),
                criteria_weights=evaluator_data.get(
                    "criteria_weights",
                    {
                        "task_completion": 0.30,
                        "rpc_correctness": 0.25,
                        "reasoning_quality": 0.20,
                        "error_handling": 0.15,
                        "response_quality": 0.10,
                    },
                ),
                pass_threshold=evaluator_data.get("pass_threshold", 0.7),
                auth=ConfigLoader._parse_auth_config(evaluator_data.get("auth", {})),
            )

        # Parse mock server config
        if "mock_server" in data:
            ms_data = data["mock_server"]
            config.mock_server = MockServerConfig(
                port=ms_data.get("port", 6800),
                host=ms_data.get("host", "localhost"),
                verbose=ms_data.get("verbose", False),
            )

        # Parse output config
        if "output" in data:
            output_data = data["output"]
            config.output = OutputConfig(
                base_dir=output_data.get("base_dir", "../results"),
                generate_reports=output_data.get("generate_reports", True),
                report_formats=output_data.get(
                    "report_formats", ["json", "yaml", "text"]
                ),
                pretty_json=output_data.get("pretty_json", True),
                include_traces=output_data.get("include_traces", True),
            )

        # Parse logging config
        if "logging" in data:
            log_data = data["logging"]
            config.logging = LoggingConfig(
                level=log_data.get("level", "INFO"),
                log_to_file=log_data.get("log_to_file", False),
                log_file=log_data.get("log_file", "llm_eval.log"),
            )

        return config

    @staticmethod
    def _parse_model_config(data: Dict[str, Any]) -> ModelConfig:
        """Parse model configuration."""
        return ModelConfig(
            name=data.get("name", "claude-3-5-sonnet-20241022"),
            temperature=data.get("temperature", 0.7),
            max_tokens=data.get("max_tokens", 4096),
        )

    @staticmethod
    def _parse_auth_config(data: Dict[str, Any]) -> AuthConfig:
        """Parse authentication configuration."""
        return AuthConfig(
            type=data.get("type", "none"),
            token=data.get("token", ""),
            api_key_header=data.get("api_key_header", "X-API-Key"),
        )

    @staticmethod
    def validate_config(config: Config) -> bool:
        """
        Validate configuration settings.

        Args:
            config: Configuration to validate

        Returns:
            True if valid, raises ValueError if invalid
        """
        # Validate execution modes
        valid_modes = ["simulated", "opencode"]
        if config.executor.mode not in valid_modes:
            raise ValueError(f"Invalid executor mode: {config.executor.mode}")
        if config.evaluator.mode not in valid_modes:
            raise ValueError(f"Invalid evaluator mode: {config.evaluator.mode}")

        # Validate criteria weights sum to 1.0
        weights_sum = sum(config.evaluator.criteria_weights.values())
        if not (0.99 <= weights_sum <= 1.01):  # Allow small floating point errors
            raise ValueError(
                f"Evaluator criteria weights must sum to 1.0, got {weights_sum}"
            )

        # Validate pass threshold
        if not (0.0 <= config.evaluator.pass_threshold <= 1.0):
            raise ValueError(
                f"Pass threshold must be between 0.0 and 1.0, got {config.evaluator.pass_threshold}"
            )

        # Validate auth types
        valid_auth_types = ["none", "bearer", "api_key"]
        if config.executor.auth.type not in valid_auth_types:
            raise ValueError(f"Invalid executor auth type: {config.executor.auth.type}")
        if config.evaluator.auth.type not in valid_auth_types:
            raise ValueError(
                f"Invalid evaluator auth type: {config.evaluator.auth.type}"
            )

        return True


# Global config instance (lazy loaded)
_global_config: Optional[Config] = None


def get_config(config_path: Optional[Path] = None, reload: bool = False) -> Config:
    """
    Get global configuration instance.

    Args:
        config_path: Optional path to config file
        reload: Force reload configuration

    Returns:
        Config object
    """
    global _global_config

    if _global_config is None or reload:
        _global_config = ConfigLoader.load(config_path)
        ConfigLoader.validate_config(_global_config)

    return _global_config


if __name__ == "__main__":
    # Test configuration loading
    config = get_config()

    print("Configuration loaded successfully:")
    print(f"  Execution mode: {config.execution_mode}")
    print(f"  Executor mode: {config.executor.mode}")
    print(f"  Executor model: {config.executor.model.name}")
    print(f"  Executor API: {config.executor.api_endpoint}")
    print(f"  Evaluator mode: {config.evaluator.mode}")
    print(f"  Evaluator model: {config.evaluator.model.name}")
    print(f"  Evaluator API: {config.evaluator.api_endpoint}")
    print(f"  Mock server port: {config.mock_server.port}")
    print(f"  Output directory: {config.output.base_dir}")
    print(f"  Pass threshold: {config.evaluator.pass_threshold}")
