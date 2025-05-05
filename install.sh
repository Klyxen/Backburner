#!/bin/bash

# install.sh for Backburner Port Scanner
# Automates cloning, dependency installation, and setup for Docker usage

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Repository details
REPO_URL="https://github.com/Klyxen/Backburner.git"
REPO_DIR="Backburner"
DOCKER_IMAGE="klyxenn/backburner:latest"

# Print messages
info() {
    echo -e "${CYAN}[INFO] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

# Check for required tools
check_requirements() {
    info "Checking for required tools..."
    command -v git >/dev/null 2>&1 || error "Git is required. Install it with your package manager (e.g., apt install git, brew install git)."
    command -v docker >/dev/null 2>&1 || error "Docker is required. Install it from https://www.docker.com/ and ensure it's running."
}

# Docker setup
setup_docker() {
    info "Setting up Docker environment..."

    # Pull Docker image
    info "Pulling Backburner Docker image ($DOCKER_IMAGE)..."
    docker pull "$DOCKER_IMAGE" || error "Failed to pull Docker image. Ensure the image exists on Docker Hub."

    success "Docker setup complete!"
}

# Print usage instructions
print_instructions() {
    echo
    echo -e "${CYAN}=== Backburner Setup Complete! ===${NC}"
    echo
    echo "You installed Backburner using Docker. Run it using these commands:"
    echo
    echo "Interactive mode (enter targets one by one):"
    echo -e "${GREEN}docker run -it $DOCKER_IMAGE${NC}"
    echo
    echo "Command-line mode (scan a single target):"
    echo -e "${GREEN}docker run -it $DOCKER_IMAGE scanme.nmap.org${NC}"
    echo
    echo "Save results to a CSV file (creates an 'output' directory locally):"
    echo -e "${GREEN}mkdir output${NC}"
    echo -e "${GREEN}docker run -it -v \$(pwd)/output:/app/output $DOCKER_IMAGE scanme.nmap.org --output /app/output/results.csv${NC}"
    echo
    echo "Test with scanme.nmap.org, and only scan systems you have permission to scan."
    echo "For more options (e.g., timeout, concurrency), see the repository: $REPO_URL"
}

# Main logic
main() {
    info "Welcome to Backburner Port Scanner setup!"
    check_requirements
    setup_docker
    print_instructions
}

main
