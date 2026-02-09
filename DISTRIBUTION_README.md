# MCP Context Protector - Quick Setup Guide

## For New Users

### 1. Quick Setup (Recommended)
```bash
# Clone or download this repository
cd mcp-context-protector

# Run the setup script
./setup.sh
```

### 2. Manual Setup
If the setup script doesn't work, follow these steps:

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # or restart your terminal

# 2. Install project dependencies
cd mcp-context-protector
uv sync

# 3. Make the launcher executable
chmod +x mcp-context-protector.sh
```

### 3. Test Installation
```bash
./mcp-context-protector.sh --help
```

### 4. Configure Your MCP Client

Add this to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "wrapped_server": {
      "command": "/full/path/to/mcp-context-protector/mcp-context-protector.sh",
      "args": ["--command", "your-original-mcp-server-command"]
    }
  }
}
```

**Important**: Use the full absolute path to `mcp-context-protector.sh` in your configuration.

## Troubleshooting

### "uv: command not found"
- Run the setup script: `./setup.sh`
- Or install uv manually: https://docs.astral.sh/uv/getting-started/installation/

### "Project dependencies not installed"
- Run: `uv sync` in the project directory

### Permission denied
- Make sure the script is executable: `chmod +x mcp-context-protector.sh`

## What This Does

This wrapper adds security controls to MCP servers:
- ✅ Server configuration pinning (trust-on-first-use)
- ✅ Tool response scanning for prompt injection attacks
- ✅ ANSI control character sanitization
- ✅ Automatic blocking of unapproved configuration changes

See the main README.md for detailed documentation.
