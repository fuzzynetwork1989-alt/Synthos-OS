# Synthos-OS Git Installation Script for Windows
# This script downloads and installs Git

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Git Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is already installed
Write-Host "Checking for existing Git installation..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>$null
    if ($gitVersion) {
        Write-Host "Git is already installed: $gitVersion" -ForegroundColor Green
        $continue = Read-Host "Do you want to reinstall? (y/N)"
        if ($continue -ne "y" -and $continue -ne "Y") {
            Write-Host "Skipping Git installation" -ForegroundColor Yellow
            exit 0
        }
    }
}
catch {
    Write-Host "Git is not installed. Proceeding with installation." -ForegroundColor Green
}

# Download Git installer
Write-Host "Downloading Git installer..." -ForegroundColor Yellow
$gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
$gitInstaller = "$env:TEMP\Git-Installer.exe"

try {
    Write-Host "Downloading from: $gitUrl" -ForegroundColor Gray
    Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller -UseBasicParsing
    Write-Host "Download complete" -ForegroundColor Green
}
catch {
    Write-Host "Failed to download Git installer: $_" -ForegroundColor Red
    Write-Host "Please download manually from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Install Git
Write-Host "Installing Git..." -ForegroundColor Yellow
try {
    Start-Process -FilePath $gitInstaller -ArgumentList "/VERYSILENT /NORESTART /DIR=C:\Program Files\Git" -Wait
    Write-Host "Git installation complete" -ForegroundColor Green
}
catch {
    Write-Host "Failed to install Git: $_" -ForegroundColor Red
    exit 1
}

# Clean up
Remove-Item $gitInstaller -Force

# Add Git to PATH
Write-Host "Adding Git to system PATH..." -ForegroundColor Yellow
$gitPath = "C:\Program Files\Git\bin"
$env:Path += ";$gitPath"
[Environment]::SetEnvironmentVariable("Path", $env:Path, "Machine")

# Verify installation
Write-Host "Verifying Git installation..." -ForegroundColor Yellow
try {
    $newVersion = git --version
    Write-Host "Git successfully installed: $newVersion" -ForegroundColor Green
}
catch {
    Write-Host "Git installation verification failed" -ForegroundColor Red
    Write-Host "Please restart your terminal and try again" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Git Installation Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Please restart your terminal to use Git" -ForegroundColor Yellow
Write-Host ""