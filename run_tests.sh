#!/bin/bash
# Run all tests for openwebui-chat-client
# Usage: ./run_tests.sh [options]
# Options:
#   -v, --verbose     Run with verbose output
#   -c, --coverage    Run with coverage report
#   -d, --delete      Run only delete_chat tests
#   -h, --help        Show this help message

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default settings
VERBOSE=""
COVERAGE=""
TEST_PATH="tests/"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE="-v"
            shift
            ;;
        -c|--coverage)
            COVERAGE="--cov=openwebui_chat_client --cov-report=term-missing --cov-report=html:htmlcov"
            shift
            ;;
        -d|--delete)
            TEST_PATH="tests/modules/test_chat_manager_delete.py tests/modules/test_async_chat_manager_delete.py tests/test_delete_chat_functionality.py"
            shift
            ;;
        -h|--help)
            echo "Usage: ./run_tests.sh [options]"
            echo ""
            echo "Options:"
            echo "  -v, --verbose     Run with verbose output"
            echo "  -c, --coverage    Run with coverage report"
            echo "  -d, --delete      Run only delete_chat tests"
            echo "  -h, --help        Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./run_tests.sh                    # Run all tests"
            echo "  ./run_tests.sh -v                 # Run all tests with verbose output"
            echo "  ./run_tests.sh -c                 # Run all tests with coverage"
            echo "  ./run_tests.sh -d -v              # Run delete_chat tests with verbose output"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check for virtual environment
if [ -f "./venv/bin/python" ]; then
    PYTHON="./venv/bin/python"
    echo -e "${GREEN}Using virtual environment Python${NC}"
elif [ -f "venv/bin/python" ]; then
    PYTHON="venv/bin/python"
    echo -e "${GREEN}Using virtual environment Python${NC}"
else
    PYTHON="python3"
    echo -e "${YELLOW}Virtual environment not found, using system Python${NC}"
fi

# Check if pytest is available
echo "Checking pytest..."
if ! $PYTHON -c "import pytest" 2>/dev/null; then
    echo -e "${RED}pytest not found. Installing test dependencies...${NC}"
    $PYTHON -m pip install pytest pytest-asyncio pytest-cov
fi

# Print test header
echo ""
echo "=========================================="
echo "Running openwebui-chat-client tests"
echo "=========================================="
echo "Python: $($PYTHON --version)"
echo "Pytest: $($PYTHON -m pytest --version | head -1)"
echo "Test path: $TEST_PATH"
echo "=========================================="
echo ""

# Run tests
if [ -n "$COVERAGE" ]; then
    echo -e "${YELLOW}Running tests with coverage...${NC}"
    $PYTHON -m pytest $TEST_PATH $VERBOSE $COVERAGE --tb=short
    
    echo ""
    echo "=========================================="
    echo -e "${GREEN}Coverage report generated in htmlcov/${NC}"
    echo "Open htmlcov/index.html in your browser to view"
    echo "=========================================="
else
    $PYTHON -m pytest $TEST_PATH $VERBOSE --tb=short
fi

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo -e "${GREEN}All tests passed!${NC}"
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo -e "${RED}Some tests failed!${NC}"
    echo "=========================================="
    exit 1
fi
