# Fish completion for Orbis Naro

# Main commands
complete -c naro -f -a "setup" -d "Set up development environment"
complete -c naro -f -a "providers" -d "Manage provider packages"
complete -c naro -f -a "build" -d "Build Docker services"
complete -c naro -f -a "start" -d "Start development services"
complete -c naro -f -a "stop" -d "Stop all services"
complete -c naro -f -a "logs" -d "Show service logs"
complete -c naro -f -a "test" -d "Run tests"
complete -c naro -f -a "lint" -d "Run code linting"
complete -c naro -f -a "format" -d "Format code"
complete -c naro -f -a "status" -d "Show environment status"
complete -c naro -f -a "shell" -d "Enter development shell"
complete -c naro -f -a "doctor" -d "Diagnose environment issues"
complete -c naro -f -a "cleanup" -d "Clean up resources"
complete -c naro -f -a "version" -d "Show version information"
complete -c naro -f -a "help" -d "Show help information"

# Provider subcommands
complete -c naro -f -n "__fish_seen_subcommand_from providers" -a "install" -d "Install provider packages"
complete -c naro -f -n "__fish_seen_subcommand_from providers" -a "test" -d "Test provider packages"
complete -c naro -f -n "__fish_seen_subcommand_from providers" -a "list" -d "List available providers"
complete -c naro -f -n "__fish_seen_subcommand_from providers" -a "validate" -d "Validate provider configuration"
complete -c naro -f -n "__fish_seen_subcommand_from providers" -a "cleanup" -d "Clean up provider resources"

# Build targets
complete -c naro -f -n "__fish_seen_subcommand_from build" -a "core" -d "Build core service"
complete -c naro -f -n "__fish_seen_subcommand_from build" -a "sdk" -d "Build SDK service"
complete -c naro -f -n "__fish_seen_subcommand_from build" -a "ui" -d "Build UI service"
complete -c naro -f -n "__fish_seen_subcommand_from build" -a "all" -d "Build all services"

# Test types
complete -c naro -f -n "__fish_seen_subcommand_from test" -a "unit" -d "Run unit tests"
complete -c naro -f -n "__fish_seen_subcommand_from test" -a "integration" -d "Run integration tests"
complete -c naro -f -n "__fish_seen_subcommand_from test" -a "e2e" -d "Run end-to-end tests"
complete -c naro -f -n "__fish_seen_subcommand_from test" -a "providers" -d "Run provider tests"
complete -c naro -f -n "__fish_seen_subcommand_from test" -a "sdk" -d "Run SDK tests"
complete -c naro -f -n "__fish_seen_subcommand_from test" -a "core" -d "Run core tests"
complete -c naro -f -n "__fish_seen_subcommand_from test" -a "all" -d "Run all tests"

# Service names for start/stop/logs
complete -c naro -f -n "__fish_seen_subcommand_from start stop logs" -a "core" -d "Core service"
complete -c naro -f -n "__fish_seen_subcommand_from start stop logs" -a "sdk" -d "SDK service"
complete -c naro -f -n "__fish_seen_subcommand_from start stop logs" -a "ui" -d "UI production service"
complete -c naro -f -n "__fish_seen_subcommand_from start stop logs" -a "ui-dev" -d "UI development service"

# Global options
complete -c naro -l help -s h -d "Show help message"
complete -c naro -l verbose -s v -d "Enable verbose output"
complete -c naro -l quiet -s q -d "Suppress output"
complete -c naro -l dry-run -d "Show what would be done without executing"
complete -c naro -l force -f -d "Force operation without confirmation"
complete -c naro -l dev-mode -d "Enable development mode"

# Test-specific options
complete -c naro -f -n "__fish_seen_subcommand_from test" -l coverage -d "Generate coverage report"
complete -c naro -f -n "__fish_seen_subcommand_from test" -l parallel -d "Run tests in parallel"
complete -c naro -f -n "__fish_seen_subcommand_from test" -l failfast -d "Stop on first failure"

# Logs-specific options
complete -c naro -f -n "__fish_seen_subcommand_from logs" -l follow -s f -d "Follow log output"
complete -c naro -f -n "__fish_seen_subcommand_from logs" -l tail -d "Number of lines to tail"