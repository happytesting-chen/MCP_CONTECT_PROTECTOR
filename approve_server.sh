#!/bin/bash

# Script to approve the SSE server automatically
cd /mnt/c/Users/Intern/Documents/mitigation/mcp-context-protector

echo "Approving SSE server at http://192.168.174.129:8000/sse..."

# Use expect to automate the approval process
expect << 'EOF'
spawn bash mcp-context-protector.sh --review-server --sse-url http://192.168.174.129:8000/sse
expect "Do you want to trust this server configuration? \[y/N\]:"
send "y\r"
expect eof
EOF

echo "Server approval completed!"



