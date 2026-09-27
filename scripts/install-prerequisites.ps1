# Synthos-OS Prerequisites Installation Script for Windows
# This script helps install required software for Synthos-OS development

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Synthos-OS Prerequisites Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check administrator privileges
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "This script requires administrator privileges. Please run as administrator." -ForegroundColor Red
    exit 1
}

# Function to check if a program is installed
function Test-ProgramInstalled {
    param([string]$Name)
    try {
        $result = Get-Command $Name -ErrorAction Stop
        return $true
    }
    catch {
        return $false
    }
}

# Check Git
Write-Host "Checking Git installation..." -ForegroundColor Yellow
if (Test-ProgramInstalled "git") {
    $gitVersion = git --version
    Write-Host "Git is installed: $gitVersion" -ForegroundColor Green
} else {
    Write-Host "Git is not installed. Please install Git from https://git-scm.com/download/win" -ForegroundColor Red
    Write-Host "After installation, restart this script." -ForegroundColor Yellow
    pause
    exit 1
}

# Check Docker
Write-Host "Checking Docker installation..." -ForegroundColor Yellow
if (Test-ProgramInstalled "docker") {
    $dockerVersion = docker --version
    Write-Host "Docker is installed: $dockerVersion" -ForegroundColor Green
} else {
    Write-Host "Docker is not installed. Please install Docker Desktop from https://www.docker.com/products/docker-desktop" -ForegroundColor Red
    Write-Host "After installation, restart this script." -ForegroundColor Yellow
    pause
    exit 1
}

# Check Docker Compose
Write-Host "Checking Docker Compose installation..." -ForegroundColor Yellow
$dockerComposeVersion = docker-compose --version 2>$null
if ($dockerComposeVersion) {
    Write-Host "Docker Compose is installed: $dockerComposeVersion" -ForegroundColor Green
} else {
    Write-Host "Docker Compose is not found. It should be included with Docker Desktop." -ForegroundColor Red
    Write-Host "Please ensure Docker Desktop is properly installed." -ForegroundColor Yellow
}

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
if (Test-ProgramInstalled "python") {
    $pythonVersion = python --version
    Write-Host "Python is installed: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "Python is not installed. Please install Python 3.10+ from https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "After installation, restart this script." -ForegroundColor Yellow
    pause
    exit 1
}

# Check Node.js (for mobile client)
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
if (Test-ProgramInstalled "node") {
    $nodeVersion = node --version
    Write-Host "Node.js is installed: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "Node.js is not installed. Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    Write-Host "This is required for the mobile client development." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Prerequisites Check Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "1. Run: .\scripts\setup-environment.ps1" -ForegroundColor White
Write-Host "2. Run: .\scripts\deploy.bat dev" -ForegroundColor White
Write-Host "3. Run: .\scripts\deploy.bat migrate" -ForegroundColor White
Write-Host ""