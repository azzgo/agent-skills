#!/usr/bin/env python3
"""
Mock aria2 JSON-RPC server for integration testing.

Implements a minimal aria2 RPC server with Milestone 1 methods:
- aria2.addUri
- aria2.tellStatus
- aria2.remove
- aria2.getGlobalStat

Usage:
    python3 mock_aria2_server.py [--port 6800] [--verbose]
"""

import json
import http.server
import socketserver
import argparse
import sys
from datetime import datetime
from typing import Dict, List


class MockAria2RequestHandler(http.server.BaseHTTPRequestHandler):
    """Handle JSON-RPC requests like aria2 daemon."""

    # Mock download state storage
    downloads: Dict[str, Dict] = {}
    request_counter: int = 0

    def _send_json_response(self, data: dict, status: int = 200):
        """Send JSON response."""
        response = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def _generate_gid(self) -> str:
        """Generate a mock GID."""
        import uuid

        return uuid.uuid4().hex[:16]

    def _log_request(self, method: str, params: list):
        """Log incoming request."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {method} {params}")

    def _handle_addUri(self, params: list) -> str:
        """Handle aria2.addUri request."""
        uris = params[0] if len(params) > 0 else []
        options = params[1] if len(params) > 1 else {}

        # Generate new GID
        gid = self._generate_gid()

        # Store download state
        total_length = 1024 * 1024 * 100  # 100 MB
        self.downloads[gid] = {
            "gid": gid,
            "status": "active",
            "totalLength": str(total_length),
            "completedLength": "0",
            "uploadLength": "0",
            "downloadSpeed": "0",
            "uploadSpeed": "0",
            "errorCode": "0",
            "errorMessage": "",
            "followedBy": [],
            "belongsTo": "0",
            "dir": options.get("dir", "/tmp"),
            "files": [
                {
                    "path": f"{options.get('dir', '/tmp')}/{options.get('out', 'file.zip')}",
                    "uris": uris,
                }
            ],
        }

        return gid

    def _handle_tellStatus(self, params: list) -> dict:
        """Handle aria2.tellStatus request."""
        gid = params[0] if len(params) > 0 else ""

        if gid not in self.downloads:
            raise Exception(f"GID {gid} not found")

        # Return copy of download status
        status = self.downloads[gid].copy()

        # Simulate progress for active downloads
        if status["status"] == "active":
            completed = int(status["completedLength"])
            total = int(status["totalLength"])
            download_speed = 1024 * 1024  # 1 MB/s

            completed = min(completed + download_speed, total)
            status["completedLength"] = str(completed)
            status["downloadSpeed"] = str(download_speed)

            if completed >= total:
                status["status"] = "complete"
                status["downloadSpeed"] = "0"

            # Update stored state
            self.downloads[gid].update(
                {
                    "completedLength": status["completedLength"],
                    "downloadSpeed": status["downloadSpeed"],
                    "status": status["status"],
                }
            )

        return status

    def _handle_remove(self, params: list) -> str:
        """Handle aria2.remove request."""
        gid = params[0] if len(params) > 0 else ""

        if gid not in self.downloads:
            raise Exception(f"GID {gid} not found")

        self.downloads[gid]["status"] = "removed"
        return gid

    def _handle_getGlobalStat(self) -> dict:
        """Handle aria2.getGlobalStat request."""
        # Count downloads by status
        num_active = sum(1 for d in self.downloads.values() if d["status"] == "active")
        num_waiting = sum(
            1 for d in self.downloads.values() if d["status"] in ["waiting", "paused"]
        )
        num_stopped = sum(
            1
            for d in self.downloads.values()
            if d["status"] in ["removed", "complete", "error"]
        )

        return {
            "downloadSpeed": str(
                num_active * 1024 * 1024
            ),  # 1 MB/s per active download
            "uploadSpeed": "0",
            "numActive": str(num_active),
            "numWaiting": str(num_waiting),
            "numStopped": str(num_stopped),
            "numStoppedTotal": str(num_stopped),
        }

    def _handle_pause(self, params: list) -> str:
        """Handle aria2.pause request."""
        gid = params[0] if len(params) > 0 else ""
        if gid not in self.downloads:
            raise Exception(f"GID {gid} not found")
        if self.downloads[gid]["status"] != "active":
            raise Exception(f"GID {gid} is not active")
        self.downloads[gid]["status"] = "paused"
        return gid

    def _handle_pauseAll(self) -> str:
        """Handle aria2.pauseAll request."""
        paused_count = 0
        for gid, download in self.downloads.items():
            if download["status"] == "active":
                download["status"] = "paused"
                paused_count += 1
        return f"OK (paused {paused_count} downloads)"

    def _handle_unpause(self, params: list) -> str:
        """Handle aria2.unpause request."""
        gid = params[0] if len(params) > 0 else ""
        if gid not in self.downloads:
            raise Exception(f"GID {gid} not found")
        if self.downloads[gid]["status"] != "paused":
            raise Exception(f"GID {gid} is not paused")
        self.downloads[gid]["status"] = "active"
        return gid

    def _handle_unpauseAll(self) -> str:
        """Handle aria2.unpauseAll request."""
        resumed_count = 0
        for gid, download in self.downloads.items():
            if download["status"] == "paused":
                download["status"] = "active"
                resumed_count += 1
        return f"OK (resumed {resumed_count} downloads)"

    def _handle_tellActive(self, params: list = None) -> list:
        """Handle aria2.tellActive request."""
        active_downloads = [
            d for d in self.downloads.values() if d["status"] == "active"
        ]
        return active_downloads[:100]  # Limit to 100 results

    def _handle_tellWaiting(self, params: list) -> list:
        """Handle aria2.tellWaiting request."""
        offset = params[0] if len(params) > 0 else 0
        num = params[1] if len(params) > 1 else 100
        waiting = [
            d for d in self.downloads.values() if d["status"] in ["waiting", "paused"]
        ]
        return waiting[offset : offset + num]

    def _handle_tellStopped(self, params: list) -> list:
        """Handle aria2.tellStopped request."""
        offset = params[0] if len(params) > 0 else 0
        num = params[1] if len(params) > 1 else 100
        stopped = [
            d
            for d in self.downloads.values()
            if d["status"] in ["removed", "complete", "error"]
        ]
        return stopped[offset : offset + num]

    def _handle_getOption(self, params: list) -> dict:
        """Handle aria2.getOption request."""
        gid = params[0] if len(params) > 0 else ""
        if gid not in self.downloads:
            raise Exception(f"GID {gid} not found")
        # Return default options
        return {
            "dir": self.downloads[gid].get("dir", "/tmp"),
            "max-download-limit": "0",
            "max-upload-limit": "0",
            "split": "5",
            "max-connection-per-server": "1",
        }

    def _handle_changeOption(self, params: list) -> str:
        """Handle aria2.changeOption request."""
        gid = params[0] if len(params) > 0 else ""
        options = params[1] if len(params) > 1 else {}
        if gid not in self.downloads:
            raise Exception(f"GID {gid} not found")
        # Store options in download
        self.downloads[gid].update(options)
        return "OK"

    def _handle_getGlobalOption(self) -> dict:
        """Handle aria2.getGlobalOption request."""
        return {
            "max-overall-download-limit": "0",
            "max-overall-upload-limit": "0",
            "max-concurrent-downloads": "5",
            "split": "5",
            "seed-time": "30",
        }

    def _handle_changeGlobalOption(self, params: list) -> str:
        """Handle aria2.changeGlobalOption request."""
        # In a real implementation, this would modify global settings
        return "OK"

    def _handle_purgeDownloadResult(self) -> str:
        """Handle aria2.purgeDownloadResult request."""
        # Remove completed/error downloads from history
        to_remove = [
            gid
            for gid, d in self.downloads.items()
            if d["status"] in ["complete", "error"]
        ]
        for gid in to_remove:
            del self.downloads[gid]
        return f"OK (removed {len(to_remove)} results)"

    def _handle_removeDownloadResult(self, params: list) -> str:
        """Handle aria2.removeDownloadResult request."""
        gid = params[0] if len(params) > 0 else ""
        if gid not in self.downloads:
            raise Exception(f"GID {gid} not found")
        if self.downloads[gid]["status"] not in ["complete", "error"]:
            raise Exception(f"GID {gid} is not a completed download")
        del self.downloads[gid]
        return "OK"

    def _handle_addTorrent(self, params: list) -> str:
        """Handle aria2.addTorrent request (base64 encoded torrent)."""
        # For mock, we accept the base64 data but don't actually process it
        options = params[1] if len(params) > 1 else {}
        gid = self._generate_gid()
        total_length = 1024 * 1024 * 500  # 500 MB mock size
        self.downloads[gid] = {
            "gid": gid,
            "status": "active",
            "totalLength": str(total_length),
            "completedLength": "0",
            "uploadLength": "0",
            "downloadSpeed": "0",
            "uploadSpeed": "0",
            "errorCode": "0",
            "errorMessage": "",
            "followedBy": [],
            "belongsTo": "0",
            "dir": options.get("dir", "/tmp"),
            "files": [
                {"path": f"{options.get('dir', '/tmp')}/torrent-download", "uris": []}
            ],
            "bittorrent": {"info": {"name": "torrent-download"}},
        }
        return gid

    def _handle_addMetalink(self, params: list) -> list:
        """Handle aria2.addMetalink request (base64 encoded metalink)."""
        # For mock, we accept the base64 data but don't actually process it
        options = params[1] if len(params) > 1 else {}
        gid = self._generate_gid()
        total_length = 1024 * 1024 * 200  # 200 MB mock size
        self.downloads[gid] = {
            "gid": gid,
            "status": "active",
            "totalLength": str(total_length),
            "completedLength": "0",
            "uploadLength": "0",
            "downloadSpeed": "0",
            "uploadSpeed": "0",
            "errorCode": "0",
            "errorMessage": "",
            "followedBy": [],
            "belongsTo": "0",
            "dir": options.get("dir", "/tmp"),
            "files": [
                {"path": f"{options.get('dir', '/tmp')}/metalink-download", "uris": []}
            ],
        }
        return [gid]  # Returns array of GIDs

    def _handle_jsonrpc_request(self, request: dict) -> dict:
        """Handle JSON-RPC 2.0 request."""
        method = request.get("method", "")
        params = request.get("params", [])
        request_id = request.get("id", "")

        # Log request
        self._log_request(method, params)

        # Remove token if present
        if params and isinstance(params[0], str) and params[0].startswith("token:"):
            params = params[1:]

        try:
            # Route to method handler
            if method == "aria2.addUri":
                result = self._handle_addUri(params)
            elif method == "aria2.tellStatus":
                result = self._handle_tellStatus(params)
            elif method == "aria2.remove":
                result = self._handle_remove(params)
            elif method == "aria2.getGlobalStat":
                result = self._handle_getGlobalStat()
            elif method == "aria2.getVersion":
                result = {
                    "version": "1.36.0",
                    "enabledFeatures": ["BitTorrent", "Metalink", "SFTP"],
                }
            elif method == "aria2.pause":
                result = self._handle_pause(params)
            elif method == "aria2.pauseAll":
                result = self._handle_pauseAll()
            elif method == "aria2.unpause":
                result = self._handle_unpause(params)
            elif method == "aria2.unpauseAll":
                result = self._handle_unpauseAll()
            elif method == "aria2.tellActive":
                result = self._handle_tellActive(params)
            elif method == "aria2.tellWaiting":
                result = self._handle_tellWaiting(params)
            elif method == "aria2.tellStopped":
                result = self._handle_tellStopped(params)
            elif method == "aria2.getOption":
                result = self._handle_getOption(params)
            elif method == "aria2.changeOption":
                result = self._handle_changeOption(params)
            elif method == "aria2.getGlobalOption":
                result = self._handle_getGlobalOption()
            elif method == "aria2.changeGlobalOption":
                result = self._handle_changeGlobalOption(params)
            elif method == "aria2.purgeDownloadResult":
                result = self._handle_purgeDownloadResult()
            elif method == "aria2.removeDownloadResult":
                result = self._handle_removeDownloadResult(params)
            elif method == "aria2.addTorrent":
                result = self._handle_addTorrent(params)
            elif method == "aria2.addMetalink":
                result = self._handle_addMetalink(params)
            elif method == "system.listMethods":
                result = [
                    "aria2.addUri",
                    "aria2.addTorrent",
                    "aria2.addMetalink",
                    "aria2.tellStatus",
                    "aria2.tellActive",
                    "aria2.tellWaiting",
                    "aria2.tellStopped",
                    "aria2.remove",
                    "aria2.removeDownloadResult",
                    "aria2.pause",
                    "aria2.pauseAll",
                    "aria2.unpause",
                    "aria2.unpauseAll",
                    "aria2.getGlobalStat",
                    "aria2.getVersion",
                    "aria2.getOption",
                    "aria2.changeOption",
                    "aria2.getGlobalOption",
                    "aria2.changeGlobalOption",
                    "aria2.purgeDownloadResult",
                    "system.listMethods",
                    "system.multicall",
                ]
            else:
                raise Exception(f"Method not found: {method}")

            return {"jsonrpc": "2.0", "id": request_id, "result": result}
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": 1, "message": str(e)},
            }

    def do_GET(self):
        """Handle GET requests (health check)."""
        if self.path == "/health":
            self._send_json_response({"status": "healthy", "service": "mock-aria2"})
        else:
            self._send_json_response({"error": "Not found", "path": self.path}, 404)

    def do_POST(self):
        """Handle POST requests."""
        if self.path != "/jsonrpc":
            self._send_json_response(
                {
                    "jsonrpc": "2.0",
                    "id": "",
                    "error": {"code": -32601, "message": "Method not found"},
                },
                404,
            )
            return

        try:
            # Read and parse request
            content_length = int(self.headers.get("Content-Length", 0))
            request_body = self.rfile.read(content_length)
            request = json.loads(request_body.decode("utf-8"))

            # Handle JSON-RPC request
            response = self._handle_jsonrpc_request(request)
            self._send_json_response(response)

        except json.JSONDecodeError as e:
            self._send_json_response(
                {
                    "jsonrpc": "2.0",
                    "id": "",
                    "error": {"code": -32700, "message": "Parse error", "data": str(e)},
                },
                400,
            )
        except Exception as e:
            self._send_json_response(
                {
                    "jsonrpc": "2.0",
                    "id": "",
                    "error": {
                        "code": -32603,
                        "message": "Internal error",
                        "data": str(e),
                    },
                },
                500,
            )

    def log_message(self, format, *args):
        """Override to control logging."""
        # Only log if server has verbose flag set
        server = getattr(self, "server", None)
        if server and getattr(server, "verbose", False):
            super().log_message(format, *args)


def run_server(port: int = 6800, verbose: bool = False):
    """Start the mock aria2 server."""
    with socketserver.TCPServer(("0.0.0.0", port), MockAria2RequestHandler) as server:
        server.verbose = verbose
        print(f"Mock aria2 server listening on port {port}")
        print("Supported methods:")
        print("  - aria2.addUri")
        print("  - aria2.tellStatus")
        print("  - aria2.remove")
        print("  - aria2.getGlobalStat")
        print("  - aria2.getVersion")
        print("  - system.listMethods")
        print()

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down mock aria2 server")
            server.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Mock aria2 JSON-RPC server for testing"
    )
    parser.add_argument(
        "--port", type=int, default=6800, help="Server port (default: 6800)"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()
    run_server(args.port, args.verbose)
