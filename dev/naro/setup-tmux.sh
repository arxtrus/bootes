#!/usr/bin/env bash
#
# tmux Setup Script for Orbis Naro
#
# This script installs and configures tmux for optimal use with Naro monitoring.
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check if tmux is already installed
check_tmux() {
    if command -v tmux >/dev/null 2>&1; then
        TMUX_VERSION=$(tmux -V | cut -d' ' -f2)
        print_success "tmux $TMUX_VERSION is already installed"
        return 0
    else
        print_warning "tmux is not installed"
        return 1
    fi
}

# Install tmux based on OS
install_tmux() {
    print_header "Installing tmux"
    
    case "$OSTYPE" in
        darwin*)
            # macOS
            if command -v brew >/dev/null 2>&1; then
                print_info "Installing tmux with Homebrew..."
                brew install tmux
            else
                print_error "Homebrew not found. Please install Homebrew first:"
                echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
                return 1
            fi
            ;;
        linux*)
            # Linux
            if command -v apt-get >/dev/null 2>&1; then
                print_info "Installing tmux with apt..."
                sudo apt-get update && sudo apt-get install -y tmux
            elif command -v yum >/dev/null 2>&1; then
                print_info "Installing tmux with yum..."
                sudo yum install -y tmux
            elif command -v dnf >/dev/null 2>&1; then
                print_info "Installing tmux with dnf..."
                sudo dnf install -y tmux
            elif command -v pacman >/dev/null 2>&1; then
                print_info "Installing tmux with pacman..."
                sudo pacman -S tmux
            else
                print_error "No supported package manager found. Please install tmux manually."
                return 1
            fi
            ;;
        msys*|cygwin*)
            # Windows (Git Bash/Cygwin)
            print_info "For Windows, please install tmux manually:"
            echo "  1. Install Windows Subsystem for Linux (WSL)"
            echo "  2. Run: sudo apt-get install tmux"
            echo "  Or use a package manager like Chocolatey: choco install tmux"
            return 1
            ;;
        *)
            print_error "Unsupported operating system: $OSTYPE"
            return 1
            ;;
    esac
}

# Create optimized tmux configuration
create_tmux_config() {
    print_header "Creating Optimized tmux Configuration"
    
    TMUX_CONFIG="$HOME/.tmux.conf.naro"
    
    cat > "$TMUX_CONFIG" << 'EOF'
# Naro tmux Configuration
# Optimized for log monitoring and development

# Basic settings
set -g default-terminal "screen-256color"
set -g history-limit 10000
set -g base-index 1
setw -g pane-base-index 1

# Enable mouse support
set -g mouse on

# Key bindings for easier navigation
bind | split-window -h
bind - split-window -v
bind r source-file ~/.tmux.conf \; display "Config reloaded!"

# Pane navigation
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Pane resizing
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# Status bar
set -g status-bg black
set -g status-fg white
set -g status-left-length 40
set -g status-left "#[fg=green]Session: #S #[fg=yellow]#I #[fg=cyan]#P "
set -g status-right "#[fg=cyan]%d %b %R"
set -g status-justify centre

# Window status
setw -g window-status-fg cyan
setw -g window-status-bg default
setw -g window-status-attr dim
setw -g window-status-current-fg white
setw -g window-status-current-bg red
setw -g window-status-current-attr bright

# Pane borders
set -g pane-border-fg green
set -g pane-border-bg black
set -g pane-active-border-fg white
set -g pane-active-border-bg yellow

# Command prompt
set -g message-fg white
set -g message-bg black
set -g message-attr bright

# Activity monitoring
setw -g monitor-activity on
set -g visual-activity on

# Auto rename windows
setw -g automatic-rename on
set -g set-titles on
set -g set-titles-string "#I:#W"

# No delay for escape key press
set -sg escape-time 0
EOF

    print_success "Created tmux configuration: $TMUX_CONFIG"
    print_info "Use this config with: tmux -f $TMUX_CONFIG"
}

# Main setup function
main() {
    print_header "Orbis Naro tmux Setup"
    
    # Check current status
    if check_tmux; then
        print_info "tmux is ready for use with Naro monitoring"
    else
        print_info "Installing tmux..."
        if install_tmux; then
            print_success "tmux installation completed"
        else
            print_error "tmux installation failed"
            exit 1
        fi
    fi
    
    # Create optimized configuration
    create_tmux_config
    
    print_header "Setup Complete"
    print_success "tmux is ready for Naro monitoring!"
    print_info "You can now use the following commands:"
    echo "  naro monitor start           # Start monitoring session"
    echo "  naro monitor dashboard       # Interactive dashboard"
    echo "  naro monitor logs <service>  # View specific service logs"
    
    print_info "Pro tips:"
    echo "  - Use Ctrl+B then arrow keys to navigate panes"
    echo "  - Use Ctrl+B then D to detach from session"
    echo "  - Use 'naro monitor attach' to reattach"
    echo "  - Enable mouse support for easier pane switching"
}

# Run main function
main "$@"