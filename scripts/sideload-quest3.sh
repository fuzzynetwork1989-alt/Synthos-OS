#!/bin/bash
# Synthos-OS Quest 3 Sideload Script
# This script sideloads the Synthos-OS APK to Quest 3

set -e

echo "========================================"
echo "  Synthos-OS Quest 3 Sideload Script"
echo "========================================"
echo ""

# Check for ADB
if ! command -v adb &> /dev/null; then
    echo "ERROR: ADB is not installed."
    echo "Install Android Platform Tools from: https://developer.android.com/studio/releases/platform-tools"
    exit 1
fi

# Check for APK file
if [ ! -f "synthos-quest3.apk" ]; then
    echo "ERROR: synthos-quest3.apk not found."
    echo "Please download the APK from GitHub releases or build it first."
    exit 1
fi

# Check device connection
echo "Checking for Quest 3 device..."
adb devices

echo ""
read -p "Is your Quest 3 listed above? (y/N): " device_found

if [[ "$device_found" != "y" && "$device_found" != "Y" ]]; then
    echo "Please ensure your Quest 3 is connected via USB and USB debugging is enabled."
    echo "To enable USB debugging on Quest 3:"
    echo "1. Put on your Quest 3 headset"
    echo "2. Go to Settings → System → Developer"
    echo "3. Enable 'Developer Mode'"
    echo "4. Enable 'USB Debugging'"
    echo "5. Connect via USB-C cable"
    exit 1
fi

echo ""
echo "Sideload APK to Quest 3..."
adb install -r synthos-quest3.apk

echo ""
echo "========================================"
echo "  Sideload Complete!"
echo "========================================"
echo ""
echo "The Synthos-OS app has been installed on your Quest 3."
echo ""
echo "To launch the app:"
echo "1. Put on your Quest 3 headset"
echo "2. Go to Library → Unknown Sources"
echo "3. Find and launch 'Synthos-OS AI Assistant'"
echo ""
echo "Note: You may need to grant permissions on first launch."
echo ""