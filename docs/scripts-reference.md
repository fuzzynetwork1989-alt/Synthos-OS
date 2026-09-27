# Synthos-OS Scripts Reference Guide
## Complete Guide to All Installation and Management Scripts

## Overview
This guide documents all scripts available in the `scripts/` directory for installing, managing, and verifying Synthos-OS across all platforms.

## Table of Contents
1. [Quick Reference](#quick-reference)
2. [Windows PowerShell Scripts](#windows-powershell-scripts)
3. [Linux/Mac Bash Scripts](#linuxmac-bash-scripts)
4. [Mobile Build Scripts](#mobile-build-scripts)
5. [Quest 3 Scripts](#quest-3-scripts)
6. [Utility Scripts](#utility-scripts)
7. [Script Execution Order](#script-execution-order)
8. [Troubleshooting](#troubleshooting)

---

## Quick Reference

### For First-Time Installation
**Windows:**
```powershell
# Option 1: Install everything automatically
.\scripts\install-all.ps1

# Option 2: Install individually
.\scripts\install-git.ps1
.\scripts\install-docker.ps1
.\scripts\install-python.ps1
.\scripts\install-nodejs.ps1
```

**Linux/Mac:**
```bash
# Install everything automatically
./scripts/install-all.sh
```

### For Setting Up Environment
**Windows:**
```powershell
.\scripts\setup-environment.ps1
```

**Linux/Mac:**
```bash
./scripts/setup-env.sh
```

### For Starting Services
**Windows:**
```batch
scripts\deploy.bat dev
```

**Linux/Mac:**
```bash
./scripts/deploy.sh dev
```

### For Building Mobile Apps
**Android:**
```bash
# Linux/Mac
./scripts/build-android.sh

# Windows
scripts\build-android.bat
```

**iOS:**
```bash
# Linux/Mac
./scripts/build-ios.sh

# Windows
scripts\build-ios.bat
```

### For Quest 3
```bash
# Setup developer mode
./scripts/setup-quest3-dev.sh

# Sideload APK
./scripts/sideload-quest3.sh  # Linux/Mac
scripts\sideload-quest3.bat # Windows
```

### For Verification
**Windows:**
```powershell
.\scripts\verify.ps1
```

**Linux/Mac:**
```bash
./scripts/verify.sh
```

### For Cleanup
**Windows:**
```powershell
.\scripts\cleanup.ps1
```

**Linux/Mac:**
```bash
./scripts/cleanup.sh
```

---

## Windows PowerShell Scripts

### install-all.ps1
**Purpose:** Install all prerequisites (Git, Docker, Python, Node.js) automatically

**When to Use:**
- First-time installation
- Complete system setup

**What It Does:**
1. Installs Git
2. Installs Docker Desktop
3. Installs Python 3.10
4. Installs Node.js (optional)

**How to Run:**
```powershell
.\scripts\install-all.ps1
```

**Prerequisites:**
- Windows 10/11
- Administrator privileges
- Internet connection

**Output:**
- All software installed
- Instructions for next steps

**Notes:**
- Requires computer restart after Docker installation
- Takes 10-20 minutes depending on internet speed

---

### install-git.ps1
**Purpose:** Install Git version control

**When to Use:**
- Git not installed
- Need to reinstall Git

**What It Does:**
- Downloads Git installer
- Installs Git silently
- Adds Git to system PATH

**How to Run:**
```powershell
.\scripts\install-git.ps1
```

**Notes:**
- Downloads Git 2.43.0
- Requires restart of terminal after installation

---

### install-docker.ps1
**Purpose:** Install Docker Desktop

**When to Use:**
- Docker not installed
- Need to reinstall Docker

**What It Does:**
- Downloads Docker Desktop installer
- Installs Docker Desktop silently

**How to Run:**
```powershell
.\scripts\install-docker.ps1
```

**Notes:**
- Requires computer restart
- After restart, start Docker Desktop from Start menu
- Wait for whale icon to appear steady before using

---

### install-python.ps1
**Purpose:** Install Python 3.10

**When to Use:**
- Python not installed
- Need to reinstall Python

**What It Does:**
- Downloads Python 3.10.13 installer
- Installs Python with PATH configuration
- Installs pip

**How to Run:**
```powershell
.\scripts\install-python.ps1
```

**Notes:**
- Installs Python 3.10.13 (latest 3.10 version)
- Adds Python to PATH automatically
- Requires terminal restart

---

### install-nodejs.ps1
**Purpose:** Install Node.js LTS

**When to Use:**
- Node.js not installed
- Need to build mobile apps

**What It Does:**
- Downloads Node.js 18.19.0 installer
- Installs Node.js and npm silently

**How to Run:**
```powershell
.\scripts\install-nodejs.ps1
```

**Notes:**
- Installs Node.js 18 LTS
- Required for mobile app development
- Optional for desktop/web only

---

### install-prerequisites.ps1
**Purpose:** Check if all prerequisites are installed

**When to Use:**
- Before running setup
- Troubleshooting installation issues

**What It Does:**
- Checks for Git
- Checks for Docker
- Checks for Python
- Checks for Node.js (optional)
- Reports missing software

**How to Run:**
```powershell
.\scripts\install-prerequisites.ps1
```

**Notes:**
- Does not install anything
- Only checks what's installed
- Use before running setup-environment.ps1

---

### setup-environment.ps1
**Purpose:** Set up Synthos-OS development environment

**When to Use:**
- After installing prerequisites
- After cloning repository

**What It Does:**
- Creates .env file from .env.example
- Installs Python dependencies
- Installs mobile client dependencies (if Node.js installed)
- Creates necessary directories
- Initializes Git repository

**How to Run:**
```powershell
.\scripts\setup-environment.ps1
```

**Prerequisites:**
- Git installed
- Docker installed
- Python installed
- Synthos-OS repository cloned

**Notes:**
- Must be run from Synthos-OS root directory
- Takes 2-5 minutes

---

### pull-ollama-models.ps1
**Purpose:** Download AI models for Ollama

**When to Use:**
- After starting services
- First-time setup
- When adding new models

**What It Does:**
- Checks Docker is running
- Checks Ollama container is running
- Downloads 5 AI models:
  - Llama2 (general purpose)
  - Mistral (high performance)
  - Neural Chat (conversational)
  - Code Llama (code generation)
  - Phi (lightweight)

**How to Run:**
```powershell
.\scripts\pull-ollama-models.ps1
```

**Prerequisites:**
- Docker Desktop running
- Synthos-OS services started
- Internet connection

**Notes:**
- Takes 10-30 minutes depending on internet speed
- Total download size: ~15-20GB
- One-time setup

---

### verify.ps1
**Purpose:** Verify all services are running correctly

**When to Use:**
- After installation
- Troubleshooting
- Before starting development

**What It Does:**
- Checks Docker installation
- Checks Docker Compose installation
- Checks Python installation
- Checks Git installation
- Checks Node.js installation (optional)
- Checks all Docker services
- Checks service health endpoints
- Checks Ollama models

**How to Run:**
```powershell
.\scripts\verify.ps1
```

**Output:**
- Pass/fail status for each check
- Troubleshooting tips if checks fail

**Notes:**
- Returns exit code 0 if all pass, 1 if any fail
- Use in CI/CD pipelines

---

### cleanup.ps1
**Purpose:** Clean up Docker resources and temporary files

**When to Use:**
- Freeing disk space
- Starting fresh
- Troubleshooting

**What It Does:**
- Stops all Synthos-OS services
- Removes dangling Docker images
- Removes unused containers
- Removes unused networks
- Cleans build cache
- Cleans log files
- Cleans cache files
- Optionally deletes data volumes

**How to Run:**
```powershell
.\scripts\cleanup.ps1
```

**Warnings:**
- Will stop all services
- Data volume deletion is optional but permanent
- Ask for confirmation before proceeding

**Notes:**
- Does not delete data unless explicitly chosen
- Safe to run regularly for maintenance

---

## Linux/Mac Bash Scripts

### install-all.sh
**Purpose:** Install all prerequisites automatically (Linux/Mac)

**When to Use:**
- First-time installation
- Complete system setup

**What It Does:**
1. Detects OS (Linux or macOS)
2. Installs Git
3. Installs Docker
4. Installs Python 3.10
5. Installs Node.js (optional)

**How to Run:**
```bash
./scripts/install-all.sh
```

**Prerequisites:**
- Linux or macOS
- sudo privileges (for system packages)
- Internet connection

**Notes:**
- Uses Homebrew on macOS
- Uses apt on Linux (Ubuntu/Debian)
- Takes 10-20 minutes

---

### setup-env.sh
**Purpose:** Set up Synthos-OS development environment (Linux/Mac)

**When to Use:**
- After installing prerequisites
- After cloning repository

**What It Does:**
- Checks prerequisites
- Creates .env file
- Installs Python dependencies
- Installs mobile client dependencies (if Node.js available)
- Creates directories
- Initializes Git repository

**How to Run:**
```bash
./scripts/setup-env.sh
```

**Prerequisites:**
- Git installed
- Docker installed
- Python installed
- Synthos-OS repository cloned

**Notes:**
- Must be run from Synthos-OS root directory
- Make script executable: `chmod +x scripts/setup-env.sh`

---

### verify.sh
**Purpose:** Verify all services are running correctly (Linux/Mac)

**When to Use:**
- After installation
- Troubleshooting
- Before starting development

**What It Does:**
- Checks Docker installation
- Checks Docker Compose installation
- Checks Python installation
- Checks Git installation
- Checks Node.js installation (optional)
- Checks all Docker services
- Checks service health endpoints
- Checks Ollama models

**How to Run:**
```bash
./scripts/verify.sh
```

**Output:**
- Pass/fail status for each check
- Troubleshooting tips if checks fail

**Notes:**
- Returns exit code 0 if all pass, 1 if any fail
- Make script executable: `chmod +x scripts/verify.sh`

---

### cleanup.sh
**Purpose:** Clean up Docker resources and temporary files (Linux/Mac)

**When to Use:**
- Freeing disk space
- Starting fresh
- Troubleshooting

**What It Does:**
- Stops all Synthos-OS services
- Removes dangling Docker images
- Removes unused containers
- Removes unused networks
- Cleans build cache
- Cleans log files
- Cleans cache files
- Optionally deletes data volumes

**How to Run:**
```bash
./scripts/cleanup.sh
```

**Warnings:**
- Will stop all services
- Data volume deletion is optional but permanent
- Ask for confirmation before proceeding

**Notes:**
- Does not delete data unless explicitly chosen
- Make script executable: `chmod +x scripts/cleanup.sh`

---

## Mobile Build Scripts

### build-android.sh (Linux/Mac)
**Purpose:** Build Android APK using EAS

**When to Use:**
- Building Android app for testing
- Building Android app for distribution

**What It Does:**
- Checks for Node.js
- Installs EAS CLI if needed
- Installs Expo CLI if needed
- Prompts for build profile
- Builds APK using EAS cloud build

**How to Run:**
```bash
cd apps/mobile-client
./scripts/build-android.sh
```

**Build Profiles:**
1. development - For testing
2. preview - For internal distribution
3. production - For Play Store
4. simulator - For testing on device

**Prerequisites:**
- Node.js installed
- Expo account configured
- EAS CLI installed (script will install if missing)

**Notes:**
- Must be run from apps/mobile-client directory
- Takes 10-30 minutes
- APK available from EAS dashboard

---

### build-android.bat (Windows)
**Purpose:** Build Android APK using EAS (Windows)

**When to Use:**
- Building Android app for testing
- Building Android app for distribution

**How to Run:**
```batch
cd apps\mobile-client
scripts\build-android.bat
```

**Notes:** Same as build-android.sh but for Windows

---

### build-ios.sh (Linux/Mac)
**Purpose:** Build iOS IPA using EAS

**When to Use:**
- Building iOS app for testing
- Building iOS app for App Store

**How to Run:**
```bash
cd apps/mobile-client
./scripts/build-ios.sh
```

**Build Profiles:**
1. development - For testing (7-day validity)
2. preview - For internal distribution (7-day validity)
3. production - For App Store (1-year validity)
4. simulator - For testing on device

**Prerequisites:**
- Node.js installed
- Expo account configured
- Apple Developer account (for production)
- EAS CLI installed (script will install if missing)

**Notes:**
- Must be run from apps/mobile-client directory
- Takes 15-45 minutes
- IPA available from EAS dashboard
- Development/preview builds expire after 7 days

---

### build-ios.bat (Windows)
**Purpose:** Build iOS IPA using EAS (Windows)

**When to Use:**
- Building iOS app for testing
- Building iOS app for App Store

**How to Run:**
```batch
cd apps\mobile-client
scripts\build-ios.bat
```

**Notes:** Same as build-ios.sh but for Windows

---

## Quest 3 Scripts

### setup-quest3-dev.sh
**Purpose:** Guide through enabling developer mode on Quest 3

**When to Use:**
- First-time Quest 3 setup
- Setting up for sideloading

**What It Does:**
- Displays step-by-step instructions
- Guides through Meta Quest app setup
- Guides through Quest 3 headset setup
- Guides through USB connection
- Verifies ADB connection

**How to Run:**
```bash
./scripts/setup-quest3-dev.sh
```

**Prerequisites:**
- Meta Quest app on phone
- Quest 3 headset
- USB-C cable
- ADB installed

**Notes:**
- Interactive guide
- Requires manual steps on phone and headset
- Verifies connection at the end

---

### sideload-quest3.sh (Linux/Mac)
**Purpose:** Sideload APK to Quest 3

**When to Use:**
- Installing Synthos-OS on Quest 3
- Updating Synthos-OS on Quest 3

**What It Does:**
- Checks for ADB
- Checks for APK file
- Checks device connection
- Installs APK to Quest 3

**How to Run:**
```bash
./scripts/sideload-quest3.sh
```

**Prerequisites:**
- ADB installed
- synthos-quest3.apk file in current directory
- Quest 3 connected via USB
- Developer mode enabled on Quest 3

**Notes:**
- APK must be named `synthos-quest3.apk`
- App appears in "Unknown Sources" on Quest 3
- Make script executable: `chmod +x scripts/sideload-quest3.sh`

---

### sideload-quest3.bat (Windows)
**Purpose:** Sideload APK to Quest 3 (Windows)

**When to Run:**
```batch
scripts\sideload-quest3.bat
```

**Notes:** Same as sideload-quest3.sh but for Windows

---

## Utility Scripts

### deploy.bat (Windows)
**Purpose:** Deploy Synthos-OS services (already exists)

**Commands:**
- `dev` - Start development environment
- `prod` - Start production environment
- `stop` - Stop all services
- `restart` - Restart all services
- `status` - Check service status
- `logs` - View service logs
- `migrate` - Run database migrations

**How to Run:**
```batch
scripts\deploy.bat [command]
```

---

### deploy.sh (Linux/Mac)
**Purpose:** Deploy Synthos-OS services (already exists)

**Commands:**
- `dev` - Start development environment
- `prod` - Start production environment
- `stop` - Stop all services
- `restart` - Restart all services
- `status` - Check service status
- `logs` - View service logs
- `migrate` - Run database migrations

**How to Run:**
```bash
./scripts/deploy.sh [command]
```

---

## Script Execution Order

### First-Time Installation (Windows)

1. **Install Prerequisites**
   ```powershell
   .\scripts\install-all.ps1
   ```

2. **Restart Computer** (after Docker installation)

3. **Start Docker Desktop** (from Start menu)

4. **Setup Environment**
   ```powershell
   .\scripts\setup-environment.ps1
   ```

5. **Start Services**
   ```powershell
   scripts\deploy.bat dev
   ```

6. **Run Migrations**
   ```powershell
   scripts\deploy.bat migrate
   ```

7. **Pull Models**
   ```powershell
   .\scripts\pull-ollama-models.ps1
   ```

8. **Verify Installation**
   ```powershell
   .\scripts\verify.ps1
   ```

### First-Time Installation (Linux/Mac)

1. **Install Prerequisites**
   ```bash
   ./scripts/install-all.sh
   ```

2. **Start Docker** (if needed)

3. **Setup Environment**
   ```bash
   ./scripts/setup-env.sh
   ```

4. **Start Services**
   ```bash
   ./scripts/deploy.sh dev
   ```

5. **Run Migrations**
   ```bash
   ./scripts/deploy.sh migrate
   ```

6. **Pull Models**
   ```bash
   docker exec -it synthos-ollama bash
   ollama pull llama2 mistral neural-chat
   exit
   ```

7. **Verify Installation**
   ```bash
   ./scripts/verify.sh
   ```

### Mobile App Build

1. **Install Node.js** (if not installed)

2. **Navigate to Mobile Client**
   ```bash
   cd apps/mobile-client
   ```

3. **Install Dependencies**
   ```bash
   npm install
   ```

4. **Build APK/IPA**
   ```bash
   # Android
   ./scripts/build-android.sh

   # iOS
   ./scripts/build-ios.sh
   ```

5. **Download from EAS Dashboard**

### Quest 3 Installation

1. **Setup Developer Mode**
   ```bash
   ./scripts/setup-quest3-dev.sh
   ```

2. **Download APK** (from GitHub releases)

3. **Sideload APK**
   ```bash
   ./scripts/sideload-quest3.sh
   ```

4. **Launch on Quest 3**
   - Library → Unknown Sources → Synthos-OS AI Assistant

---

## Troubleshooting

### Script Won't Run (Windows)

**Symptom:** "Execution Policy" error

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Or right-click script → Properties → Unblock

### Script Won't Run (Linux/Mac)

**Symptom:** "Permission denied"

**Solution:**
```bash
chmod +x scripts/script-name.sh
```

### Docker Not Found

**Symptom:** "docker: command not found"

**Solution:**
- Ensure Docker Desktop is installed
- Ensure Docker Desktop is running
- Restart terminal
- On Linux, may need to log out and back in

### Python Not Found

**Symptom:** "python: command not found"

**Solution:**
- Ensure Python is installed
- Check PATH includes Python
- Restart terminal
- On Windows, ensure "Add to PATH" was checked during installation

### Node.js Not Found

**Symptom:** "node: command not found"

**Solution:**
- Install Node.js using install-nodejs.ps1 or install-all.sh
- Restart terminal
- Check PATH includes Node.js

### Services Won't Start

**Symptom:** Services keep restarting or fail to start

**Solution:**
- Ensure Docker Desktop is running
- Check disk space
- Check port conflicts (8000-8006)
- Run cleanup script
- Try: `docker-compose down && docker-compose up -d`

### Models Won't Download

**Symptom:** "Failed to pull model"

**Solution:**
- Check internet connection
- Check Docker has enough disk space
- Check Ollama container is running
- Try pulling models manually
- Run cleanup script first

### Quest 3 Not Detected

**Symptom:** "No device found"

**Solution:**
- Ensure USB debugging is enabled
- Ensure Developer Mode is enabled
- Try different USB cable
- Restart Quest 3
- Restart ADB server: `adb kill-server && adb start-server`

---

## Script Best Practices

### Always Run as Administrator (Windows)
- Right-click PowerShell → "Run as Administrator"
- Or use elevated command prompt

### Always Make Scripts Executable (Linux/Mac)
```bash
chmod +x scripts/*.sh
```

### Check Script Location
- Windows scripts end in `.ps1` or `.bat`
- Linux/Mac scripts end in `.sh`
- Mobile build scripts must be run from `apps/mobile-client`

### Read Output Carefully
- Scripts provide important information
- Check for errors or warnings
- Follow "Next Steps" instructions

### Keep Scripts Updated
- Pull latest changes from repository
- Scripts may be updated with new features

### Use Verify Script
- Run verify script after installation
- Run verify script when troubleshooting
- Returns exit code for automation

---

## Script Maintenance

### Adding New Scripts
1. Create script in `scripts/` directory
2. Make executable (Linux/Mac): `chmod +x scripts/new-script.sh`
3. Update this documentation
4. Test on all platforms

### Updating Existing Scripts
1. Test changes locally
2. Update documentation
3. Commit changes
4. Pull request

### Script Dependencies
- Windows: PowerShell 5.1+
- Linux: Bash 4.0+
- macOS: Bash 3.2+
- All: Docker, Python 3.10+

---

## Support

If you encounter script issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review platform-specific installation guides
3. Check GitHub Issues for known problems
4. Ensure all prerequisites are installed
5. Run verify script to diagnose issues

---

## Quick Reference Card

### Windows
```powershell
# Install everything
.\scripts\install-all.ps1

# Setup environment
.\scripts\setup-environment.ps1

# Start services
scripts\deploy.bat dev

# Run migrations
scripts\deploy.bat migrate

# Pull models
.\scripts\pull-ollama-models.ps1

# Verify
.\scripts\verify.ps1

# Cleanup
.\scripts\cleanup.ps1
```

### Linux/Mac
```bash
# Install everything
./scripts/install-all.sh

# Setup environment
./scripts/setup-env.sh

# Start services
./scripts/deploy.sh dev

# Run migrations
./scripts/deploy.sh migrate

# Pull models
docker exec -it synthos-ollama bash
ollama pull llama2 mistral neural-chat
exit

# Verify
./scripts/verify.sh

# Cleanup
./scripts/cleanup.sh
```

### Mobile
```bash
# Build Android
cd apps/mobile-client
./scripts/build-android.sh

# Build iOS
./scripts/build-ios.sh
```

### Quest 3
```bash
# Setup developer mode
./scripts/setup-quest3-dev.sh

# Sideload APK
./scripts/sideload-quest3.sh
```

---

## Conclusion

This script suite provides automated installation and management for Synthos-OS across all platforms. Use the scripts in the recommended order for smooth installation, and refer to this guide for troubleshooting and best practices.

For more detailed information, see the platform-specific installation guides in `docs/installation/`.