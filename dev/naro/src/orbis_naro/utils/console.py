"""
Console utilities for Orbis Naro.

This module provides console configuration and utilities for rich output
formatting and user interaction.
"""

import sys
from typing import Optional

from rich.console import Console
from rich.theme import Theme


# Custom theme for Naro
naro_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red bold",
    "success": "green",
    "accent": "blue bold",
    "muted": "dim",
    "highlight": "magenta",
})


def get_console(
    verbose: bool = False,
    quiet: bool = False,
    force_terminal: Optional[bool] = None,
    width: Optional[int] = None,
) -> Console:
    """
    Get a configured Rich console instance.
    
    Args:
        verbose: Enable verbose output
        quiet: Suppress output
        force_terminal: Force terminal mode
        width: Console width
        
    Returns:
        Configured Rich console
    """
    # Determine if we should use rich formatting
    if force_terminal is None:
        # Auto-detect based on environment
        force_terminal = sys.stdout.isatty() and not quiet
    
    # Configure console
    console = Console(
        theme=naro_theme,
        force_terminal=force_terminal,
        width=width,
        quiet=quiet,
        stderr=False,  # Use stdout for all output
    )
    
    return console


def print_header(console: Console, text: str) -> None:
    """Print a formatted header."""
    console.print(f"\n[accent]{text}[/accent]", style="bold")


def print_success(console: Console, text: str) -> None:
    """Print a success message."""
    console.print(f"✅ [success]{text}[/success]")


def print_error(console: Console, text: str) -> None:
    """Print an error message."""
    console.print(f"❌ [error]{text}[/error]")


def print_warning(console: Console, text: str) -> None:
    """Print a warning message."""
    console.print(f"⚠️  [warning]{text}[/warning]")


def print_info(console: Console, text: str) -> None:
    """Print an info message."""
    console.print(f"ℹ️  [info]{text}[/info]")


def print_step(console: Console, step: int, total: int, text: str) -> None:
    """Print a step in a process."""
    console.print(f"[accent][{step}/{total}][/accent] {text}")


def print_table_row(console: Console, columns: list[str], widths: Optional[list[int]] = None) -> None:
    """Print a table row with proper formatting."""
    if widths:
        formatted_columns = []
        for col, width in zip(columns, widths):
            formatted_columns.append(f"{col:<{width}}")
        console.print("  " + " ".join(formatted_columns))
    else:
        console.print("  " + " ".join(columns))


def confirm(console: Console, message: str, default: bool = False) -> bool:
    """
    Ask for user confirmation.
    
    Args:
        console: Rich console instance
        message: Confirmation message
        default: Default value if user just presses enter
        
    Returns:
        True if user confirms, False otherwise
    """
    if default:
        prompt = f"{message} [Y/n]: "
    else:
        prompt = f"{message} [y/N]: "
    
    try:
        response = console.input(prompt).strip().lower()
        
        if not response:
            return default
        
        return response in ('y', 'yes', 'true', '1')
    
    except (KeyboardInterrupt, EOFError):
        console.print("\nOperation cancelled.")
        return False


def progress_spinner(console: Console, message: str):
    """
    Context manager for showing a progress spinner.
    
    Args:
        console: Rich console instance
        message: Message to show with spinner
        
    Example:
        with progress_spinner(console, "Loading..."):
            time.sleep(2)
    """
    return console.status(message, spinner="dots")


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def format_size(bytes_size: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        bytes_size: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f}{unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f}PB"


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text with ellipsis if too long.
    
    Args:
        text: Text to truncate
        max_length: Maximum length before truncation
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."