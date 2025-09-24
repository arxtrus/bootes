#!/bin/bash
# Code formatting with Black and isort

set -e

echo "Running code formatting..."

# Check if any Python files are staged
if git diff --cached --name-only | grep -q '\.py$'; then
    echo "Formatting Python files with Black..."
    python3 -m black --line-length=88 --target-version=py39 .
    
    echo "Sorting imports with isort..."
    python3 -m isort --profile=black --line-length=88 .
    
    echo "Code formatting completed"
else
    echo "No Python files to format"
fi

# Format JavaScript/TypeScript files if present
if git diff --cached --name-only | grep -qE '\.(js|jsx|ts|tsx|json|yaml|yml|md)$'; then
    if command -v prettier >/dev/null 2>&1; then
        echo "Formatting JS/TS/JSON/YAML/MD files with Prettier..."
        npx prettier --write "**/*.{js,jsx,ts,tsx,json,yaml,yml,md}"
        echo "Prettier formatting completed"
    else
        echo "Prettier not found, skipping JS/TS formatting"
    fi
fi