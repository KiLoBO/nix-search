#!/usr/bin/env bash

echo -e "\033[0;32m✓ Development environment ready!\033[0m"
echo -e "\033[0;34mYou are now in the NixOS container at /workspace (project root)\033[0m"
echo -e "\033[0;34mRun your TUI with: uv run <your_script>\033[0m"
echo ""

exec bash
