# Synthos-OS Desktop Installation Guide
## Complete Step-by-Step Instructions for Beginners

## Overview
This guide will walk you through installing Synthos-OS Desktop on your Windows computer. Synthos-OS Desktop is a native application that provides a full-featured AI operating system experience on your desktop.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Pre-Installation Setup](#pre-installation-setup)
3. [Installation Steps](#installation-steps)
4. [First Launch Configuration](#first-launch-configuration)
5. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10 or later (64-bit)
- **Processor**: Intel Core i5 or AMD Ryzen 5 (2016 or newer)
- **Memory**: 8GB RAM
- **Storage**: 20GB free disk space
- **Graphics**: Integrated graphics or better

### Recommended Requirements
- **Operating System**: Windows 11 (64-bit)
- **Processor**: Intel Core i7 or AMD Ryzen 7 (2020 or newer)
- **Memory**: 16GB RAM
- **Storage**: 50GB free disk space (SSD recommended)
- **Graphics**: Dedicated GPU with 4GB VRAM

---

## Pre-Installation Setup

### Step 1: Install Required Software

#### 1.1 Install Git
Git is required to download Synthos-OS and for version control.

1. Download Git from the official website:
   - Go to: https://git-scm.com/download/win
   - Click on "Windows" to download the installer
   - Choose the "Standalone" version (includes Git Bash)

2. Run the Git installer:
   - Double-click the downloaded `.exe` file
   - Click "Next" through the installation wizard
   - **Important**: Make sure to check "Add Git to PATH" during installation
   - Click "Install" and wait for installation to complete
   - Click "Finish"

3. Verify Git installation:
   - Open Command Prompt (search for "cmd" in Windows)
   - Type: `git --version`
   - You should see something like: `git version 2.40.0.windows.1`
   - If you see this, Git is installed correctly!

#### 1.2 Install Docker Desktop
Docker is required to run the Synthos-OS services.

1. Download Docker Desktop:
   - Go to: https://www.docker.com/products/docker-desktop
   - Click "Download for Windows"
   - Choose "Windows" version

2. Install Docker Desktop:
   - Double-click the downloaded `.exe` file
   - Click "Ok" if asked for permissions
   - Click "Install" and wait for installation
   - When asked, uncheck "Use WSL 2" if you're not sure (it's optional)
   - Click "Finish" and restart your computer when prompted

3. Start Docker Desktop:
   - After restart, find "Docker Desktop" in your Start menu
   - Click to open it
   - Wait for the Docker whale icon to appear in your system tray (bottom right)
   - The icon should be steady (not animating) when Docker is ready

4. Verify Docker installation:
   - Open Command Prompt
   - Type: `docker --version`
   - You should see something like: `Docker version 24.0.0`
   - Type: `docker-compose --version`
   - You should see the Docker Compose version

#### 1.3 Install Python
Python is required for running Synthos-OS services.

1. Download Python:
   - Go to: https://www.python.org/downloads/
   - Click "Download Python 3.10.x" (choose the latest 3.10 version)
   - Download the Windows installer (64-bit)

2. Install Python:
   - Double-click the downloaded `.exe` file
   - **CRITICAL**: Check the box that says "Add Python to PATH"
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

3. Verify Python installation:
   - Open Command Prompt
   - Type: `python --version`
   - You should see something like: `Python 3.10.11`
   - Type: `pip --version`
   - You should see the pip version

#### 1.4 Install Node.js (Optional)
Node.js is required if you want to use the mobile client development tools.

1. Download Node.js:
   - Go to: https://nodejs.org/
   - Download the "LTS" (Long Term Support) version

2. Install Node.js:
   - Double-click the downloaded `.msi` file
   - Click "Next" through the installation wizard
   - Click "Install" and wait for completion
   - Click "Finish"

3. Verify Node.js installation:
   - Open Command Prompt
   - Type: `node --version`
   - Type: `npm --version`

### Step 2: Download Synthos-OS

#### 2.1 Clone the Repository
1. Open Command Prompt
2. Navigate to where you want to install Synthos-OS (your Desktop is recommended):
   ```
   cd C:\Users\YourUsername\Desktop
   ```
3. Clone the repository:
   ```
   git clone https://github.com/fuzzynetwork1989-alt/Synthos-OS.git
   ```
4. Navigate into the Synthos-OS directory:
   ```
   cd Synthos-OS
   ```

#### 2.2 Alternative: Download ZIP File
If you don't want to use Git:

1. Go to: https://github.com/fuzzynetwork1989-alt/Synthos-OS
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to your Desktop
5. Rename the extracted folder to "Synthos-OS"

### Step 3: Run Pre-Installation Script

We've created an automated script to check if everything is ready.

1. Navigate to the Synthos-OS directory in Command Prompt
2. Run the prerequisite checker:
   ```
   scripts\install-prerequisites.ps1
   ```
3. The script will check:
   - Git installation
   - Docker installation
   - Python installation
   - Node.js installation (optional)
4. If any issues are found, the script will tell you what to fix

---

## Installation Steps

### Step 4: Set Up Environment

#### 4.1 Configure Environment Variables
1. In the Synthos-OS directory, you'll see a file called `.env.example`
2. Copy this file to create your own configuration:
   ```
   copy .env.example .env
   ```
3. Open the `.env` file with Notepad or any text editor
4. You'll see configuration options. For beginners, the defaults are fine
5. Save and close the file

#### 4.2 Run Environment Setup Script
1. Run the automated setup script:
   ```
   scripts\setup-environment.ps1
   ```
2. This script will:
   - Install Python dependencies
   - Install mobile client dependencies (if Node.js is installed)
   - Create necessary directories
   - Initialize Git repository

### Step 5: Start Synthos-OS Services

#### 5.1 Start All Services
1. Run the deployment script:
   ```
   scripts\deploy.bat dev
   ```
2. This will start all the backend services:
   - API Gateway
   - Model Gateway
   - Memory Engine
   - RSI Engine
   - Cognitive Engine
   - Tool Execution Engine
   - PostgreSQL database
   - Redis cache
   - Ollama AI model service

3. Wait for all services to start (this may take 2-5 minutes on first run)
4. You'll see "done" messages when each service is ready

#### 5.2 Verify Services Are Running
1. Run the status check:
   ```
   scripts\deploy.bat status
   ```
2. You should see all services listed as "Up"

### Step 6: Run Database Migrations

1. Run the migration script:
   ```
   scripts\deploy.bat migrate
   ```
2. This sets up the database tables needed for Synthos-OS
3. You should see "Migrations completed successfully!"

### Step 7: Download AI Models

#### 7.1 Pull Ollama Models
1. Run the model pull script:
   ```
   scripts\pull-ollama-models.ps1
   ```
2. This will download the AI models:
   - Llama2 (general purpose)
   - Mistral (high performance)
   - Neural Chat (conversational)
   - Code Llama (code generation)
   - Phi (lightweight model)

3. This may take 10-30 minutes depending on your internet speed
4. Each model is several GB in size

#### 7.2 Verify Models Are Downloaded
1. The script will list available models when complete
2. You should see all 5 models listed

---

## First Launch Configuration

### Step 8: Launch Desktop Application

#### 8.1 Build Desktop Application
1. Navigate to the desktop shell directory:
   ```
   cd apps\desktop-shell
   ```
2. Install dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm run tauri dev
   ```
4. The desktop application window will open

#### 8.2 Alternative: Use Web Interface
If the desktop app has issues, you can use the web interface:

1. Open your web browser
2. Go to: http://localhost:3000
3. This is the Operator Console web interface

### Step 9: Initial Setup Wizard

When you first launch Synthos-OS Desktop, you'll see a setup wizard:

#### 9.1 Welcome Screen
- Click "Get Started" to begin

#### 9.2 Model Selection
- Choose your default AI model:
  - **Llama2**: Good all-around choice
  - **Mistral**: Higher performance, requires more resources
  - **Neural Chat**: Best for conversations
  - **Phi**: Lightweight, good for older computers
- Click "Next"

#### 9.3 Memory Configuration
- Choose how much memory to allocate:
  - **Conservative**: 2GB (good for 8GB RAM systems)
  - **Balanced**: 4GB (recommended for 16GB RAM systems)
  - **Aggressive**: 8GB (for systems with 32GB+ RAM)
- Click "Next"

#### 9.4 Feature Selection
- Choose which features to enable:
  - ✅ Voice input (microphone access)
  - ✅ File access (for document analysis)
  - ✅ Web browsing (for research)
  - ✅ Code execution (for programming tasks)
- Click "Next"

#### 9.5 Privacy Settings
- Choose your privacy preferences:
  - **Local Only**: All data stays on your computer
  - **Cloud Backup**: Optional cloud sync (requires account)
- Click "Finish"

### Step 10: Verify Installation

#### 10.1 Test Basic Functionality
1. In the Synthos-OS interface, try a simple question:
   - Type: "Hello, can you introduce yourself?"
   - Press Enter or click Send
2. You should get a response from the AI

#### 10.2 Check System Status
1. Click on "Settings" (gear icon)
2. Click on "System Status"
3. You should see all services showing as "Connected"

---

## Post-Installation Configuration

### Step 11: Configure Desktop Shortcut

#### 11.1 Create Desktop Shortcut
1. Right-click on your Desktop
2. Select "New" → "Shortcut"
3. For location, type:
   ```
   cmd /c "cd C:\Users\YourUsername\Desktop\Synthos-OS && scripts\deploy.bat dev && timeout /t 5 && start http://localhost:3000"
   ```
4. Name it "Synthos-OS"
5. Click "Finish"

#### 11.2 Alternative: Create Batch File
1. Open Notepad
2. Paste this:
   ```batch
   @echo off
   cd C:\Users\YourUsername\Desktop\Synthos-OS
   scripts\deploy.bat dev
   timeout /t 5
   start http://localhost:3000
   ```
3. Save as "Synthos-OS.bat" on your Desktop
4. Double-click this file to start Synthos-OS

### Step 12: Configure Auto-Start (Optional)

#### 12.1 Add to Startup Folder
1. Press `Win + R` to open Run dialog
2. Type: `shell:startup`
3. Create a shortcut to your Synthos-OS batch file
4. Synthos-OS will now start automatically when you log in

---

## Troubleshooting

### Issue: Docker Desktop Won't Start

**Symptoms**: Docker whale icon keeps spinning, or you get "Docker daemon not running" error

**Solutions**:
1. Make sure Docker Desktop is running
2. Check Windows Subsystem for Linux (WSL) is enabled:
   - Open PowerShell as Administrator
   - Run: `wsl --install`
   - Restart your computer
3. Try restarting Docker Desktop:
   - Right-click Docker icon in system tray
   - Select "Restart"
4. Check if virtualization is enabled in BIOS:
   - Restart your computer
   - Enter BIOS (usually F2, F10, or Delete key)
   - Enable virtualization (VT-x or AMD-V)
   - Save and restart

### Issue: Python Installation Fails

**Symptoms**: "python is not recognized" error

**Solutions**:
1. Make sure you checked "Add Python to PATH" during installation
2. If you forgot, reinstall Python and check the box this time
3. Or manually add Python to PATH:
   - Search for "Environment Variables" in Windows
   - Add Python path to System PATH
   - Typical path: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python310`

### Issue: Services Won't Start

**Symptoms**: "docker-compose up" fails or services keep restarting

**Solutions**:
1. Check Docker is running: `docker ps`
2. Check port conflicts:
   - Another program might be using ports 8000-8006
   - Stop conflicting programs or change ports in `.env` file
3. Check logs: `docker-compose logs [service-name]`
4. Try restarting: `docker-compose down && docker-compose up -d`

### Issue: Models Won't Download

**Symptoms**: "Failed to pull model" error

**Solutions**:
1. Check internet connection
2. Check Docker has enough disk space
3. Try pulling models manually:
   ```
   docker exec -it synthos-ollama ollama pull llama2
   ```
4. Increase Docker disk allocation in Docker Desktop settings

### Issue: Desktop App Won't Open

**Symptoms**: Desktop app crashes or won't start

**Solutions**:
1. Use web interface instead: http://localhost:3000
2. Check Node.js is installed: `node --version`
3. Install desktop dependencies: `cd apps\desktop-shell && npm install`
4. Check system meets minimum requirements

### Issue: Slow Performance

**Symptoms**: Synthos-OS responds slowly

**Solutions**:
1. Check system resources:
   - Open Task Manager (Ctrl + Shift + Esc)
   - Check CPU and Memory usage
2. Use lighter model (Phi instead of Llama2)
3. Reduce memory allocation in settings
4. Close other applications
5. Make sure Docker has enough resources allocated

---

## Advanced Configuration

### Enable GPU Acceleration (If Available)

If you have an NVIDIA GPU, you can enable GPU acceleration for faster AI processing:

1. Install NVIDIA drivers:
   - Go to: https://www.nvidia.com/Download/index.aspx
   - Download and install drivers for your GPU

2. Enable GPU in Docker:
   - Open Docker Desktop
   - Go to Settings → General
   - Check "Use GPU for supported images"
   - Restart Docker

3. Update `.env` file:
   ```
   ENABLE_GPU=true
   ```

### Configure Custom Models

You can add custom models to Ollama:

1. Access Ollama container:
   ```
   docker exec -it synthos-ollama bash
   ```
2. Pull custom model:
   ```
   ollama pull [model-name]
   ```
3. Exit container:
   ```
   exit
   ```
4. Model will be available in Synthos-OS settings

---

## Next Steps

After successful installation:

1. **Explore the Interface**: Familiarize yourself with the Synthos-OS interface
2. **Read the User Guide**: Learn about advanced features
3. **Configure Settings**: Customize your experience
4. **Install Mobile App**: Get Synthos-OS on your phone
5. **Join the Community**: Get help and share experiences

---

## Support

If you encounter issues not covered here:

1. Check the [Troubleshooting Guide](../troubleshooting.md)
2. Search [GitHub Issues](https://github.com/fuzzynetwork1989-alt/Synthos-OS/issues)
3. Ask for help in the community forums
4. Check system requirements match your hardware

---

## Quick Reference

### Essential Commands
```batch
# Start Synthos-OS
scripts\deploy.bat dev

# Check status
scripts\deploy.bat status

# View logs
scripts\deploy.bat logs

# Stop Synthos-OS
scripts\deploy.bat stop

# Restart Synthos-OS
scripts\deploy.bat restart
```

### Important URLs
- **Web Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Model Gateway**: http://localhost:8002/docs
- **Health Check**: http://localhost:8000/health

### File Locations
- **Configuration**: `.env` file in Synthos-OS directory
- **Logs**: `logs/` directory
- **Data**: `data/` directory
- **Services**: `services/` directory

---

Congratulations! You now have Synthos-OS Desktop installed and running. Enjoy your AI-powered operating system experience!