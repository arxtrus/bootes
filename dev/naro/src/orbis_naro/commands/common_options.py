"""
Common CLI options and decorators for Orbis Naro commands.

This module provides reusable CLI options and decorators that can be applied
to multiple commands to ensure consistency across the CLI interface.
"""

import functools
from typing import Callable, Any

import click


def verbose_option(f: Callable) -> Callable:
    """Add verbose option to command."""
    return click.option(
        '--verbose', '-v',
        is_flag=True,
        help='Enable verbose output',
        envvar='NARO_VERBOSE'
    )(f)


def quiet_option(f: Callable) -> Callable:
    """Add quiet option to command."""
    return click.option(
        '--quiet', '-q',
        is_flag=True,
        help='Suppress output',
        envvar='NARO_QUIET'
    )(f)


def dry_run_option(f: Callable) -> Callable:
    """Add dry-run option to command."""
    return click.option(
        '--dry-run',
        is_flag=True,
        help='Show what would be done without executing',
        envvar='NARO_DRY_RUN'
    )(f)


def force_option(f: Callable) -> Callable:
    """Add force option to command."""
    return click.option(
        '--force',
        is_flag=True,
        help='Force operation without confirmation',
        envvar='NARO_FORCE'
    )(f)


def parallel_option(f: Callable) -> Callable:
    """Add parallel option to command."""
    return click.option(
        '--parallel', '-j',
        type=int,
        help='Number of parallel processes',
        envvar='NARO_PARALLEL'
    )(f)


def timeout_option(default: int = 300) -> Callable:
    """Add timeout option to command with configurable default."""
    def decorator(f: Callable) -> Callable:
        return click.option(
            '--timeout',
            type=int,
            default=default,
            help=f'Timeout in seconds (default: {default})',
            envvar='NARO_TIMEOUT'
        )(f)
    return decorator


def output_format_option(f: Callable) -> Callable:
    """Add output format option to command."""
    return click.option(
        '--output', '-o',
        type=click.Choice(['text', 'json', 'yaml', 'table']),
        default='text',
        help='Output format',
        envvar='NARO_OUTPUT_FORMAT'
    )(f)


def config_file_option(f: Callable) -> Callable:
    """Add config file option to command."""
    return click.option(
        '--config', '-c',
        type=click.Path(exists=True, dir_okay=False),
        help='Path to configuration file',
        envvar='NARO_CONFIG_FILE'
    )(f)


def common_options(f: Callable) -> Callable:
    """Apply common options to a command."""
    f = verbose_option(f)
    f = quiet_option(f) 
    f = dry_run_option(f)
    f = force_option(f)
    return f


def docker_options(f: Callable) -> Callable:
    """Apply Docker-related options to a command.""" 
    f = click.option(
        '--docker-compose-file',
        type=click.Path(exists=True, dir_okay=False),
        help='Path to docker-compose.yml file',
        envvar='NARO_DOCKER_COMPOSE_FILE'
    )(f)
    f = click.option(
        '--no-cache',
        is_flag=True,
        help='Do not use cache when building Docker images',
        envvar='NARO_NO_CACHE'
    )(f)
    f = click.option(
        '--pull',
        is_flag=True,
        help='Always attempt to pull newer versions of images',
        envvar='NARO_PULL'
    )(f)
    return f


def test_options(f: Callable) -> Callable:
    """Apply test-related options to a command."""
    f = click.option(
        '--coverage',
        is_flag=True,
        help='Generate coverage report',
        envvar='NARO_COVERAGE'
    )(f)
    f = click.option(
        '--fail-fast',
        is_flag=True,
        help='Stop on first test failure',
        envvar='NARO_FAIL_FAST'
    )(f)
    f = click.option(
        '--test-pattern',
        help='Pattern to match test files',
        envvar='NARO_TEST_PATTERN'
    )(f)
    f = parallel_option(f)
    return f


def provider_options(f: Callable) -> Callable:
    """Apply provider-related options to a command."""
    f = click.option(
        '--provider-dir',
        type=click.Path(exists=True, file_okay=False, dir_okay=True),
        help='Path to providers directory',
        envvar='NARO_PROVIDERS_DIR'
    )(f)
    f = click.option(
        '--skip-dependencies',
        is_flag=True,
        help='Skip installing provider dependencies',
        envvar='NARO_SKIP_DEPENDENCIES'
    )(f)
    f = click.option(
        '--editable',
        is_flag=True,
        default=True,
        help='Install in editable mode',
        envvar='NARO_EDITABLE'
    )(f)
    return f


def handle_common_params(ctx: click.Context) -> dict[str, Any]:
    """Extract and validate common parameters from context."""
    params = {}
    
    # Get global options from parent context
    if ctx.parent and ctx.parent.obj:
        params.update(ctx.parent.obj)
    
    # Override with local options if present
    for key in ['verbose', 'quiet', 'dry_run', 'force']:
        if key in ctx.params and ctx.params[key] is not None:
            params[key] = ctx.params[key]
    
    # Validate conflicting options
    if params.get('verbose') and params.get('quiet'):
        raise click.ClickException("Cannot use --verbose and --quiet together")
    
    return params


def requires_project_root(f: Callable) -> Callable:
    """Decorator to ensure project root is available."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        if not ctx.obj or not ctx.obj.get('project_root'):
            raise click.ClickException(
                "Project root not found. Run command from within an Orbis project "
                "or use --project-root option."
            )
        return f(*args, **kwargs)
    return wrapper


def requires_docker(f: Callable) -> Callable:
    """Decorator to ensure Docker is available."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            import docker
            client = docker.from_env()
            client.ping()
        except Exception as e:
            raise click.ClickException(
                f"Docker is not available or not running: {e}"
            ) from e
        return f(*args, **kwargs)
    return wrapper