# Synthos-OS Mobile Build Script for iOS (Windows)
# This script builds the iOS IPA using EAS

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Synthos-OS iOS Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the mobile-client directory
if (-not (Test-Path "package.json")) {
    Write-Host "ERROR: package.json not found. Please run this script from the apps/mobile-client directory." -ForegroundColor Red
    exit 1
}

# Check for Node.js
try {
    $nodeVersion = node --version 2>$null
    Write-Host "Node.js version: $nodeVersion" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Node.js is not installed." -ForegroundColor Red
    exit 1
}

# Check for EAS CLI
try {
    $easVersion = eas --version 2>$null
    Write-Host "EAS CLI version: $easVersion" -ForegroundColor Green
}
catch {
    Write-Host "EAS CLI not found. Installing..." -ForegroundColor Yellow
    npm install -g eas-cli
}

# Check for Expo CLI
try {
    $expoVersion = expo --version 2>$null
    Write-Host "Expo CLI version: $expoVersion" -ForegroundColor Green
}
catch {
    Write-Host "Expo CLI not found. Installing..." -ForegroundColor Yellow
    npm install -g expo-cli
}

# Ask for build profile
Write-Host "Select build profile:" -ForegroundColor White
Write-Host "1. development (for testing, 7-day validity)" -ForegroundColor Gray
Write-Host "2. preview (for internal distribution, 7-day validity)" -ForegroundColor Gray
Write-Host "3. production (for App Store, 1-year validity)" -ForegroundColor Gray
Write-Host "4. simulator (for testing on device)" -ForegroundColor Gray
$profileChoice = Read-Host "Enter choice (1-4)"

switch ($profileChoice) {
    "1" { $profile = "development" }
    "2" { $profile = "preview" }
    "3" { $profile = "production" }
    "4" { $profile = "simulator" }
    default { 
        Write-Host "Invalid choice. Using 'development' profile." -ForegroundColor Yellow
        $profile = "development"
    }
}

Write-Host ""
Write-Host "Building iOS IPA with profile: $profile" -ForegroundColor Cyan
Write-Host "This may take 15-45 minutes..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Note: iOS builds require a Mac computer. This script will use EAS cloud build." -ForegroundColor Yellow
Write-Host ""

# Build the IPA
eas build --platform ios --profile $profile

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Build Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your IPA has been built and should be available for download from the EAS dashboard." -ForegroundColor White
Write-Host "Visit: https://expo.dev/accounts/YOUR_ACCOUNT/projects/synthos-os/builds" -ForegroundColor Gray
Write-Host ""
Write-Host "To install the IPA:" -ForegroundColor White
Write-Host "1. Download the IPA from the EAS dashboard" -ForegroundColor Gray
Write-Host "2. Install via TestFlight (recommended)" -ForegroundColor Gray
Write-Host "3. Or install via AltStore (for sideloading)" -ForegroundColor Gray
Write-Host ""
Write-Host "Note: Development and preview builds expire after 7 days." -ForegroundColor Yellow
Write-Host "Production builds are valid for 1 year." -ForegroundColor Yellow
Write-Host ""