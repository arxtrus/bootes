#!/bin/bash
# Validate file formats and common issues

set -e

echo "Validating files..."

# Check file endings
echo "Fixing trailing whitespace..."
find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.md" -o -name "*.yaml" -o -name "*.yml" -o -name "*.json" \) \
    -not -path "./.venv/*" -not -path "./.git/*" \
    -exec sed -i '' 's/[[:space:]]*$//' {} \;

echo "Ensuring files end with newline..."
find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.md" -o -name "*.yaml" -o -name "*.yml" -o -name "*.json" \) \
    -not -path "./.venv/*" -not -path "./.git/*" \
    -exec sh -c 'if [ -n "$(tail -c1 "$1")" ]; then echo "" >> "$1"; fi' _ {} \;

# Validate YAML files
echo "Validating YAML files..."
for file in $(find . -name "*.yaml" -o -name "*.yml" | grep -v ".venv" | grep -v ".git"); do
    if command -v python3 >/dev/null 2>&1; then
        python3 -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null || {
            echo "Invalid YAML: $file"
            exit 1
        }
    fi
done

# Validate JSON files
echo "Validating JSON files..."
for file in $(find . -name "*.json" | grep -v ".venv" | grep -v ".git"); do
    if command -v python3 >/dev/null 2>&1; then
        python3 -c "import json; json.load(open('$file'))" 2>/dev/null || {
            echo "Invalid JSON: $file"
            exit 1
        }
    fi
done

# Validate TOML files
echo "Validating TOML files..."
for file in $(find . -name "*.toml" | grep -v ".venv" | grep -v ".git"); do
    if command -v python3 >/dev/null 2>&1; then
        python3 -c "import tomllib; tomllib.load(open('$file', 'rb'))" 2>/dev/null || \
        python3 -c "import toml; toml.load('$file')" 2>/dev/null || {
            echo "Invalid TOML: $file"
            exit 1
        }
    fi
done

# Check for large files
echo "Checking for large files..."
large_files=$(find . -type f -size +10M -not -path "./.venv/*" -not -path "./.git/*" | head -5)
if [ -n "$large_files" ]; then
    echo "Large files found (>10MB):"
    echo "$large_files"
fi

# Check for merge conflicts
echo "Checking for merge conflicts..."
if find . -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.md" | \
   grep -v ".venv" | grep -v ".git" | \
   xargs grep -l "<<<<<<< \|======= \|>>>>>>> " | head -1 | grep -q .; then
    echo "Merge conflict markers found!"
    find . -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.md" | \
    grep -v ".venv" | grep -v ".git" | \
    xargs grep -Hn "<<<<<<< \|======= \|>>>>>>> " | head -5
    exit 1
fi

echo "File validation completed"