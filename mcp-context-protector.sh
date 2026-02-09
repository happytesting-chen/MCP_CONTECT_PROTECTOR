#!/bin/bash
cd "$(dirname "$0")"

# Load .env file if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

/home/fengmin/.local/bin/uv run mcp-context-protector "$@"
