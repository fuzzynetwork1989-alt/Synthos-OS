# Synthos-OS Docker Desktop Installation Script for Windows
# This script downloads and installs Docker Desktop

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Docker Desktop Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is already installed
Write-Host "Checking for existing Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    if ($dockerVersion) {
        Write-Host "Docker is already installed: $dockerVersion" -ForegroundColor Green
        $continue = Read-Host "Do you want to reinstall? (y/N)"
        if ($continue -ne "y" -and $continue -ne "Y") {
            Write-Host "Skipping Docker installation" -ForegroundColor Yellow
            exit 0
        }
    }
}
catch {
    Write-Host "Docker is not installed. Proceeding with installation." -ForegroundColor Green
}

# Download Docker Desktop installer
Write-Host "Downloading Docker Desktop installer..." -ForegroundColor Yellow
$dockerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
$dockerInstaller = "$env:TEMP\Docker-Desktop-Installer.exe"

try {
    Write-Host "Downloading from: $dockerUrl" -ForegroundColor Gray
    Invoke-WebRequest -Uri $dockerUrl -OutFile $dockerInstaller -UseBasicParsing
    Write-Host "Download complete" -ForegroundColor Green
}
catch {
    Write-Host "Failed to download Docker installer: $_" -ForegroundColor Red
    Write-Host "Please download manually from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Install Docker Desktop
Write-Host "Installing Docker Desktop..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Gray
try {
    Start-Process -FilePath $dockerInstaller -ArgumentList "install --quiet" -Wait
    Write-Host "Docker Desktop installation complete" -ForegroundColor Green
}
catch {
    Write-Host "Failed to install Docker Desktop: $_" -ForegroundColor Red
    exit 1
}

# Clean up
Remove-Item $dockerInstaller -Force

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Docker Desktop Installation Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host "1. Restart your computer" -ForegroundColor White
Write-Host "2. Start Docker Desktop from your Start menu" -ForegroundColor White
Write-Host "3. Wait for the Docker whale icon to appear steady in system tray" -ForegroundColor White
Write-Host "4. Run: docker --version to verify installation" -ForegroundColor White
Write-Host ""