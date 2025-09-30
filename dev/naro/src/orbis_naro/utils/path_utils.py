"""
Path utilities for Orbis Naro.

This module provides utilities for finding project directories,
managing file paths, and working with the Orbis project structure.
"""

import os
from pathlib import Path
from typing import Optional, List

from .exceptions import ProjectNotFoundError


def find_project_root(start_path: Optional[Path] = None) -> Path:
    """
    Find the Orbis project root directory.
    
    Looks for indicators of an Orbis project like pyproject.toml,
    orbis-core/, providers/ directories, etc.
    
    Args:
        start_path: Path to start searching from (default: current directory)
        
    Returns:
        Path to project root
        
    Raises:
        ProjectNotFoundError: If project root cannot be found
    """
    if start_path is None:
        start_path = Path.cwd()
    
    current = start_path.resolve()
    
    # Look for project indicators
    project_indicators = [
        "pyproject.toml",
        "orbis-core",
        "orbis-sdk", 
        "providers",
        "dev/naro",
        ".git",
    ]
    
    # Search up the directory tree
    while current != current.parent:
        # Check if this looks like the project root
        indicator_count = 0
        for indicator in project_indicators:
            if (current / indicator).exists():
                indicator_count += 1
        
        # If we find multiple indicators, this is likely the root
        if indicator_count >= 3:
            return current
        
        # Also check for specific Orbis markers
        if (current / "orbis-core" / "src" / "api" / "main.py").exists():
            return current
            
        if (current / "providers" / "common" / "pyproject.toml").exists():
            return current
        
        current = current.parent
    
    raise ProjectNotFoundError(str(start_path))


def get_providers_dir(project_root: Path) -> Path:
    """
    Get the providers directory path.
    
    Args:
        project_root: Project root directory
        
    Returns:
        Path to providers directory
    """
    return project_root / "providers"


def get_dev_dir(project_root: Path) -> Path:
    """
    Get the dev tools directory path.
    
    Args:
        project_root: Project root directory
        
    Returns:
        Path to dev directory
    """
    return project_root / "dev"


def get_naro_dir(project_root: Path) -> Path:
    """
    Get the naro tool directory path.
    
    Args:
        project_root: Project root directory
        
    Returns:
        Path to naro directory
    """
    return project_root / "dev" / "naro"


def get_core_dir(project_root: Path) -> Path:
    """
    Get the orbis-core directory path.
    
    Args:
        project_root: Project root directory
        
    Returns:
        Path to orbis-core directory
    """
    return project_root / "orbis-core"


def get_sdk_dir(project_root: Path) -> Path:
    """
    Get the orbis-sdk directory path.
    
    Args:
        project_root: Project root directory
        
    Returns:
        Path to orbis-sdk directory
    """
    return project_root / "orbis-sdk"


def find_provider_dirs(providers_dir: Path) -> List[Path]:
    """
    Find all provider directories.
    
    Args:
        providers_dir: Path to providers directory
        
    Returns:
        List of provider directory paths
    """
    if not providers_dir.exists():
        return []
    
    provider_dirs = []
    for item in providers_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            # Check if it looks like a provider (has pyproject.toml)
            if (item / "pyproject.toml").exists():
                provider_dirs.append(item)
    
    return sorted(provider_dirs)


def get_docker_compose_file(project_root: Path, env: str = "dev") -> Path:
    """
    Get the appropriate docker-compose file path.
    
    Args:
        project_root: Project root directory
        env: Environment (dev, prod, test)
        
    Returns:
        Path to docker-compose file
    """
    if env == "dev":
        compose_file = project_root / "docker-compose.yml"
    else:
        compose_file = project_root / f"docker-compose.{env}.yml"
    
    # Fallback to main compose file if specific env file doesn't exist
    if not compose_file.exists():
        compose_file = project_root / "docker-compose.yml"
    
    return compose_file


def get_config_dir() -> Path:
    """
    Get the user configuration directory for Naro.
    
    Returns:
        Path to config directory
    """
    home = Path.home()
    config_dir = home / ".naro"
    config_dir.mkdir(exist_ok=True)
    return config_dir


def get_cache_dir() -> Path:
    """
    Get the cache directory for Naro.
    
    Returns:
        Path to cache directory
    """
    cache_dir = get_config_dir() / "cache"
    cache_dir.mkdir(exist_ok=True)
    return cache_dir


def get_logs_dir() -> Path:
    """
    Get the logs directory for Naro.
    
    Returns:
        Path to logs directory
    """
    logs_dir = get_config_dir() / "logs"
    logs_dir.mkdir(exist_ok=True)
    return logs_dir


def is_relative_to(path: Path, parent: Path) -> bool:
    """
    Check if path is relative to parent (for Python < 3.9 compatibility).
    
    Args:
        path: Path to check
        parent: Parent path
        
    Returns:
        True if path is relative to parent
    """
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def ensure_dir(path: Path) -> Path:
    """
    Ensure directory exists, creating it if necessary.
    
    Args:
        path: Directory path to ensure
        
    Returns:
        The directory path
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_remove(path: Path) -> bool:
    """
    Safely remove a file or directory.
    
    Args:
        path: Path to remove
        
    Returns:
        True if removed successfully, False otherwise
    """
    try:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            import shutil
            shutil.rmtree(path)
        return True
    except (OSError, PermissionError):
        return False


def find_files(directory: Path, pattern: str, recursive: bool = True) -> List[Path]:
    """
    Find files matching a pattern.
    
    Args:
        directory: Directory to search in
        pattern: Glob pattern to match
        recursive: Whether to search recursively
        
    Returns:
        List of matching file paths
    """
    if not directory.exists():
        return []
    
    if recursive:
        return sorted(directory.rglob(pattern))
    else:
        return sorted(directory.glob(pattern))


def get_relative_path(path: Path, relative_to: Path) -> str:
    """
    Get relative path as string, with fallback to absolute path.
    
    Args:
        path: Path to make relative
        relative_to: Base path for relative calculation
        
    Returns:
        Relative path string, or absolute path if not relative
    """
    try:
        return str(path.relative_to(relative_to))
    except ValueError:
        return str(path)