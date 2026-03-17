#!/bin/bash

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "Error: backend directory not found"
    exit 1
fi

echo "Starting Yuanyuan Li - Personal Profile Assistant..."
echo "Make sure you have set your ANTHROPIC_API_KEY in .env"
echo ""

# Change to backend directory and start the server
cd backend && uv run uvicorn app:app --reload --port 8000