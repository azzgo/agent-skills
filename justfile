# Test commands for aria2-json-rpc-skills
# Uses UV for isolated dependency management (no global pollution)

# Run all tests (M1, M2, M3 with isolated dependencies)
test:
    @./run_tests.sh

# Run all unit tests only
test-unit:
    @./run_tests.sh

# Run Milestone 1 tests (core operations, no external deps)
test-m1:
    @./run_tests.sh milestone1

# Run Milestone 2 tests (advanced control, no external deps)
test-m2:
    @./run_tests.sh milestone2

# Run Milestone 3 tests (torrent/WebSocket, installs websockets in isolated env)
test-m3:
    @./run_tests.sh milestone3

# Run mock server integration test only
test-mock-server:
    python3 tests/integration/test_mock_server.py

# Run specific test file with UV (for files needing dependencies)
test-file-uv path:
    uv run python -m pytest {{path}} -v

# Run specific test file with unittest (no dependencies)
test-file path:
    python3 -m unittest {{path}}

# Install UV (one-time setup)
install-uv:
    @echo "Installing UV for dependency management..."
    @curl -LsSf https://astral.sh/uv/install.sh | sh
    @echo "✓ UV installed. You may need to restart your shell or run:"
    @echo "  export PATH=\"\$HOME/.cargo/bin:\$PATH\""

# Check if UV is installed
check-uv:
    @command -v uv >/dev/null 2>&1 && echo "✓ UV is installed" || (echo "✗ UV not found. Run 'just install-uv'"; exit 1)