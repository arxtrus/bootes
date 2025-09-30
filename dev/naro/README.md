# Orbis Naro
Orbis Naro helps you easily develop and manage the complex multi-package structure of the Orbis project.

**Location**: `dev/naro/` - can be run from the project root with the `naro` command.

## Quick Start

### Option 1: UV Setup (Recommended)

UV is a fast Python package installer and dependency resolver. Use this for the best performance:

```bash
# Set up using UV (automatically installs UV if needed)
cd dev/naro
./setup-uv.sh

# Verify installation
naro development uv-info

# Use UV commands
naro development uv-sync
naro development uv-add pytest --dev
```

### Option 2: Traditional Setup

```bash
# Complete environment setup
naro setup

# Install providers
naro providers install

# Start services
naro start

# Run tests
naro test --all
```

## Features

### 1. Provider Management

```bash
# Install all providers
naro providers install

# Install a specific provider
naro providers install yahoo

# Test providers
naro providers test
naro providers test yahoo
```

### 2. Service Management

```bash
# Start all services
naro start

# Start a specific service
naro start core

# Stop services
naro stop

# Check service status
naro status
```

### 3. Build Management

```bash
# Build all services
naro build all

# Build specific services
naro build core
naro build sdk
```

### 4. Log Management

```bash
# Logs for all services
naro logs

# Logs for a specific service
naro logs core

# Follow logs in real time
naro logs core --follow
```

### 5. Test Management

```bash
# Run all tests
naro test --all

# Run tests by component
naro test providers
naro test sdk
naro test core
```

### 6. Code Quality

```bash
# Run lint checks
naro lint

# Lint a specific path
naro lint providers/yahoo

# Run code formatting
naro format

# Format a specific path
naro format providers
```

## Usage Details

### Provider Development Workflow

```bash
# 1. Install dependencies for a new provider
naro providers install common manager

# 2. Write code and run tests
naro providers test yahoo

# 3. Check code quality
naro lint providers/yahoo
naro format providers/yahoo

# 4. Run integration tests
naro test --all
```

### Service Development Workflow

```bash
# 1. Set up environment
naro setup

# 2. Start service
naro start

# 3. Rebuild after code changes
naro build core

# 4. Check logs
naro logs core --follow

# 5. Run tests
naro test core
```

### Troubleshooting Workflow

```bash
# 1. Check current status
naro status

# 2. Review logs
naro logs

# 3. Restart services
naro stop
naro start

# 4. Reinstall providers
naro providers install
```

## Advanced Usage

### Reset Development Environment

```bash
# Clean existing environment
naro stop
docker-compose down -v

# Set up a new environment
naro setup
```

### Developing a Specific Provider

```bash
# Yahoo provider example
naro providers install common manager
naro providers install yahoo
naro providers test yahoo
```

### Code Quality Management

```bash
# Lint entire project
naro lint

# Lint providers only
naro lint providers

# Auto-format project
naro format

# Format a specific file
naro format providers/yahoo/src
```

## Naro vs Manual Commands

### Install Providers

**Using Naro:**

```bash
naro providers install
```

**Manual:**

```bash
cd providers/common && python3 -m pip install -e .
cd ../manager && python3 -m pip install -e .
cd ../yahoo && python3 -m pip install -e .
```

### Run Tests

**Using Naro:**

```bash
naro test --all
```

**Manual:**

```bash
cd providers/common && pytest
cd ../yahoo && pytest
cd ../../orbis-sdk && pytest
cd ../orbis-core && pytest
```

### Manage Services

**Using Naro:**

```bash
naro start
naro logs core --follow
```

**Manual:**

```bash
docker-compose up -d
docker-compose logs -f core
```

## Debugging Tools

### Provider Diagnostics

```bash
# Verify provider installations
python3 -c "from orbis.providers.manager import get_manager; print('✅ Manager OK')"
python3 -c "from orbis.providers.yahoo import YahooFinanceProvider; print('✅ Yahoo OK')"

# Auto-discovery test
python3 -c "
from orbis.providers.manager import get_manager
manager = get_manager(auto_discover=True)
print('Available providers:', manager.get_available_providers())
"
```

### Service Connectivity Tests

```bash
# API connection test
curl http://localhost:8000/docs

# Core service logs
naro logs core

# Provider functionality test
python3 -c "
import asyncio
from orbis.providers.manager import get_manager

async def test():
    manager = get_manager(auto_discover=True)
    quote = await manager.get_stock_quote('AAPL')
    print(f'Stock quote: {quote.symbol} = ${quote.price}')

asyncio.run(test())
"
```

## Performance Monitoring

```bash
# Check service resource usage
docker stats

# Analyze logs by level
naro logs core | grep ERROR
naro logs core | grep WARNING

# Response time test
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000/api/v1/stocks/AAPL/info"
```

## Customization

### Add Custom Commands

Modify the `naro` script to add project-specific commands:

```python
def custom_command(self):
    """Custom project-specific command"""
    self.print_header("Running Custom Command")
    # Implement custom logic here
```

### Environment-Specific Configurations

```bash
# Development environment
naro start

# Production simulation
COMPOSE_FILE=docker-compose.prod.yml naro start
```

## Troubleshooting

### Common Issues

1. **Provider import error**

   ```bash
   naro providers install
   ```

2. **Docker service error**

   ```bash
   naro stop
   docker system prune -f
   naro build all
   naro start
   ```

3. **Permission error**

   ```bash
   chmod +x naro
   ```

4. **Python environment issues**

   ```bash
   python3 -m pip install --upgrade pip
   naro setup
   ```

## Best Practices

1. Run `naro setup` before starting development.
2. Before committing, run `naro test --all && naro lint`.
3. After adding a provider, run `naro providers install && naro providers test`.
4. When issues occur, check `naro status && naro logs`.
5. Regularly run `naro format` to maintain code consistency.
