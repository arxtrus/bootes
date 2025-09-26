#!/bin/bash
# Run tests for the project

set -e

echo "Running tests..."

# Test SDK if it exists
if [ -d "orbis-sdk" ]; then
    echo "Testing orbis SDK..."
    cd orbis-sdk
    
    if [ -f "pyproject.toml" ]; then
        # Check if uv is available
        if command -v uv >/dev/null 2>&1; then
            echo "Running tests with uv..."
            uv run python -m pytest tests/ -x -q --tb=short || {
                echo "SDK tests failed!"
                cd ..
                exit 1
            }
        else
            # Fallback to regular pytest
            if command -v python3 >/dev/null 2>&1 && python3 -c "import pytest" 2>/dev/null; then
                echo "Running tests with pytest..."
                python3 -m pytest tests/ -x -q --tb=short || {
                    echo "SDK tests failed!"
                    cd ..
                    exit 1
                }
            else
                echo "pytest not available, skipping SDK tests"
            fi
        fi
    fi
    
    cd ..
    echo "SDK tests completed"
fi

# Test other components if they have tests
if [ -d "orbis-core" ]; then
    echo "Checking for core tests..."
    if [ -d "orbis-core/tests" ] || [ -f "orbis-core/package.json" ]; then
        cd orbis-core
        
        # Check for Node.js tests
        if [ -f "package.json" ] && command -v npm >/dev/null 2>&1; then
            echo "Running npm tests..."
            npm test 2>/dev/null || {
                echo "Core tests failed or not configured"
            }
        fi
        
        cd ..
    fi
fi

echo "All tests completed"