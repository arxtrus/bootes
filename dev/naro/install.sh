#!/bin/bash
# Orbis Naro simple installation script

set -e

echo "🚀 Installing Orbis Naro..."

# Install uv if not available
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install naro locally
echo "🔧 Installing naro..."
cd "$(dirname "$0")"
uv sync

# Create global naro command
mkdir -p ~/.local/bin
NARO_PATH="$(pwd)"
cat > ~/.local/bin/naro << EOF
#!/bin/bash
cd "${NARO_PATH}" || {
    echo "❌ Cannot find naro installation"
    exit 1
}
uv run python -m orbis_naro "\$@"
EOF

chmod +x ~/.local/bin/naro

# Add to PATH if needed
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc 2>/dev/null || true
    echo "✅ Added ~/.local/bin to PATH"
fi

echo "✅ Orbis Naro installed!"
echo "💡 Restart terminal or run: export PATH=\"\$HOME/.local/bin:\$PATH\""
echo "🎯 Then run: naro setup"