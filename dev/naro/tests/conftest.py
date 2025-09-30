"""
Test configuration for Orbis Naro.

This module contains pytest fixtures and configuration for testing
the Naro CLI tool.
"""

import tempfile
from pathlib import Path
from typing import Iterator

import pytest
from click.testing import CliRunner


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a Click CLI runner for testing commands."""
    return CliRunner()


@pytest.fixture
def temp_project_dir() -> Iterator[Path]:
    """Provide a temporary directory that looks like an Orbis project."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_dir = Path(temp_dir)
        
        # Create basic project structure
        (project_dir / "pyproject.toml").write_text("[project]\nname = 'test-orbis'\n")
        (project_dir / "orbis-core").mkdir()
        (project_dir / "orbis-sdk").mkdir()
        (project_dir / "providers").mkdir()
        (project_dir / "providers" / "common").mkdir()
        (project_dir / "providers" / "common" / "pyproject.toml").write_text("[project]\nname = 'test'\n")
        
        yield project_dir


@pytest.fixture
def mock_docker_available(monkeypatch):
    """Mock Docker availability."""
    def mock_ping():
        return True
    
    def mock_from_env():
        class MockClient:
            def ping(self):
                return mock_ping()
        return MockClient()
    
    monkeypatch.setattr("docker.from_env", mock_from_env)


@pytest.fixture
def mock_console():
    """Provide a mock console for testing."""
    from unittest.mock import Mock
    return Mock()