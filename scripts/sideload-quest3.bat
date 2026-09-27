# Synthos-OS Quest 3 Sideload Script (Windows)
# This script sideloads the Synthos-OS APK to Quest 3

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Synthos-OS Quest 3 Sideload Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check for ADB
try {
    $adbVersion = adb version 2>$null
    Write-Host "ADB version: $adbVersion" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: ADB is not installed." -ForegroundColor Red
    Write-Host "Install Android Platform Tools from: https://developer.android.com/studio/releases/platform-tools" -ForegroundColor Yellow
    exit 1
}

# Check for APK file
if (-not (Test-Path "synthos-quest3.apk")) {
    Write-Host "ERROR: synthos-quest3.apk not found." -ForegroundColor Red
    Write-Host "Please download the APK from GitHub releases or build it first." -ForegroundColor Yellow
    exit 1
}

# Check device connection
Write-Host "Checking for Quest 3 device..." -ForegroundColor Yellow
adb devices

Write-Host ""
$deviceFound = Read-Host "Is your Quest 3 listed above? (y/N)"

if ($deviceFound -ne "y" -and $deviceFound -ne "Y") {
    Write-Host "Please ensure your Quest 3 is connected via USB and USB debugging is enabled." -ForegroundColor Yellow
    Write-Host "To enable USB debugging on Quest 3:" -ForegroundColor White
    Write-Host "1. Put on your Quest 3 headset" -ForegroundColor Gray
    Write-Host "2. Go to Settings → System → Developer" -ForegroundColor Gray
    Write-Host "3. Enable 'Developer Mode'" -ForegroundColor Gray
    Write-Host "4. Enable 'USB Debugging'" -ForegroundColor Gray
    Write-Host "5. Connect via USB-C cable" -ForegroundColor Gray
    exit 1
}

Write-Host ""
Write-Host "Sideload APK to Quest 3..." -ForegroundColor Cyan
adb install -r synthos-quest3.apk

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Sideload Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The Synthos-OS app has been installed on your Quest 3." -ForegroundColor White
Write-Host ""
Write-Host "To launch the app:" -ForegroundColor White
Write-Host "1. Put on your Quest 3 headset" -ForegroundColor Gray
Write-Host "2. Go to Library → Unknown Sources" -ForegroundColor Gray
Write-Host "3. Find and launch 'Synthos-OS AI Assistant'" -ForegroundColor Gray
Write-Host ""
Write-Host "Note: You may need to grant permissions on first launch." -ForegroundColor Yellow
Write-Host ""