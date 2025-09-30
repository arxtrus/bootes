#!/bin/bash
# Bash completion for Orbis Naro

_naro_completion() {
    local cur prev opts commands
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Main commands
    commands="setup providers build start stop logs test lint format status shell doctor cleanup version help development services testing maintenance ci"
    
    # Provider subcommands
    provider_commands="install test list validate cleanup"
    
    # Development subcommands
    development_commands="setup shell lint format docs install-hooks uv-info uv-sync uv-add uv-remove uv-lock"
    
    # Build targets
    build_targets="core sdk ui all"
    
    # Test types
    test_types="unit integration e2e providers sdk core all"
    
    case "${prev}" in
        naro)
            COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
            return 0
            ;;
        providers)
            COMPREPLY=( $(compgen -W "${provider_commands}" -- ${cur}) )
            return 0
            ;;
        development)
            COMPREPLY=( $(compgen -W "${development_commands}" -- ${cur}) )
            return 0
            ;;
        build)
            COMPREPLY=( $(compgen -W "${build_targets}" -- ${cur}) )
            return 0
            ;;
        test)
            COMPREPLY=( $(compgen -W "${test_types}" -- ${cur}) )
            return 0
            ;;
        start|stop|logs)
            COMPREPLY=( $(compgen -W "core sdk ui ui-dev" -- ${cur}) )
            return 0
            ;;
        *)
            # Handle options
            case "${cur}" in
                -*)
                    opts="--help --verbose --quiet --dry-run --force --dev-mode"
                    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
                    return 0
                    ;;
                *)
                    COMPREPLY=( $(compgen -f -- ${cur}) )
                    return 0
                    ;;
            esac
            ;;
    esac
}

complete -F _naro_completion naro
complete -F _naro_completion ./naro