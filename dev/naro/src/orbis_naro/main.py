#!/usr/bin/env python3
"""
Main entry point for Orbis Naro CLI.
"""

import sys
from pathlib import Path
from typing import Optional

import click
import rich_click as rc
from rich.console import Console
from rich.traceback import install

# Install rich traceback handler
install(show_locals=True)

# Configure rich-click
rc.rich_click.USE_RICH_MARKUP = True
rc.rich_click.USE_MARKDOWN = True
rc.rich_click.SHOW_ARGUMENTS = True
rc.rich_click.GROUP_ARGUMENTS_OPTIONS = True
rc.rich_click.SHOW_METAVARS_COLUMN = False
rc.rich_click.APPEND_METAVARS_HELP = True

from .commands import (
    development_commands,
    provider_commands,
    service_commands,
    testing_commands,
    maintenance_commands,
    ci_commands,
)
from .utils.console import get_console
from .utils.exceptions import NaroException
from .utils.path_utils import find_project_root


console = Console()


@click.group(
    name="naro",
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
    envvar="NARO_VERBOSE",
)
@click.option(
    "--quiet",
    "-q", 
    is_flag=True,
    help="Suppress output",
    envvar="NARO_QUIET",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be done without executing",
    envvar="NARO_DRY_RUN",
)
@click.option(
    "--force",
    is_flag=True,
    help="Force operation without confirmation",
    envvar="NARO_FORCE",
)
@click.option(
    "--project-root",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Path to project root directory",
    envvar="NARO_PROJECT_ROOT",
)
@click.pass_context
def main(
    ctx: click.Context,
    verbose: bool,
    quiet: bool,
    dry_run: bool,
    force: bool,
    project_root: Optional[Path],
) -> None:
    """
    **Orbis Naro** - Development Environment Management Tool
    
    A comprehensive development environment management tool,
    designed to simplify the complex multi-package development workflow of the Orbis financial 
    data platform.
    
    ## Quick Start
    
    ```bash
    # Set up development environment
    naro setup
    
    # Start services  
    naro start
    
    # Run tests
    naro test --all
    
    # Stop services
    naro stop
    ```
    
    ## Common Commands
    
    - `naro providers install` - Install provider packages
    - `naro build core` - Build specific service
    - `naro test providers` - Run provider tests
    - `naro logs core --follow` - Follow service logs
    - `naro shell` - Enter development shell
    - `naro doctor` - Diagnose environment issues
    """
    # Initialize context object
    if ctx.obj is None:
        ctx.obj = {}
    
    # Set global options
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet  
    ctx.obj["dry_run"] = dry_run
    ctx.obj["force"] = force
    
    # Find and set project root
    if project_root:
        ctx.obj["project_root"] = project_root
    else:
        try:
            ctx.obj["project_root"] = find_project_root()
        except NaroException as e:
            console.print(f"[red]Error: {e}[/red]")
            sys.exit(1)
    
    # Configure console
    ctx.obj["console"] = get_console(verbose=verbose, quiet=quiet)
    
    # If no command is provided, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# Register command groups
main.add_command(development_commands.development)
main.add_command(provider_commands.providers)
main.add_command(service_commands.services)
main.add_command(testing_commands.testing)
main.add_command(maintenance_commands.maintenance)
main.add_command(ci_commands.ci)


# Add aliases for common commands
@main.command(name="setup", hidden=True)
@click.pass_context
def setup_alias(ctx: click.Context) -> None:
    """Alias for 'naro development setup'"""
    ctx.invoke(development_commands.setup)


@main.command(name="start", hidden=True)
@click.pass_context
def start_alias(ctx: click.Context) -> None:
    """Alias for 'naro services start'"""
    ctx.invoke(service_commands.start)


@main.command(name="stop", hidden=True)
@click.pass_context  
def stop_alias(ctx: click.Context) -> None:
    """Alias for 'naro services stop'"""
    ctx.invoke(service_commands.stop)


@main.command(name="status", hidden=True)
@click.pass_context
def status_alias(ctx: click.Context) -> None:
    """Alias for 'naro services status'"""
    ctx.invoke(service_commands.status)


@main.command(name="logs", hidden=True)
@click.argument("service", required=False)
@click.option("--follow", "-f", is_flag=True, help="Follow log output")
@click.pass_context
def logs_alias(ctx: click.Context, service: Optional[str], follow: bool) -> None:
    """Alias for 'naro services logs'"""
    ctx.invoke(service_commands.logs, service=service, follow=follow)


@main.command(name="test", hidden=True)
@click.argument("test_type", required=False)
@click.option("--all", "run_all", is_flag=True, help="Run all tests")
@click.pass_context
def test_alias(ctx: click.Context, test_type: Optional[str], run_all: bool) -> None:
    """Alias for 'naro testing run'"""
    ctx.invoke(testing_commands.run, test_type=test_type, run_all=run_all)


@main.command(name="build", hidden=True)
@click.argument("target", required=False, default="all")
@click.pass_context
def build_alias(ctx: click.Context, target: str) -> None:
    """Alias for 'naro services build'"""
    ctx.invoke(service_commands.build, target=target)


@main.command(name="shell", hidden=True)
@click.pass_context
def shell_alias(ctx: click.Context) -> None:
    """Alias for 'naro development shell'"""
    ctx.invoke(development_commands.shell)


@main.command(name="doctor", hidden=True)
@click.pass_context
def doctor_alias(ctx: click.Context) -> None:
    """Alias for 'naro maintenance doctor'"""
    ctx.invoke(maintenance_commands.doctor)


@main.command(name="cleanup", hidden=True)
@click.pass_context
def cleanup_alias(ctx: click.Context) -> None:
    """Alias for 'naro maintenance cleanup'"""
    ctx.invoke(maintenance_commands.cleanup)


@main.command(name="version", hidden=True)
@click.pass_context
def version_alias(ctx: click.Context) -> None:
    """Alias for 'naro maintenance version'"""
    ctx.invoke(maintenance_commands.version)


@main.command(name="lint", hidden=True)
@click.argument("path", required=False)
@click.pass_context
def lint_alias(ctx: click.Context, path: Optional[str]) -> None:
    """Alias for 'naro development lint'"""
    ctx.invoke(development_commands.lint, path=path)


@main.command(name="format", hidden=True)
@click.argument("path", required=False)
@click.pass_context
def format_alias(ctx: click.Context, path: Optional[str]) -> None:
    """Alias for 'naro development format'"""
    ctx.invoke(development_commands.format, path=path)


def cli_main() -> None:
    """Entry point for the CLI."""
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(130)
    except NaroException as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        if "--verbose" in sys.argv or "-v" in sys.argv:
            console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    cli_main()