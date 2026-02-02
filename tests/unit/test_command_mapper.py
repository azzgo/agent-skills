#!/usr/bin/env python3
"""
Unit tests for natural language command mapper.

Tests command parsing, method selection, and parameter extraction.
"""

import unittest
import sys
import os

# Add scripts directory to path
script_dir = os.path.join(
    os.path.dirname(__file__), "..", "..", "skills", "aria2-json-rpc", "scripts"
)
sys.path.insert(0, script_dir)
from command_mapper import CommandMapper


class TestCommandMapper(unittest.TestCase):
    """Test natural language command mapping."""

    def setUp(self):
        """Set up test fixtures."""
        self.mapper = CommandMapper()

    def test_download_http_url(self):
        """Test parsing download command with HTTP URL."""
        result = self.mapper.map_command("download http://example.com/file.zip")

        self.assertIsNotNone(result)
        method, params = result
        self.assertEqual(method, "aria2.addUri")
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0], ["http://example.com/file.zip"])

    def test_download_https_url(self):
        """Test parsing download command with HTTPS URL."""
        result = self.mapper.map_command("download https://example.com/file.iso")

        self.assertIsNotNone(result)
        method, params = result
        self.assertEqual(method, "aria2.addUri")
        self.assertEqual(params[0], ["https://example.com/file.iso"])

    def test_download_ftp_url(self):
        """Test parsing download command with FTP URL."""
        result = self.mapper.map_command("fetch ftp://mirror.org/archive.tar.gz")

        self.assertIsNotNone(result)
        method, params = result
        self.assertEqual(method, "aria2.addUri")
        self.assertEqual(params[0], ["ftp://mirror.org/archive.tar.gz"])

    def test_download_magnet_link(self):
        """Test parsing download command with magnet link."""
        magnet_link = "magnet:?xt=urn:btih:1234567890abcdef"
        result = self.mapper.map_command(f"download {magnet_link}")

        self.assertIsNotNone(result)
        method, params = result
        self.assertEqual(method, "aria2.addUri")
        self.assertEqual(params[0], [magnet_link])

    def test_show_status_with_full_gid(self):
        """Test parsing show status command with full 16-char GID."""
        gid = "2089b05ecca3d829"
        result = self.mapper.map_command(f"show status for GID {gid}")

        self.assertIsNotNone(result)
        method, params = result
        self.assertEqual(method, "aria2.tellStatus")
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0], gid)

    def test_check_status_with_gid(self):
        """Test parsing check status command."""
        gid = "1234567890abcdef"
        result = self.mapper.map_command(f"check status {gid}")

        self.assertIsNotNone(result)
        method, params = result
        self.assertEqual(method, "aria2.tellStatus")
        self.assertEqual(params[0], gid)

    def test_remove_download_with_gid(self):
        """Test parsing remove download command."""
        gid = "2089b05ecca3d829"
        result = self.mapper.map_command(f"remove GID {gid}")

        self.assertIsNotNone(result)
        method, params = result
        self.assertEqual(method, "aria2.remove")
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0], gid)

    def test_delete_download_with_gid(self):
        """Test parsing delete download command."""
        gid = "1234567890abcdef"
        result = self.mapper.map_command(f"delete {gid}")

        self.assertIsNotNone(result)
        method, params = result
        self.assertEqual(method, "aria2.remove")
        self.assertEqual(params[0], gid)

    def test_show_global_stats(self):
        """Test parsing show global stats command."""
        result = self.mapper.map_command("show global stats")

        self.assertIsNotNone(result)
        method, params = result
        self.assertEqual(method, "aria2.getGlobalStat")
        self.assertEqual(len(params), 0)

    def test_get_global_statistics(self):
        """Test parsing get global statistics command."""
        result = self.mapper.map_command("get global statistics")

        self.assertIsNotNone(result)
        method, params = result
        self.assertEqual(method, "aria2.getGlobalStat")
        self.assertEqual(len(params), 0)

    def test_whats_downloading(self):
        """Test parsing 'what's downloading' command."""
        result = self.mapper.map_command("what's downloading")

        self.assertIsNotNone(result)
        method, params = result
        self.assertEqual(method, "aria2.getGlobalStat")
        self.assertEqual(len(params), 0)

    def test_unrecognized_command(self):
        """Test handling unrecognized command."""
        result = self.mapper.map_command("this command is not recognized")

        self.assertIsNone(result)

    def test_incomplete_gid_too_short(self):
        """Test handling incomplete GID (too short)."""
        result = self.mapper.map_command("show status for abc123")

        self.assertIsNone(result)

    def test_incomplete_gid_not_hex(self):
        """Test handling incomplete GID (not hex)."""
        result = self.mapper.map_command("show status for 1234567890ghijkl")

        self.assertIsNone(result)

    def test_remove_with_full_gid(self):
        """Test remove command requires full GID."""
        gid = "2089b05ecca3d829"
        result = self.mapper.map_command(f"remove download {gid}")

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "aria2.remove")

    def test_case_insensitive_matching(self):
        """Test case-insensitive command matching."""
        commands = [
            "DOWNLOAD http://example.com/file.zip",
            "Show Status for GID 2089b05ecca3d829",
            "SHOW GLOBAL STATS",
        ]

        for cmd in commands:
            result = self.mapper.map_command(cmd)
            self.assertIsNotNone(result, f"Command should match: {cmd}")

    def test_supported_commands_structure(self):
        """Test get_supported_commands returns proper structure."""
        commands = self.mapper.get_supported_commands()

        self.assertIsInstance(commands, dict)
        self.assertIn("add_uri", commands)
        self.assertIn("tell_status", commands)
        self.assertIn("remove", commands)
        self.assertIn("get_global_stat", commands)

        # Each method should have a list of example commands
        for method, examples in commands.items():
            self.assertIsInstance(examples, list)
            self.assertTrue(len(examples) > 0)
            for example in examples:
                self.assertIsInstance(example, str)

    def test_whitespace_handling(self):
        """Test handling of extra whitespace."""
        result = self.mapper.map_command("  download   http://example.com/file.zip  ")

        self.assertIsNotNone(result)
        method, params = result
        self.assertEqual(method, "aria2.addUri")


if __name__ == "__main__":
    unittest.main()
