#!/bin/bash
# Security checks with Bandit and other security tools

set -e

echo "Running security checks..."

# Security scan with Bandit
if find . -name "*.py" -not -path "./.venv/*" -not -path "./.*" -not -path "./tests/*" | head -1 | grep -q .; then
    echo "Running Bandit security scanner..."
    
    python3 -m bandit -r . \
        -f json \
        -o bandit-report.json \
        --exclude=".venv,tests,.*" \
        --skip=B101 \
        2>/dev/null || {
            # Check if there are actual security issues (not just warnings)
            if [ -f bandit-report.json ]; then
                issues=$(python3 -c "import json; data=json.load(open('bandit-report.json')); print(len([r for r in data.get('results', []) if r.get('issue_severity') in ['HIGH', 'MEDIUM']]))" 2>/dev/null || echo "0")
                if [ "$issues" -gt "0" ]; then
                    echo "Security issues found!"
                    python3 -c "import json; data=json.load(open('bandit-report.json')); [print(f\"  {r['filename']}:{r['line_number']} - {r['issue_text']}\") for r in data.get('results', []) if r.get('issue_severity') in ['HIGH', 'MEDIUM']]" 2>/dev/null || true
                    exit 1
                fi
            fi
        }
    
    echo "Security check completed"
else
    echo "No Python files to security check"
fi

# Check for secrets and sensitive information
echo "Checking for potential secrets..."
if find . -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" | \
   grep -v ".venv" | grep -v ".git" | \
   xargs grep -i "password\|secret\|api[_-]key\|token" | \
   grep -v "# noqa" | head -5 | grep -q .; then
    echo "Potential secrets found (check if they are false positives):"
    find . -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" | \
    grep -v ".venv" | grep -v ".git" | \
    xargs grep -in "password\|secret\|api[_-]key\|token" | \
    grep -v "# noqa" | head -5 || true
else
    echo "No obvious secrets found"
fi