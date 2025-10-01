#!/bin/bash
# Orbis Naro uninstall script

echo "🗑️  Uninstalling Orbis Naro..."

# Remove global naro command
if [[ -f ~/.local/bin/naro ]]; then
    rm -f ~/.local/bin/naro
    echo "✅ Removed naro command"
fi

# Uninstall pip package if exists
if python3 -m pip list | grep -q "orbis-naro"; then
    echo "🔧 Removing pip package..."
    python3 -m pip uninstall orbis-naro -y
    echo "✅ Removed orbis-naro package"
fi

# Check for uv installation
if command -v uv &> /dev/null && [[ -f "$(dirname "$0")/pyproject.toml" ]]; then
    echo "🔧 Removing uv installation..."
    cd "$(dirname "$0")"
    uv pip uninstall orbis-naro 2>/dev/null || true
    echo "✅ Cleaned uv installation"
fi

echo "✅ Orbis Naro uninstalled!"
echo "💡 You may want to remove ~/.local/bin from PATH manually if not needed"