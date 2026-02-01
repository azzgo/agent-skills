#!/usr/bin/env python3
"""
Natural language command mapping for aria2-json-rpc skill.

Maps natural language commands to aria2 RPC methods with parameter extraction.
Enables AI agents to interpret commands like:
- "download http://example.com/file.zip"
- "show status for GID 2089b05ecca3d829"
- "remove download 2089b05ecca3d829"
- "show global stats"
"""

import re
from typing import Dict, List, Any, Optional, Tuple


class CommandMapper:
    """
    Maps natural language commands to aria2 RPC method calls.

    Uses keyword detection and pattern matching for intent classification.
    """

    # Milestone 1 command patterns
    PATTERNS = {
        # addUri patterns - order matters, most specific first
        "add_uri": [
            r"^download\s+(https?://\S+|ftp://\S+|magnet:\S+|sftp://\S+)",
            r"^add\s+(?:download\s+)?(?:uri\s+)?(https?://\S+|ftp://\S+|magnet:\S+)",
            r"^fetch\s+(https?://\S+|ftp://\S+|sftp://\S+)",
        ],
        # tellStatus patterns - require full GID
        "tell_status": [
            r"^(?:show|get|check)\s+status\s+(?:for\s+)?(?:gid\s+)?([a-f0-9]{16})",
            r"^status\s+of\s+(?:gid\s+)?([a-f0-9]{16})",
        ],
        # remove patterns - require full GID
        "remove": [
            r"^remove\s+(?:download\s+)?(?:gid\s+)?([a-f0-9]{16})",
            r"^delete\s+(?:download\s+)?(?:gid\s+)?([a-f0-9]{16})",
            r"^cancel\s+(?:download\s+)?(?:gid\s+)?([a-f0-9]{16})",
        ],
        # getGlobalStat patterns - no parameters
        "get_global_stat": [
            r"^(?:show|get|display)\s+global\s+(?:stats?|statistics)",
            r"^(?:show|get)\s+(?:overall|all)\s+(?:stats?|statistics)",
            r"^what'?s\s+downloading\??$",
            r"^how\s+many\s+(?:downloads?|tasks?)\??$",
        ],
    }

    def __init__(self):
        """Initialize the command mapper."""
        self.compiled_patterns = {}
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns for faster matching."""
        for method, patterns in self.PATTERNS.items():
            self.compiled_patterns[method] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]

    def map_command(self, command: str) -> Optional[Tuple[str, List[Any]]]:
        """
        Map a natural language command to an aria2 RPC method and parameters.

        Args:
            command: Natural language command string

        Returns:
            Tuple of (method_name, params) if matched, None otherwise
            Example: ("aria2.addUri", [["http://example.com/file.zip"]])
        """
        command = command.strip()

        # Try each method's patterns
        for method, compiled_patterns in self.compiled_patterns.items():
            for pattern in compiled_patterns:
                match = pattern.search(command)
                if match:
                    # Extract parameters based on method
                    params = self._extract_params(method, match, command)
                    rpc_method = self._method_to_rpc(method)
                    return (rpc_method, params)

        return None

    def _method_to_rpc(self, method: str) -> str:
        """Convert internal method name to aria2 RPC method name."""
        mapping = {
            "add_uri": "aria2.addUri",
            "tell_status": "aria2.tellStatus",
            "remove": "aria2.remove",
            "get_global_stat": "aria2.getGlobalStat",
        }
        return mapping.get(method, method)

    def _extract_params(self, method: str, match: re.Match, command: str) -> List[Any]:
        """
        Extract parameters from regex match based on method type.

        Args:
            method: Internal method name
            match: Regex match object
            command: Original command string

        Returns:
            List of parameters for RPC method
        """
        if method == "add_uri":
            # Extract URIs (single URI from match group)
            uri = match.group(1).strip()

            # Return as array of URIs (aria2.addUri expects array of URIs)
            return [[uri]]

        elif method == "tell_status":
            # Extract GID
            gid = match.group(1).strip()
            return [gid]

        elif method == "remove":
            # Extract GID
            gid = match.group(1).strip()
            return [gid]

        elif method == "get_global_stat":
            # No parameters needed
            return []

        return []

    def _looks_like_uri(self, text: str) -> bool:
        """Check if text looks like a URI."""
        # Check for common URI schemes
        uri_schemes = ["http://", "https://", "ftp://", "sftp://", "magnet:", "file://"]
        text_lower = text.lower()

        for scheme in uri_schemes:
            if text_lower.startswith(scheme):
                return True

        # Check for common file extensions (might be relative path or filename)
        if any(
            text.endswith(ext)
            for ext in [".zip", ".tar", ".gz", ".iso", ".mp4", ".pdf", ".torrent"]
        ):
            return True

        return False

    def get_supported_commands(self) -> Dict[str, List[str]]:
        """
        Get documentation of supported commands.

        Returns:
            Dictionary mapping method names to example commands
        """
        return {
            "add_uri": [
                "download http://example.com/file.zip",
                "add download https://example.com/file.iso",
                "fetch ftp://mirror.org/archive.tar.gz",
            ],
            "tell_status": [
                "show status for GID 2089b05ecca3d829",
                "status of 2089b05ecca3d829",
                "check status 2089b05ecca3d829",
            ],
            "remove": [
                "remove download 2089b05ecca3d829",
                "delete 2089b05ecca3d829",
                "cancel download 2089b05ecca3d829",
            ],
            "get_global_stat": [
                "show global stats",
                "get global statistics",
                "what's downloading",
                "how many downloads",
            ],
        }


def main():
    """Test command mapping."""
    print("Testing natural language command mapper...")
    print()

    mapper = CommandMapper()

    # Test commands
    test_commands = [
        "download http://example.com/file.zip",
        "download http://example.com/file1.zip http://example.com/file2.zip",
        "show status for GID 2089b05ecca3d829",
        "status of abc123def456",
        "remove download 2089b05ecca3d829",
        "show global stats",
        "what's downloading",
        "this should not match anything",
    ]

    for command in test_commands:
        result = mapper.map_command(command)
        if result:
            method, params = result
            print(f"✓ '{command}'")
            print(f"  → {method}")
            print(f"  → params: {params}")
        else:
            print(f"✗ '{command}'")
            print(f"  → No match")
        print()

    # Show supported commands
    print("Supported Commands:")
    print()
    for method, examples in mapper.get_supported_commands().items():
        print(f"{method}:")
        for example in examples:
            print(f"  - {example}")
        print()


if __name__ == "__main__":
    main()
