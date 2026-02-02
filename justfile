# Test commands for aria2-json-rpc-skills
# Uses UV for isolated dependency management (no global pollution)

# Run all unit tests
test:
    @./run_unit_tests.sh

# Run all unit tests (alias)
test-unit:
    @./run_unit_tests.sh

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
    @echo "Copying skill directory (isolated environment)..."
    @cp -r skills/aria2-json-rpc .manual-test/.opencode/skills/
    @echo "Copying test documentation..."
    @cp docs/manual-test/instruct.md .manual-test/instruct.md
    @cp docs/manual-test/test-aria2.md .manual-test/.opencode/command/test-aria2.md
    @cp docs/manual-test/README.md .manual-test/README.md
    @echo "Creating skill config in skill root directory..."
    @cp skills/aria2-json-rpc/assets/config.example.json .manual-test/.opencode/skills/aria2-json-rpc/config.json
    @echo "✓ Manual test environment ready"
    @echo ""
    @echo "Next steps:"
    @echo "1. Start aria2 daemon: just manual-test-start-aria2 6800 test-secret"
    @echo "2. Navigate to .manual-test/ directory"
    @echo "3. Follow instructions in README.md"

manual-test-start-aria2 port='6800' secret='test-secret':
    @echo "Starting aria2 daemon on port {{port}}..."
    @if pgrep -f "aria2c.*--rpc-listen-port.*{{port}}" > /dev/null; then \
        echo "✓ aria2 daemon already running on port {{port}}"; \
    else \
        aria2c \
            --enable-rpc \
            --rpc-listen-all=true \
            --rpc-listen-port={{port}} \
            --rpc-secret={{secret}} \
            --rpc-allow-origin-all \
            --dir=/tmp/aria2-test-downloads \
            --log=/tmp/aria2-test.log \
            -D \
            && echo "✓ aria2 daemon started on port {{port}}" \
            && echo "  Download directory: /tmp/aria2-test-downloads" \
            && echo "  Log file: /tmp/aria2-test.log"; \
    fi
    @echo "Updating config.json with port and secret..."
    @if [ -f ".manual-test/.opencode/skills/aria2-json-rpc/config.json" ]; then \
        python3 -c "import json; f='.manual-test/.opencode/skills/aria2-json-rpc/config.json'; config=json.load(open(f)); config['port']={{port}}; config['secret']='{{secret}}' if '{{secret}}' else None; json.dump(config, open(f, 'w'), indent=2)" \
        && echo "✓ config.json updated with port={{port}} and secret={{secret}}"; \
    else \
        echo "⚠ Warning: config.json not found. Run 'just manual-test-setup' first."; \
    fi

manual-test-stop-aria2:
    @echo "Stopping aria2 daemon..."
    @pkill -f "aria2c.*--enable-rpc" && echo "✓ aria2 daemon stopped" || echo "✗ aria2 daemon not running"

manual-test-status:
    @echo "Manual test environment status:"
    @echo ""
    @if [ -d ".manual-test" ]; then echo "✓ Test directory exists"; else echo "✗ Test directory missing (run: just manual-test-setup)"; fi
    @if [ -d ".manual-test/.opencode/skills/aria2-json-rpc" ]; then echo "✓ Skill directory exists"; else echo "✗ Skill directory missing"; fi
    @if [ -f ".manual-test/.opencode/skills/aria2-json-rpc/config.json" ]; then echo "✓ Skill config exists"; else echo "✗ Skill config missing"; fi
    @if [ -f ".manual-test/instruct.md" ]; then echo "✓ Test instructions exist"; else echo "✗ Test instructions missing"; fi
    @if [ -f ".manual-test/README.md" ]; then echo "✓ README exists"; else echo "✗ README missing"; fi
    @echo ""
    @if pgrep -f "aria2c.*--enable-rpc" > /dev/null; then \
        echo "✓ aria2 daemon: RUNNING"; \
    else \
        echo "✗ aria2 daemon: NOT RUNNING (run: just manual-test-start-aria2 6800 test-secret)"; \
    fi

manual-test-run:
    @echo "Manual test instructions:"
    @echo ""
    @echo "Prerequisites:"
    @echo "1. Set up environment: just manual-test-setup"
    @echo "2. Start aria2 daemon: just manual-test-start-aria2 6800 test-secret"
    @echo ""
    @echo "Running tests:"
    @echo "1. Navigate to .manual-test/ directory"
    @echo "2. Load aria2-json-rpc skill in OpenCode from .opencode/skills/"
    @echo "3. Follow instructions in README.md or instruct.md"
    @echo "4. Or use OpenCode command: /test-aria2"
    @echo ""
    @echo "Test results will be saved to results/ directory"

manual-test-clean:
    @echo "Cleaning manual test environment..."
    @just manual-test-stop-aria2
    @rm -rf .manual-test
    @rm -rf /tmp/aria2-test-downloads
    @echo "✓ Manual test environment cleaned"
