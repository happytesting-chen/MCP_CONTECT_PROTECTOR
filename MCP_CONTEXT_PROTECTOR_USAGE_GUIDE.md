# MCP Context Protector - Complete Usage Guide

## Overview

MCP Context Protector is a security wrapper for MCP (Model Context Protocol) servers that protects against prompt injection attacks, malicious tool responses, and unauthorized server configuration changes. It acts as a transparent proxy between your MCP client and MCP servers, providing multiple layers of security.


## Installation of mcp-context-protector

### Prerequisites
- Python 3.11 or higher
- `uv` package manager

### Step 1: Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Clone and Install
```bash
# Clone the repository
git clone https://github.com/trailofbits/mcp-context-protector
cd mcp-context-protector

# Install dependencies
uv sync
```

---
## MCP client(cursor) setup to wrapper mcp server

### customized guardrail-provider exmaple:
"kali-remote-mcp-wrapper": {
        "command": "/mnt/c/Users/Intern/Documents/mitigation/mcp-context-protector/mcp-context-protector.sh",
        "args": [
          "--sse-url","http://192.168.174.129:8000/sse",
          "--guardrail-provider", "Claude"
        ],
        "env": {
         "ANTHROPIC_API_KEY": "sk-ant-xxxx"
          }

} ### need to configure guardrail-provider, if you want to use Claude
```

# The Protection Workflow

Step 1: Initial Setup - Server Appears Blocked

After configuring the wrapper in `mcp.json` and restarting Cursor:

**Expected behavior:**
- All MCP tools show as `context-protector-block`
- **This is normal** - security is working as intended
- Tools are blocked until you review and approve the server


### Step 2: Review and Approve the Server

Before tools become available, you must manually review the server configuration:
```bash
# Review all unapproved servers
./mcp-context-protector.sh --review-all-servers

# Or review a specific server
./mcp-context-protector.sh --review-server --sse-url http://192.168.174.129:8000/sse
```
we can only see the metadata for the mcp server, choose this server to be trusted, then the tools in the servers will be available

### Step 3: Invoke MCP Tools (Runtime Scanning)

Once approved, use the tools normally through your MCP client (Cursor/Claude):

**What happens behind the scenes:**
- Every tool invocation is proxied through mcp-context-protector
- Tool responses are scanned by the guardrail provider
- Malicious responses are quarantined automatically


### Step 4: Monitor Logs

**View real-time activity in Cursor:**
1. Press `Ctrl + Shift + P`
2. Type: "Developer: Show Logs"
3. Select: "MCP" from dropdown
4. Watch for scan results and quarantine events

# Check quarantine database
cat ~/.mcp-context-protector/quarantine.json

in the agent chat session: the suspicious tool will be flagged as qunrantined by the mcp-context-protextor

### Step 5: Block or Remove Malicious Servers

**⚠️ Important Limitation:**
- Quarantine only blocks individual responses
- Malicious tools remain available for future calls
- You must manually remove dangerous servers


### additional remarks:
the cusmized claude is configured through anthropic_provider.py
after configuration, can check the available guardrail-providers.
**List available providers:**
```bash
./mcp-context-protector.sh --list-guardrail-providers
```







