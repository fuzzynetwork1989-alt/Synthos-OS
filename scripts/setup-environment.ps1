# Synthos-OS Environment Setup Script for Windows
# This script sets up the development environment for Synthos-OS

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Synthos-OS Environment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set error action preference
$ErrorActionPreference = "Stop"

# Function to check if a command exists
function Test-Command {
    param([string]$Command)
    try {
        $null = Get-Command $Command -ErrorAction Stop
        return $true
    }
    catch {
        return $false
    }
}

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
$requiredCommands = @("git", "docker", "docker-compose", "python")
$missingCommands = @()

foreach ($cmd in $requiredCommands) {
    if (-not (Test-Command $cmd)) {
        $missingCommands += $cmd
    }
}

if ($missingCommands.Count -gt 0) {
    Write-Host "Missing prerequisites: $($missingCommands -join ', ')" -ForegroundColor Red
    Write-Host "Please run .\scripts\install-prerequisites.ps1 first" -ForegroundColor Yellow
    exit 1
}

Write-Host "All prerequisites found!" -ForegroundColor Green
Write-Host ""

# Create .env file if it doesn't exist
Write-Host "Setting up environment variables..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env file from .env.example" -ForegroundColor Green
} else {
    Write-Host ".env file already exists" -ForegroundColor Green
}

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip
    pip install -e .
    Write-Host "Python dependencies installed successfully" -ForegroundColor Green
}
catch {
    Write-Host "Failed to install Python dependencies: $_" -ForegroundColor Red
    exit 1
}

# Install Node.js dependencies for mobile client
Write-Host "Installing mobile client dependencies..." -ForegroundColor Yellow
if (Test-Command "npm") {
    try {
        Set-Location "apps\mobile-client"
        npm install
        Set-Location "..\.."
        Write-Host "Mobile client dependencies installed successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "Failed to install mobile client dependencies: $_" -ForegroundColor Red
        Write-Host "Continuing without mobile client setup..." -ForegroundColor Yellow
    }
} else {
    Write-Host "npm not found, skipping mobile client setup" -ForegroundColor Yellow
}

# Create logs directory
Write-Host "Creating directories..." -ForegroundColor Yellow
$directories = @("logs", "data", "data\postgres", "data\redis", "data\ollama")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created directory: $dir" -ForegroundColor Green
    }
}

# Initialize Git if not already initialized
Write-Host "Checking Git repository..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit - Synthos-OS setup"
    Write-Host "Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "Git repository already exists" -ForegroundColor Green
}

# Pull Ollama models after Docker starts
Write-Host "Note: Ollama models will be pulled after starting Docker services" -ForegroundColor Yellow
Write-Host "Run: .\scripts\deploy.bat dev" -ForegroundColor Cyan
Write-Host "Then run: .\scripts\pull-ollama-models.ps1" -ForegroundColor Cyan

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Environment Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "1. Start services: .\scripts\deploy.bat dev" -ForegroundColor White
Write-Host "2. Run migrations: .\scripts\deploy.bat migrate" -ForegroundColor White
Write-Host "3. Pull models: .\scripts\pull-ollama-models.ps1" -ForegroundColor White
Write-Host "4. Access services:" -ForegroundColor White
Write-Host "   - API Gateway: http://localhost:8000" -ForegroundColor Gray
Write-Host "   - Model Gateway: http://localhost:8002" -ForegroundColor Gray
Write-Host "   - Memory Engine: http://localhost:8003" -ForegroundColor Gray
Write-Host "   - RSI Engine: http://localhost:8004" -ForegroundColor Gray
Write-Host ""