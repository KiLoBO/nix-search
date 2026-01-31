#!/usr/bin/env bash

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}Building NixOS dev environment...${NC}"
cd "$SCRIPT_DIR"
docker-compose build

echo -e "${BLUE}Starting container...${NC}"
docker-compose run --rm nix-dev
