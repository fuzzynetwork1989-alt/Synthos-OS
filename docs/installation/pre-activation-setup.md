# Synthos-OS Pre-Activation Setup Guide
## Everything You Need to Do Before Getting Synthos-OS Running

## Overview
This guide covers ALL the preparation steps you need to complete BEFORE you can run Synthos-OS. Follow these steps in order to ensure a smooth first launch.

## Table of Contents
1. [Pre-Installation Checklist](#pre-installation-checklist)
2. [Software Installation](#software-installation)
3. [System Preparation](#system-preparation)
4. [Script Execution Guide](#script-execution-guide)
5. [Environment Configuration](#environment-configuration)
- [Service Startup Sequence](#service-startup-sequence)
- [Verification Steps](#verification-steps)
- [Common Pitfalls](#common-pitfalls)

---

## Pre-Installation Checklist

### Hardware Requirements Check

#### ✅ Computer Requirements
- [ ] Operating System: Windows 10/11, macOS 10.15+, or Linux
- [ ] Processor: Intel Core i5/AMD Ryzen 5 or better (2016+)
- [ ] Memory: 8GB RAM minimum (16GB recommended)
- [ ] Storage: 50GB free disk space (100GB recommended)
- [ ] Graphics: Integrated or dedicated GPU

#### ✅ Network Requirements
- [ ] Internet connection for initial setup
- [ ] Local network for optimal performance
- [ ] 5GHz Wi-Fi recommended (for mobile/Quest)
- [ ] 25 Mbps bandwidth for model downloads

#### ✅ Optional Hardware
- [ ] NVIDIA GPU (for GPU acceleration)
- [ ] Mobile device (for mobile app)
- [ ] Meta Quest 3 (for VR app)
- [ ] Microphone (for voice input)
- [ ] Webcam (for vision input)

---

## Software Installation

### Step 1: Install Git

#### Why It's Needed
Git is required to download Synthos-OS from GitHub and for version control.

#### Installation Instructions

**Windows:**
1. Download from: https://git-scm.com/download/win
2. Run the installer
3. **CRITICAL**: Check "Add Git to PATH"
4. Click through the installation wizard
5. Click "Finish"

**Verification:**
```bash
git --version
```
You should see something like: `git version 2.40.0.windows.1`

**If It Fails:**
- Reinstall and check "Add Git to PATH"
- Or add manually to system PATH

### Step 2: Install Docker Desktop

#### Why It's Needed
Docker is required to run the Synthos-OS backend services (database, cache, AI models, etc.).

#### Installation Instructions

**Windows:**
1. Download from: https://www.docker.com/products/docker-desktop
2. Run the installer
3. Click "OK" on permission prompts
4. Click "Install"
5. Restart your computer when prompted
6. After restart, open Docker Desktop
7. Wait for the whale icon to appear steady in system tray

**Verification:**
```bash
docker --version
docker-compose --version
```

**If It Fails:**
- Make sure virtualization is enabled in BIOS
- Restart Docker Desktop
- Check Windows Subsystem for Linux (WSL) is enabled

**macOS:**
```bash
brew install docker docker-compose
```

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### Step 3: Install Python

#### Why It's Needed
Python is required to run the Synthos-OS backend services.

#### Installation Instructions

**Windows:**
1. Download from: https://www.python.org/downloads/
2. Download Python 3.10.x (latest 3.10 version)
3. Run the installer
4. **CRITICAL**: Check "Add Python to PATH"
5. Click "Install Now"
6. Click "Close"

**Verification:**
```bash
python --version
pip --version
```

**If It Fails:**
- Reinstall and check "Add Python to PATH"
- Add Python to PATH manually

**macOS:**
```bash
brew install python@3.10
```

**Linux:**
```bash
sudo apt-get install python3 python3-pip
```

### Step 4: Install Node.js (Optional)

#### Why It's Needed
Node.js is required for:
- Mobile client development
- Web UI development
- Some tool execution features

#### Installation Instructions

**Windows:**
1. Download from: https://nodejs.org/
2. Download LTS version
3. Run the installer
4. Click through the wizard
5. Click "Install"

**Verification:**
```bash
node --version
npm --version
```

**If It Fails:**
- Try reinstalling with admin privileges
- Check for conflicting installations

**macOS:**
```bash
brew install node
```

**Linux:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

## System Preparation

### Step 5: Clone Synthos-OS Repository

#### Why It's Needed
Download the SynththOS source code to your computer.

#### Instructions

**Option 1: Using Git (Recommended)**
```bash
# Navigate to where you want to install (Desktop is recommended)
cd C:\Users\YourUsername\Desktop

# Clone the repository
git clone https://github.com/fuzzynetwork1989-alt/Synthos-OS.git

# Navigate into the directory
cd Synthos-OS
```

**Option 2: Download ZIP File**
1. Go to: https://github.com/fuzzynetwork1989-alt/Synthos-OS
2. Click green "Code" button
3. Click "Download ZIP"
4. Extract to Desktop
5. Rename extracted folder to "Synthos-OS"

**Verification:**
```bash
ls
# You should see the Synthos-OS directory
```

### Step 6: Navigate to Synthos-OS Directory

#### Instructions
```bash
cd Synthos-OS
```

**Verification:**
```bash
# You should see folders like:
# apps/, services/, docs/, scripts/, etc.
ls
```

### Step 7: Check Directory Structure

#### Required Directories
Make sure these directories exist:
- `apps/` - Application interfaces
- `services/` - Backend services
- `scripts/` - Installation and deployment scripts
- `docs/` - Documentation
- `migrations/` - Database migrations

**Verification:**
```bash
ls apps
ls services
ls scripts
```

---

## Script Execution Guide

### Step 8: Run Prerequisite Checker (Windows)

#### Script Location
`scripts\install-prerequisites.ps1`

#### When to Run
Run this BEFORE any other setup to verify your system is ready.

#### How to Run

**Method 1: PowerShell (Recommended)**
```powershell
# Open PowerShell as Administrator
# Navigate to Synthos-OS directory
cd C:\Users\YourUsername\Desktop\Synthos-OS

# Run the script
.\scripts\install-prerequisites.ps1
```

**Method 2: Right-Click and Run**
1. Right-click on `install-prerequisites.ps1`
2. Select "Run with PowerShell"
3. If prompted about execution policy, choose "Run once"

#### What It Does
- Checks if Git is installed
- Checks if Docker is installed
- Checks if Python is installed
- Checks if Node.js is installed
- Reports any missing software

#### Expected Output
```
========================================
  Synthos-OS Prerequisites Installer
========================================

Checking Git installation...
Git is installed: git version 2.40.0.windows.1

Checking Docker installation...
Docker is installed: Docker version 24.0.0

Checking Python installation...
Python is installed: Python 3.10.11

All prerequisites found!
```

#### If It Fails
- Install any missing software following the instructions in [Software Installation](#software-installation)
- Run the script again to verify

### Step 9: Run Environment Setup Script (Windows)

#### Script Location
`scripts\setup-environment.ps1`

#### When to Run
Run this AFTER the prerequisite checker passes.

#### How to Run
```powershell
# Navigate to Synthos-OS directory
cd C:\Users\YourUsername\Desktop\Synthos-OS

# Run the script
.\scripts\setup-environment.ps1
```

#### What It Does
- Installs Python dependencies
- Installs mobile client dependencies (if Node.js is installed)
- Creates necessary directories (logs, data, etc.)
- Initializes Git repository
- Creates .env configuration file

#### Expected Output
```
========================================
  Synthos-OS Environment Setup
========================================

Checking prerequisites...
All prerequisites found!

Setting up environment variables...
Created .env file from .env.example

Installing Python dependencies...
Python dependencies installed successfully

Installing mobile client dependencies...
Mobile client dependencies installed successfully

Creating directories...
Created directory: logs
Created directory: data
Created directory: data\postgres
Created directory: data\redis
Created directory: data\ollama

Checking Git repository...
Git repository initialized

Next steps:
1. Start services: .\scripts\deploy.bat dev
2. Run migrations: .\scripts\deploy.bat migrate
3. Pull models: .\scripts\pull-ollama-models.ps1
```

#### If It Fails
- Check you have admin privileges
- Verify prerequisite checker passed
- Check your internet connection for package downloads

### Step 10: Run Deployment Script (Windows)

#### Script Location
`scripts\deploy.bat`

#### When to Run
Run this AFTER environment setup is complete.

#### How to Run
```batch
# Navigate to Synthos-OS directory
cd C:\Users\YourUsername\Desktop\Synthos-OS

# Start development environment
scripts\deploy.bat dev
```

#### What It Does
- Starts Docker containers for all services
- Pulls Docker images if needed
- Configures networking between services
- Starts all backend services

#### Expected Output
```
Creating network "synthos-os_default"
Creating volume "synthos-os_postgres_data"
Creating volume "synthos-os_redis_data"
Creating volume "synthos-os_ollama_data"
Creating synthos-postgres ... done
Creating synthos-redis ... done
Creating synthos-ollama ... done
Creating synthos-api-gateway ... done
Creating synthos-model-gateway ... done
Creating synthos-memory-engine ... done
Creating synthos-rsi-engine ... done
Creating synthos-cognitive-engine ... done
Creating synthos-tool-execution-engine ... done
```

#### Expected Time
- **First run**: 5-10 minutes (pulling Docker images)
- **Subsequent runs**: 1-2 minutes

#### If It Fails
- Check Docker Desktop is running
- Check your internet connection
- Check available disk space
- Check port conflicts (8000-8006)

### Step 11: Run Migration Script (Windows)

#### Script Location
`scripts\deploy.bat migrate`

#### When to Run
Run this AFTER services are started.

#### How to Run
```batch
# Navigate to SynthosOS directory
cd C:\Users\YourUsername\Desktop\Synthos-OS

# Run migrations
scripts\deploy.bat migrate
```

#### What It Does
- Applies database schema changes
- Creates necessary database tables
- Sets up indexes for performance

#### Expected Output
```
Running database migrations...
CREATE TABLE IF NOT EXISTS memory_entries ...
CREATE INDEX idx_memory_entries_content ...
Running migrations completed successfully!
```

#### If It Fails
- Check PostgreSQL container is running
- Check database connection in .env file
- Manually run SQL scripts if needed

### Step 12: Pull Ollama Models (Windows)

#### Script Location
`scripts\pull-ollama-models.ps1`

#### When to Run
Run this AFTER migrations are complete.

#### How to Run
```powershell
# Navigate to Synthos-OS directory
cd C:\Users\YourUsername\Desktop\Synthos-OS

# Pull models
.\scripts\pull-ollama-models.ps1
```

#### What It Does
- Connects to Ollama container
- Downloads AI models:
  - Llama2 (general purpose)
  - Mistral (high performance)
  - Neural Chat (conversational)
  - Code Llama (code generation)
  - Phi (lightweight)
- Lists available models

#### Expected Output
```
========================================
  Ollama Model Pull Script
========================================

Checking Docker status...
Docker is running
Checking Ollama container...
Ollama container is running

Pulling Ollama models...
Pulling llama2...
Successfully pulled llama2
Pulling mistral...
Successfully pulled mistral
Pulling neural-chat...
Successfully pulled neural-chat
Pulling codellama...
Successfully pulled codellama
Pulling phi...
Successfully pulled phi

Available models in Ollama:
NAME              ID              SIZE      MODIFIED
llama2:latest      a3f041611...  3.8 GB    2 days ago
...
```

#### Expected Time
- **On fast connection**: 10-20 minutes
- **On slow connection**: 30-60 minutes
- **Total size**: ~15-20GB

#### If It Fails
- Check your internet connection
- Check Docker has enough disk space
- Check Ollama container is running
- Try pulling models manually

---

## Linux/Mac Script Execution

### Equivalent Commands

#### Prerequisites Check
```bash
# Linux/Mac don't have a prerequisite checker script
# Check manually:
git --version
docker --version
python --version
node --version  # optional
```

#### Environment Setup
```bash
# Linux/Mac don't have an automated setup script
# Follow manual setup in README
cd Synthos-OS
cp .env.example .env
pip install -e .
cd apps/mobile-client && npm install && cd ../..
```

#### Deployment
```bash
# Start services
./scripts/deploy.sh dev

# Run migrations
./scripts/deploy.sh migrate
```

#### Pull Models
```bash
# Pull models manually
docker exec -it synthos-ollama bash
ollama pull llama2 mistral neural-chat codellama phi
exit
```

---

## Environment Configuration

### Step 13: Configure Environment Variables

#### Why It's Needed
Environment variables configure how Synthos-OS connects to your system.

#### Instructions

**Windows:**
1. Navigate to Synthos-OS directory
2. You should see a `.env.example` file
3. Copy it to create your own configuration:
   ```batch
   copy .env.example .env
   ```
4. Open `.env` with Notepad or text editor
5. Review and modify settings if needed

**Key Settings to Review:**
```bash
# Database password
POSTGRES_PASSWORD=your_secure_password

# Service URLs (usually fine as defaults)
API_GATEWAY_URL=http://localhost:8000
MODEL_GATEWAY_URL=http://localhost:8002
MEMORY_ENGINE_URL=http://localhost:8003
```

**Verification:**
```bash
# Check .env file exists
ls .env
```

### Step 14: Configure Firewall (Windows)

#### Why It's Needed
Firewall may block connections between services.

#### Instructions

**Windows Firewall:**
1. Open Windows Security
2. Go to "Firewall & network protection"
3. Click "Allow an app through firewall"
4. Click "Change settings"
5. Add allowed apps:
   - Docker Desktop
   - Python
   - Git (if needed)
6. Allow both private and public networks

**Antivirus Software:**
- Add SynthosOS directories to exclusions
- Add Docker to exclusions
- Add Python to exclusions

---

## Service Startup Sequence

### Step 15: Start Services in Correct Order

#### Correct Startup Order
Follow this sequence for smooth startup:

1. **Start Docker Desktop** (if not running)
2. **Run deployment script** - `scripts\deploy.bat dev`
3. **Wait for services to stabilize** (2-5 minutes)
4. **Run migrations** - `scripts\deploy.bat migrate`
5. **Pull models** - `scripts\pull-ollama-models.ps1`
6. **Start Web UI** (optional) - `cd apps/operator-console && npm run dev`
7. **Start Desktop App** (optional) - `cd apps/desktop-shell && npm run tauri dev`

#### Verify Each Step
After each step, verify before proceeding:

**After Docker:**
```bash
docker ps
# Should show docker desktop running
```

**After Deploy:**
```bash
docker-compose ps
# Should show all services as "Up"
```

**After Migrations:**
```bash
# Should see "Migrations completed successfully"
```

**After Models:**
```bash
# Should see all 5 models listed
```

---

## Verification Steps

### Step 16: Verify Backend Services

#### Check Service Status
```bash
scripts\deploy.bat status
```

**Expected Output:**
```
NAME                      STATUS
synthos-postgres         Up
synthos-redis           Up
synthos-ollama           Up
synthos-api-gateway      Up
synthos-model-gateway    Up
synthos-memory-engine    Up
synthos-rsi-engine       Up
synthos-cognitive-engine  Up
synthos-tool-execution-engine Up
```

#### Test API Endpoints
```bash
# Test API Gateway
curl http://localhost:8000/health

# Test Model Gateway
curl http://localhost:8002/health

# Test Memory Engine
curl http://localhost:8003/health

# Test RSI Engine
curl http://localhost:8004/health
```

**Expected Response:**
```json
{
  "status": "healthy"
}
```

### Step 17: Verify Ollama Models

#### Check Available Models
```bash
docker exec synthos-ollama ollama list
```

**Expected Output:**
```
NAME              ID              SIZE      MODIFIED
llama2:latest      a3f041611...  3.8 GB    2 days ago
mistral:latest     123456789...  4.1 GB    2 days ago
neural-chat:latest  987654321...  3.5 GB    2 days ago
codellama:latest   555566677...  4.2 GB    2 days ago
phi:latest         111122233...  2.1 GB    2 days ago
```

#### Test Model Gateway
```bash
curl http://localhost:8002/models
```

**Expected Response:**
```json
{
  "models": [
    {
      "name": "llama2:latest",
      "provider": "ollama",
      "capabilities": ["chat", "completion"],
      "context_length": 4096,
      "parameters": "unknown"
    }
  ]
}
```

### Step 18: Verify Database

#### Check PostgreSQL Connection
```bash
docker exec synthos-postgres psql -U synthos -d synthos_os -c "SELECT version();"
```

**Expected Output:**
```
 version
----------
  15.3
```

#### Check Tables Exist
```bash
docker exec synthos-postgres psql -U synthos -d synthos_os -c "\dt"
```

**Expected Output:**
```
                 List of relations
 Schema |        Name         | Type  |  Owner
--------+---------------------+-------+--------
 public | memory_entries     | table | synthos
 public | memory_stats       | table | synthos
```

---

## Common Pitfalls

### Pitfall 1: Skipping Prerequisite Check

**Problem:** You skip the prerequisite checker and run into issues later.

**Solution:** Always run `scripts\install-prerequisites.ps1` first.

### Pitfall 2: Docker Not Running

**Problem:** Docker Desktop is not running when you try to start services.

**Solution:** Always start Docker Desktop before running deployment script.

**Check:**
```bash
docker ps
# If error, start Docker Desktop
```

### Pitfall 3: Wrong Directory

**Problem:** Running scripts from wrong directory.

**Solution:** Always navigate to Synthos-OS root directory first.

**Check:**
```bash
cd C:\Users\YourUsername\Desktop\Synthos-OS
pwd  # Should show Synthos-OS path
```

### Pitfall: Port Conflicts

**Problem**: Ports 8000-8006 are already in use.

**Solution:**
1. Check what's using the ports:
   ```bash
   netstat -ano | findstr :8000
   ```
2. Stop conflicting services
3. Or change ports in `.env` file

### Pitfall: Insufficient Disk Space

**Problem:** Not enough disk space for Docker images and models.

**Solution:**
1. Check disk space: `wmic logicaldisk get size`
2. Free up at least 50GB space
3. Clear Docker images if needed:
   ```bash
   docker system prune -a
   ```

### Pitfall: Network Issues

**Problem:** Services can't connect to each other.

**Solution:**
1. Check Windows Firewall settings
2. Check Docker network settings
3. Restart Docker Desktop
4. Check if VPN is interfering

### Pitfall: Running Scripts as Wrong User

**Problem:** Permission errors when running scripts.

**Solution:**
1. Run PowerShell as Administrator
2. Or use "Run as Administrator" on right-click

### Pitfall: .env File Issues

**Problem:** Configuration not being read.

**Solution:**
1. Verify `.env` file exists
2. Check file is not corrupted
3. Try recreating from `.env.example`

---

## Pre-Activation Checklist

### Final Verification

Before attempting to use Synthos-OS, verify:

#### ✅ Software Installed
- [ ] Git installed and working
- [ ] Docker Desktop installed and running
- [ ] Python 3.10+ installed
- [ ] Node.js installed (if using mobile client)

#### ✅ Repository Downloaded
- [ ] Synthos-OS cloned or downloaded
- [ ] Navigated to Synthos-OS directory
- [ ] Directory structure verified

#### ✅ Scripts Executed
- [ ] Prerequisite checker passed
- [ ] Environment setup completed
- [ ] Deployment script executed
- [ ] Migrations applied
- [ ] Models downloaded

#### ✅ Services Running
- [ ] All Docker containers are "Up"
- [ ] API Gateway responding
- [ ] Model Gateway responding
- [ ] Memory Engine responding
- [ ] RSI Engine responding
- [ ] Ollama models downloaded

#### ✅ Configuration
- [ ] .env file configured
- [ ] Firewall configured
- [ ] Antivirus exclusions added
- [ ] Network connectivity verified

#### ✅ Verification Tests
- [ ] Health endpoints responding
- [ ] Database tables created
- [ ] Models accessible
- [ ] Service-to-service communication working

---

## Quick Reference

### Windows Script Execution Order
```batch
# 1. Prerequisites (first time only)
.\scripts\install-prerequisites.ps1

# 2. Environment setup (first time only)
.\scripts\setup-environment.ps1

# 3. Start services (every time)
.\scripts\deploy.bat dev

# 4. Run migrations (first time or after schema changes)
.\scripts\deploy.bat migrate

# 5. Pull models (first time only)
.\scripts\pull-ollama-models.ps1
```

### Linux/Mac Script Execution Order
```bash
# 1. Check prerequisites
git --version
docker --version
python --version

# 2. Environment setup
cp .env.example .env
pip install -e .
cd apps/mobile-client && npm install && cd ../..

# 3. Start services
./scripts/deploy.sh dev

# 4. Run migrations
./scripts/deploy.sh migrate

# 5. Pull models
docker exec -it synthos-ollama bash
ollama pull llama2 mistral neural-chat codellama phi
exit
```

### Essential Commands
```bash
# Check Docker status
docker ps

# Check service logs
docker-compose logs [service-name]

# Restart specific service
docker-compose restart [service-name]

# Stop all services
docker-compose down

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Important URLs
- **Web UI**: http://localhost:3000
- **API Gateway**: http://localhost:8000
- **Model Gateway**: http://localhost:8002
- **Memory Engine**: http://localhost:8003
- **RSI Engine**: http://localhost:8004
- **Cognitive Engine**: http://localhost:8005
- **Tool Execution Engine**: http://localhost:8006

---

## Troubleshooting Pre-Activation Issues

### Issue: Script Won't Run

**Symptoms:** "Execution Policy" error or script won't execute

**Solutions:**
1. Run PowerShell as Administrator
2. Change execution policy:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Right-click script → Properties → Unblock

### Issue: Docker Commands Fail

**Symptoms:** "docker" command not recognized

**Solutions:**
1. Restart Docker Desktop
2. Restart your computer
3. Reinstall Docker Desktop
4. Add Docker to PATH manually

### Issue: Python Commands Fail

**Symptoms:** "python" command not recognized

**Solutions:**
1. Check Python was added to PATH during installation
2. Restart Command Prompt/PowerShell
3. Add Python to PATH manually
4. Reinstall Python with "Add to PATH" checked

### Issue: Services Won't Start

**Symptoms:** Services keep restarting or fail to start

**Solutions:**
1. Check Docker Desktop is running
2. Check disk space
3. Check port conflicts
4. Check Docker logs:
   ```bash
   docker-compose logs [service-name]
   ```
5. Try restarting:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

---

## Next Steps After Pre-Activation

Once all pre-activation steps are complete:

1. **Launch Web UI**: Open http://localhost:3000
2. **Test Basic Functionality**: Try a simple AI query
3. **Configure Settings**: Customize your experience
4. **Install Mobile App**: Get Synthos-OS on your phone
5. **Install Quest 3 App**: Install on your Meta Quest 3
6. **Explore Features**: Try advanced features like RSI and tools

---

## Support

If you encounter issues during pre-activation:

1. Check the [Common Pitfalls](#common-pitfalls) section
2. Review the troubleshooting section in platform-specific guides
3. Check GitHub Issues for known problems
4. Verify all checklist items are complete
5. Try the "Common Pitfalls" solutions

---

## Emergency Recovery

### Reset Everything

If everything is broken and you want to start fresh:

```bash
# Stop all services
docker-compose down

# Remove all volumes (WARNING: deletes all data)
docker-compose down -v

# Remove all images
docker system prune -a

# Reinstall from scratch
# Follow this guide from the beginning
```

---

Congratulations! You have completed all pre-activation steps. Synthos-OS is now ready to run. Follow the platform-specific installation guides to install the user interfaces and start using Synthos-OS!