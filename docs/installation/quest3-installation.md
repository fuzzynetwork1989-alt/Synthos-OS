# Synthos-OS Meta Quest 3 Installation Guide
## Complete Step-by-Step Instructions for VR/AR AI Experience

## Overview
Synthos-OS for Meta Quest 3 provides a revolutionary spatial computing AI experience that integrates seamlessly with your headset throughout the entire OS. Unlike any other AI assistant, Synthos-OS becomes an integral part of your Quest 3 experience, accessible from anywhere in the system.

## Key Features
- **System-Wide Integration**: Access Synthos-OS from any app, menu, or system screen
- **Meta AI Alternative**: Choose Synthos-OS as your preferred AI assistant
- **Spatial Interface**: 3D holographic AI interaction in your physical space
- **Voice Commands**: Voice activation from anywhere in Quest OS
- **Hand Tracking**: Natural gesture-based AI interaction
- **Passthrough AI**: AI assistance while viewing real world
- **Mixed Reality**: AI overlays on your real environment
- **Cross-App Context**: AI that understands what you're doing across apps

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Pre-Installation Setup](#pre-installation-setup)
3. [Installation Methods](#installation-methods)
4. [Meta Quest Store Installation](#meta-quest-store-installation)
5. [Sideload Installation](#sideload-installation)
6. [System Integration Setup](#system-integration-setup)
7. [Replacing Meta AI](#replacing-meta-ai)
8. [Spatial Configuration](#spatial-configuration)
9. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Hardware Requirements
- **Device**: Meta Quest 3 (128GB or 512GB)
- **Firmware**: Quest 3 system software v60 or later
- **Controllers**: Touch controllers or hand tracking
- **Audio**: Built-in speakers or headphones recommended
- **Storage**: 5GB free space for app + 10GB for AI models

### Software Requirements
- **Meta Horizon OS**: Latest version
- **Developer Mode**: Enabled (for sideloading)
- **ADB**: Android Debug Bridge (for sideloading)
- **PC for Development**: Windows or Mac (for building/installing)

### Network Requirements
- **Wi-Fi**: 5GHz connection recommended
- **Internet**: Required for initial setup and model downloads
- **Local Network**: Recommended for low-latency AI responses
- **Bandwidth**: 25 Mbps recommended for initial setup

---

## Pre-Installation Setup

### Step 1: Enable Developer Mode on Quest 3

#### 1.1 Enable Developer Mode in Settings
1. Put on your Quest 3 headset
2. Go to Settings → System → Developer
3. Toggle "Developer Mode" to ON
4. You'll need to confirm with your phone/email

#### 1.2 Confirm Developer Mode
1. You'll receive a confirmation email or notification
2. Follow the instructions to confirm
3. Developer mode will be enabled within a few minutes

#### 1.3 Verify Developer Mode
1. Go back to Settings → System → Developer
2. You should see "Developer Mode: ON"
3. Note your device IP address for later steps

### Step 2: Set Up ADB on Your Computer

#### 2.1 Install ADB (Android Debug Bridge)

**Windows:**
1. Download Android Platform Tools: https://developer.android.com/studio/releases/platform-tools
2. Extract the ZIP file
3. Open Command Prompt in the extracted folder
4. Verify installation: `adb version`

**macOS:**
```bash
# Using Homebrew
brew install android-platform-tools

# Or download from Android website
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install android-tools-adb

# Or download from Android website
```

#### 2.2 Enable USB Debugging on Quest 3
1. Put on Quest 3 headset
2. Go to Settings → System → Developer
3. Toggle "USB Debugging" to ON
4. Accept the debugging prompt on your phone/computer

#### 2.3 Connect Quest 3 to Computer
1. Connect Quest 3 to your computer via USB-C cable
2. Open Command Prompt/Terminal
3. Verify connection:
   ```bash
   adb devices
   ```
4. You should see your Quest 3 device listed

### Step 3: Install Synthos-OS Backend Services

The Quest 3 app requires the Synthos-OS backend services to be running. If you haven't installed them yet, follow the [Desktop Installation Guide](desktop-installation.md) through Step 7.

#### 3.1 Verify Backend Services
```bash
# Check services are running
scripts\deploy.bat status  # Windows
./scripts/deploy.sh status  # Linux/Mac
```

#### 3.2 Note Backend IP Address
1. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig | findstr IPv4
   
   # Linux/Mac
   ifconfig | grep inet
   ```
2. Write down this IP address (e.g., 192.168.1.100)
3. You'll need this for Quest 3 app configuration

---

## Installation Methods

### Method 1: Meta Quest Store (Recommended)
Easiest method - install directly from the official Quest Store.

### Method 2: Sideload APK (Advanced)
Install the APK file directly to your Quest 3.

### Method 3: Development Build (For Developers)
Build and install from source code.

---

## Meta Quest Store Installation

### Step 4: Install from Quest Store

#### 4.1 Open Quest Store
1. Put on your Quest 3 headset
2. Press the Quest button on your right controller
3. Navigate to "Store" from the universal menu
4. Search for "Synthos-OS"

#### 4.2 Download and Install
1. Select "Synthos-OS AI Assistant" from search results
2. Click "Get" or "Install"
3. Wait for download and installation to complete
4. The app will appear in your library

#### 4.3 Launch Synthos-OS
1. Go to "Library" in the universal menu
2. Find "Synthos-OS AI Assistant"
3. Click to launch the app

---

## Sideload Installation

### Step 5: Download APK File

#### 5.1 Download from GitHub Releases
1. On your computer, visit: https://github.com/fuzzynetwork1989-alt/Synthos-OS/releases
2. Download the latest Quest 3 APK file (`synthos-quest3-vX.X.X.apk`)
3. Save the file to a known location

#### 5.2 Transfer APK to Quest 3
1. Connect Quest 3 to your computer via USB
2. Use ADB to push the APK:
   ```bash
   adb push synthos-quest3.apk /sdcard/Download/
   ```
3. Or use SideQuest (recommended method)

### Step 6: Install Using SideQuest

#### 6.1 Install SideQuest
1. Download SideQuest from: https://sidequestvr.com/
2. Install on your computer
3. Connect your Quest 3 to your computer

#### 6.2 Install APK via SideQuest
1. Open SideQuest
2. Your Quest 3 should appear in the device list
3. Click on "Install APK"
4. Select the APK file you downloaded
5. Click "Install"
6. Wait for installation to complete

### Step 7: Verify Installation
1. On your Quest 3, go to "Library" → "Unknown Sources"
2. Find "Synthos-OS AI Assistant"
3. Launch the app to verify it works

---

## System Integration Setup

### Step 8: Configure System-Wide Integration

This is the revolutionary feature that makes Synthos-OS accessible from anywhere in Quest OS.

#### 8.1 Enable System Integration
1. Launch Synthos-OS on your Quest 3
2. Go to Settings → System Integration
3. Enable "System-Wide Access"
4. Grant required permissions:
   - System overlay permission
   - Voice access permission
   - Camera access for passthrough
   - Microphone access for voice commands

#### 8.2 Configure Voice Activation
Set up voice commands to access Synthos-OS from anywhere:

1. Go to Settings → Voice Commands
2. Enable "Global Voice Activation"
3. Set wake word (default: "Hey Synthos")
4. Configure sensitivity level
5. Test wake word: "Hey Synthos"

#### 8.3 Configure Hand Tracking
Enable natural gesture-based interaction:

1. Go to Settings → Hand Tracking
2. Enable "Hand Tracking Integration"
3. Calibrate hand tracking:
   - Follow on-screen instructions
   - Make the specified gestures
   - Complete calibration

#### 8.4 Configure Spatial Interface
Set up where the AI appears in your space:

1. Go to Settings → Spatial Interface
2. Choose AI placement:
   - **Front View**: AI appears in front of you
   - **Follow View**: AI follows your gaze
   - **Fixed Position**: AI stays in one spot
3. Set AI distance (how far away it appears)
4. Set AI size
5. Choose AI avatar style

---

## Replacing Meta AI

### Step 9: Replace Meta AI with Synthos-OS

This is a key feature - you can choose Synthos-OS instead of the native Meta AI assistant.

#### 9.1 Enable Meta AI Replacement
1. In Synthos-OS Settings, go to "System Integration"
2. Enable "Replace Meta AI"
3. Confirm you want to replace the default assistant

#### 9.2 Configure Replacement Behavior
Choose how Synthos-OS replaces Meta AI:

1. **Complete Replacement**: Synthos-OS handles all AI interactions
2. **Hybrid Mode**: Use Synthos-OS for complex tasks, Meta AI for simple ones
3. **Context-Aware**: Automatically choose based on context

#### 9.3 Set Voice Command Override
When you say "Hey Meta", it will route to Synthos-OS instead:

1. Go to Settings → Voice Commands
2. Enable "Intercept Meta Commands"
3. Configure which commands to intercept:
   - "Hey Meta" → Routes to Synthos-OS
   - "Hey Facebook" → Routes to Synthos-OS
   - Custom commands

#### 9.4 Configure Menu Integration
Replace Meta AI in system menus:

1. Go to Settings → Menu Integration
2. Enable "System Menu Integration"
3. Synthos-OS will appear in:
   - Universal menu search
   - App launcher search
   - Settings search
   - Browser address bar

### Step 10: Test Integration

#### 10.1 Test Voice Activation
1. Say "Hey Synthos" from anywhere in Quest OS
2. Synthos-OS should activate
3. Try a command: "What can you help me with?"

#### 10.2 Test Menu Integration
1. Open the universal menu (Quest button)
2. Start typing a search query
3. Synthos-OS should appear as an option
4. Select Synthos-OS for the search

#### 10.3 Test In-App Integration
1. Open any app (Browser, TV, etc.)
2. Activate Synthos-OS with voice or gesture
3. Ask a question related to what you're doing
4. Synthos-OS should provide contextual assistance

---

## Spatial Configuration

### Step 11: Configure Spatial AI Interface

#### 11.1 Choose AI Avatar Style
Select how Synthos-OS appears in your space:

1. Go to Settings → Spatial Interface → Avatar
2. Choose style:
   - **Holographic**: Blue-tinted hologram (classic sci-fi)
   - **Realistic**: Photorealistic human appearance
   - **Abstract**: Geometric or particle-based
   - **Minimal**: Simple orb or sphere
3. Customize appearance:
   - Colors
   - Size
   - Transparency level

#### 11.2 Set Spatial Behavior
Configure how the AI moves in your space:

1. Go to Settings → Spatial Interface → Behavior
2. Choose behavior:
   - **Static**: Stays in one place
   - **Follow Gaze**: Moves to where you're looking
   - **Room-Scale**: Can move around your room
   - **Hand-Follow**: Follows your hand position
3. Set movement speed
4. Set transition smoothness

#### 11.3 Configure Passthrough Integration
Enable AI assistance while viewing the real world:

1. Go to Settings → Passthrough
2. Enable "Passthrough AI"
3. Configure how AI appears:
   - **Overlay**: AI overlaid on real world view
   - **Ghost Mode**: Semi-transparent AI
   - **Full Passthrough**: AI appears in your real space
4. Set depth perception
5. Configure occlusion (real objects block AI)

### Step 12: Configure Cross-App Context

#### 12.1 Enable App Awareness
Synthos-OS can understand what app you're using:

1. Go to Settings → App Awareness
2. Enable "Cross-App Context"
3. Grant permission to read currently running app
4. Configure privacy level:
   - **App Name Only**: Only knows which app
   - **Screen Content**: Can see what's on screen
   - **Full Context**: Understands what you're doing

#### 12.2 Configure Per-App Behavior
Customize how Synthos-OS behaves in different apps:

1. Go to Settings → App Settings
2. Add apps to customize:
   - **Browser**: Research assistant mode
   - **TV**: Entertainment companion mode
   - **Games**: Strategy guide mode
   - **Productivity**: Task assistant mode
3. Configure behavior for each app

---

## Advanced Configuration

### Step 13: Configure Backend Connection

#### 13.1 Local Backend (Recommended)
Connect to Synthos-OS running on your local network:

1. Go to Settings → Connection
2. Choose "Local Backend"
3. Enter your computer's IP address
4. Enter port: 8000 (API Gateway)
5. Test connection

#### 13.2 Cloud Backend (Optional)
Connect to cloud-hosted Synthos-OS:

1. Go to Settings → Connection
2. Choose "Cloud Backend"
3. Enter cloud URL
4. Enter API key if required
5. Test connection

#### 13.3 Hybrid Mode
Use local backend for speed, cloud for advanced features:

1. Go to Settings → Connection
2. Choose "Hybrid Mode"
3. Configure which features use which backend
4. Set fallback behavior

### Step 14: Configure AI Models

#### 14.1 Select Models for Quest 3
Choose models optimized for VR/AR:

1. Go to Settings → Models
2. Choose models:
   - **Primary Model**: Main AI model
   - **Vision Model**: For camera/passthrough processing
   - **Audio Model**: For voice processing
3. Recommended models for Quest 3:
   - **Llama2 7B**: Good balance of performance and quality
   - **Mistral 7B**: Higher performance
   - **Phi-3**: Lightweight, good for battery life

#### 14.2 Optimize for VR/AR
Configure models for optimal VR/AR performance:

1. Go to Settings → VR Optimization
2. Enable "VR Mode"
3. Configure:
   - **Response Length**: Shorter for faster responses
   - **Temperature**: Lower for more focused responses
   - **Max Tokens**: Reduce for lower latency
4. Enable "Response Streaming" for real-time responses

---

## Troubleshooting

### Quest 3 Issues

#### App Won't Install
- **Solution**: Ensure Developer Mode is enabled
- **Solution**: Check Quest 3 firmware is up to date
- **Solution**: Verify APK is compatible with your Quest 3
- **Solution**: Try SideQuest instead of direct ADB

#### App Crashes on Launch
- **Solution**: Check backend services are running
- **Solution**: Verify connection settings
- **Solution**: Reinstall the app
- **Solution**: Check Quest 3 storage space

#### System Integration Not Working
- **Solution**: Ensure permissions are granted
- **Solution**: Check "System-Wide Access" is enabled
- **Solution**: Restart Quest 3
- **Solution**: Re-enable integration in settings

#### Voice Commands Not Working
- **Solution**: Check microphone permission
- **Solution**: Check voice activation is enabled
- **Solution**: Recalibrate voice settings
- **Solution**: Try a different wake word

#### Hand Tracking Not Working
- **Solution**: Ensure hand tracking is enabled in Quest settings
- **Solution**: Calibrate hand tracking in Synthos-OS settings
- **Solution**: Check lighting conditions
- **Solution**: Ensure controllers are not interfering

### Connection Issues

#### Can't Connect to Backend
- **Solution**: Verify backend services are running
- **Solution**: Check IP address is correct
- **Solution**: Ensure device is on same network
- **Solution**: Check firewall settings
- **Solution**: Try cloud backend instead

#### High Latency
- **Solution**: Use local backend instead of cloud
- **Solution**: Use lighter model (Phi)
- **Solution**: Reduce response length
- **Solution**: Use 5GHz Wi-Fi
- **Solution**: Move closer to Wi-Fi router

#### Intermittent Connection
- **Solution**: Check Wi-Fi signal strength
- **Solution**: Use wired connection if possible
- **Solution**: Check for interference
- **Solution**: Restart Quest 3

### Performance Issues

#### Poor Frame Rate
- **Solution**: Reduce AI complexity
- **Solution**: Lower graphics settings in Synthos-OS
- **Solution**: Close other apps
- **Solution**: Reduce spatial complexity
- **Solution**: Use simpler AI avatar

#### Battery Drain
- **Solution**: Use lighter model
- **Solution**: Reduce AI processing frequency
- **Solution**: Disable features you don't use
- **Solution**: Lower Wi-Fi frequency
- **Solution**: Enable battery saver mode

#### Overheating
- **Solution**: Take breaks from VR
- **Solution**: Reduce AI processing
- **Solution**: Ensure proper ventilation
- **Solution**: Check for firmware updates

---

## Unique Features

### System-Wide AI Access

#### Anywhere Activation
Unlike other AI assistants that only work within their app, Synthos-OS can be activated from anywhere:

- **From Universal Menu**: Press Quest button, say "Hey Synthos"
- **From Any App**: Use voice command while using any app
- **From Home Screen**: Always available from your main screen
- **From Passthrough**: Activate while viewing real world

#### Contextual Awareness
Synthos-OS understands what you're doing:

- **App Recognition**: Knows which app you're using
- **Task Understanding**: Understands what you're trying to do
- **Spatial Awareness**: Knows where you are in your room
- **Gesture Recognition**: Understands your hand movements

### Revolutionary AI Integration

#### Replacement of Meta AI
Choose Synthos-OS as your primary AI assistant:

- **Voice Command Interception**: "Hey Meta" routes to Synthos-OS
- **Menu Integration**: Synthos-OS in system search
- **System Settings**: Synthos-OS in settings assistance
- **Browser Integration**: Synthos-OS in web search

#### Spatial Computing Native
Built specifically for VR/AR from the ground up:

- **3D Interaction**: Natural hand gestures
- **Spatial Audio**: Directional voice responses
- **Room Mapping**: AI understands your space
- **Passthrough AI**: AI overlays on real world
- **Mixed Reality**: Seamless blend of real and virtual

---

## Advanced Features

### Multi-Modal Interaction

#### Voice + Gesture + Gaze
Combine input methods for rich interaction:

1. **Voice**: Give commands
2. **Gesture**: Point, wave, make shapes
3. **Gaze**: Look at objects to indicate interest
4. Synthos-OS combines all inputs for understanding

#### Spatial Memory
AI remembers things in your physical space:

1. Go to Settings → Spatial Memory
2. Enable "Spatial Memory"
3. Synthos-OS will remember:
   - Where you placed virtual objects
   - Your spatial preferences
   - Room layout and furniture
   - Interaction history in different locations

### Passthrough AI

#### Real-World Assistance
AI helps you with real-world tasks:

1. Enable Passthrough mode
2. Synthos-OS appears in your real space
3. Ask for help with:
   - "How do I fix this?"
   - "What should I do next?"
   - "Explain how this works"
4. AI can recognize objects and provide guidance

---

## Security and Privacy

### Local Processing
By default, Synthos-OS Quest 3 uses local backend:
- All processing happens on your local network
- No data sent to cloud servers
- Camera and microphone data processed locally
- Maximum privacy

### Cloud Features (Optional)
If you enable cloud features:
- Review what data is uploaded
- Understand encryption methods
- Check data retention policies
- Use strong authentication

### Permission Management

#### Camera Permission
- **Purpose**: Spatial mapping, object recognition, passthrough
- **Privacy**: Data processed locally
- **Control**: Can be disabled, affects spatial features

#### Microphone Permission
- **Purpose**: Voice commands, audio processing
- **Privacy**: Audio processed locally
- **Control**: Can be disabled, affects voice features

#### Storage Permission
- **Purpose**: Save spatial data, preferences
- **Privacy**: Data stored locally
- **Control**: Can be limited to app-specific storage

---

## Next Steps

After successful Quest 3 installation:

1. **Complete Calibration**: Run through all calibration steps
2. **Test Integration**: Try activating from different apps
3. **Customize Avatar**: Choose your preferred AI appearance
4. **Configure Voice**: Set up wake words and commands
5. **Explore Features**: Try spatial memory, passthrough AI, etc.
6. **Set Routines**: Configure automation for common tasks

---

## Quick Reference

### Essential Quest 3 Commands
```bash
# Enable Developer Mode
# Settings → System → Developer → Developer Mode: ON

# Enable USB Debugging
# Settings → System → Developer → USB Debugging: ON

# Connect via ADB
adb devices

# Install APK via ADB
adb install synthos-quest3.apk

# Install via SideQuest
# Use SideQuest GUI to install APK

# Check connection
adb shell ping 192.168.1.100  # Your computer's IP
```

### Voice Commands
- "Hey Synthos" - Activate AI
- "What can you do?" - Get help
- "Stop listening" - Deactivate voice
- "Show me" - Make AI visible
- "Hide" - Hide AI

### Gesture Commands
- **Point**: Direct AI attention
- **Wave**: Get AI attention
- **Thumbs Up**: Confirm/Yes
- **Thumbs Down**: Deny/No
- **Open Hand**: Show more info
- **Fist**: Stop/Cancel

### Important Settings Paths
- **System Integration**: Settings → System Integration
- **Voice Commands**: Settings → Voice Commands
- **Spatial Interface**: Settings → Spatial Interface
- **Connection**: Settings → Connection
- **Models**: Settings → Models

---

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [Meta Quest Developer Documentation](https://developer.oculus.com/)
3. Check [SideQuest Documentation](https://sidequestvr.com/)
4. Check [GitHub Issues](https://github.com/fuzzynetwork1989-alt/Synthos-OS/issues)
5. Verify Quest 3 firmware is up to date

---

Congratulations! You now have Synthos-OS Meta Quest 3 installed with revolutionary system-wide AI integration. Experience AI like never before - accessible from anywhere in your Quest 3, replacing Meta AI, and providing spatial computing capabilities that no other AI assistant can match!