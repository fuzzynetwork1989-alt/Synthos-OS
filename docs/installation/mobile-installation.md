# Synthos-OS Mobile Installation Guide
## Complete Step-by-Step Instructions for iOS and Android

## Overview
This guide will walk you through installing Synthos-OS Mobile on your iOS or Android device. You can either install the pre-built app or build it yourself from source.

## Table of Contents
1. [Installation Options](#installation-options)
2. [Pre-Built App Installation](#pre-built-app-installation)
3. [Building from Source (Android)](#building-from-source-android)
4. [Building from Source (iOS)](#building-from-source-ios)
5. [APK Installation for Android](#apk-installation-for-android)
6. [iOS Installation](#ios-installation)
7. [Mobile App Configuration](#mobile-app-configuration)
8. [Troubleshooting](#troubleshooting)

---

## Installation Options

### Option 1: Pre-Built App (Easiest)
- **Android**: Download APK file and install
- **iOS**: Download TestFlight link or sideload
- **Best for**: Most users who want quick installation

### Option 2: Build from Source (Advanced)
- **Android**: Build APK using Expo/EAS
- **iOS**: Build IPA using Expo/EAS
- **Best for**: Developers who want to customize the app

### Option 3: Development Mode (For Testing)
- **Android**: Use Expo Go app
- **iOS**: Use Expo Go app
- **Best for**: Testing during development

---

## Pre-Built App Installation

### Android APK Installation

#### Step 1: Download APK File
1. Visit the Synthos-OS releases page: https://github.com/fuzzynetwork1989-alt/Synthos-OS/releases
2. Download the latest Android APK file (`synthos-mobile-vX.X.X.apk`)
3. Save the file to your device's Downloads folder

#### Step 2: Enable Unknown Sources
Android requires you to allow installation from unknown sources for apps not from Play Store.

**Android 8.0+ (Oreo and newer):**
1. Go to Settings → Apps & notifications → Special app access → Install unknown apps
2. Find your file manager app (e.g., "Files", "My Files")
3. Enable "Allow from this source"

**Android 7.0 and older:**
1. Go to Settings → Security
2. Enable "Unknown sources"

#### Step 3: Install APK
1. Open your file manager app
2. Navigate to Downloads folder
3. Tap on the APK file you downloaded
4. Review permissions requested by the app
5. Tap "Install"
6. Wait for installation to complete
7. Tap "Open" to launch Synthos-OS Mobile

#### Step 4: Grant Permissions
On first launch, the app will request permissions:
- **Camera**: For visual input and AR features
- **Microphone**: For voice commands
- **Storage**: For file access
- **Location**: For context-aware features
- **Bluetooth**: For device connectivity

Grant these permissions for full functionality.

### iOS Installation

#### Step 1: TestFlight Installation (Recommended)
1. Visit the Synthos-OS TestFlight link (if available)
2. Accept the TestFlight invitation
3. Install the TestFlight app from App Store
4. Open TestFlight and install Synthos-OS Mobile

#### Step 2: AltStore Installation (Alternative)
If TestFlight is not available, you can use AltStore to sideload the app.

**Prerequisites:**
- Mac computer with Xcode
- Apple Developer account (free or paid)
- AltStore app on your iOS device

**Installation Steps:**
1. Install AltStore on your iOS device
2. Download the IPA file from GitHub releases
3. Open AltStore and sign in with your Apple ID
4. Tap the "+" button to install the IPA file
5. Follow the on-screen instructions

---

## Building from Source (Android)

### Prerequisites

#### Step 1: Install Node.js
1. Download Node.js from https://nodejs.org/
2. Install the LTS version
3. Verify installation: `node --version`

#### Step 2: Install Expo CLI
```bash
npm install -g expo-cli
```

#### Step 3: Install Expo Application
1. Install Expo Go app from Google Play Store
2. This app allows you to test development builds

### Building Process

#### Step 4: Clone Repository
```bash
git clone https://github.com/fuzzynetwork1989-alt/Synthos-OS.git
cd Synthos-OS
```

#### Step 5: Install Dependencies
```bash
cd apps/mobile-client
npm install
```

#### Step 6: Configure Environment
1. Copy environment file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` file with your backend URLs:
   ```env
   EXPO_PUBLIC_API_GATEWAY_URL=http://YOUR_COMPUTER_IP:8000
   EXPO_PUBLIC_MODEL_GATEWAY_URL=http://YOUR_COMPUTER_IP:8002
   EXPO_PUBLIC_MEMORY_ENGINE_URL=http://YOUR_COMPUTER_IP:8003
   ```
3. Replace `YOUR_COMPUTER_IP` with your actual IP address

#### Step 7: Start Development Server
```bash
npm start
```

#### Step 8: Test with Expo Go
1. Open Expo Go app on your Android device
2. Scan the QR code shown in the terminal
3. The app will load in Expo Go

### Building APK with EAS

#### Step 9: Install EAS CLI
```bash
npm install -g eas-cli
```

#### Step 10: Configure EAS
```bash
eas build:configure
```

#### Step 11: Build APK
```bash
# Development build
eas build --platform android --profile development

# Preview build
eas build --platform android --profile preview

# Production build
eas build --platform android --profile production
```

#### Step 12: Download APK
1. After build completes, EAS will provide a download link
2. Download the APK file
3. Install on your Android device using the Pre-Built App Installation steps

---

## Building from Source (iOS)

### Prerequisites

#### Step 1: Mac Computer Required
iOS development requires a Mac computer with:
- macOS 12.0 or later
- Xcode 14.0 or later
- Apple Developer account (free or paid)

#### Step 2: Install Xcode
1. Download Xcode from Mac App Store
2. Install Xcode (15GB+ download)
3. Install Command Line Tools:
   ```bash
   xcode-select --install
   ```

#### Step 3: Install CocoaPods
```bash
sudo gem install cocoapods
```

#### Step 4: Install Node.js
1. Download Node.js from https://nodejs.org/
2. Install the LTS version
3. Verify installation: `node --version`

#### Step 5: Install Expo CLI
```bash
npm install -g expo-cli
```

### Building Process

#### Step 6: Clone Repository
```bash
git clone https://github.com/fuzzynetwork1989-alt/Synthos-OS.git
cd Synthos-OS
```

#### Step 7: Install Dependencies
```bash
cd apps/mobile-client
npm install
```

#### Step 8: Install iOS Dependencies
```bash
cd ios
pod install
cd ..
```

#### Step 9: Configure Environment
1. Copy environment file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` file with your backend URLs

#### Step 10: Start Development Server
```bash
npm start
```

#### Step 11: Test with Expo Go
1. Install Expo Go from App Store
2. Open Expo Go app on your iOS device
3. Scan the QR code shown in the terminal
4. The app will load in Expo Go

### Building IPA with EAS

#### Step 12: Install EAS CLI
```bash
npm install -g eas-cli
```

#### Step 13: Configure EAS
```bash
eas build:configure
```

#### Step 14: Configure Apple Developer Account
1. You'll need an Apple Developer account
2. Free account: Good for 7-day builds
3. Paid account ($99/year): Good for 1-year builds

#### Step 15: Build IPA
```bash
# Development build
eas build --platform ios --profile development

# Preview build
eas build --platform ios --profile preview

# Production build
eas build --platform ios --profile production
```

#### Step 16: Download IPA
1. After build completes, EAS will provide a download link
2. Download the IPA file
3. Install on your iOS device using TestFlight or AltStore

---

## APK Installation for Android

### Direct Installation

#### Method 1: From Device Storage
1. Transfer APK file to your Android device
2. Use file manager to locate the APK
3. Tap the APK file
4. Grant permissions and install

#### Method 2: From Computer via USB
1. Connect Android device to computer via USB
2. Enable USB debugging on device:
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times to enable Developer Options
   - Go to Settings → Developer Options
   - Enable "USB Debugging"
3. On computer, use ADB to install:
   ```bash
   adb install synthos-mobile.apk
   ```

#### Method 3: via Cloud Storage
1. Upload APK to Google Drive, Dropbox, etc.
2. Download on Android device
3. Install as per Method 1

### Troubleshooting APK Installation

#### "Parse Error" or "There was a problem parsing the package"
- APK file may be corrupted
- Download the APK again
- Ensure you downloaded the correct version for your Android version

#### "App not installed" error
- Uninstall previous version first
- Clear cache of file manager app
- Restart device and try again

#### "Installation blocked" error
- Check if "Unknown sources" is enabled
- Check if your device has security apps blocking installation
- Temporarily disable antivirus/security apps

---

## iOS Installation

### TestFlight Installation

#### Step 1: Join TestFlight
1. Click the TestFlight invitation link
2. Open in TestFlight app
3. Accept the invitation

#### Step 2: Install TestFlight
If TestFlight is not installed:
1. Download from App Store
2. Open the app and sign in with your Apple ID

#### Step 3: Install Synthos-OS
1. In TestFlight, find Synthos-OS Mobile
2. Tap "Install"
3. Wait for installation to complete
4. Launch the app

### AltStore Installation

#### Step 1: Install AltStore
1. Download AltStore from https://altstore.io/
2. Sideload AltStore onto your iOS device
3. Open AltStore and sign in with your Apple ID

#### Step 2: Download IPA
1. Download the IPA file from GitHub releases
2. Transfer to your iOS device (via AirDrop, cloud storage, etc.)

#### Step 3: Install with AltStore
1. Open AltStore
2. Tap the "+" button
3. Select the IPA file
4. Enter your Apple ID password
5. Wait for installation to complete

#### Step 4: Re-signing (Every 7 Days)
Free developer builds need to be re-signed every 7 days:
1. Open AltStore
2. Find Synthos-OS in "My Apps"
3. Tap "Re-sign"

### iOS Enterprise Installation

For enterprise distribution:

#### Step 1: Obtain Enterprise Certificate
- Apple Developer Enterprise Program ($299/year)
- Create distribution certificate
- Create provisioning profile

#### Step 2: Build Enterprise IPA
Use EAS with enterprise profile:
```bash
eas build --platform ios --profile enterprise
```

#### Step 3: Distribute via MDM
- Upload to Mobile Device Management (MDM) system
- Deploy to devices via MDM

---

## Mobile App Configuration

### First Launch Setup

#### Step 1: Backend Connection
On first launch, the app will ask for backend connection:

1. **Local Network**: If SynthOS backend is on your local network
   - Enter your computer's IP address
   - Port 8000 (API Gateway)

2. **Cloud**: If using cloud deployment
   - Enter cloud URL
   - Enter API key if required

#### Step 2: Model Selection
Choose your preferred AI model:
- **Llama2**: Good all-around choice
- **Mistral**: Higher performance
- **Neural Chat**: Best for conversations
- **Phi**: Lightweight, good for older devices

#### Step 3: Permissions
Grant requested permissions:
- **Camera**: For visual input
- **Microphone**: For voice commands
- **Storage**: For file access
- **Location**: For context-aware features

### Settings Configuration

#### General Settings
- **Theme**: Light, Dark, or Auto
- **Language**: Interface language
- **Response Length**: Maximum tokens
- **Temperature**: Creativity level

#### Model Settings
- **Default Model**: Primary AI model
- **Fallback Models**: Backup models
- **Resource Allocation**: Memory and CPU limits
- **Advanced Parameters**: Custom model settings

#### Connection Settings
- **Backend URL**: API Gateway address
- **Connection Timeout**: Request timeout
- **Retry Policy**: Retry behavior on failure

#### Voice Settings
- **Voice Input**: Enable/disable microphone
- **Voice Output**: Text-to-speech
- **Wake Word**: Activate with voice
- **Language**: Voice recognition language

### Advanced Configuration

#### Custom Backend
If you're running Synthos-OS on a different server:

1. Go to Settings → Connection
2. Enter custom backend URL
3. Configure authentication if required
4. Test connection

#### Model Fine-Tuning
Advanced users can configure model-specific parameters:

1. Go to Settings → Model → Advanced
2. Select model
3. Configure:
   - Temperature (0.0 - 1.0)
   - Top P (0.0 - 1.0)
   - Top K (1 - 100)
   - Repeat Penalty (0.0 - 2.0)
   - Max Tokens (1 - 4096)

#### Memory Configuration
Configure mobile memory settings:

1. Go to Settings → Memory
2. Configure:
   - Local storage limit
   - Cloud sync (if available)
   - Memory retention policy
   - Search indexing

---

## Troubleshooting

### Android Issues

#### App Won't Install
- **Solution**: Enable "Unknown sources" in security settings
- **Solution**: Check Android version compatibility
- **Solution**: Ensure APK is not corrupted

#### App Crashes on Launch
- **Solution**: Clear app cache and data
- **Solution**: Reinstall the app
- **Solution**: Check device compatibility
- **Solution**: Report crash logs

#### Can't Connect to Backend
- **Solution**: Check if backend services are running
- **Solution**: Verify IP address is correct
- **Solution**: Check network connectivity
- **Solution**: Ensure device is on same network as backend

#### Battery Drain
- **Solution**: Reduce resource allocation in settings
- **Solution**: Use lighter model (Phi)
- **Solution**: Enable battery optimization
- **Solution**: Close other apps

### iOS Issues

#### TestFlight Installation Fails
- **Solution**: Check TestFlight app is updated
- **Solution**: Ensure Apple ID is correct
- **Solution**: Try force-closing TestFlight and reopening

#### AltStore Installation Fails
- **Solution**: Ensure AltStore is properly sideloaded
- **Solution**: Check Apple ID credentials
- **Solution**: Reinstall AltStore
- **Solution**: Check iOS version compatibility

#### App Won't Open
- **Solution**: Re-sign the app (free developer builds expire in 7 days)
- **Solution**: Reinstall the app
- **Solution**: Check iOS version compatibility
- **Solution**: Report crash logs

#### Connection Issues
- **Solution**: Check local network connection
- **Solution**: Verify backend URL is correct
- **Solution**: Check if backend services are running
- **Solution**: Try using cellular data to test

### Cross-Platform Issues

#### Features Not Working
- **Solution**: Check permissions are granted
- **Solution**: Verify backend services support the feature
- **Solution**: Check app version matches backend version
- **Solution**: Update to latest app version

#### Performance Issues
- **Solution**: Use lighter model
- **Solution**: Reduce resource allocation
- **Solution**: Close other apps
- **Solution**: Restart device

#### Sync Issues
- **Solution**: Check cloud sync settings
- **Solution**: Verify internet connection
- **Solution**: Check cloud service status
- **Solution**: Re-enable sync in settings

---

## Development Mode Testing

### Using Expo Go

#### Android Testing
1. Install Expo Go from Google Play Store
2. Start development server: `npm start` in mobile-client directory
3. Scan QR code with Expo Go
4. App loads in Expo Go for testing

#### iOS Testing
1. Install Expo Go from App Store
2. Start development server: `npm start` in mobile-client directory
3. Scan QR code with Expo Go
4. App loads in Expo Go for testing

### Development Build

#### Android Development Build
```bash
eas build --platform android --profile development
```
This creates a development build with:
- Faster build times
- Debug menu enabled
- Development tools
- Not suitable for production

#### iOS Development Build
```bash
eas build --platform ios --profile development
```
This creates a development build with:
- Debug menu enabled
- Development tools
- Faster build times
- Must be re-signed every 7 days

---

## Security Considerations

### App Permissions

#### Camera Permission
- **Purpose**: Visual input, AR features, document scanning
- **Privacy**: Images processed locally (unless cloud features enabled)
- **Control**: Can be disabled in settings

#### Microphone Permission
- **Purpose**: Voice commands, audio processing
- **Privacy**: Audio processed locally (unless cloud features enabled)
- **Control**: Can be disabled in settings

#### Storage Permission
- **Purpose**: File access, document processing
- **Privacy**: Files processed locally
- **Control**: Can be limited to specific directories

#### Location Permission
- **Purpose**: Context-aware features
- **Privacy**: Location used locally
- **Control**: Can be disabled in settings

### Data Privacy

#### Local-Only Mode
Synthos-OS Mobile runs in local-only mode by default:
- All data stays on your device
- No data sent to cloud servers
- AI processing happens locally via backend

#### Cloud Features
If you enable cloud features:
- Review what data is uploaded
- Understand encryption and security
- Review privacy policy
- Use strong passwords

---

## Next Steps

After successful mobile installation:

1. **Test Basic Features**: Try chat, memory, and tools
2. **Configure Settings**: Customize the app to your preferences
3. **Enable Voice**: Set up voice commands for hands-free use
4. **Explore Advanced Features**: Try RSI, tools, and memory management
5. **Join Community**: Get help and share experiences

---

## Quick Reference

### Android Commands
```bash
# Install from GitHub
git clone https://github.com/fuzzynetwork1989-alt/Synthos-OS.git
cd Synthos-OS/apps/mobile-client
npm install

# Start development
npm start

# Build APK
eas build --platform android --profile production

# Install via ADB
adb install synthos-mobile.apk
```

### iOS Commands
```bash
# Install from GitHub
git clone https://github.com/fuzzynetwork1989-alt/Synthos-OS.git
cd Synthos-OS/apps/mobile-client
npm install

# Install iOS dependencies
cd ios && pod install && cd ..

# Start development
npm start

# Build IPA
eas build --platform ios --profile production
```

### Important URLs
- **Expo**: https://expo.dev
- **EAS Build**: https://expo.dev/build
- **TestFlight**: https://testflight.apple.com
- **AltStore**: https://altstore.io

### File Locations
- **Mobile App Code**: `apps/mobile-client/`
- **Configuration**: `apps/mobile-client/.env`
- **Build Outputs**: EAS provides download links
- **Android Build**: `apps/mobile-client/android/`
- **iOS Build**: `apps/mobile-client/ios/`

---

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [Expo Documentation](https://docs.expo.dev/)
3. Check [GitHub Issues](https://github.com/fuzzynetwork1989-alt/Synthos-OS/issues)
4. Check device compatibility

---

Congratulations! You now have Synthos-OS Mobile installed on your device. Enjoy AI-powered capabilities on the go!