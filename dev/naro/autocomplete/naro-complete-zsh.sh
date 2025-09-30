#compdef naro

# Zsh completion for Orbis Naro

_naro() {
    local context state line
    typeset -A opt_args

    _arguments \
        '1: :_naro_commands' \
        '*:: :->args' \
        && return 0

    case $state in
        args)
            case ${words[1]} in
                providers)
                    _arguments \
                        '1: :(install test list validate cleanup)' \
                        '*: :_files'
                    ;;
                build)
                    _arguments \
                        '1: :(core sdk ui all)' \
                        '*: :_files'
                    ;;
                test)
                    _arguments \
                        '1: :(unit integration e2e providers sdk core all)' \
                        '--verbose[Enable verbose output]' \
                        '--coverage[Generate coverage report]' \
                        '*: :_files'
                    ;;
                start|stop|logs)
                    _arguments \
                        '1: :(core sdk ui ui-dev)' \
                        '--follow[Follow log output]' \
                        '*: :_files'
                    ;;
                *)
                    _files
                    ;;
            esac
            ;;
    esac
}

_naro_commands() {
    local commands
    commands=(
        'setup:Set up development environment'
        'providers:Manage provider packages'
        'build:Build Docker services'
        'start:Start development services'
        'stop:Stop all services'
        'logs:Show service logs'
        'test:Run tests'
        'lint:Run code linting'
        'format:Format code'
        'status:Show environment status'
        'shell:Enter development shell'
        'doctor:Diagnose environment issues'
        'cleanup:Clean up resources'
        'version:Show version information'
        'help:Show help information'
    )
    _describe 'commands' commands
}

_naro "$@"