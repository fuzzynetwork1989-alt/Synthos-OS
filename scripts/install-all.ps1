# Synthos-OS All-in-One Installation Script for Windows
# This script installs all prerequisites automatically

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Synthos-OS All-in-One Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will install:" -ForegroundColor White
Write-Host "  1. Git" -ForegroundColor Gray
Write-Host "  2. Docker Desktop" -ForegroundColor Gray
Write-Host "  3. Python 3.10" -ForegroundColor Gray
Write-Host "  4. Node.js (optional)" -ForegroundColor Gray
Write-Host ""

$installNode = Read-Host "Install Node.js? (Y/n)"
if ([string]::IsNullOrEmpty($installNode)) { $installNode = "y" }

Write-Host ""
Write-Host "Starting installation process..." -ForegroundColor Yellow
Write-Host ""

# Install Git
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 1: Installing Git" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
& "$PSScriptRoot\install-git.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Git installation failed. Aborting." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Install Docker
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 2: Installing Docker Desktop" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
& "$PSScriptRoot\install-docker.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker installation failed. Aborting." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Install Python
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 3: Installing Python 3.10" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
& "$PSScriptRoot\install-python.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python installation failed. Aborting." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Install Node.js (optional)
if ($installNode -eq "y" -or $installNode -eq "Y") {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Step 4: Installing Node.js" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    & "$PSScriptRoot\install-nodejs.ps1"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Node.js installation failed. Continuing..." -ForegroundColor Yellow
    }
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  All Prerequisites Installed!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Restart your computer" -ForegroundColor White
Write-Host "2. Start Docker Desktop from your Start menu" -ForegroundColor White
Write-Host "3. Wait for Docker to be ready (whale icon steady)" -ForegroundColor White
Write-Host "4. Run: .\scripts\setup-environment.ps1" -ForegroundColor White
Write-Host "5. Run: .\scripts\deploy.bat dev" -ForegroundColor White
Write-Host ""