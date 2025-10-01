"""
Service management commands for Orbis Naro.
"""

from typing import Optional
import subprocess

import click

from .common_options import (
    common_options,
    requires_project_root,
)


@click.group(name="services")
def services() -> None:
    """Service management commands"""
    pass


@services.command(name="build")
@click.argument("target", required=False, default="all")
@common_options
@requires_project_root
def build(target: str, **kwargs) -> None:
    """Build services"""
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    
    console.print(f"[bold blue]Building {target}[/bold blue]")
    
    try:
        if target == "all":
            subprocess.run(["docker-compose", "build"], cwd=project_root, check=True)
        else:
            subprocess.run(["docker-compose", "build", target], cwd=project_root, check=True)
        console.print("✅ Build completed successfully")
    except subprocess.CalledProcessError:
        console.print("❌ Build failed")
    except FileNotFoundError:
        console.print("❌ docker-compose not found")


@services.command(name="start")
@common_options
@requires_project_root
def start(**kwargs) -> None:
    """Start services"""
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    
    console.print("[bold blue]Starting Services[/bold blue]")
    
    try:
        subprocess.run(["docker-compose", "up", "-d"], cwd=project_root, check=True)
        console.print("✅ Services started successfully")
    except subprocess.CalledProcessError:
        console.print("❌ Failed to start services")
    except FileNotFoundError:
        console.print("❌ docker-compose not found")


@services.command(name="stop")
@common_options
@requires_project_root
def stop(**kwargs) -> None:
    """Stop services"""
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    
    console.print("[bold blue]Stopping Services[/bold blue]")
    
    try:
        subprocess.run(["docker-compose", "down"], cwd=project_root, check=True)
        console.print("✅ Services stopped successfully")
    except subprocess.CalledProcessError:
        console.print("❌ Failed to stop services")
    except FileNotFoundError:
        console.print("❌ docker-compose not found")


@services.command(name="status")
@common_options
@requires_project_root
def status(**kwargs) -> None:
    """Check service status"""
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    
    console.print("[bold blue]Service Status[/bold blue]")
    
    try:
        subprocess.run(["docker-compose", "ps"], cwd=project_root, check=True)
    except subprocess.CalledProcessError:
        console.print("❌ Failed to check status")
    except FileNotFoundError:
        console.print("❌ docker-compose not found")


@services.command(name="logs")
@click.argument("service", required=False)
@click.option("--follow", "-f", is_flag=True, help="Follow log output")
@common_options
@requires_project_root
def logs(service: Optional[str], follow: bool, **kwargs) -> None:
    """View service logs"""
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    
    if service:
        console.print(f"[bold blue]Logs for {service}[/bold blue]")
    else:
        console.print("[bold blue]All Service Logs[/bold blue]")
    
    try:
        cmd = ["docker-compose", "logs"]
        if follow:
            cmd.append("-f")
        if service:
            cmd.append(service)
        
        subprocess.run(cmd, cwd=project_root, check=True)
    except subprocess.CalledProcessError:
        console.print("❌ Failed to show logs")
    except FileNotFoundError:
        console.print("❌ docker-compose not found")