#!/usr/bin/env python3
"""Simple script to remove a server from the MCP context protector database."""

import json
import sys
from pathlib import Path

def remove_server_from_config(server_url: str):
    """Remove a server from the MCP context protector configuration."""
    
    # Path to the servers database
    config_dir = Path.home() / ".mcp-context-protector"
    servers_file = config_dir / "servers.json"
    
    if not servers_file.exists():
        print(f"No servers database found at {servers_file}")
        return False
    
    # Load the current configuration
    try:
        with open(servers_file, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading servers file: {e}")
        return False
    
    # Find and remove the server
    servers = data.get("servers", {})
    removed = False
    
    # Look for the server by URL (it might be stored with different key formats)
    keys_to_remove = []
    for key, server_entry in servers.items():
        if server_url in key or server_url == server_entry.get("identifier"):
            keys_to_remove.append(key)
            print(f"Found server to remove: {key}")
    
    # Remove the servers
    for key in keys_to_remove:
        del servers[key]
        removed = True
        print(f"Removed server: {key}")
    
    if not removed:
        print(f"Server {server_url} not found in database")
        print("Available servers:")
        for key in servers.keys():
            print(f"  - {key}")
        return False
    
    # Save the updated configuration
    try:
        # Create backup first
        backup_file = servers_file.with_suffix('.json.backup')
        with open(backup_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Backup created: {backup_file}")
        
        # Save updated config
        with open(servers_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Updated servers database: {servers_file}")
        return True
        
    except Exception as e:
        print(f"Error saving updated configuration: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python remove_server.py <server_url>")
        print("Example: python remove_server.py http://192.168.174.129:8000/sse")
        sys.exit(1)
    
    server_url = sys.argv[1]
    success = remove_server_from_config(server_url)
    sys.exit(0 if success else 1)



