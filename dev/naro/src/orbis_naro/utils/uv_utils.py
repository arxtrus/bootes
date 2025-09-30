"""
UV (Universal Python Package Manager) utilities for Orbis Naro.

This module provides utilities for working with uv, the fast Python package installer
and dependency resolver, including installation, environment management, and 
package operations.
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
import shutil

from .exceptions import DependencyError, CommandExecutionError
from .console import get_console


def check_uv_available() -> bool:
    """
    Check if uv is available on the system.
    
    Returns:
        True if uv is available, False otherwise
    """
    return shutil.which("uv") is not None


def get_uv_version() -> Optional[str]:
    """
    Get the installed uv version.
    
    Returns:
        Version string if uv is available, None otherwise
    """
    if not check_uv_available():
        return None
    
    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        # Extract version from output like "uv 0.1.18"
        return result.stdout.strip().split()[1]
    except (subprocess.CalledProcessError, IndexError):
        return None


def install_uv() -> bool:
    """
    Install uv using the recommended installation method.
    
    Returns:
        True if installation was successful, False otherwise
    """
    console = get_console()
    
    console.print("🔧 Installing uv (Universal Python Package Manager)...")
    
    try:
        # Use the official uv installation script
        if sys.platform.startswith("win"):
            # Windows installation
            cmd = ["powershell", "-c", "irm https://astral.sh/uv/install.ps1 | iex"]
        else:
            # Unix-like systems (Linux, macOS)
            cmd = ["curl", "-LsSf", "https://astral.sh/uv/install.sh", "|", "sh"]
            # Use shell=True for pipe operations
            result = subprocess.run(
                "curl -LsSf https://astral.sh/uv/install.sh | sh",
                shell=True,
                check=True
            )
            console.print("✅ uv installed successfully")
            return True
            
    except subprocess.CalledProcessError as e:
        console.print(f"❌ Failed to install uv: {e}")
        return False


def uv_sync(
    project_dir: Path,
    dev: bool = True,
    extra: Optional[List[str]] = None,
    verbose: bool = False
) -> bool:
    """
    Sync dependencies using uv.
    
    Args:
        project_dir: Project directory containing pyproject.toml
        dev: Include development dependencies
        extra: Extra dependency groups to install
        verbose: Enable verbose output
        
    Returns:
        True if sync was successful, False otherwise
    """
    console = get_console(verbose=verbose)
    
    if not check_uv_available():
        console.print("❌ uv is not available. Please install it first.")
        return False
    
    cmd = ["uv", "sync"]
    
    if dev:
        cmd.append("--dev")
    
    if extra:
        for group in extra:
            cmd.extend(["--extra", group])
    
    if verbose:
        cmd.append("--verbose")
    
    try:
        console.print(f"🔄 Syncing dependencies with uv...")
        result = subprocess.run(
            cmd,
            cwd=project_dir,
            check=True,
            capture_output=not verbose,
            text=True
        )
        
        console.print("✅ Dependencies synced successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        console.print(f"❌ Failed to sync dependencies: {e}")
        if hasattr(e, 'stderr') and e.stderr:
            console.print(f"Error details: {e.stderr}")
        return False


def uv_add(
    project_dir: Path,
    packages: List[str],
    dev: bool = False,
    optional: Optional[str] = None,
    verbose: bool = False
) -> bool:
    """
    Add packages using uv.
    
    Args:
        project_dir: Project directory
        packages: List of packages to add
        dev: Add as development dependencies
        optional: Add to optional dependency group
        verbose: Enable verbose output
        
    Returns:
        True if packages were added successfully, False otherwise
    """
    console = get_console(verbose=verbose)
    
    if not check_uv_available():
        console.print("❌ uv is not available. Please install it first.")
        return False
    
    cmd = ["uv", "add"] + packages
    
    if dev:
        cmd.append("--dev")
    
    if optional:
        cmd.extend(["--optional", optional])
    
    if verbose:
        cmd.append("--verbose")
    
    try:
        console.print(f"📦 Adding packages: {', '.join(packages)}")
        result = subprocess.run(
            cmd,
            cwd=project_dir,
            check=True,
            capture_output=not verbose,
            text=True
        )
        
        console.print("✅ Packages added successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        console.print(f"❌ Failed to add packages: {e}")
        return False


def uv_remove(
    project_dir: Path,
    packages: List[str],
    dev: bool = False,
    verbose: bool = False
) -> bool:
    """
    Remove packages using uv.
    
    Args:
        project_dir: Project directory
        packages: List of packages to remove
        dev: Remove from development dependencies
        verbose: Enable verbose output
        
    Returns:
        True if packages were removed successfully, False otherwise
    """
    console = get_console(verbose=verbose)
    
    if not check_uv_available():
        console.print("❌ uv is not available. Please install it first.")
        return False
    
    cmd = ["uv", "remove"] + packages
    
    if dev:
        cmd.append("--dev")
    
    if verbose:
        cmd.append("--verbose")
    
    try:
        console.print(f"🗑️  Removing packages: {', '.join(packages)}")
        result = subprocess.run(
            cmd,
            cwd=project_dir,
            check=True,
            capture_output=not verbose,
            text=True
        )
        
        console.print("✅ Packages removed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        console.print(f"❌ Failed to remove packages: {e}")
        return False


def uv_lock(project_dir: Path, verbose: bool = False) -> bool:
    """
    Generate or update uv.lock file.
    
    Args:
        project_dir: Project directory
        verbose: Enable verbose output
        
    Returns:
        True if lock was successful, False otherwise
    """
    console = get_console(verbose=verbose)
    
    if not check_uv_available():
        console.print("❌ uv is not available. Please install it first.")
        return False
    
    cmd = ["uv", "lock"]
    
    if verbose:
        cmd.append("--verbose")
    
    try:
        console.print("🔒 Generating dependency lock file...")
        result = subprocess.run(
            cmd,
            cwd=project_dir,
            check=True,
            capture_output=not verbose,
            text=True
        )
        
        console.print("✅ Lock file generated successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        console.print(f"❌ Failed to generate lock file: {e}")
        return False


def uv_run(
    project_dir: Path,
    command: List[str],
    verbose: bool = False
) -> subprocess.CompletedProcess:
    """
    Run a command in the uv environment.
    
    Args:
        project_dir: Project directory
        command: Command to run
        verbose: Enable verbose output
        
    Returns:
        CompletedProcess result
    """
    cmd = ["uv", "run"] + command
    
    return subprocess.run(
        cmd,
        cwd=project_dir,
        capture_output=not verbose,
        text=True
    )


def uv_pip_install(
    packages: List[str],
    editable: bool = False,
    requirements_file: Optional[Path] = None,
    verbose: bool = False
) -> bool:
    """
    Install packages using uv pip.
    
    Args:
        packages: List of packages to install
        editable: Install in editable mode
        requirements_file: Requirements file to install from
        verbose: Enable verbose output
        
    Returns:
        True if installation was successful, False otherwise
    """
    console = get_console(verbose=verbose)
    
    if not check_uv_available():
        console.print("❌ uv is not available. Please install it first.")
        return False
    
    cmd = ["uv", "pip", "install"]
    
    if editable:
        cmd.append("--editable")
    
    if requirements_file:
        cmd.extend(["--requirement", str(requirements_file)])
    else:
        cmd.extend(packages)
    
    if verbose:
        cmd.append("--verbose")
    
    try:
        if requirements_file:
            console.print(f"📦 Installing from requirements file: {requirements_file}")
        else:
            console.print(f"📦 Installing packages: {', '.join(packages)}")
            
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=not verbose,
            text=True
        )
        
        console.print("✅ Packages installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        console.print(f"❌ Failed to install packages: {e}")
        return False


def get_uv_info(project_dir: Path) -> Dict[str, Any]:
    """
    Get information about the uv project.
    
    Args:
        project_dir: Project directory
        
    Returns:
        Dictionary with project information
    """
    info = {
        "uv_available": check_uv_available(),
        "uv_version": get_uv_version(),
        "project_dir": str(project_dir),
        "pyproject_exists": (project_dir / "pyproject.toml").exists(),
        "lock_file_exists": (project_dir / "uv.lock").exists(),
    }
    
    return info


def setup_uv_project(project_dir: Path, verbose: bool = False) -> bool:
    """
    Set up a complete uv project environment.
    
    Args:
        project_dir: Project directory
        verbose: Enable verbose output
        
    Returns:
        True if setup was successful, False otherwise
    """
    console = get_console(verbose=verbose)
    
    console.print("🔧 Setting up uv project environment...")
    
    # Check if uv is available
    if not check_uv_available():
        console.print("⚠️  uv not found. Attempting to install...")
        if not install_uv():
            console.print("❌ Failed to install uv. Please install manually.")
            return False
    
    # Initialize uv project if needed
    if not (project_dir / "pyproject.toml").exists():
        console.print("🆕 Initializing new uv project...")
        try:
            subprocess.run(
                ["uv", "init", "--name", "orbis-naro"],
                cwd=project_dir,
                check=True
            )
        except subprocess.CalledProcessError as e:
            console.print(f"❌ Failed to initialize uv project: {e}")
            return False
    
    # Sync dependencies
    if not uv_sync(project_dir, dev=True, verbose=verbose):
        return False
    
    # Generate lock file
    if not uv_lock(project_dir, verbose=verbose):
        return False
    
    console.print("✅ uv project setup completed successfully!")
    return True