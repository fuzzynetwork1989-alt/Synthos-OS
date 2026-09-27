#!/bin/bash
# Synthos-OS Quest 3 Enable Developer Mode Script
# This script helps enable developer mode on Quest 3

echo "========================================"
echo "  Quest 3 Developer Mode Setup"
echo "========================================"
echo ""
echo "This script will guide you through enabling developer mode on your Quest 3."
echo ""
echo "Steps to enable developer mode:"
echo ""
echo "1. Enable Developer Mode in Meta Quest App:"
echo "   - Open the Meta Quest app on your phone"
echo "   - Tap Menu (three lines) → Devices"
echo "   - Select your Quest 3 headset"
echo "   - Tap 'Developer Mode'"
echo "   - Toggle 'Developer Mode' to ON"
echo "   - Confirm with your phone/email"
echo ""
echo "2. Enable USB Debugging on Quest 3:"
echo "   - Put on your Quest 3 headset"
echo "   - Go to Settings → System → Developer"
echo "   - Toggle 'USB Debugging' to ON"
echo "   - Accept the debugging prompt on your phone"
echo ""
echo "3. Connect Quest 3 to Computer:"
echo "   - Connect Quest 3 to your computer via USB-C cable"
echo "   - Ensure you have ADB installed"
echo ""
echo "4. Verify Connection:"
echo "   - Run: adb devices"
echo "   - Your Quest 3 should appear in the list"
echo ""
echo "Press Enter to continue once you've completed these steps..."
read

# Check for ADB
if ! command -v adb &> /dev/null; then
    echo ""
    echo "ERROR: ADB is not installed."
    echo "Install Android Platform Tools from: https://developer.android.com/studio/releases/platform-tools"
    exit 1
fi

# Check device connection
echo ""
echo "Checking for Quest 3 device..."
adb devices

echo ""
echo "========================================"
echo "  Developer Mode Setup Complete!"
echo "========================================"
echo ""
echo "If your Quest 3 is listed above, you're ready to sideload apps!"
echo ""
echo "Next steps:"
echo "1. Download the Synthos-OS APK"
echo "2. Run: ./scripts/sideload-quest3.sh (Linux/Mac) or scripts\sideload-quest3.bat (Windows)"
echo ""