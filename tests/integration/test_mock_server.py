#!/usr/bin/env python3
"""
Test mock aria2 server integration.

This script tests the mock server to ensure it responds correctly to JSON-RPC requests.
"""

import json
import http.client
import time
import subprocess
import sys
import os


def test_mock_server(port=16801):
    """Test the mock aria2 server."""
    # Start mock server in background
    server_script = os.path.join(os.path.dirname(__file__), "mock_aria2_server.py")

    print("Starting mock aria2 server...")
    server_process = subprocess.Popen(
        [sys.executable, server_script, "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for server to start
    time.sleep(2)

    try:
        # Test 1: getGlobalStat
        print("\nTest 1: aria2.getGlobalStat")
        conn = http.client.HTTPConnection("localhost", port)
        headers = {"Content-Type": "application/json"}

        request = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "aria2.getGlobalStat",
            "params": [],
        }

        conn.request("POST", "/jsonrpc", json.dumps(request), headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode())

        print(f"  Status: {response.status}")
        print(f"  Response: {json.dumps(data, indent=4)}")

        if "result" in data:
            print("  ✓ Test passed")
        else:
            print("  ✗ Test failed")

        conn.close()

        # Test 2: addUri
        print("\nTest 2: aria2.addUri")
        conn = http.client.HTTPConnection("localhost", port)

        request = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "aria2.addUri",
            "params": [["http://example.com/file.zip"]],
        }

        conn.request("POST", "/jsonrpc", json.dumps(request), headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode())

        print(f"  Status: {response.status}")
        print(f"  Response: {json.dumps(data, indent=4)}")

        if "result" in data and "gid" in str(data["result"]):
            print("  ✓ Test passed")
            gid = data["result"]
        else:
            print("  ✗ Test failed")
            gid = None

        conn.close()

        # Test 3: tellStatus (if we got a GID)
        if gid:
            print("\nTest 3: aria2.tellStatus")
            conn = http.client.HTTPConnection("localhost", port)

            request = {
                "jsonrpc": "2.0",
                "id": "3",
                "method": "aria2.tellStatus",
                "params": [gid],
            }

            conn.request("POST", "/jsonrpc", json.dumps(request), headers)
            response = conn.getresponse()
            data = json.loads(response.read().decode())

            print(f"  Status: {response.status}")
            print(f"  Response: {json.dumps(data, indent=4)}")

            if "result" in data and data["result"].get("gid") == gid:
                print("  ✓ Test passed")
            else:
                print("  ✗ Test failed")

            conn.close()

            # Test 4: remove
            print("\nTest 4: aria2.remove")
            conn = http.client.HTTPConnection("localhost", port)

            request = {
                "jsonrpc": "2.0",
                "id": "4",
                "method": "aria2.remove",
                "params": [gid],
            }

            conn.request("POST", "/jsonrpc", json.dumps(request), headers)
            response = conn.getresponse()
            data = json.loads(response.read().decode())

            print(f"  Status: {response.status}")
            print(f"  Response: {json.dumps(data, indent=4)}")

            if "result" in data and data["result"] == gid:
                print("  ✓ Test passed")
            else:
                print("  ✗ Test failed")

            conn.close()

        print("\n✓ All tests completed successfully")

    except Exception as e:
        print(f"\n✗ Test error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        # Stop server
        print("\nStopping mock aria2 server...")
        server_process.terminate()
        server_process.wait(timeout=5)


if __name__ == "__main__":
    test_mock_server()
