"""
Custom exceptions for Orbis Naro.

This module defines custom exception classes used throughout the Naro CLI tool
to provide meaningful error messages and appropriate error handling.
"""


class NaroException(Exception):
    """Base exception for all Naro-related errors."""
    
    def __init__(self, message: str, exit_code: int = 1) -> None:
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code


class ProjectNotFoundError(NaroException):
    """Raised when Orbis project root cannot be found."""
    
    def __init__(self, path: str) -> None:
        message = (
            f"Orbis project not found at '{path}'. "
            "Make sure you're running this command from within an Orbis project directory."
        )
        super().__init__(message, exit_code=2)


class DockerNotAvailableError(NaroException):
    """Raised when Docker is not available or not running."""
    
    def __init__(self, reason: str = None) -> None:
        if reason:
            message = f"Docker is not available: {reason}"
        else:
            message = (
                "Docker is not available or not running. "
                "Please ensure Docker is installed and the daemon is running."
            )
        super().__init__(message, exit_code=3)


class ProviderError(NaroException):
    """Raised when there's an error with provider operations."""
    
    def __init__(self, provider_name: str, message: str) -> None:
        full_message = f"Provider '{provider_name}': {message}"
        super().__init__(full_message, exit_code=4)


class ConfigurationError(NaroException):
    """Raised when there's a configuration-related error."""
    
    def __init__(self, message: str, config_file: str = None) -> None:
        if config_file:
            full_message = f"Configuration error in '{config_file}': {message}"
        else:
            full_message = f"Configuration error: {message}"
        super().__init__(full_message, exit_code=5)


class CommandExecutionError(NaroException):
    """Raised when a command execution fails."""
    
    def __init__(self, command: str, return_code: int, stderr: str = None) -> None:
        message = f"Command failed: {command} (exit code {return_code})"
        if stderr:
            message += f"\nError output: {stderr}"
        super().__init__(message, exit_code=6)


class DependencyError(NaroException):
    """Raised when a required dependency is missing or incompatible."""
    
    def __init__(self, dependency: str, version_required: str = None, version_found: str = None) -> None:
        message = f"Dependency error: {dependency}"
        if version_required:
            message += f" (required: {version_required}"
            if version_found:
                message += f", found: {version_found}"
            message += ")"
        super().__init__(message, exit_code=7)


class TestFailureError(NaroException):
    """Raised when tests fail."""
    
    def __init__(self, test_type: str, failures: int, total: int) -> None:
        message = f"{test_type} tests failed: {failures}/{total} tests failed"
        super().__init__(message, exit_code=8)


class BuildError(NaroException):
    """Raised when build operations fail."""
    
    def __init__(self, target: str, message: str) -> None:
        full_message = f"Build failed for '{target}': {message}"
        super().__init__(full_message, exit_code=9)


class NetworkError(NaroException):
    """Raised when network operations fail."""
    
    def __init__(self, operation: str, url: str = None) -> None:
        message = f"Network error during {operation}"
        if url:
            message += f" to {url}"
        super().__init__(message, exit_code=10)


class ValidationError(NaroException):
    """Raised when validation fails."""
    
    def __init__(self, what: str, reason: str) -> None:
        message = f"Validation failed for {what}: {reason}"
        super().__init__(message, exit_code=11)


class SecurityError(NaroException):
    """Raised when security checks fail."""
    
    def __init__(self, issue: str, severity: str = "unknown") -> None:
        message = f"Security issue detected ({severity}): {issue}"
        super().__init__(message, exit_code=12)


def handle_exception(exc: Exception) -> int:
    """
    Handle exceptions and return appropriate exit code.
    
    Args:
        exc: The exception to handle
        
    Returns:
        Exit code for the application
    """
    if isinstance(exc, NaroException):
        return exc.exit_code
    elif isinstance(exc, KeyboardInterrupt):
        return 130  # Standard exit code for SIGINT
    elif isinstance(exc, FileNotFoundError):
        return 2
    elif isinstance(exc, PermissionError):
        return 13
    else:
        return 1  # Generic error