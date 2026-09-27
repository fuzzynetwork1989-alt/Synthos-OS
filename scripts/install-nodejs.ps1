# Synthos-OS Node.js Installation Script for Windows
# This script downloads and installs Node.js LTS

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Node.js Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is already installed
Write-Host "Checking for existing Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>$null
    if ($nodeVersion) {
        Write-Host "Node.js is already installed: $nodeVersion" -ForegroundColor Green
        $continue = Read-Host "Do you want to reinstall? (y/N)"
        if ($continue -ne "y" -and $continue -ne "Y") {
            Write-Host "Skipping Node.js installation" -ForegroundColor Yellow
            exit 0
        }
    }
}
catch {
    Write-Host "Node.js is not installed. Proceeding with installation." -ForegroundColor Green
}

# Download Node.js installer
Write-Host "Downloading Node.js LTS installer..." -ForegroundColor Yellow
$nodeUrl = "https://nodejs.org/dist/v18.19.0/node-v18.19.0-x64.msi"
$nodeInstaller = "$env:TEMP\Node-Installer.msi"

try {
    Write-Host "Downloading from: $nodeUrl" -ForegroundColor Gray
    Invoke-WebRequest -Uri $nodeUrl -OutFile $nodeInstaller -UseBasicParsing
    Write-Host "Download complete" -ForegroundColor Green
}
catch {
    Write-Host "Failed to download Node.js installer: $_" -ForegroundColor Red
    Write-Host "Please download manually from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Install Node.js
Write-Host "Installing Node.js..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Gray
try {
    Start-Process -FilePath "msiexec.exe" -ArgumentList "/i `"$nodeInstaller`" /quiet /norestart" -Wait
    Write-Host "Node.js installation complete" -ForegroundColor Green
}
catch {
    Write-Host "Failed to install Node.js: $_" -ForegroundColor Red
    exit 1
}

# Clean up
Remove-Item $nodeInstaller -Force

# Refresh environment variables
Write-Host "Refreshing environment variables..." -ForegroundColor Yellow
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Verify installation
Write-Host "Verifying Node.js installation..." -ForegroundColor Yellow
try {
    $newNodeVersion = node --version
    Write-Host "Node.js successfully installed: $newNodeVersion" -ForegroundColor Green
    
    $npmVersion = npm --version
    Write-Host "Npm successfully installed: $npmVersion" -ForegroundColor Green
}
catch {
    Write-Host "Node.js installation verification failed" -ForegroundColor Red
    Write-Host "Please restart your terminal and try again" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Node.js Installation Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Please restart your terminal to use Node.js" -ForegroundColor Yellow
Write-Host ""