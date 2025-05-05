#!/bin/bash

# install.sh for Backburner Port Scanner
# Automates cloning, dependency installation, and setup for Python or Docker

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
}

# Check if Docker is installed and running
check_docker() {
    if command -v docker >/dev/null 2>&1; then
        docker info >/dev/null 2>&1 && return 0
        error "Docker is installed but not running. Start Docker Desktop or the Docker daemon."
    fi
    return 1
}

# Install Python dependencies
install_python() {
    info "Setting up Python environment..."

    # Check for Python 3.7+
    if ! command -v python3 >/dev/null 2>&1 || ! python3 --version | grep -qE '3\.[7-9]|3\.[1-9][0-9]'; then
        error "Python 3.7 or higher is required. Install it from python.org or your package manager."
    fi

    # Check for pip
    if ! command -v pip3 >/dev/null 2>&1; then
        info "Installing pip..."
        python3 -m ensurepip --upgrade || error "Failed to install pip."
        python3 -m pip install --upgrade pip || error "Failed to upgrade pip."
    fi

    # Clone repository if not already cloned
    if [ ! -d "$REPO_DIR" ]; then
        info "Cloning Backburner repository..."
        git clone "$REPO_URL" "$REPO_DIR" || error "Failed to clone repository."
    fi
    cd "$REPO_DIR" || error "Failed to enter repository directory."

    # Install dependencies from requirements.txt
    if [ -f "requirements.txt" ]; then
        info "Installing dependencies from requirements.txt..."
        pip3 install -r requirements.txt || error "Failed to install dependencies."
    fi

    # Install Backburner as a package
    info "Installing Backburner package..."
    pip3 install . || error "Failed to install Backburner package."

    success "Python setup complete!"
}

# Install Docker setup
install_docker() {
    info "Setting up Docker environment..."

    # Check for Docker
    if ! check_docker; then
        error "Docker is not installed. Install it from docker.com and ensure it's running."
    fi

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
    if [ "$1" = "python" ]; then
        echo "You installed Backburner locally with Python. Run it using these commands:"
        echo
        echo "Interactive mode (enter targets one by one):"
        echo -e "${GREEN}backburner${NC}"
        echo
        echo "Command-line mode (scan a single target):"
        echo -e "${GREEN}backburner scanme.nmap.org${NC}"
        echo
        echo "Save results to a CSV file:"
        echo -e "${GREEN}backburner scanme.nmap.org --output results.csv${NC}"
        echo
        echo "Note: Results are saved in the $REPO_DIR directory."
    else
        echo "You installed Backburner with Docker. Run it using these commands:"
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
        echo "Note: CSV files are saved in the 'output' directory in your current working directory."
    fi
    echo
    echo "Test with scanme.nmap.org, and only scan systems you have permission to scan."
    echo "For more options (e.g., timeout, concurrency), see the README: $REPO_URL"
}

# Main logic
main() {
    info "Welcome to Backburner Port Scanner setup!"
    check_requirements

    echo "Choose your setup method:"
    echo "1) Python (local installation)"
    echo "2) Docker (containerized)"
    read -p "Enter 1 or 2: " choice

    case "$choice" in
        1)
            install_python
            print_instructions "python"
            ;;
        2)
            install_docker
            print_instructions "docker"
            ;;
        *)
            error "Invalid choice. Please run the script again and select 1 or 2."
            ;;
    esac
}

main
