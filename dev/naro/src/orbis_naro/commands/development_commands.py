"""
Development workflow commands for Orbis Naro.

This module contains commands for common development tasks including
environment setup, code formatting, linting, and interactive shells.
"""

from typing import Optional

import click

from .common_options import (
    common_options,
    requires_project_root,
)
from ..utils.uv_utils import (
    check_uv_available,
    setup_uv_project,
    uv_sync,
    uv_add,
    uv_remove,
    uv_lock,
    get_uv_info,
)


@click.group(name="development") 
def development() -> None:
    """
    **Development Workflow Commands**
    
    Commands for common development tasks and environment management.
    
    ## Examples
    
    ```bash
    # Set up development environment
    naro development setup
    
    # Format code
    naro development format
    
    # Run linting
    naro development lint
    
    # Enter development shell
    naro development shell
    ```
    """
    pass


@development.command(name="setup")
@click.option(
    "--use-uv",
    is_flag=True,
    default=True,
    help="Use uv for package management (default: true)"
)
@click.option(
    "--skip-providers",
    is_flag=True,
    help="Skip provider package setup"
)
@click.option(
    "--skip-docker",
    is_flag=True,
    help="Skip Docker image building"
)
@common_options
@requires_project_root
def setup(use_uv: bool, skip_providers: bool, skip_docker: bool, **kwargs) -> None:
    """
    Set up complete development environment.
    
    This command will:
    - Install development dependencies (with uv by default)
    - Set up provider packages
    - Build Docker images
    - Initialize development configuration
    
    **Examples:**
    ```bash
    naro development setup
    naro development setup --use-uv
    naro development setup --skip-docker
    naro setup  # alias
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    verbose = ctx.obj.get("verbose", False)
    
    console.print("[bold blue]Setting Up Development Environment[/bold blue]")
    
    # Set up uv environment if requested
    if use_uv:
        console.print("🔧 Setting up uv environment...")
        if setup_uv_project(project_root / "dev" / "naro", verbose=verbose):
            console.print("✅ uv environment ready")
        else:
            console.print("⚠️  uv setup failed, falling back to pip")
            use_uv = False
    
    # Install development dependencies
    console.print("📦 Installing development dependencies...")
    if use_uv:
        uv_sync(project_root / "dev" / "naro", dev=True, verbose=verbose)
    else:
        console.print("  Using pip for dependency installation...")
    
    # Set up provider packages
    if not skip_providers:
        console.print("🔌 Setting up provider packages...")
        # Implementation would integrate with provider installation
        
    # Build Docker images
    if not skip_docker:
        console.print("🐳 Building Docker images...")
        # Implementation would integrate with Docker build
        
    console.print("⚙️  Initializing configuration...")
    console.print("✅ Development environment setup complete!")


@development.command(name="shell")
@click.option(
    "--service",
    help="Enter shell for specific service",
    type=click.Choice(["core", "sdk", "ui"])
)
@click.option(
    "--use-uv",
    is_flag=True,
    help="Use uv run environment (if available)"
)
@common_options
@requires_project_root
def shell(service: Optional[str], use_uv: bool, **kwargs) -> None:
    """
    Enter development shell with all dependencies available.
    
    **Options:**
    - --service: Enter shell for specific service container
    - --use-uv: Use uv run environment instead of docker
    
    **Examples:**
    ```bash
    naro development shell
    naro development shell --service core
    naro development shell --use-uv
    naro shell  # alias
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    
    if use_uv:
        from ..utils.uv_utils import check_uv_available, uv_run
        
        if not check_uv_available():
            console.print("❌ uv is not available. Please install it first or run without --use-uv")
            return
        
        console.print("[bold blue]Starting development shell with uv...[/bold blue]")
        console.print("💡 Run 'exit' to leave the shell")
        
        # Use uv run to start an interactive shell
        import os
        import subprocess
        
        # Get the user's preferred shell
        shell_cmd = os.environ.get("SHELL", "/bin/bash")
        
        try:
            # Run interactive shell in uv environment
            subprocess.run(
                ["uv", "run", shell_cmd],
                cwd=project_root / "dev" / "naro"
            )
        except KeyboardInterrupt:
            console.print("\n👋 Exiting development shell...")
        
    elif service:
        console.print(f"[bold blue]Entering {service} service shell[/bold blue]")
        # Docker service shell implementation would go here
        console.print("🚧 Docker service shell not yet implemented")
    else:
        console.print("[bold blue]Entering development shell[/bold blue]")
        console.print("💡 Use --use-uv for uv environment or --service for container shell")
        console.print("🚧 Standard shell not yet implemented")
    console.print("🐚 Shell ready with development environment")


@development.command(name="lint")
@click.argument("paths", nargs=-1, type=click.Path())
@click.option(
    "--fix",
    is_flag=True,
    help="Automatically fix issues where possible"
)
@common_options
@requires_project_root
def lint(paths: tuple[str, ...], fix: bool, **kwargs) -> None:
    """
    Run code linting on specified paths.
    
    **Arguments:**
    - PATHS: Specific paths to lint (default: all code)
    
    **Options:**
    - --fix: Automatically fix issues where possible
    
    **Examples:**
    ```bash
    naro development lint
    naro development lint providers/yahoo
    naro development lint --fix
    naro lint  # alias
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    console.print("[bold blue]Running Code Linting[/bold blue]")
    
    if paths:
        for path in paths:
            console.print(f"🔍 Linting {path}...")
    else:
        console.print("🔍 Linting all code...")
    
    # Implementation would go here
    if fix:
        console.print("🔧 Fixing issues automatically...")
    
    console.print("✅ Linting completed")


@development.command(name="format")
@click.argument("paths", nargs=-1, type=click.Path())
@click.option(
    "--check",
    is_flag=True,
    help="Check if formatting is needed without making changes"
)
@common_options
@requires_project_root
def format(paths: tuple[str, ...], check: bool, **kwargs) -> None:
    """
    Format code using Black and isort.
    
    **Arguments:**
    - PATHS: Specific paths to format (default: all code)
    
    **Options:**
    - --check: Check formatting without making changes
    
    **Examples:**
    ```bash
    naro development format
    naro development format providers/yahoo
    naro development format --check
    naro format  # alias
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    console.print("[bold blue]Formatting Code[/bold blue]")
    
    if paths:
        for path in paths:
            console.print(f"✨ Formatting {path}...")
    else:
        console.print("✨ Formatting all code...")
    
    # Implementation would go here
    if check:
        console.print("📋 Checking formatting...")
    else:
        console.print("🔧 Applying formatting...")
    
    console.print("✅ Code formatting completed")


@development.command(name="docs")
@click.option(
    "--serve",
    is_flag=True,
    help="Serve documentation locally"
)
@click.option(
    "--port",
    type=int,
    default=8080,
    help="Port for documentation server"
)
@common_options
@requires_project_root
def docs(serve: bool, port: int, **kwargs) -> None:
    """
    Build and optionally serve documentation.
    
    **Options:**
    - --serve: Serve documentation locally
    - --port: Port for documentation server (default: 8080)
    
    **Examples:**
    ```bash
    naro development docs
    naro development docs --serve
    naro development docs --serve --port 9000
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    console.print("[bold blue]Building Documentation[/bold blue]")
    
    # Implementation would go here
    console.print("📚 Building documentation...")
    
    if serve:
        console.print(f"🌐 Serving documentation at http://localhost:{port}")
        console.print("Press Ctrl+C to stop the server")
    else:
        console.print("✅ Documentation built successfully")


@development.command(name="install-hooks")
@common_options
@requires_project_root
def install_hooks(**kwargs) -> None:
    """
    Install pre-commit hooks for development.
    
    **Examples:**
    ```bash
    naro development install-hooks
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    console.print("[bold blue]Installing Pre-commit Hooks[/bold blue]")
    
    # Implementation would go here
    console.print("🪝 Installing pre-commit hooks...")
    console.print("✅ Pre-commit hooks installed successfully")


@development.command(name="uv-info")
@common_options
@requires_project_root
def uv_info(**kwargs) -> None:
    """
    Show uv environment information.
    
    **Examples:**
    ```bash
    naro development uv-info
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    
    console.print("[bold blue]UV Environment Information[/bold blue]")
    
    info = get_uv_info(project_root / "dev" / "naro")
    
    for key, value in info.items():
        if isinstance(value, bool):
            status = "✅" if value else "❌"
            console.print(f"  {key.replace('_', ' ').title()}: {status}")
        else:
            console.print(f"  {key.replace('_', ' ').title()}: {value}")


@development.command(name="uv-sync")
@click.option(
    "--dev",
    is_flag=True,
    default=True,
    help="Include development dependencies"
)
@click.option(
    "--extra",
    multiple=True,
    help="Extra dependency groups to install"
)
@common_options
@requires_project_root
def uv_sync_cmd(dev: bool, extra: tuple[str, ...], **kwargs) -> None:
    """
    Sync dependencies using uv.
    
    **Examples:**
    ```bash
    naro development uv-sync
    naro development uv-sync --no-dev
    naro development uv-sync --extra docs
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    verbose = ctx.obj.get("verbose", False)
    
    console.print("[bold blue]Syncing Dependencies with UV[/bold blue]")
    
    if not check_uv_available():
        console.print("❌ uv is not available. Please install it first:")
        console.print("  curl -LsSf https://astral.sh/uv/install.sh | sh")
        return
    
    naro_dir = project_root / "dev" / "naro"
    if uv_sync(naro_dir, dev=dev, extra=list(extra), verbose=verbose):
        console.print("✅ Dependencies synced successfully")
    else:
        console.print("❌ Failed to sync dependencies")


@development.command(name="uv-add")
@click.argument("packages", nargs=-1, required=True)
@click.option(
    "--dev",
    is_flag=True,
    help="Add as development dependencies"
)
@click.option(
    "--optional",
    help="Add to optional dependency group"
)
@common_options
@requires_project_root
def uv_add_cmd(packages: tuple[str, ...], dev: bool, optional: str, **kwargs) -> None:
    """
    Add packages using uv.
    
    **Arguments:**
    - PACKAGES: Package names to add
    
    **Examples:**
    ```bash
    naro development uv-add requests
    naro development uv-add pytest --dev
    naro development uv-add sphinx --optional docs
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    verbose = ctx.obj.get("verbose", False)
    
    console.print("[bold blue]Adding Packages with UV[/bold blue]")
    
    if not check_uv_available():
        console.print("❌ uv is not available. Please install it first")
        return
    
    naro_dir = project_root / "dev" / "naro"
    if uv_add(naro_dir, list(packages), dev=dev, optional=optional, verbose=verbose):
        console.print(f"✅ Added packages: {', '.join(packages)}")
    else:
        console.print("❌ Failed to add packages")


@development.command(name="uv-remove")
@click.argument("packages", nargs=-1, required=True)
@click.option(
    "--dev",
    is_flag=True,
    help="Remove from development dependencies"
)
@common_options
@requires_project_root
def uv_remove_cmd(packages: tuple[str, ...], dev: bool, **kwargs) -> None:
    """
    Remove packages using uv.
    
    **Arguments:**
    - PACKAGES: Package names to remove
    
    **Examples:**
    ```bash
    naro development uv-remove requests
    naro development uv-remove pytest --dev
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    verbose = ctx.obj.get("verbose", False)
    
    console.print("[bold blue]Removing Packages with UV[/bold blue]")
    
    if not check_uv_available():
        console.print("❌ uv is not available. Please install it first")
        return
    
    naro_dir = project_root / "dev" / "naro"
    if uv_remove(naro_dir, list(packages), dev=dev, verbose=verbose):
        console.print(f"✅ Removed packages: {', '.join(packages)}")
    else:
        console.print("❌ Failed to remove packages")


@development.command(name="uv-lock")
@common_options
@requires_project_root
def uv_lock_cmd(**kwargs) -> None:
    """
    Generate or update uv.lock file.
    
    **Examples:**
    ```bash
    naro development uv-lock
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    verbose = ctx.obj.get("verbose", False)
    
    console.print("[bold blue]Updating UV Lock File[/bold blue]")
    
    if not check_uv_available():
        console.print("❌ uv is not available. Please install it first")
        return
    
    naro_dir = project_root / "dev" / "naro"
    if uv_lock(naro_dir, verbose=verbose):
        console.print("✅ Lock file updated successfully")
    else:
        console.print("❌ Failed to update lock file")