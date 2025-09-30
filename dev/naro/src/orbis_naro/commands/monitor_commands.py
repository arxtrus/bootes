"""
Monitor Commands for Orbis Naro

This module provides tmux-based log monitoring and session management capabilities
for the Orbis development environment, similar to Apache Airflow Breeze.
"""

import subprocess
import time
import signal
import sys
from pathlib import Path
from typing import Optional, List, Dict
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live

from .common_options import common_options, requires_project_root


@click.group(name="monitor")
def monitor() -> None:
    """
    **Monitoring Commands**
    
    tmux-based log monitoring and session management for development services.
    Provides real-time log viewing, session management, and multi-pane monitoring
    similar to Apache Airflow Breeze.
    
    **Key Features:**
    - Multi-service log monitoring in tmux panes
    - Session persistence and restoration
    - Real-time log streaming
    - Customizable layouts
    - Easy navigation between services
    
    **Examples:**
    ```bash
    naro monitor start           # Start monitoring session
    naro monitor logs core       # View core service logs
    naro monitor dashboard       # Interactive dashboard
    naro monitor session list   # List active sessions
    ```
    """
    pass


@monitor.command(name="start")
@click.option(
    "--session-name",
    default="orbis-monitor",
    help="Name for the tmux session"
)
@click.option(
    "--layout",
    type=click.Choice(["grid", "vertical", "horizontal", "dashboard"]),
    default="grid",
    help="Layout for tmux panes"
)
@click.option(
    "--services",
    help="Comma-separated list of services to monitor (default: all)"
)
@click.option(
    "--auto-attach",
    is_flag=True,
    default=True,
    help="Automatically attach to the session"
)
@common_options
@requires_project_root
def start_monitoring(
    session_name: str,
    layout: str,
    services: Optional[str],
    auto_attach: bool,
    **kwargs
) -> None:
    """
    Start tmux monitoring session with service logs.
    
    Creates a tmux session with multiple panes showing real-time logs
    from different Orbis services. Supports various layouts and
    automatic service detection.
    
    **Options:**
    - --session-name: Custom name for tmux session
    - --layout: Choose pane layout (grid, vertical, horizontal, dashboard)
    - --services: Specify which services to monitor
    - --auto-attach: Automatically attach to session after creation
    
    **Examples:**
    ```bash
    naro monitor start
    naro monitor start --layout dashboard
    naro monitor start --services core,ui,sdk
    naro monitor start --session-name my-session --no-auto-attach
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    
    console.print(f"[bold blue]Starting monitoring session: {session_name}[/bold blue]")
    
    # Parse services
    if services:
        service_list = [s.strip() for s in services.split(",")]
    else:
        service_list = _detect_services(project_root)
    
    console.print(f"📊 Monitoring services: {', '.join(service_list)}")
    
    # Check if tmux is available
    if not _check_tmux_available():
        console.print("❌ tmux is not installed. Please install tmux first.")
        console.print("💡 Install with: brew install tmux (macOS) or apt-get install tmux (Ubuntu)")
        return
    
    # Kill existing session if it exists
    _kill_session_if_exists(session_name)
    
    # Create new session
    _create_monitoring_session(session_name, service_list, layout, project_root, console)
    
    if auto_attach:
        console.print(f"🔗 Attaching to session: {session_name}")
        console.print("💡 Use Ctrl+B then D to detach, or 'naro monitor attach' to reattach")
        _attach_to_session(session_name)
    else:
        console.print(f"✅ Session created: {session_name}")
        console.print(f"🔗 Attach with: naro monitor attach {session_name}")


@monitor.command(name="attach")
@click.argument("session_name", default="orbis-monitor")
@common_options
def attach_session(session_name: str, **kwargs) -> None:
    """
    Attach to an existing monitoring session.
    
    **Arguments:**
    - SESSION_NAME: Name of the tmux session to attach to
    
    **Examples:**
    ```bash
    naro monitor attach
    naro monitor attach my-session
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    if not _session_exists(session_name):
        console.print(f"❌ Session '{session_name}' does not exist")
        console.print("📋 Available sessions:")
        _list_sessions(console)
        return
    
    console.print(f"🔗 Attaching to session: {session_name}")
    _attach_to_session(session_name)


@monitor.command(name="detach")
@common_options
def detach_session(**kwargs) -> None:
    """
    Detach from current tmux session.
    
    **Examples:**
    ```bash
    naro monitor detach
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    try:
        subprocess.run(["tmux", "detach"], check=True)
        console.print("🔓 Detached from tmux session")
    except subprocess.CalledProcessError:
        console.print("❌ No active tmux session or failed to detach")


@monitor.command(name="stop")
@click.argument("session_name", default="orbis-monitor")
@common_options
def stop_monitoring(session_name: str, **kwargs) -> None:
    """
    Stop and kill a monitoring session.
    
    **Arguments:**
    - SESSION_NAME: Name of the tmux session to stop
    
    **Examples:**
    ```bash
    naro monitor stop
    naro monitor stop my-session
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    if _kill_session_if_exists(session_name):
        console.print(f"✅ Stopped monitoring session: {session_name}")
    else:
        console.print(f"⚠️  Session '{session_name}' was not running")


@monitor.command(name="list")
@common_options
def list_sessions(**kwargs) -> None:
    """
    List all active tmux sessions.
    
    **Examples:**
    ```bash
    naro monitor list
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    
    console.print("[bold blue]Active tmux sessions:[/bold blue]")
    _list_sessions(console)


@monitor.command(name="status")
@common_options
@requires_project_root
def service_status(**kwargs) -> None:
    """
    Show status of all Orbis services.
    
    Displays current status, ports, and basic health information
    for all services defined in docker-compose files.
    
    **Examples:**
    ```bash
    naro monitor status
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    
    console.print("[bold blue]📊 Orbis Services Status[/bold blue]")
    
    services = _detect_services(project_root)
    compose_file = _get_active_compose_file(project_root)
    
    console.print(f"📁 Using: {Path(compose_file).name}")
    console.print("")
    
    # Create status table
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Service", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("State")
    table.add_column("Health")
    
    for service in services:
        status_info = _get_service_status(service, project_root)
        
        # Status with emoji
        if status_info["state"] == "running":
            status_display = "🟢 Running"
            health = "✅ Healthy" if _check_service_running(service, project_root) else "⚠️ Unknown"
        elif status_info["state"] == "exited":
            status_display = "🔴 Stopped"
            health = "❌ Down"
        else:
            status_display = "🟡 Unknown"
            health = "❓ Unknown"
        
        table.add_row(
            service,
            status_display,
            status_info.get("status", "Unknown"),
            health
        )
    
    console.print(table)
    
    # Show helpful commands
    console.print("\n💡 [bold blue]Quick Actions:[/bold blue]")
    console.print("  naro start                    # Start all services")
    console.print("  naro monitor start            # Start log monitoring")
    console.print("  naro monitor dashboard        # Interactive dashboard")


@monitor.command(name="logs")
@click.argument("service")
@click.option(
    "--follow",
    "-f",
    is_flag=True,
    help="Follow log output (like tail -f)"
)
@click.option(
    "--lines",
    "-n",
    default=100,
    help="Number of lines to show"
)
@common_options
@requires_project_root
def view_logs(service: str, follow: bool, lines: int, **kwargs) -> None:
    """
    View logs for a specific service.
    
    **Arguments:**
    - SERVICE: Name of the service to view logs for
    
    **Options:**
    - --follow, -f: Follow log output in real-time
    - --lines, -n: Number of recent lines to show
    
    **Examples:**
    ```bash
    naro monitor logs core
    naro monitor logs ui --follow
    naro monitor logs api --lines 50
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    
    console.print(f"[bold blue]Viewing logs for service: {service}[/bold blue]")
    
    # Get log command for the service
    log_cmd = _get_service_log_command(service, project_root, follow, lines)
    
    if not log_cmd:
        console.print(f"❌ Unknown service: {service}")
        console.print("📋 Available services:")
        for svc in _detect_services(project_root):
            console.print(f"  - {svc}")
        return
    
    try:
        if follow:
            console.print("💡 Press Ctrl+C to stop following logs")
            subprocess.run(log_cmd, shell=True)
        else:
            result = subprocess.run(log_cmd, shell=True, capture_output=True, text=True)
            console.print(result.stdout)
    except KeyboardInterrupt:
        console.print("\n👋 Stopped following logs")


@monitor.command(name="dashboard")
@click.option(
    "--refresh-interval",
    default=2,
    help="Dashboard refresh interval in seconds"
)
@common_options
@requires_project_root
def dashboard(refresh_interval: int, **kwargs) -> None:
    """
    Start interactive monitoring dashboard.
    
    Provides a real-time dashboard showing service status, logs,
    and system metrics in a rich terminal interface.
    
    **Options:**
    - --refresh-interval: How often to refresh data (seconds)
    
    **Examples:**
    ```bash
    naro monitor dashboard
    naro monitor dashboard --refresh-interval 5
    ```
    """
    ctx = click.get_current_context()
    console = ctx.obj["console"]
    project_root = ctx.obj["project_root"]
    
    console.print("[bold blue]Starting Orbis Monitoring Dashboard[/bold blue]")
    console.print("💡 Press Ctrl+C to exit")
    
    try:
        _run_dashboard(project_root, refresh_interval, console)
    except KeyboardInterrupt:
        console.print("\n👋 Exiting dashboard")


# Helper functions

def _check_tmux_available() -> bool:
    """Check if tmux is available on the system."""
    try:
        subprocess.run(["tmux", "-V"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def _detect_services(project_root: Path) -> List[str]:
    """Auto-detect available services from docker-compose files."""
    services = []
    
    # Check docker-compose files in priority order
    compose_files = [
        ("docker-compose.dev.yml", "Development"),
        ("docker-compose.yml", "Default"),
        ("docker-compose.prod.yml", "Production")
    ]
    
    for compose_file, env_type in compose_files:
        compose_path = project_root / compose_file
        if compose_path.exists():
            try:
                import yaml
                with open(compose_path) as f:
                    compose_data = yaml.safe_load(f)
                    if "services" in compose_data:
                        detected_services = list(compose_data["services"].keys())
                        services.extend(detected_services)
                        # Prefer development environment services
                        if env_type == "Development":
                            break
            except ImportError:
                # Fallback to Orbis default services
                services = ["core", "ui-dev", "sdk"]
                break
            except Exception:
                continue
    
    # Remove duplicates and sort, prioritize common development services
    unique_services = list(dict.fromkeys(services))  # Preserve order while removing duplicates
    
    # Filter out services that are typically not monitored
    filtered_services = [s for s in unique_services if not s.endswith('-test') and not s.endswith('-db')]
    
    return filtered_services if filtered_services else ["core", "ui-dev", "sdk"]


def _session_exists(session_name: str) -> bool:
    """Check if a tmux session exists."""
    try:
        subprocess.run(
            ["tmux", "has-session", "-t", session_name],
            capture_output=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def _kill_session_if_exists(session_name: str) -> bool:
    """Kill tmux session if it exists."""
    if _session_exists(session_name):
        subprocess.run(["tmux", "kill-session", "-t", session_name])
        return True
    return False


def _create_monitoring_session(
    session_name: str,
    services: List[str],
    layout: str,
    project_root: Path,
    console: Console
) -> None:
    """Create tmux session with monitoring panes."""
    
    # Create new session
    subprocess.run([
        "tmux", "new-session", "-d", "-s", session_name,
        "-c", str(project_root)
    ])
    
    # Create panes for each service
    for i, service in enumerate(services):
        if i == 0:
            # First pane is already created
            pane_id = f"{session_name}:0.0"
        else:
            # Split window for additional panes
            if layout == "vertical":
                subprocess.run(["tmux", "split-window", "-v", "-t", session_name])
            elif layout == "horizontal":
                subprocess.run(["tmux", "split-window", "-h", "-t", session_name])
            else:  # grid or dashboard
                if i % 2 == 1:
                    subprocess.run(["tmux", "split-window", "-h", "-t", session_name])
                else:
                    subprocess.run(["tmux", "split-window", "-v", "-t", session_name])
            
            pane_id = f"{session_name}:0.{i}"
        
        # Start log monitoring in each pane
        log_cmd = _get_service_log_command(service, project_root, follow=True, lines=50)
        if log_cmd:
            # Add header with service info and helpful commands
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            header_cmd = (
                f"clear; "
                f"echo '🚀 Monitoring {service.upper()} Service Logs'; "
                f"echo '📂 Project: {project_root.name}'; "
                f"echo '⏰ Started: {current_time}'; "
                f"echo '💡 Press Ctrl+C to stop, Ctrl+B+D to detach'; "
                f"echo ''; "
                f"{log_cmd}"
            )
            
            subprocess.run([
                "tmux", "send-keys", "-t", pane_id,
                header_cmd,
                "Enter"
            ])
        else:
            # Show helpful error message with troubleshooting
            error_cmd = (
                f"clear; "
                f"echo '❌ Service {service} not found or not running'; "
                f"echo ''; "
                f"echo '💡 Troubleshooting:'; "
                f"echo '  1. Check if service is defined: docker compose ps'; "
                f"echo '  2. Start services: naro start'; "
                f"echo '  3. Check service status: naro services status'; "
                f"echo ''; "
                f"echo 'Available services:'; "
                f"docker compose -f {_get_active_compose_file(project_root)} config --services || echo 'No compose file found'"
            )
            
            subprocess.run([
                "tmux", "send-keys", "-t", pane_id,
                error_cmd,
                "Enter"
            ])
    
    # Apply layout
    if layout == "grid":
        subprocess.run(["tmux", "select-layout", "-t", session_name, "tiled"])
    elif layout == "dashboard":
        subprocess.run(["tmux", "select-layout", "-t", session_name, "main-horizontal"])
    
    # Set pane titles
    for i, service in enumerate(services):
        subprocess.run([
            "tmux", "select-pane", "-t", f"{session_name}:0.{i}",
            "-T", f"{service.upper()}"
        ])


def _attach_to_session(session_name: str) -> None:
    """Attach to tmux session."""
    subprocess.run(["tmux", "attach-session", "-t", session_name])


def _list_sessions(console: Console) -> None:
    """List active tmux sessions."""
    try:
        result = subprocess.run(
            ["tmux", "list-sessions"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.stdout.strip():
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Session")
            table.add_column("Windows")
            table.add_column("Created")
            table.add_column("Status")
            
            for line in result.stdout.strip().split('\n'):
                parts = line.split(':')
                if len(parts) >= 2:
                    session_info = parts[1].strip()
                    table.add_row(parts[0], session_info, "Active", "✅")
            
            console.print(table)
        else:
            console.print("📭 No active tmux sessions")
            
    except subprocess.CalledProcessError:
        console.print("❌ Failed to list tmux sessions")


def _get_service_log_command(
    service: str,
    project_root: Path,
    follow: bool = False,
    lines: int = 100
) -> Optional[str]:
    """Get the appropriate log command for a service."""
    
    # Determine which compose file to use
    compose_file = _get_active_compose_file(project_root)
    
    # Docker compose log commands with proper formatting
    compose_cmd = f"docker compose -f {compose_file}"
    
    # Add timestamp and color options for better readability
    base_opts = "--timestamps"
    
    if follow:
        return f"{compose_cmd} logs {base_opts} -f --tail {lines} {service} 2>&1"
    else:
        return f"{compose_cmd} logs {base_opts} --tail {lines} {service} 2>&1"


def _get_active_compose_file(project_root: Path) -> str:
    """Determine which docker-compose file to use."""
    
    # Priority order: dev -> default -> prod
    compose_files = [
        "docker-compose.dev.yml",
        "docker-compose.yml", 
        "docker-compose.prod.yml"
    ]
    
    for compose_file in compose_files:
        compose_path = project_root / compose_file
        if compose_path.exists():
            return str(compose_path)
    
    # Fallback to default
    return str(project_root / "docker-compose.yml")


def _run_dashboard(project_root: Path, refresh_interval: int, console: Console) -> None:
    """Run the interactive monitoring dashboard."""
    
    def generate_dashboard():
        layout = Layout()
        
        # Create header with compose file info
        compose_file = _get_active_compose_file(project_root)
        compose_name = Path(compose_file).name
        header = Panel(
            f"[bold blue]🚀 Orbis Monitoring Dashboard[/bold blue]\n"
            f"Project: {project_root.name} | Compose: {compose_name} | Refresh: {refresh_interval}s\n"
            f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            style="blue"
        )
        
        # Service status table with detailed information
        services = _detect_services(project_root)
        table = Table(show_header=True, header_style="bold green")
        table.add_column("Service", style="cyan")
        table.add_column("Status", style="bold")
        table.add_column("State")
        table.add_column("Ports", style="yellow")
        table.add_column("Updated", style="dim")
        
        for service in services:
            status_info = _get_service_status(service, project_root)
            
            # Status with emoji
            if status_info["state"] == "running":
                status_display = "🟢 Running"
                status_style = "green"
            elif status_info["state"] == "exited":
                status_display = "🔴 Stopped"
                status_style = "red"
            else:
                status_display = "🟡 Unknown"
                status_style = "yellow"
            
            # Format ports
            ports_display = "N/A"
            if status_info.get("ports"):
                ports_list = []
                for port_info in status_info["ports"]:
                    if isinstance(port_info, dict):
                        url = f"{port_info.get('URL', 'N/A')}"
                        ports_list.append(url)
                ports_display = ", ".join(ports_list) if ports_list else "N/A"
            
            table.add_row(
                service,
                f"[{status_style}]{status_display}[/{status_style}]",
                status_info.get("status", "Unknown"),
                ports_display,
                time.strftime("%H:%M:%S")
            )
        
        # System info panel
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            system_info = Panel(
                f"[bold yellow]💻 System Resources[/bold yellow]\n"
                f"CPU: {cpu_percent:.1f}% | "
                f"Memory: {memory.percent:.1f}% | "
                f"Disk: {disk.percent:.1f}%",
                style="yellow"
            )
        except ImportError:
            system_info = Panel(
                "[bold yellow]💻 System Resources[/bold yellow]\n"
                "Install psutil for system metrics: pip install psutil",
                style="yellow"
            )
        
        # Layout structure
        layout.split_column(
            Layout(header, size=4),
            Layout(table, name="services"),
            Layout(system_info, size=3),
        )
        
        return layout
    
    # Live dashboard
    with Live(generate_dashboard(), refresh_per_second=1/refresh_interval) as live:
        while True:
            time.sleep(refresh_interval)
            live.update(generate_dashboard())


def _check_service_running(service: str, project_root: Path) -> bool:
    """Check if a service is running."""
    try:
        compose_file = _get_active_compose_file(project_root)
        result = subprocess.run(
            ["docker", "compose", "-f", compose_file, "ps", service],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        # Check if service is in "Up" state
        return "Up" in result.stdout and service in result.stdout
    except subprocess.CalledProcessError:
        return False


def _get_service_status(service: str, project_root: Path) -> Dict[str, str]:
    """Get detailed status information for a service."""
    try:
        compose_file = _get_active_compose_file(project_root)
        result = subprocess.run(
            ["docker", "compose", "-f", compose_file, "ps", service, "--format", "json"],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        if result.returncode == 0 and result.stdout.strip():
            import json
            try:
                status_data = json.loads(result.stdout)
                if isinstance(status_data, list) and len(status_data) > 0:
                    service_info = status_data[0]
                    return {
                        "name": service_info.get("Name", service),
                        "state": service_info.get("State", "Unknown"),
                        "status": service_info.get("Status", "Unknown"),
                        "ports": service_info.get("Publishers", [])
                    }
            except json.JSONDecodeError:
                pass
        
        # Fallback for older docker-compose versions
        result = subprocess.run(
            ["docker", "compose", "-f", compose_file, "ps", service],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        if "Up" in result.stdout:
            return {"name": service, "state": "running", "status": "Up", "ports": []}
        else:
            return {"name": service, "state": "exited", "status": "Down", "ports": []}
            
    except subprocess.CalledProcessError:
        return {"name": service, "state": "unknown", "status": "Unknown", "ports": []}