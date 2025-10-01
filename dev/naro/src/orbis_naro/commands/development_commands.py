"""
Development workflow commands for Orbis Naro.
"""

from typing import Optional
import subprocess

import click

from .common_options import (
    common_options,
    requires_project_root,
)
# No additional utils needed


@click.group(name="development") 
def development() -> None:
    """Development commands"""
    pass


@development.command(name="setup")
@common_options
@requires_project_root
def setup(**kwargs) -> None:
    """Setup development environment"""
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    console.print("[bold blue]Setting Up Development Environment[/bold blue]")
    
    try:
        # Just sync dependencies
        subprocess.run(["uv", "sync"], check=True)
        console.print("✅ Setup complete!")
    except subprocess.CalledProcessError:
        console.print("❌ Setup failed. Run 'uv sync' manually")
    except FileNotFoundError:
        console.print("❌ uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh")


@development.command(name="test")
@click.option("--all", "run_all", is_flag=True, help="Run all tests")
@common_options
@requires_project_root
def test(run_all: bool, **kwargs) -> None:
    """Run tests"""
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    
    console.print("[bold blue]Running Tests[/bold blue]")
    
    try:
        if run_all:
            console.print("🧪 Running all tests...")
            subprocess.run(["pytest", "-v"], cwd=project_root, check=True)
        else:
            console.print("🧪 Running core tests...")
            subprocess.run(["pytest", "tests/", "-v"], cwd=project_root, check=True)
        
        console.print("✅ Tests completed successfully")
    except subprocess.CalledProcessError:
        console.print("❌ Tests failed")
    except FileNotFoundError:
        console.print("❌ pytest not found. Run 'naro setup' first")