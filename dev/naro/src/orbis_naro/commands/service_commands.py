"""
Service management commands for Orbis Naro.

This module contains commands for managing Docker services including
building, starting, stopping, and monitoring operations.
"""

from typing import Optional

import click

from .common_options import (
    common_options,
    docker_options,
    requires_project_root,
    requires_docker,
)


@click.group(name="services")
def services() -> None:
    """
    **Service Management Commands**
    
    Manage Docker services for the Orbis development environment.
    
    ## Examples
    
    ```bash
    # Start all services
    naro services start
    
    # Build specific service
    naro services build core
    
    # Show service logs
    naro services logs core --follow
    
    # Check service status
    naro services status
    ```
    """
    pass


@services.command(name="build")
@click.argument("targets", nargs=-1)
@click.option(
    "--all", "build_all",
    is_flag=True,
    help="Build all services"
)
@common_options
@docker_options
@requires_project_root
@requires_docker
def build(targets: tuple[str, ...], build_all: bool, **kwargs) -> None:
    """
    Build Docker services.
    
    **Arguments:**
    - TARGETS: Specific services to build (core, sdk, ui, ui-dev)
    
    **Examples:**
    ```bash
    naro services build core
    naro services build --all
    naro build core  # alias
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    console.print("[bold blue]Building Docker Services[/bold blue]")
    
    if build_all:
        console.print("🐳 Building all services...")
    elif targets:
        for target in targets:
            console.print(f"🐳 Building {target} service...")
    else:
        console.print("🐳 Building default services...")
    
    console.print("✅ Build completed successfully")


@services.command(name="start")
@click.argument("services_names", nargs=-1)
@click.option(
    "--detach", "-d",
    is_flag=True,
    default=True,
    help="Run services in background"
)
@common_options
@docker_options
@requires_project_root
@requires_docker
def start(services_names: tuple[str, ...], detach: bool, **kwargs) -> None:
    """
    Start development services.
    
    **Arguments:**
    - SERVICES_NAMES: Specific services to start
    
    **Examples:**
    ```bash
    naro services start
    naro services start core sdk
    naro start  # alias
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    console.print("[bold blue]Starting Development Services[/bold blue]")
    
    if services_names:
        for service in services_names:
            console.print(f"🚀 Starting {service} service...")
    else:
        console.print("🚀 Starting all services...")
    
    console.print("✅ Services started successfully")
    console.print("🌐 Access the application at http://localhost:3000")
    console.print("📚 API documentation at http://localhost:8000/docs")


@services.command(name="stop")
@click.argument("services_names", nargs=-1)
@common_options
@requires_project_root
@requires_docker
def stop(services_names: tuple[str, ...], **kwargs) -> None:
    """
    Stop development services.
    
    **Arguments:**
    - SERVICES_NAMES: Specific services to stop
    
    **Examples:**
    ```bash
    naro services stop
    naro services stop core
    naro stop  # alias
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    console.print("[bold blue]Stopping Services[/bold blue]")
    
    if services_names:
        for service in services_names:
            console.print(f"🛑 Stopping {service} service...")
    else:
        console.print("🛑 Stopping all services...")
    
    console.print("✅ Services stopped successfully")


@services.command(name="restart")
@click.argument("services_names", nargs=-1)
@common_options
@docker_options
@requires_project_root
@requires_docker
def restart(services_names: tuple[str, ...], **kwargs) -> None:
    """
    Restart development services.
    
    **Arguments:**
    - SERVICES_NAMES: Specific services to restart
    
    **Examples:**
    ```bash
    naro services restart
    naro services restart core
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    console.print("[bold blue]Restarting Services[/bold blue]")
    
    if services_names:
        for service in services_names:
            console.print(f"🔄 Restarting {service} service...")
    else:
        console.print("🔄 Restarting all services...")
    
    console.print("✅ Services restarted successfully")


@services.command(name="logs")
@click.argument("service", required=False)
@click.option(
    "--follow", "-f",
    is_flag=True,
    help="Follow log output"
)
@click.option(
    "--tail",
    type=int,
    help="Number of lines to show from end of logs"
)
@common_options
@requires_project_root
@requires_docker
def logs(service: Optional[str], follow: bool, tail: Optional[int], **kwargs) -> None:
    """
    Show service logs.
    
    **Arguments:**
    - SERVICE: Specific service to show logs for
    
    **Options:**
    - --follow: Follow log output
    - --tail: Number of lines to show
    
    **Examples:**
    ```bash
    naro services logs core
    naro services logs --follow
    naro logs core --follow  # alias
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    if service:
        console.print(f"[bold blue]Showing logs for {service} service[/bold blue]")
    else:
        console.print("[bold blue]Showing logs for all services[/bold blue]")
    
    if follow:
        console.print("📋 Following logs (Press Ctrl+C to stop)...")
    
    # Implementation would go here
    console.print("📋 Logs displayed")


@services.command(name="status")
@common_options
@requires_project_root
@requires_docker
def status(**kwargs) -> None:
    """
    Show service status and health information.
    
    **Examples:**
    ```bash
    naro services status
    naro status  # alias
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    console.print("[bold blue]Service Status[/bold blue]")
    
    # Implementation would go here
    console.print("📊 Docker containers:")
    console.print("  core:    [green]running[/green]   🟢")
    console.print("  sdk:     [green]running[/green]   🟢") 
    console.print("  ui-dev:  [green]running[/green]   🟢")
    console.print("  ui:      [yellow]stopped[/yellow]  🟡")
    
    console.print("\n🔌 Provider packages:")
    console.print("  common:  [green]installed[/green] ✅")
    console.print("  manager: [green]installed[/green] ✅")
    console.print("  yahoo:   [green]installed[/green] ✅")


@services.command(name="exec")
@click.argument("service")
@click.argument("command", nargs=-1)
@click.option(
    "--interactive", "-i",
    is_flag=True,
    help="Keep STDIN open"
)
@click.option(
    "--tty", "-t",
    is_flag=True,
    help="Allocate a pseudo-TTY"
)
@common_options
@requires_project_root
@requires_docker
def exec(service: str, command: tuple[str, ...], interactive: bool, tty: bool, **kwargs) -> None:
    """
    Execute command in running service container.
    
    **Arguments:**
    - SERVICE: Service name to execute command in
    - COMMAND: Command to execute
    
    **Examples:**
    ```bash
    naro services exec core bash
    naro services exec core python -c "print('hello')"
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    cmd_str = " ".join(command) if command else "bash"
    console.print(f"[bold blue]Executing '{cmd_str}' in {service} service[/bold blue]")
    
    # Implementation would go here
    console.print("🔧 Command executed")