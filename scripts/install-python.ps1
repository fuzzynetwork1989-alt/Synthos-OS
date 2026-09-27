# Synthos-OS Python Installation Script for Windows
# This script downloads and installs Python 3.10

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Python Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is already installed
Write-Host "Checking for existing Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion) {
        Write-Host "Python is already installed: $pythonVersion" -ForegroundColor Green
        $continue = Read-Host "Do you want to reinstall? (y/N)"
        if ($continue -ne "y" -and $continue -ne "Y") {
            Write-Host "Skipping Python installation" -ForegroundColor Yellow
            exit 0
        }
    }
}
catch {
    Write-Host "Python is not installed. Proceeding with installation." -ForegroundColor Green
}

# Download Python installer
Write-Host "Downloading Python 3.10 installer..." -ForegroundColor Yellow
$pythonUrl = "https://www.python.org/ftp/python/3.10.13/python-3.10.13-amd64.exe"
$pythonInstaller = "$env:TEMP\Python-Installer.exe"

try {
    Write-Host "Downloading from: $pythonUrl" -ForegroundColor Gray
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller -UseBasicParsing
    Write-Host "Download complete" -ForegroundColor Green
}
catch {
    Write-Host "Failed to download Python installer: $_" -ForegroundColor Red
    Write-Host "Please download manually from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Install Python with all recommended settings
Write-Host "Installing Python 3.10..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Gray
try {
    $arguments = @(
        "/quiet",
        "InstallAllUsers=1",
        "PrependPath=1",
        "Include_test=0"
    )
    Start-Process -FilePath $pythonInstaller -ArgumentList $arguments -Wait
    Write-Host "Python installation complete" -ForegroundColor Green
}
catch {
    Write-Host "Failed to install Python: $_" -ForegroundColor Red
    exit 1
}

# Clean up
Remove-Item $pythonInstaller -Force

# Refresh environment variables
Write-Host "Refreshing environment variables..." -ForegroundColor Yellow
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Verify installation
Write-Host "Verifying Python installation..." -ForegroundColor Yellow
try {
    $newVersion = python --version
    Write-Host "Python successfully installed: $newVersion" -ForegroundColor Green
    
    $pipVersion = pip --version
    Write-Host "Pip successfully installed: $pipVersion" -ForegroundColor Green
}
catch {
    Write-Host "Python installation verification failed" -ForegroundColor Red
    Write-Host "Please restart your terminal and try again" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Python Installation Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Please restart your terminal to use Python" -ForegroundColor Yellow
Write-Host ""