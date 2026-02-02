# Test commands for aria2-json-rpc-skills

# Run all tests (unit + mock server integration)
test:
    python3 -m unittest discover tests/unit && python3 tests/integration/test_mock_server.py

# Run unit tests only
test-unit:
    python3 -m unittest discover tests/unit

# Run mock server integration test only
test-mock-server:
    python3 tests/integration/test_mock_server.py

# Run specific test file (unittest format only)
test-file *path:
    python3 -m unittest {{path}}