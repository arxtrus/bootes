#!/usr/bin/env bash
#
# Setup Naro Symbolic Links
#
# This script creates convenient symbolic links to make naro accessible
# from various locations within the project.
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_error() {
    echo -e "${RED}❌ $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Get project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

print_header "Setting up Naro Symbolic Links"

print_info "Project root: $PROJECT_ROOT"

# Locations where we want naro to be accessible
declare -A LINK_LOCATIONS=(
    ["$PROJECT_ROOT/orbis-core/naro"]="Orbis Core directory"
    ["$PROJECT_ROOT/orbis-sdk/naro"]="Orbis SDK directory"
    ["$PROJECT_ROOT/providers/naro"]="Providers directory"
)

# Source naro script
NARO_SOURCE="$PROJECT_ROOT/naro"

if [[ ! -f "$NARO_SOURCE" ]]; then
    print_error "Source naro script not found at: $NARO_SOURCE"
    exit 1
fi

# Create symbolic links
for link_path in "${!LINK_LOCATIONS[@]}"; do
    location_desc="${LINK_LOCATIONS[$link_path]}"
    
    print_info "Creating link in $location_desc..."
    
    # Remove existing link if it exists
    if [[ -L "$link_path" ]]; then
        rm "$link_path"
        print_info "Removed existing link"
    elif [[ -f "$link_path" ]]; then
        print_error "File already exists at $link_path (not a symlink)"
        continue
    fi
    
    # Create directory if it doesn't exist
    link_dir="$(dirname "$link_path")"
    if [[ ! -d "$link_dir" ]]; then
        print_info "Creating directory: $link_dir"
        mkdir -p "$link_dir"
    fi
    
    # Create relative symbolic link
    relative_path="$(realpath --relative-to="$link_dir" "$NARO_SOURCE")"
    ln -s "$relative_path" "$link_path"
    
    print_success "Created link: $link_path -> $relative_path"
done

print_header "Setup Complete"

print_success "Naro symbolic links created successfully!"
print_info "You can now run './naro' from the following directories:"

for link_path in "${!LINK_LOCATIONS[@]}"; do
    if [[ -L "$link_path" ]]; then
        location_desc="${LINK_LOCATIONS[$link_path]}"
        relative_dir="$(realpath --relative-to="$PROJECT_ROOT" "$(dirname "$link_path")")"
        echo "  - $relative_dir/ ($location_desc)"
    fi
done

print_info "Examples:"
echo "  cd orbis-core && ./naro providers install"
echo "  cd providers && ./naro test --all"
echo "  cd orbis-sdk && ./naro start"