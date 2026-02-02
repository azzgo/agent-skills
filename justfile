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

# Manual testing setup
manual-test-setup:
    @echo "Setting up manual test environment..."
    @mkdir -p .manual-test/.opencode/skills
    @mkdir -p .manual-test/.opencode/command
    @mkdir -p .manual-test/results
    @echo "Creating symlinks..."
    @ln -sfn ../../skills/aria2-json-rpc .manual-test/.opencode/skills/aria2-json-rpc
    @echo "Copying test documentation..."
    @cp docs/manual-test/instruct.md .manual-test/instruct.md
    @cp docs/manual-test/test-aria2.md .manual-test/.opencode/command/test-aria2.md
    @cp docs/manual-test/README.md .manual-test/README.md
    @echo "Creating test config..."
    @cp skills/aria2-json-rpc/assets/config.example.json .manual-test/config.json
    @echo "✓ Manual test environment ready"

manual-test-start-aria2 port secret:
    @PORT={{port}} SECRET={{secret}}
    @echo "Starting aria2 daemon on port ${PORT:-6800}..."
    @if pgrep -f "aria2c.*--rpc-listen-port.*${PORT:-6800}" > /dev/null; then \
        echo "✓ aria2 daemon already running on port ${PORT:-6800}"; \
    else \
        aria2c \
            --enable-rpc \
            --rpc-listen-all=true \
            --rpc-listen-port=${PORT:-6800} \
            --rpc-secret=${SECRET} \
            --rpc-allow-origin-all \
            --dir=/tmp/aria2-test-downloads \
            --log=/tmp/aria2-test.log \
            -D \
            && echo "✓ aria2 daemon started on port ${PORT:-6800}" \
            && echo "  Download directory: /tmp/aria2-test-downloads" \
            && echo "  Log file: /tmp/aria2-test.log"; \
    fi

manual-test-stop-aria2:
    @echo "Stopping aria2 daemon..."
    @pkill -f "aria2c.*--enable-rpc" && echo "✓ aria2 daemon stopped" || echo "✗ aria2 daemon not running"

manual-test-status:
    @echo "Manual test environment status:"
    @echo ""
    @if [ -d ".manual-test" ]; then echo "✓ Test directory exists"; else echo "✗ Test directory missing"; fi
    @if [ -L ".manual-test/.opencode/skills/aria2-json-rpc" ]; then echo "✓ Skill symlink exists"; else echo "✗ Skill symlink missing"; fi
    @if [ -f ".manual-test/config.json" ]; then echo "✓ Test config exists"; else echo "✗ Test config missing"; fi
    @if [ -f ".manual-test/instruct.md" ]; then echo "✓ Test instructions exist"; else echo "✗ Test instructions missing"; fi
    @echo ""
    @if pgrep -f "aria2c.*--enable-rpc" > /dev/null; then \
        echo "✓ aria2 daemon: RUNNING"; \
    else \
        echo "✗ aria2 daemon: NOT RUNNING"; \
    fi

manual-test-run:
    @echo "Running manual tests..."
    @echo ""
    @echo "Prerequisites:"
    @echo "1. Start aria2 daemon: just manual-test-start-aria2 6800 test-secret"
    @echo "2. Load aria2-json-rpc skill in OpenCode from .manual-test/.opencode/skills/"
    @echo "3. Use instructions from .manual-test/instruct.md"
    @echo ""
    @echo "Test results will be saved to .manual-test/results/"

manual-test-clean:
    @echo "Cleaning manual test environment..."
    @just manual-test-stop-aria2
    @rm -rf .manual-test
    @rm -rf /tmp/aria2-test-downloads
    @echo "✓ Manual test environment cleaned"