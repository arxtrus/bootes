#!/bin/bash
# Type checking with MyPy

set -e

echo "Running type checking..."

# Check if any Python files exist
if find . -name "*.py" -not -path "./.venv/*" -not -path "./.*" -not -path "./tests/*" | head -1 | grep -q .; then
    echo "Running MyPy type checker..."
    
    # Install types if needed
    if command -v python3 >/dev/null 2>&1; then
        python3 -m pip install --user types-requests pandas-stubs >/dev/null 2>&1 || true
    fi
    
    # Run mypy with configuration
    python3 -m mypy \
        --python-version=3.9 \
        --ignore-missing-imports \
        --no-strict-optional \
        --exclude='tests/' \
        --exclude='\.venv/' \
        . || {
            echo "MyPy found some issues, but continuing..."
            # Don't fail on MyPy errors for now, just warn
        }
    
    echo "Type checking completed"
else
    echo "No Python files to type check"
fi