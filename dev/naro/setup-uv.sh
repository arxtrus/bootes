#!/usr/bin/env bash
#
# Orbis Naro UV Setup Script
#
# This script sets up the Orbis Naro development environment using uv,
# the fast Python package installer and dependency resolver.
#
# Usage:
#   ./setup-uv.sh
#   ./setup-uv.sh --install-uv  # Force uv installation
#   ./setup-uv.sh --no-sync     # Skip dependency sync
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Options
INSTALL_UV=false
SKIP_SYNC=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --install-uv)
            INSTALL_UV=true
            shift
            ;;
        --no-sync)
            SKIP_SYNC=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--install-uv] [--no-sync]"
            echo "  --install-uv    Force uv installation"
            echo "  --no-sync       Skip dependency synchronization"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if uv is available
check_uv() {
    if command -v uv >/dev/null 2>&1; then
        UV_VERSION=$(uv --version | cut -d' ' -f2)
        print_success "uv $UV_VERSION is available"
        return 0
    else
        print_warning "uv is not available"
        return 1
    fi
}

# Install uv
install_uv() {
    print_header "Installing UV"
    
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Windows
        print_info "Installing uv on Windows..."
        powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    else
        # Unix-like systems (Linux, macOS)
        print_info "Installing uv on Unix-like system..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
    fi
    
    # Source the shell configuration to make uv available
    if [[ -f "$HOME/.bashrc" ]]; then
        source "$HOME/.bashrc"
    elif [[ -f "$HOME/.zshrc" ]]; then
        source "$HOME/.zshrc"
    fi
    
    # Check if installation was successful
    if check_uv; then
        print_success "uv installed successfully"
    else
        print_error "Failed to install uv"
        exit 1
    fi
}

# Set up uv project
setup_uv_project() {
    print_header "Setting Up UV Project"
    
    cd "$SCRIPT_DIR"
    
    # Initialize uv project if pyproject.toml doesn't exist
    if [[ ! -f "pyproject.toml" ]]; then
        print_info "Initializing new uv project..."
        uv init --name orbis-naro
    else
        print_info "pyproject.toml already exists"
    fi
    
    # Sync dependencies
    if [[ "$SKIP_SYNC" != "true" ]]; then
        print_info "Syncing dependencies..."
        uv sync --dev
        print_success "Dependencies synced"
    else
        print_info "Skipping dependency sync"
    fi
    
    # Generate lock file
    print_info "Generating lock file..."
    uv lock
    print_success "Lock file generated"
}

# Set up provider packages
setup_providers() {
    print_header "Setting Up Provider Packages"
    
    cd "$PROJECT_ROOT"
    
    # Install provider packages in editable mode
    PROVIDERS=("providers/common" "providers/manager" "providers/yahoo")
    
    for provider in "${PROVIDERS[@]}"; do
        if [[ -d "$provider" ]]; then
            print_info "Installing $provider..."
            cd "$PROJECT_ROOT/$provider"
            uv pip install -e .
            print_success "Installed $provider"
            cd "$PROJECT_ROOT"
        else
            print_warning "Provider $provider not found at $PROJECT_ROOT/$provider"
            print_info "Available providers:"
            if [[ -d "$PROJECT_ROOT/providers" ]]; then
                ls -la "$PROJECT_ROOT/providers/"
            fi
        fi
    done
}

# Main setup function
main() {
    print_header "Orbis Naro UV Setup"
    
    print_info "Project root: $PROJECT_ROOT"
    print_info "Naro directory: $SCRIPT_DIR"
    
    # Check if uv is available or install it
    if ! check_uv || [[ "$INSTALL_UV" == "true" ]]; then
        install_uv
    fi
    
    # Set up uv project
    setup_uv_project
    
    # Set up provider packages
    setup_providers
    
    print_header "Setup Complete"
    print_success "Orbis Naro development environment is ready!"
    print_info "You can now use the following commands:"
    echo "  ./naro --help                    # Show help"
    echo "  ./naro development uv-info       # Show uv environment info"
    echo "  ./naro development uv-sync       # Sync dependencies"
    echo "  ./naro development setup         # Full environment setup"
    
    print_info "To run commands in the uv environment:"
    echo "  cd $SCRIPT_DIR && uv run <command>"
    echo "  cd $SCRIPT_DIR && uv run python --version"
}

# Run main function
main "$@"