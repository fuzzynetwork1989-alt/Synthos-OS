#!/bin/bash
# Synthos-OS Environment Setup Script for Linux/Mac
# This script sets up the development environment

set -e

echo "========================================"
echo "  Synthos-OS Environment Setup"
echo "========================================"
echo ""

# Check prerequisites
echo "Checking prerequisites..."
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed. Run ./scripts/install-all.sh first."
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed. Run ./scripts/install-all.sh first."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python is not installed. Run ./scripts/install-all.sh first."
    exit 1
fi

echo "All prerequisites found!"
echo ""

# Create .env file
echo "Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from .env.example"
else
    echo ".env file already exists"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
python3 -m pip install --upgrade pip
pip3 install -e .
echo "Python dependencies installed successfully"
echo ""

# Install mobile client dependencies (if Node.js is available)
if command -v node &> /dev/null; then
    echo "Installing mobile client dependencies..."
    cd apps/mobile-client
    npm install
    cd ../..
    echo "Mobile client dependencies installed successfully"
else
    echo "Node.js not found, skipping mobile client setup"
    echo "Install Node.js to enable mobile client development"
fi
echo ""

# Create directories
echo "Creating directories..."
mkdir -p logs
mkdir -p data
mkdir -p data/postgres
mkdir -p data/redis
mkdir -p data/ollama
echo "Directories created"
echo ""

# Initialize Git repository
echo "Checking Git repository..."
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Synthos-OS setup"
    echo "Git repository initialized"
else
    echo "Git repository already exists"
fi
echo ""

echo "========================================"
echo "  Environment Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Start services: ./scripts/deploy.sh dev"
echo "2. Run migrations: ./scripts/deploy.sh migrate"
echo "3. Pull models: docker exec -it synthos-ollama bash"
echo "               ollama pull llama2 mistral neural-chat"
echo "               exit"
echo ""