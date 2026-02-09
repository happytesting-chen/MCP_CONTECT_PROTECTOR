"""Simple security guardrail provider that works without external APIs."""

import logging
import re
from typing import Any

from contextprotector.guardrail_types import GuardrailAlert, GuardrailProvider, ToolResponse
from contextprotector.mcp_config import MCPServerConfig

logger = logging.getLogger("simple_security_provider")


class SimpleSecurityProvider(GuardrailProvider):
    """Simple security guardrail provider that detects basic threats without external APIs.
    
    This provider uses pattern matching to detect common security issues:
    - Command injection attempts
    - Suspicious shell commands
    - Potential prompt injection
    - Base64 encoded content (often used in attacks)
    - ANSI escape sequences
    """

    def __init__(self) -> None:
        """Initialize the simple security provider."""
        logger.info("Initializing SimpleSecurityProvider")
        super().__init__()
        
        # Suspicious patterns to detect
        self.suspicious_patterns = [
            # Command injection patterns
            r'(?:^|\s)(?:curl|wget|nc|netcat|bash|sh|powershell|cmd)(?:\s|$)',
            r'(?:^|\s)(?:rm\s+-rf|sudo\s+rm|del\s+/[sf])',
            r'(?:^|\s)(?:chmod\s+\+x|chmod\s+777)',
            
            # Network/system access
            r'(?:^|\s)(?:ssh|scp|ftp|telnet)(?:\s|$)',
            r'(?:^|\s)(?:ping|nslookup|dig)(?:\s|$)',
            
            # Suspicious base64 (common in attacks)
            r'(?:echo|printf).*\|.*base64.*--decode',
            r'base64\s+--decode.*\|\s*(?:bash|sh)',
            
            # Prompt injection attempts
            r'(?:ignore|forget|disregard).*(?:previous|above|prior).*(?:instruction|prompt|rule)',
            r'(?:system|assistant|ai).*(?:prompt|instruction).*(?:override|bypass|ignore)',
            r'(?:jailbreak|prompt.?injection|adversarial.?prompt)',
            
            # ANSI escape sequences (potential terminal manipulation)
            r'\x1b\[[0-9;]*[a-zA-Z]',
            r'\\(?:033|x1b)\[[0-9;]*[a-zA-Z]',
            
            # Suspicious file operations
            r'(?:^|\s)(?:cat|head|tail|less|more)\s+/etc/(?:passwd|shadow|hosts)',
            r'(?:^|\s)(?:find|locate)\s+.*-exec',
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE | re.MULTILINE) 
                                 for pattern in self.suspicious_patterns]

    @property
    def name(self) -> str:
        """Get the provider name."""
        return "SimpleSecurityProvider"

    def _scan_content(self, content: str, context: str = "") -> GuardrailAlert | None:
        """Scan content for suspicious patterns.
        
        Args:
            content: The content to scan
            context: Context description for logging
            
        Returns:
            GuardrailAlert if suspicious content found, None otherwise
        """
        if not content:
            return None
            
        logger.info("Scanning %s content (%d chars)", context, len(content))
        
        # Check each pattern
        for i, pattern in enumerate(self.compiled_patterns):
            match = pattern.search(content)
            if match:
                matched_text = match.group(0)
                logger.warning("Suspicious pattern detected in %s: %s", context, matched_text)
                
                return GuardrailAlert(
                    explanation=f"Suspicious pattern detected: {matched_text.strip()}",
                    data={
                        "pattern_index": i,
                        "matched_text": matched_text,
                        "context": context,
                        "content_length": len(content),
                        "match_position": match.start(),
                    }
                )
        
        # Check for excessive base64 content (might be encoded payload)
        base64_matches = re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', content)
        if len(base64_matches) > 3 or any(len(match) > 100 for match in base64_matches):
            logger.warning("Excessive base64 content detected in %s", context)
            return GuardrailAlert(
                explanation="Excessive base64 encoded content detected (potential payload)",
                data={
                    "base64_matches": len(base64_matches),
                    "longest_match": max(len(match) for match in base64_matches) if base64_matches else 0,
                    "context": context,
                }
            )
        
        logger.info("No suspicious patterns found in %s", context)
        return None

    def check_server_config(self, config: MCPServerConfig) -> GuardrailAlert | None:
        """Check server configuration for security issues.
        
        Args:
            config: The server configuration to check
            
        Returns:
            GuardrailAlert if issues found, None otherwise
        """
        logger.info("Checking server config with %d tools", len(config.tools))
        
        # Check server instructions
        if config.instructions:
            alert = self._scan_content(config.instructions, "server instructions")
            if alert:
                return alert
        
        # Check tool descriptions and schemas
        for tool_name, tool_def in config.tools.items():
            # Check tool description
            if tool_def.description:
                alert = self._scan_content(tool_def.description, f"tool '{tool_name}' description")
                if alert:
                    return alert
            
            # Check parameter descriptions in schema
            if tool_def.input_schema and isinstance(tool_def.input_schema, dict):
                schema_str = str(tool_def.input_schema)
                alert = self._scan_content(schema_str, f"tool '{tool_name}' schema")
                if alert:
                    return alert
        
        return None

    def check_tool_response(self, tool_response: ToolResponse) -> GuardrailAlert | None:
        """Check tool response for security issues.
        
        Args:
            tool_response: The tool response to check
            
        Returns:
            GuardrailAlert if issues found, None otherwise
        """
        logger.info("Checking tool response from: %s", tool_response.tool_name)
        
        # Scan the tool output
        alert = self._scan_content(
            tool_response.tool_output, 
            f"tool '{tool_response.tool_name}' response"
        )
        
        if alert:
            # Add tool-specific context
            alert.data.update({
                "tool_name": tool_response.tool_name,
                "tool_input": tool_response.tool_input,
                "tool_output_length": len(tool_response.tool_output),
            })
        
        return alert



