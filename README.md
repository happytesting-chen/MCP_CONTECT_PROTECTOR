Protection Workflow (End-to-End)

This section describes the complete protection lifecycle, from initial setup to runtime enforcement, using MCP Context Protector as a runtime security layer for MCP-based tools.

Step 1 — Enable MCP Context Protector (Default-Deny Applied)

This step inserts MCP Context Protector into the MCP communication path and enforces a default-deny security posture.

What You Do (One-Time Setup)
1. Install MCP Context Protector

Install the MCP Context Protector wrapper script on the client host.

2. Configure the MCP client to use the wrapper

Configure your MCP client (for example, Cursor) to launch MCP Context Protector instead of connecting directly to the MCP server.

Example: mcp.json (Cursor)
{
  "kali-remote-mcp-wrapper": {
    "command": "/mnt/c/Users/Intern/Documents/mitigation/mcp-context-protector/mcp-context-protector.sh",
    "args": [
      "--sse-url",
      "http://192.168.174.129:8000/sse",
      "--guardrail-provider",
      "Claude"
    ],
    "env": {
      "ANTHROPIC_API_KEY": "sk-ant-xxxx"
    }
  }
}

What Happens Automatically

All MCP traffic is routed through MCP Context Protector

The MCP server is detected but remains untrusted by default

All exposed tools appear as:

context-protector-block

Security Principle

Default-Deny
Newly discovered MCP servers are blocked by default until explicitly approved by a human operator.

Step 2 — Review and Approve MCP Server (Human-in-the-Loop Trust)

Before any tools can be used, the MCP server must be explicitly reviewed and trusted.

Review Commands

Review all unapproved servers:

./mcp-context-protector.sh --review-all-servers


Review a specific server:

./mcp-context-protector.sh \
  --review-server \
  --sse-url http://192.168.174.129:8000/sse

What Is Reviewed

Only MCP server metadata is reviewed:

Tool names

Tool descriptions

Input schemas

Output schemas

What Is NOT Reviewed

Tool execution

Runtime tool behavior

Tool responses

MCP server source code

Result of Approval

Once approved:

The MCP server is marked as trusted

Tools become visible and callable in the MCP client

Step 3 — Runtime Tool Invocation and Response Scanning

After the server is trusted, tools can be used normally.

At runtime, MCP Context Protector:

Proxies every MCP tool invocation

Intercepts all tool responses

Sends responses to the configured guardrail provider (e.g. Claude)

Blocks or quarantines suspicious responses before they reach the LLM

Inspection Model

Runtime behavioral inspection

Response-level enforcement

No static analysis

Step 4 — Monitoring and Visibility

Security activity is observable in real time.

View MCP Logs in Cursor

Press Ctrl + Shift + P

Select Developer: Show Logs

Choose MCP

What You Can See

Guardrail scan decisions

Quarantine events

Runtime enforcement outcomes

Step 5 — Quarantine Handling and Operator Action
Quarantine Storage
cat ~/.mcp-context-protector/quarantine.json

What Quarantine Means

Only the specific tool response instance is blocked

The tool itself remains callable

The MCP server remains connected

Operator Responsibility

If a server or tool is malicious:

Manually remove or disable it in the MCP client configuration, or

Enforce upstream MCP server access controls

Important Limitation (Security Boundary)

⚠️ MCP Context Protector does NOT:

Disable tools permanently

Remove MCP servers automatically

Sandbox or execute MCP tools

Perform static code scanning

Positioning

MCP Context Protector is a runtime detection and containment layer,
not a firewall, static code scanner, or execution sandbox.
