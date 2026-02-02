#!/usr/bin/env bash
#
# Unit test runner for aria2-json-rpc-skills using UV for dependency management.
#
# This script runs all unit tests in an isolated environment using UV,
# preventing pollution of the global Python environment.
#
# Usage:
#   ./run_unit_tests.sh         # Run all unit tests
#

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Unit Test Runner (UV)"
echo "=========================================="
echo ""

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}ERROR: UV is not installed${NC}"
    echo ""
    echo "UV is required for isolated dependency management."
    echo "Install UV from: https://github.com/astral-sh/uv"
    echo ""
    echo "Quick install:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ UV is installed${NC}"
echo ""

echo "Running all unit tests..."
TEST_PATTERN="tests/unit/"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    uv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
    echo ""
fi

# Install dependencies in isolated environment
echo -e "${YELLOW}Installing dependencies in isolated environment...${NC}"
uv pip install --quiet pytest websockets
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Run tests with UV
echo "Running tests..."
echo ""

# Try to use pytest if available, otherwise fall back to unittest
if uv run python -c "import pytest" 2>/dev/null; then
    # Use pytest
    if uv run python -m pytest $TEST_PATTERN -v --tb=short; then
        echo ""
        echo -e "${GREEN}=========================================="
        echo "✓ All tests passed!"
        echo -e "==========================================${NC}"
        exit 0
    else
        echo ""
        echo -e "${RED}=========================================="
        echo "✗ Some tests failed"
        echo -e "==========================================${NC}"
        exit 1
    fi
else
    # Fall back to unittest
    if uv run python -m unittest discover $TEST_PATTERN -v; then
        echo ""
        echo -e "${GREEN}=========================================="
        echo "✓ All tests passed!"
        echo -e "==========================================${NC}"
        exit 0
    else
        echo ""
        echo -e "${RED}=========================================="
        echo "✗ Some tests failed"
        echo -e "==========================================${NC}"
        exit 1
    fi
fi
