#!/bin/bash
# Synthos-OS Mobile Build Script for iOS
# This script builds the iOS IPA using EAS

set -e

echo "========================================"
echo "  Synthos-OS iOS Build Script"
echo "========================================"
echo ""

# Check if we're in the mobile-client directory
if [ ! -f "package.json" ]; then
    echo "ERROR: package.json not found. Please run this script from the apps/mobile-client directory."
    exit 1
fi

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed."
    exit 1
fi

# Check for EAS CLI
if ! command -v eas &> /dev/null; then
    echo "EAS CLI not found. Installing..."
    npm install -g eas-cli
fi

# Check for Expo CLI
if ! command -v expo &> /dev/null; then
    echo "Expo CLI not found. Installing..."
    npm install -g expo-cli
fi

# Ask for build profile
echo "Select build profile:"
echo "1. development (for testing, 7-day validity)"
echo "2. preview (for internal distribution, 7-day validity)"
echo "3. production (for App Store, 1-year validity)"
echo "4. simulator (for testing on device)"
read -p "Enter choice (1-4): " profile_choice

case $profile_choice in
    1)
        profile="development"
        ;;
    2)
        profile="preview"
        ;;
    3)
        profile="production"
        ;;
    4)
        profile="simulator"
        ;;
    *)
        echo "Invalid choice. Using 'development' profile."
        profile="development"
        ;;
esac

echo ""
echo "Building iOS IPA with profile: $profile"
echo "This may take 15-45 minutes..."
echo ""

# Build the IPA
eas build --platform ios --profile $profile

echo ""
echo "========================================"
echo "  Build Complete!"
echo "========================================"
echo ""
echo "Your IPA has been built and should be available for download from the EAS dashboard."
echo "Visit: https://expo.dev/accounts/YOUR_ACCOUNT/projects/synthos-os/builds"
echo ""
echo "To install the IPA:"
echo "1. Download the IPA from the EAS dashboard"
echo "2. Install via TestFlight (recommended)"
echo "3. Or install via AltStore (for sideloading)"
echo ""
echo "Note: Development and preview builds expire after 7 days."
echo "Production builds are valid for 1 year."
echo ""