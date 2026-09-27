#!/bin/bash
# Synthos-OS All-in-One Installation Script for Linux/Mac
# This script installs all prerequisites automatically

set -e

echo "========================================"
echo "  Synthos-OS All-in-One Installer"
echo "========================================"
echo ""
echo "This script will install:"
echo "  1. Git"
echo "  2. Docker"
echo "  3. Python 3.10"
echo "  4. Node.js (optional)"
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo "Detected OS: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
    echo "Detected OS: macOS"
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

echo ""

# Ask about Node.js
read -p "Install Node.js? (Y/n): " install_node
if [[ -z "$install_node" ]]; then
    install_node="y"
fi

echo ""
echo "Starting installation process..."
echo ""

# Install Git
echo "========================================"
echo "  Step 1: Installing Git"
echo "========================================"
if command -v git &> /dev/null; then
    echo "Git is already installed: $(git --version)"
    read -p "Reinstall? (y/N): " reinstall_git
    if [[ "$reinstall_git" != "y" && "$reinstall_git" != "Y" ]]; then
        echo "Skipping Git installation"
    else
        if [[ "$OS" == "linux" ]]; then
            sudo apt-get update
            sudo apt-get install -y git
        elif [[ "$OS" == "mac" ]]; then
            if command -v brew &> /dev/null; then
                brew install git
            else
                echo "Homebrew not found. Installing..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                brew install git
            fi
        fi
    fi
else
    if [[ "$OS" == "linux" ]]; then
        sudo apt-get update
        sudo apt-get install -y git
    elif [[ "$OS" == "mac" ]]; then
        if command -v brew &> /dev/null; then
            brew install git
        else
            echo "Homebrew not found. Installing..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            brew install git
        fi
    fi
fi
echo "Git version: $(git --version)"
echo ""

# Install Docker
echo "========================================"
echo "  Step 2: Installing Docker"
echo "========================================"
if command -v docker &> /dev/null; then
    echo "Docker is already installed: $(docker --version)"
    read -p "Reinstall? (y/N): " reinstall_docker
    if [[ "$reinstall_docker" != "y" && "$reinstall_docker" != "Y" ]]; then
        echo "Skipping Docker installation"
    else
        if [[ "$OS" == "linux" ]]; then
            curl -fsSL https://get.docker.com -o get-docker.sh
            sudo sh get-docker.sh
            sudo usermod -aG docker $USER
            rm get-docker.sh
        elif [[ "$OS" == "mac" ]]; then
            if command -v brew &> /dev/null; then
                brew install --cask docker
            else
                echo "Homebrew not found. Installing..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                brew install --cask docker
            fi
        fi
    fi
else
    if [[ "$OS" == "linux" ]]; then
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        rm get-docker.sh
    elif [[ "$OS" == "mac" ]]; then
        if command -v brew &> /dev/null; then
            brew install --cask docker
        else
            echo "Homebrew not found. Installing..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            brew install --cask docker
        fi
    fi
fi
echo "Docker version: $(docker --version)"
echo ""

# Install Python
echo "========================================"
echo "  Step 3: Installing Python 3.10"
echo "========================================"
if command -v python3 &> /dev/null; then
    echo "Python is already installed: $(python3 --version)"
    read -p "Reinstall? (y/N): " reinstall_python
    if [[ "$reinstall_python" != "y" && "$reinstall_python" != "Y" ]]; then
        echo "Skipping Python installation"
    else
        if [[ "$OS" == "linux" ]]; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
        elif [[ "$OS" == "mac" ]]; then
            if command -v brew &> /dev/null; then
                brew install python@3.10
            else
                echo "Homebrew not found. Installing..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                brew install python@3.10
            fi
        fi
    fi
else
    if [[ "$OS" == "linux" ]]; then
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv
    elif [[ "$OS" == "mac" ]]; then
        if command -v brew &> /dev/null; then
            brew install python@3.10
        else
            echo "Homebrew not found. Installing..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            brew install python@3.10
        fi
    fi
fi
echo "Python version: $(python3 --version)"
echo ""

# Install Node.js (optional)
if [[ "$install_node" == "y" || "$install_node" == "Y" ]]; then
    echo "========================================"
    echo "  Step 4: Installing Node.js"
    echo "========================================"
    if command -v node &> /dev/null; then
        echo "Node.js is already installed: $(node --version)"
        read -p "Reinstall? (y/N): " reinstall_node
        if [[ "$reinstall_node" != "y" && "$reinstall_node" != "Y" ]]; then
            echo "Skipping Node.js installation"
        else
            if [[ "$OS" == "linux" ]]; then
                curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
                sudo apt-get install -y nodejs
            elif [[ "$OS" == "mac" ]]; then
                if command -v brew &> /dev/null; then
                    brew install node
                else
                    echo "Homebrew not found. Installing..."
                    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                    brew install node
                fi
            fi
        fi
    else
        if [[ "$OS" == "linux" ]]; then
            curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
            sudo apt-get install -y nodejs
        elif [[ "$OS" == "mac" ]]; then
            if command -v brew &> /dev/null; then
                brew install node
            else
                echo "Homebrew not found. Installing..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                brew install node
            fi
        fi
    fi
    echo "Node.js version: $(node --version)"
    echo "Npm version: $(npm --version)"
    echo ""
fi

echo "========================================"
echo "  All Prerequisites Installed!"
echo "========================================"
echo ""
echo "IMPORTANT NEXT STEPS:"
echo "1. Start Docker Desktop (if on macOS)"
echo "2. Run: ./scripts/setup-env.sh"
echo "3. Run: ./scripts/deploy.sh dev"
echo ""
echo "NOTE: If you just installed Docker on Linux, you may need to log out and log back in for group changes to take effect."
echo ""