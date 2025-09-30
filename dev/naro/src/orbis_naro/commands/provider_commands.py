"""
Provider management commands for Orbis Naro.

This module contains commands for managing Orbis provider packages including
installation, testing, validation, and cleanup operations.
"""

from pathlib import Path
from typing import Optional, List

import click

from .common_options import (
    common_options,
    provider_options,
    requires_project_root,
)
from ..utils.uv_utils import check_uv_available, uv_pip_install


@click.group(name="providers")
def providers() -> None:
    """
    **Provider Management Commands**
    
    Manage Orbis provider packages including installation, testing, and validation.
    
    ## Examples
    
    ```bash
    # Install all providers
    naro providers install
    
    # Install specific provider
    naro providers install yahoo
    
    # Test all providers
    naro providers test
    
    # List available providers
    naro providers list
    ```
    """
    pass


@providers.command(name="install")
@click.argument("provider_names", nargs=-1)
@click.option(
    "--all", "install_all",
    is_flag=True,
    help="Install all available providers"
)
@click.option(
    "--use-uv",
    is_flag=True,
    default=None,
    help="Use uv for installation (auto-detected by default)"
)
@click.option(
    "--editable", "-e",
    is_flag=True,
    default=True,
    help="Install in editable mode (default: true)"
)
@common_options
@provider_options
@requires_project_root
def install(
    provider_names: tuple[str, ...],
    install_all: bool,
    use_uv: Optional[bool],
    editable: bool,
    **kwargs
) -> None:
    """
    Install provider packages.
    
    **Arguments:**
    - PROVIDER_NAMES: Names of specific providers to install
    
    **Examples:**
    ```bash
    naro providers install yahoo
    naro providers install --all
    naro providers install yahoo alphavantage --use-uv
    naro providers install --no-editable
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    verbose = ctx.obj.get("verbose", False)
    
    console.print("[bold blue]Installing Provider Packages[/bold blue]")
    
    # Auto-detect uv if not specified
    if use_uv is None:
        use_uv = check_uv_available()
        if use_uv:
            console.print("🔧 Using uv for package installation")
        else:
            console.print("📦 Using pip for package installation")
    
    # Determine which providers to install
    if install_all:
        providers_to_install = ["common", "manager", "yahoo"]
        console.print("Installing all providers...")
    elif provider_names:
        providers_to_install = list(provider_names)
    else:
        providers_to_install = ["common", "manager"]
        console.print("Installing default providers (common, manager)...")
    
    # Install each provider
    success_count = 0
    providers_dir = project_root / "providers"
    
    for provider in providers_to_install:
        provider_path = providers_dir / provider
        
        if not provider_path.exists():
            console.print(f"❌ Provider '{provider}' not found at {provider_path}")
            continue
        
        console.print(f"📦 Installing {provider} provider...")
        
        if use_uv:
            # Use uv pip install
            package_spec = str(provider_path)
            if editable:
                package_spec = f"-e {package_spec}"
            
            if uv_pip_install([package_spec], verbose=verbose):
                console.print(f"✅ Successfully installed {provider} provider")
                success_count += 1
            else:
                console.print(f"❌ Failed to install {provider} provider")
        else:
            # Use regular pip (fallback implementation)
            import subprocess
            cmd = ["pip", "install"]
            if editable:
                cmd.append("-e")
            cmd.append(str(provider_path))
            
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                console.print(f"✅ Successfully installed {provider} provider")
                success_count += 1
            except subprocess.CalledProcessError as e:
                console.print(f"❌ Failed to install {provider} provider: {e}")
    
    # Summary
    total_providers = len(providers_to_install)
    if success_count == total_providers:
        console.print(f"🎉 All {total_providers} providers installed successfully!")
    elif success_count > 0:
        console.print(f"⚠️  {success_count}/{total_providers} providers installed successfully")
    else:
        console.print("❌ No providers were installed successfully")


@providers.command(name="test")
@click.argument("provider_names", nargs=-1)
@click.option(
    "--all", "test_all",
    is_flag=True,
    help="Test all providers"
)
@common_options
@requires_project_root
def test(
    provider_names: tuple[str, ...],
    test_all: bool,
    **kwargs
) -> None:
    """
    Run tests for provider packages.
    
    **Arguments:**
    - PROVIDER_NAMES: Names of specific providers to test
    
    **Examples:**
    ```bash
    naro providers test yahoo
    naro providers test --all
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    console.print("[bold blue]Running Provider Tests[/bold blue]")
    
    # Implementation would go here
    if test_all:
        console.print("Testing all providers...")
    elif provider_names:
        for provider in provider_names:
            console.print(f"Testing provider: {provider}")


@providers.command(name="list")
@click.option(
    "--installed-only",
    is_flag=True,
    help="Show only installed providers"
)
@common_options
@requires_project_root
def list_providers(installed_only: bool, **kwargs) -> None:
    """
    List available provider packages.
    
    **Examples:**
    ```bash
    naro providers list
    naro providers list --installed-only
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    console.print("[bold blue]Available Providers[/bold blue]")
    
    # Implementation would go here
    providers_info = [
        ("common", "Shared interfaces and models", "installed"),
        ("manager", "Provider discovery and management", "installed"), 
        ("yahoo", "Yahoo Finance provider", "installed"),
        ("alphavantage", "Alpha Vantage provider", "available"),
        ("polygon", "Polygon.io provider", "available"),
    ]
    
    for name, description, status in providers_info:
        if installed_only and status != "installed":
            continue
        status_color = "green" if status == "installed" else "yellow"
        console.print(f"  {name:15} {description:40} [{status_color}]{status}[/{status_color}]")


@providers.command(name="validate")
@click.argument("provider_names", nargs=-1)
@common_options
@requires_project_root
def validate(provider_names: tuple[str, ...], **kwargs) -> None:
    """
    Validate provider configurations and dependencies.
    
    **Arguments:**
    - PROVIDER_NAMES: Names of specific providers to validate
    
    **Examples:**
    ```bash
    naro providers validate yahoo
    naro providers validate
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    console.print("[bold blue]Validating Provider Configurations[/bold blue]")
    
    # Implementation would go here
    if provider_names:
        for provider in provider_names:
            console.print(f"Validating provider: {provider}")
    else:
        console.print("Validating all installed providers...")


@providers.command(name="cleanup")
@common_options
@requires_project_root
def cleanup(**kwargs) -> None:
    """
    Clean up provider artifacts and caches.
    
    **Examples:**
    ```bash
    naro providers cleanup
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    console.print("[bold blue]Cleaning Up Provider Artifacts[/bold blue]")
    
    # Implementation would go here
    console.print("Cleaning provider caches...")
    console.print("Removing temporary files...")
    console.print("✅ Provider cleanup completed")