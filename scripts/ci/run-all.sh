#!/bin/bash
# Master CI script that runs all checks

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}Running bootes CI Pipeline...${NC}"
echo "=================================="

# Track failures
FAILED_CHECKS=()

# Function to run a check
run_check() {
    local name="$1"
    local script="$2"
    
    echo -e "\n${BLUE}Step: $name${NC}"
    echo "-------------------"
    
    if [ -f "$SCRIPT_DIR/$script" ]; then
        chmod +x "$SCRIPT_DIR/$script"
        if "$SCRIPT_DIR/$script"; then
            echo -e "${GREEN}$name passed${NC}"
        else
            echo -e "${RED}$name failed${NC}"
            FAILED_CHECKS+=("$name")
            return 1
        fi
    else
        echo -e "${YELLOW}$script not found, skipping $name${NC}"
    fi
}

# Run all checks
run_check "File Validation" "validate-files.sh" || true
run_check "Code Formatting" "format-code.sh" || true
run_check "Code Linting" "lint-code.sh" || true
run_check "Type Checking" "type-check.sh" || true
run_check "Security Check" "security-check.sh" || true
run_check "Tests" "test-code.sh" || true

# Summary
echo -e "\n${BLUE}=================================="
echo -e "CI Pipeline Summary${NC}"
echo "=================================="

if [ ${#FAILED_CHECKS[@]} -eq 0 ]; then
    echo -e "${GREEN}All checks passed!${NC}"
    echo "Your code is ready for commit."
    exit 0
else
    echo -e "${RED}Failed checks:${NC}"
    for check in "${FAILED_CHECKS[@]}"; do
        echo -e "  ${RED}- $check${NC}"
    done
    echo ""
    echo -e "${YELLOW}Please fix the issues above before committing.${NC}"
    exit 1
fi