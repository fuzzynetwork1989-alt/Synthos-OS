#!/bin/bash
# Synthos-OS Mobile Build Script for Android
# This script builds the Android APK using EAS

set -e

echo "========================================"
echo "  Synthos-OS Android Build Script"
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
echo "1. development (for testing)"
echo "2. preview (for internal distribution)"
echo "3. production (for Play Store)"
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
echo "Building Android APK with profile: $profile"
echo "This may take 10-30 minutes..."
echo ""

# Build the APK
eas build --platform android --profile $profile

echo ""
echo "========================================"
echo "  Build Complete!"
echo "========================================"
echo ""
echo "Your APK has been built and should be available for download from the EAS dashboard."
echo "Visit: https://expo.dev/accounts/YOUR_ACCOUNT/projects/synthos-os/builds"
echo ""
echo "To install the APK:"
echo "1. Download the APK from the EAS dashboard"
echo "2. Transfer to your Android device"
echo "3. Enable 'Unknown sources' in security settings"
echo "4. Install the APK"
echo ""