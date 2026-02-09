# 🛡️ MCP Context Protector - Protection Workflow

> **Runtime Security Layer for Model Context Protocol (MCP) Tools**

This document describes the complete protection lifecycle, from initial setup to runtime enforcement, using MCP Context Protector as a runtime security layer for MCP-based tools.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Workflow Diagram](#workflow-diagram)
- [Step 1: Enable Protection](#step-1--enable-mcp-context-protector)
- [Step 2: Review & Approve](#step-2--review-and-approve-mcp-server)
- [Step 3: Runtime Scanning](#step-3--runtime-tool-invocation-and-response-scanning)
- [Step 4: Monitoring](#step-4--monitoring-and-visibility)
- [Step 5: Quarantine Handling](#step-5--quarantine-handling-and-operator-action)
- [Security Boundaries](#security-boundaries)

---

## 🎯 Overview

MCP Context Protector enforces a **default-deny security posture** with human-in-the-loop approval and runtime response inspection to prevent malicious MCP tool outputs from reaching LLMs.

### Key Principles

- ✅ **Default-Deny**: New servers blocked until explicitly approved
- 👤 **Human Approval**: Trust decisions require operator review
- 🔍 **Runtime Inspection**: Behavioral analysis of tool responses
- 🚫 **Response Blocking**: Suspicious outputs quarantined before reaching LLM

---

## 🔄 Workflow Diagram

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Install   │───▶│   Review    │───▶│    Scan     │───▶│  Quarantine │───▶│   Monitor   │
│  Protection │    │  & Approve  │    │  Responses  │    │   Threats   │    │  & Review   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## 📥 Step 1 — Enable MCP Context Protector

> **Objective**: Insert MCP Context Protector into the communication path and apply default-deny security

### What You Do (One-Time Setup)

#### 1️⃣ Install MCP Context Protector

Install the MCP Context Protector wrapper script on the client host.
```
# Example installation
## Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
## Download mcp-context-protector
git clone https://github.com/happytesting-chen/MCP_CONTECT_PROTECTOR.git
## Install dependencies
cd MCP_CONTECT_PROTECTOR
uv sync
```

#### 2️⃣ Start the remote MCP Server: 
python3 server.py 

#### 3️⃣  Configure the MCP Client

Configure your MCP client (e.g., Cursor, Claude Desktop) to launch MCP Context Protector instead of connecting directly to the MCP server.

**Example: `mcp.json` (Cursor)**

```json
{
  "kali-remote-mcp-wrapper": {
    "command": "/mnt/c/Users/Intern/Documents/mitigation/mcp-context-protector/mcp-context-protector.sh",
    "args": [
      "--sse-url", "http://192.168.174.129:8000/sse",
      "--guardrail-provider", "Claude"
    ],
    "env": {
      "ANTHROPIC_API_KEY": "sk-ant-xxxx"
    }
  }
}
```

### What Happens Automatically

| Action | Result |
|--------|--------|
| 🔀 **Traffic Routing** | All MCP traffic is routed through MCP Context Protector |
| 🔒 **Default State** | MCP server detected but remains **UNTRUSTED** by default |
| 🚫 **Tool Visibility** | All exposed tools appear as `context-protector-block` |

### 🔐 Security Principle

> **Default-Deny**: Newly discovered MCP servers are **blocked by default** until explicitly approved by a human operator.

---

## 👁️ Step 2 — Review and Approve MCP Server

> **Objective**: Human-in-the-loop trust decision before tools can be used

### Review Commands

**Review all unapproved servers:**
```bash
./mcp-context-protector.sh --review-all-servers
```

**Review a specific server:**
```bash
./mcp-context-protector.sh --review-server --sse-url http://192.168.174.129:8000/sse
```

### What Is Reviewed

Only **MCP server metadata** is reviewed:

- ✅ Tool names
- ✅ Tool descriptions
- ✅ Input schemas
- ✅ Output schemas

### What Is NOT Reviewed

- ❌ Tool execution
- ❌ Runtime tool behavior
- ❌ Tool responses
- ❌ MCP server source code

### Result of Approval

Once approved:

| Before | After |
|--------|-------|
| 🚫 Server untrusted | ✅ Server marked as **trusted** |
| 🔒 Tools blocked | 🔓 Tools **visible and callable** in MCP client |

---

## 🔍 Step 3 — Runtime Tool Invocation and Response Scanning

> **Objective**: Active protection during production use

After the server is trusted, tools can be used normally. At runtime, MCP Context Protector:

### Protection Flow

```
1. 📤 Proxy every MCP tool invocation
        ↓
2. 🔍 Intercept all tool responses
        ↓
3. 🤖 Send responses to guardrail provider (e.g., Claude)
        ↓
4. 🛡️ Block or quarantine suspicious responses before they reach the LLM
```

### Inspection Model

| Feature | Description |
|---------|-------------|
| **Runtime Behavioral Inspection** | Analyzes tool behavior during execution |
| **Response-Level Enforcement** | Blocks at the response level, not code level |
| **No Static Analysis** | Does not scan MCP server source code |

---

## 📊 Step 4 — Monitoring and Visibility

> **Objective**: Real-time observability of security activity

### View MCP Logs in Cursor

1. Press `Ctrl + Shift + P`
2. Select `Developer: Show Logs`
3. Choose `MCP`

### What You Can See

- ✅ **Guardrail scan decisions** — What was allowed or blocked
- ⚠️ **Quarantine events** — When responses were quarantined
- 📊 **Runtime enforcement outcomes** — Overall security posture

### Example Log Output

```
[2024-02-09 14:32:15] ✓ Tool invocation: file_read - ALLOWED
[2024-02-09 14:32:18] ⚠️ Response scan: SUSPICIOUS pattern detected
[2024-02-09 14:32:18] 🛡️ Action: QUARANTINED - blocked from LLM context
[2024-02-09 14:32:22] ✓ Tool invocation: web_search - ALLOWED
```

---

## 🗃️ Step 5 — Quarantine Handling and Operator Action

> **Objective**: Review and respond to blocked threats

### Quarantine Storage

View quarantined responses:

```bash
cat ~/.mcp-context-protector/quarantine.json
```

### What Quarantine Means

| Scope | Status |
|-------|--------|
| ⚠️ Specific response instance | ❌ **Blocked** |
| 🔧 Tool itself | ✅ **Remains callable** |
| 🌐 MCP server connection | ✅ **Stays connected** |

> **Important**: Only the suspicious response is blocked — the tool and server remain operational.

### Operator Responsibility

If a server or tool is confirmed malicious:

1. **Manually remove or disable it** in the MCP client configuration, OR
2. **Enforce upstream MCP server access controls**

---

## ⚠️ Security Boundaries

### What MCP Context Protector DOES

| Capability | Description |
|------------|-------------|
| ✅ Runtime detection & containment | Detects threats during execution |
| ✅ Response-level inspection | Scans tool responses before LLM |
| ✅ Default-deny onboarding | Blocks unknown servers by default |
| ✅ Human-approved trust | Requires operator approval |
| ✅ Quarantine suspicious outputs | Blocks malicious responses |
| ✅ Real-time monitoring | Provides visibility into security events |

### What MCP Context Protector Does NOT Do

| Limitation | Explanation |
|------------|-------------|
| ❌ Disable tools permanently | Tools remain callable after quarantine |
| ❌ Remove MCP servers automatically | Operator must manually remove malicious servers |
| ❌ Sandbox or execute MCP tools | Not an execution environment |
| ❌ Perform static code scanning | Does not analyze server source code |
| ❌ Act as a firewall | Not a network-level security control |
| ❌ Prevent all attack vectors | Defense-in-depth layer, not complete protection |

### 🎯 Positioning

> **MCP Context Protector is a runtime detection and containment layer — NOT a firewall, static code scanner, or execution sandbox.**

It complements other security controls and should be part of a defense-in-depth strategy.

---

## 📝 Summary

MCP Context Protector provides:

- 🔒 **Default-deny security** — New servers blocked until human approval
- 🔍 **Runtime protection** — Scans tool responses before they reach LLM
- 🔄 **Transparent proxy** — Sits between client and server invisibly
- 👤 **Operator-driven** — Security decisions require human review
- 🛡️ **Detection layer** — Complements but doesn't replace other controls

---

## 📚 Additional Resources

- [Installation Guide](#)
- [Configuration Reference](#)
- [Troubleshooting](#)
- [Security Best Practices](#)

---

**License**: [Your License Here]  
**Maintainer**: [Your Name/Team]  
**Version**: 1.0.0
