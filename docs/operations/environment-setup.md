# Synthos-OS Environment Setup Guide

## Prerequisites Installation

### Windows Setup

#### 1. Install Git
1. Download Git from https://git-scm.com/download/win
2. Run the installer with default settings
3. Verify installation:
```powershell
git --version
```

#### 2. Install Docker Desktop
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
2. Run the installer
3. Start Docker Desktop after installation
4. Verify installation:
```powershell
docker --version
docker-compose --version
```

#### 3. Install Python
1. Download Python 3.10+ from https://www.python.org/downloads/
2. Run the installer (check "Add Python to PATH")
3. Verify installation:
```powershell
python --version
```

#### 4. Install Node.js (for mobile client)
1. Download Node.js from https://nodejs.org/
2. Run the installer
3. Verify installation:
```powershell
node --version
npm --version
```

### Linux/Mac Setup

#### 1. Install Git
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install git

# macOS
brew install git
```

#### 2. Install Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# macOS
brew install docker docker-compose
```

#### 3. Install Python
```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-pip python3-venv

# macOS
brew install python@3.10
```

#### 4. Install Node.js
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS
brew install node
```

## Automated Setup

### Windows PowerShell Setup

1. **Run prerequisite checker**
```powershell
.\scripts\install-prerequisites.ps1
```

2. **Set up development environment**
```powershell
.\scripts\setup-environment.ps1
```

3. **Start services**
```powershell
.\scripts\deploy.bat dev
```

4. **Pull Ollama models**
```powershell
.\scripts\pull-ollama-models.ps1
```

### Linux/Mac Setup

1. **Make scripts executable**
```bash
chmod +x scripts/*.sh
```

2. **Set up development environment**
```bash
./scripts/deploy.sh dev
```

3. **Run database migrations**
```bash
./scripts/deploy.sh migrate
```

4. **Pull Ollama models**
```bash
docker exec -it synthos-ollama bash
ollama pull llama2
ollama pull mistral
ollama pull neural-chat
exit
```

## Manual Setup

### 1. Clone Repository
```bash
git clone https://github.com/fuzzynetwork1989-alt/Synthos-OS.git
cd Synthos-OS
```

### 2. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Set database passwords, API keys, etc.
```

### 3. Install Python Dependencies
```bash
# Install project dependencies
pip install -e .

# Or use requirements.txt
pip install -r requirements.txt
```

### 4. Install Mobile Client Dependencies
```bash
cd apps/mobile-client
npm install
cd ../..
```

### 5. Start Services
```bash
# Start all services with Docker Compose
docker-compose up -d

# Or use deployment script
./scripts/deploy.sh dev  # Linux/Mac
scripts\deploy.bat dev   # Windows
```

### 6. Run Database Migrations
```bash
# Apply database schema
docker-compose exec postgres psql -U synthos -d synthos_os -f /docker-entrypoint-initdb.d/001_create_memory_tables.sql

# Or use deployment script
./scripts/deploy.sh migrate  # Linux/Mac
scripts\deploy.bat migrate   # Windows
```

### 7. Pull Ollama Models
```bash
# Enter Ollama container
docker exec -it synthos-ollama bash

# Pull models
ollama pull llama2
ollama pull mistral
ollama pull neural-chat
ollama pull codellama
ollama pull phi

# Exit container
exit
```

## Service Verification

### Check Service Status
```bash
# Using Docker Compose
docker-compose ps

# Using deployment script
./scripts/deploy.sh status  # Linux/Mac
scripts\deploy.bat status   # Windows
```

### Test Individual Services
```bash
# API Gateway
curl http://localhost:8000/health

# Model Gateway
curl http://localhost:8002/health

# Memory Engine
curl http://localhost:8003/health

# RSI Engine
curl http://localhost:8004/health

# Cognitive Engine
curl http://localhost:8005/health

# Tool Execution Engine
curl http://localhost:8006/health

# Ollama
curl http://localhost:11434/api/tags
```

## Troubleshooting

### Docker Issues

#### Docker not starting
```bash
# Check Docker status
docker info

# Restart Docker Desktop
# Windows: Restart Docker Desktop application
# Linux: sudo systemctl restart docker
```

#### Container won't start
```bash
# Check logs
docker-compose logs [service-name]

# Rebuild containers
docker-compose down
docker-compose up -d --build
```

### Database Issues

#### PostgreSQL connection refused
```bash
# Check PostgreSQL container
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres

# Check database connection
docker-compose exec postgres psql -U synthos -d synthos_os
```

#### Migration errors
```bash
# Check migration files
ls migrations/

# Apply migrations manually
docker-compose exec postgres psql -U synthos -d synthos_os -f /docker-entrypoint-initdb.d/001_create_memory_tables.sql
```

### Ollama Issues

#### Models not downloading
```bash
# Check Ollama container
docker-compose logs ollama

# Pull models manually
docker exec -it synthos-ollama ollama pull llama2

# Check available models
docker exec -it synthos-ollama ollama list
```

#### Ollama not responding
```bash
# Restart Ollama container
docker-compose restart ollama

# Check Ollama status
curl http://localhost:11434/api/tags
```

### Python Issues

#### Dependencies not installing
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies separately
pip install fastapi uvicorn pydantic sqlalchemy asyncpg redis httpx

# Use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -e .
```

#### Import errors
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Install project in development mode
pip install -e .

# Check for conflicting packages
pip list
```

### Port Conflicts

#### Services can't start due to port conflicts
```bash
# Check what's using ports
netstat -ano | findstr :8000  # Windows
lsof -i :8000                # Linux/Mac

# Change ports in .env file
# Or stop conflicting services
```

## Development Workflow

### Starting Development Environment
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Code Changes
```bash
# Services auto-reload with code changes in development mode
# Just edit files and the services will restart automatically

# Manual restart if needed
docker-compose restart [service-name]
```

### Testing
```bash
# Run Python tests
pytest tests/

# Run mobile client tests
cd apps/mobile-client
npm test
```

### Database Changes
```bash
# Create new migration
# Add SQL file to migrations/ directory

# Apply migration
docker-compose exec postgres psql -U synthos -d synthos_os -f /docker-entrypoint-initdb.d/[migration-file].sql
```

## Environment Variables

### Required Variables
```bash
# Database
POSTGRES_PASSWORD=your_secure_password

# API Keys (optional)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Service URLs
MODEL_GATEWAY_URL=http://localhost:8002
MEMORY_ENGINE_URL=http://localhost:8003
```

### Optional Variables
```bash
# Development
DEBUG=true
ENVIRONMENT=development

# Service Ports
API_GATEWAY_PORT=8000
MODEL_GATEWAY_PORT=8002
MEMORY_ENGINE_PORT=8003
RSI_ENGINE_PORT=8004
COGNITIVE_ENGINE_PORT=8005
TOOL_EXECUTION_ENGINE_PORT=8006
```

## Next Steps

After completing environment setup:

1. **Verify all services are running**
   ```bash
   ./scripts/deploy.sh status
   ```

2. **Test API endpoints**
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8002/models
   ```

3. **Access applications**
   - Operator Console: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

4. **Review documentation**
   - [Architecture Guide](../architecture/overview.md)
   - [Deployment Guide](deployment-guide.md)
   - [API Documentation](../api/)

## Support

For issues:
- Check [Troubleshooting](#troubleshooting) section
- Review [GitHub Issues](https://github.com/fuzzynetwork1989-alt/Synthos-OS/issues)
- Check service logs: `docker-compose logs [service-name]`