#!/bin/bash

# MCP Context Protector Setup Script
# This script helps users set up the project dependencies

set -e  # Exit on any error

echo "🔧 Setting up MCP Context Protector..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ 'uv' is not installed."
    echo "📦 Installing uv..."
    
    # Install uv
    if command -v curl &> /dev/null; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    else
        echo "❌ curl is not available. Please install curl first or install uv manually:"
        echo "   Visit: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
    
    # Source the shell configuration to make uv available
    if [ -f "$HOME/.bashrc" ]; then
        source "$HOME/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        source "$HOME/.zshrc"
    fi
    
    # Check if uv is now available
    if ! command -v uv &> /dev/null; then
        echo "⚠️  uv was installed but is not in PATH. Please restart your terminal or run:"
        echo "   source ~/.bashrc  # or source ~/.zshrc"
        echo "   Then run this setup script again."
        exit 1
    fi
fi

echo "✅ uv is available"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Install project dependencies
echo "📦 Installing project dependencies..."
uv sync

# Make the launcher script executable
chmod +x mcp-context-protector.sh

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Test the installation:"
echo "   ./mcp-context-protector.sh --help"
echo ""
echo "2. Configure your MCP client to use this wrapper:"
echo "   Command: $(pwd)/mcp-context-protector.sh"
echo "   Args: [--command \"your-mcp-server-command\"]"
echo ""
echo "3. See README.md for detailed usage instructions"
