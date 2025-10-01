"""
Maintenance commands for Orbis Naro.
"""

import subprocess

import click

from .common_options import (
    common_options,
    requires_project_root,
)


@click.group(name="maintenance")
def maintenance() -> None:
    """Maintenance commands"""
    pass


@maintenance.command(name="cleanup")
@common_options
@requires_project_root
def cleanup(**kwargs) -> None:
    """Clean up environment"""
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    
    console.print("[bold blue]Cleaning Up Environment[/bold blue]")
    
    try:
        # Clean Docker containers and images
        subprocess.run(["docker", "system", "prune", "-f"], cwd=project_root, check=True)
        console.print("✅ Docker cleanup completed")
        
        # Clean Python cache
        subprocess.run(["find", ".", "-name", "__pycache__", "-type", "d", "-exec", "rm", "-rf", "{}", "+"], 
                      cwd=project_root, check=True)
        console.print("✅ Python cache cleaned")
        
        console.print("✅ Cleanup completed successfully")
    except subprocess.CalledProcessError:
        console.print("❌ Cleanup failed")
    except FileNotFoundError:
        console.print("❌ Required tools not found")