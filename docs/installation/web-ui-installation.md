# Synthos-OS Web UI Installation Guide
## Complete Step-by-Step Instructions for Beginners

## Overview
The Synthos-OS Web UI (Operator Console) provides a browser-based interface to access all Synthos-OS features. This is the easiest way to get started with Synthos-OS as it requires no additional software installation beyond the backend services.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Pre-Installation Setup](#pre-installation-setup)
3. [Web UI Installation Steps](#web-ui-installation-steps)
4. [Accessing the Web Interface](#accessing-the-web-interface)
5. [Web Interface Tour](#web-interface-tour)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.15+, or Linux (any modern distribution)
- **Processor**: Intel Core i3 or AMD equivalent (2015 or newer)
- **Memory**: 4GB RAM (8GB recommended)
- **Storage**: 10GB free disk space
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, or Edge 90+

### Recommended Requirements
- **Operating System**: Windows 11, macOS 12+, or modern Linux
- **Processor**: Intel Core i5 or AMD Ryzen 5 (2018 or newer)
- **Memory**: 8GB RAM (16GB recommended)
- **Storage**: 20GB free disk space (SSD recommended)
- **Browser**: Latest version of Chrome, Firefox, Safari, or Edge

### Network Requirements
- **Internet Connection**: Required for first-time setup and model downloads
- **Local Network**: Synthos-OS runs locally, so no internet is required after initial setup
- **Bandwidth**: 10 Mbps recommended for model downloads (can be several GB)

---

## Pre-Installation Setup

### Step 1: Complete Backend Installation

The Web UI requires the backend services to be running first. If you haven't installed the backend yet, follow the appropriate guide:

- **Windows**: Follow the [Desktop Installation Guide](desktop-installation.md) through Step 7
- **Linux/Mac**: Follow the manual setup instructions in the main README

### Step 2: Verify Backend Services Are Running

Before accessing the Web UI, ensure all backend services are operational:

#### 2.1 Check Service Status
```bash
# Windows
scripts\deploy.bat status

# Linux/Mac
./scripts/deploy.sh status
```

You should see all services showing as "Up" or "healthy":
- API Gateway
- Model Gateway
- Memory Engine
- RSI Engine
- Cognitive Engine
- Tool Execution Engine
- PostgreSQL
- Redis
- Ollama

#### 2.2 Verify Web UI Service
The Web UI (Operator Console) should also be running. Check if it's listed in the status.

If not, start it separately:
```bash
# Navigate to operator console directory
cd apps/operator-console

# Install dependencies (first time only)
npm install

# Start the web UI
npm run dev
```

---

## Web UI Installation Steps

### Step 3: Install Node.js (if not already installed)

The Web UI requires Node.js to run.

#### 3.1 Check if Node.js is Installed
Open Command Prompt or Terminal and type:
```bash
node --version
```

If you see a version number (like `v18.17.0`), Node.js is installed. Skip to Step 4.

#### 3.2 Install Node.js

**Windows:**
1. Go to: https://nodejs.org/
2. Download the "LTS" (Long Term Support) version
3. Run the installer
4. Click "Next" through the wizard
5. Click "Install" and wait for completion
6. Click "Finish"

**macOS:**
1. Install Homebrew if not already installed:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Node.js:
   ```bash
   brew install node
   ```

**Linux:**
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Other distributions
# Use your package manager or download from nodejs.org
```

#### 3.3 Verify Node.js Installation
```bash
node --version
npm --version
```

### Step 4: Install Web UI Dependencies

#### 4.1 Navigate to Web UI Directory
```bash
# From Synthos-OS root directory
cd apps/operator-console
```

#### 4.2 Install Dependencies
```bash
npm install
```

This will install all required packages including:
- React and related libraries
- UI components
- Build tools
- Development dependencies

**Note**: This may take several minutes on first run.

#### 4.3 Verify Installation
Check that `node_modules` folder was created in the operator-console directory.

### Step 5: Configure Web UI

#### 5.1 Environment Configuration
The Web UI needs to know where the backend services are located.

1. Check if `.env` file exists in `apps/operator-console`
2. If not, create it:
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```

3. Open the `.env` file in a text editor
4. Verify the backend URLs are correct:
   ```env
   VITE_API_GATEWAY_URL=http://localhost:8000
   VITE_MODEL_GATEWAY_URL=http://localhost:8002
   VITE_MEMORY_ENGINE_URL=http://localhost:8003
   VITE_RSI_ENGINE_URL=http://localhost:8004
   ```
5. Save the file

#### 5.2 Port Configuration
By default, the Web UI runs on port 3000. If this port is already in use:

1. Open `.env` file
2. Change the port:
   ```env
   VITE_PORT=3001
   ```
3. Save the file

### Step 6: Start Web UI Development Server

#### 6.1 Start the Server
```bash
npm run dev
```

You should see output like:
```
  VITE v5.0.0  ready in 1234 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

#### 6.2 Keep the Server Running
Keep this terminal window open. The development server must remain running to access the Web UI.

#### 6.3 Background Option (Advanced)
If you want to run it in the background:

**Windows:**
```bash
start /B npm run dev
```

**Linux/Mac:**
```bash
npm run dev &
```

---

## Accessing the Web Interface

### Step 7: Open Web Browser

#### 7.1 Recommended Browsers
- **Chrome**: Best overall compatibility
- **Firefox**: Good alternative
- **Edge**: Works well on Windows
- **Safari**: Works on macOS

Avoid older browsers as they may not support modern JavaScript features.

#### 7.2 Navigate to Web UI
Open your web browser and go to:
```
http://localhost:3000
```

If you changed the port in Step 5.2, use that port instead:
```
http://localhost:3001
```

### Step 8: First Launch

#### 8.1 Loading Screen
When you first access the Web UI, you'll see a loading screen while it connects to the backend services.

#### 8.2 Connection Status
The Web UI will show connection status for each service:
- 🟢 Green: Connected
- 🔴 Red: Disconnected
- 🟡 Yellow: Connecting

If any services show as disconnected, check the backend services are running.

#### 8.3 Login Screen
On first launch, you'll see a login screen:
- **Default Username**: `admin`
- **Default Password**: `admin` (change this after first login)

Enter the credentials and click "Login".

---

## Web Interface Tour

### Step 9: Main Dashboard

After logging in, you'll see the main dashboard with:

#### 9.1 Sidebar Navigation
- **Chat**: AI conversation interface
- **Memory**: Memory management and search
- **Settings**: Configuration options
- **Tools**: Tool execution interface
- **RSI**: Recursive self-improvement controls
- **System Status**: System health monitoring

#### 9.2 Main Content Area
The main area shows the currently selected feature.

#### 9.3 Status Bar
At the bottom, you'll see:
- Connection status
- Active model
- Memory usage
- Current system mode

### Step 10: Configure Basic Settings

#### 10.1 Access Settings
Click on "Settings" in the sidebar.

#### 10.2 General Settings
In the General tab, you can configure:
- **Default Model**: Choose your preferred AI model
- **Response Length**: Maximum tokens for AI responses
- **Temperature**: Creativity level (0.0 = conservative, 1.0 = creative)
- **Language**: Interface language

#### 10.3 Model Settings
In the Model tab, you can:
- Select from available models
- Configure model-specific parameters
- Set fallback models
- Adjust resource allocation

### Step 11: Test Basic Functionality

#### 11.1 Send a Test Message
1. Click on "Chat" in the sidebar
2. Type a simple message: "Hello, can you introduce yourself?"
3. Click "Send" or press Enter
4. Wait for the AI response

#### 11.2 Verify Response
You should receive a response from the AI. If successful, the Web UI is working correctly!

---

## Web Interface Features

### Chat Interface

#### Message Types
- **User Messages**: Your messages (shown on right)
- **AI Responses**: AI responses (shown on left)
- **System Messages**: System notifications (shown in center)

#### Chat Features
- **Message History**: Scroll through conversation
- **Clear Chat**: Start a new conversation
- **Export Chat**: Download conversation as text file
- **Voice Input**: Use microphone for voice commands (if enabled)

### Memory Management

#### Memory Types
- **Short-term Memory**: Current session context
- **Long-term Memory**: Persistent knowledge storage
- **Episodic Memory**: Specific events and experiences

#### Memory Features
- **Search**: Search through your memory
- **Add Memory**: Manually add information to memory
- **Memory Categories**: Organize memories by topic
- **Memory Stats**: View memory usage statistics

### Tool Execution

#### Available Tools
- **File Operations**: Read, write, analyze files
- **Web Search**: Search the internet
- **Code Execution**: Run code snippets
- **Data Analysis**: Process and analyze data

#### Tool Features
- **Tool Registry**: View available tools
- **Tool Logs**: See tool execution history
- **Safety Settings**: Configure tool safety levels

### RSI Controls

#### RSI Features
- **Start Cycle**: Manually trigger improvement cycle
- **View History**: See past improvement cycles
- **Cognitive DNA**: View evolved improvement patterns
- **Safety Overrides**: Configure autonomous mode

#### Autonomous Mode
- **Enable/Disable**: Turn autonomous self-improvement on/off
- **Strategy Selection**: Choose improvement strategy
- **Resource Limits**: Set resource budgets

---

## Troubleshooting

### Issue: Web UI Won't Load

**Symptoms**: Browser shows "This site can't be reached" or similar error

**Solutions**:
1. Check if development server is running:
   ```bash
   # Check if process is running
   netstat -ano | findstr :3000  # Windows
   lsof -i :3000                # Linux/Mac
   ```
2. Restart the development server:
   ```bash
   # Stop current server (Ctrl+C)
   npm run dev
   ```
3. Check if port is correct (default is 3000)
4. Try different browser
5. Clear browser cache and cookies

### Issue: Backend Connection Failed

**Symptoms**: Web UI shows "Backend disconnected" or services won't connect

**Solutions**:
1. Verify backend services are running:
   ```bash
   scripts\deploy.bat status  # Windows
   ./scripts/deploy.sh status  # Linux/Mac
   ```
2. Check backend URLs in `.env` file
3. Check for firewall or antivirus blocking connections
4. Try accessing backend API directly:
   ```
   http://localhost:8000/health
   ```

### Issue: AI Responses Are Slow

**Symptoms**: AI takes a long time to respond

**Solutions**:
1. Check system resources (CPU, Memory usage)
2. Try using a lighter model (Phi instead of Llama2)
3. Reduce response length in settings
4. Check if Docker has enough resources allocated
5. Close other applications

### Issue: White Screen or Blank Page

**Symptoms**: Web UI loads but shows blank screen

**Solutions**:
1. Check browser console for errors (F12)
2. Clear browser cache
3. Try different browser
4. Check if Node.js version is compatible (should be 18+)
5. Reinstall dependencies:
   ```bash
   rm -rf node_modules package-lock.json  # Linux/Mac
   rmdir /s /q node_modules package-lock.json  # Windows
   npm install
   ```

### Issue: Features Not Working

**Symptoms**: Specific features (voice, file access, etc.) don't work

**Solutions**:
1. Check browser permissions
2. Enable microphone access for voice input
3. Check if required backend services are running
4. Review feature-specific settings
5. Check browser compatibility

---

## Advanced Configuration

### Custom Domain Access

#### Access from Other Devices
To access the Web UI from other devices on your network:

1. Start development server with host binding:
   ```bash
   npm run dev -- --host 0.0.0.0
   ```
2. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig | findstr IPv4
   
   # Linux/Mac
   ifconfig | grep inet
   ```
3. Access from other devices:
   ```
   http://YOUR_IP_ADDRESS:3000
   ```

#### SSL/HTTPS Setup
For secure access:

1. Install SSL certificate
2. Configure development server to use HTTPS
3. Update `.env` file with HTTPS URLs

### Production Build

#### Build for Production
To create a production build of the Web UI:

1. Build the application:
   ```bash
   npm run build
   ```
2. This creates a `dist/` folder with optimized files
3. Serve with a production web server (nginx, Apache, etc.)

#### Environment Configuration
Create production environment file:
```bash
cp .env.example .env.production
```

Configure production URLs and settings in `.env.production`.

---

## Performance Optimization

### Browser Performance

#### Enable Hardware Acceleration
1. Chrome: Settings → System → "Use hardware acceleration when available"
2. Firefox: Options → General → Performance → "Use recommended performance settings"

#### Clear Browser Cache
Regularly clear browser cache to ensure smooth performance:
- Chrome: Ctrl + Shift + Delete
- Firefox: Ctrl + Shift + Delete
- Safari: Command + Option + E

### Network Performance

#### Use Local Network
For best performance, access Web UI from local network rather than internet.

#### Reduce Latency
Ensure your computer and router are optimized for low latency.

---

## Security Considerations

### Access Control

#### Change Default Password
Immediately change the default admin password:
1. Go to Settings → Account
2. Change password
3. Use a strong, unique password

#### Network Security
- Don't expose Web UI to public internet without proper security
- Use firewall rules to restrict access
- Consider VPN for remote access

### Data Privacy

#### Local-Only Mode
Synthos-OS runs locally by default. Your data stays on your computer.

#### Cloud Features
If you enable cloud features:
- Review privacy policy
- Understand what data is uploaded
- Use encryption for sensitive data

---

## Next Steps

After successful Web UI installation:

1. **Explore Features**: Try out different features and capabilities
2. **Customize Settings**: Configure Synthos-OS to your preferences
3. **Install Mobile App**: Get Synthos-OS on your mobile device
4. **Set Up Voice**: Configure voice input for hands-free operation
5. **Learn Advanced Features**: Explore RSI, tools, and memory management

---

## Quick Reference

### Essential Commands
```bash
# Start Web UI
cd apps/operator-console
npm run dev

# Stop Web UI
# Press Ctrl+C in the terminal

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Build for production
npm run build
```

### Important URLs
- **Web UI**: http://localhost:3000
- **API Gateway**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs

### File Locations
- **Web UI Code**: `apps/operator-console/`
- **Configuration**: `apps/operator-console/.env`
- **Build Output**: `apps/operator-console/dist/`
- **Dependencies**: `apps/operator-console/node_modules/`

---

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [Desktop Installation Guide](desktop-installation.md) for backend issues
3. Check [GitHub Issues](https://github.com/fuzzynetwork1989-alt/Synthos-OS/issues)
4. Verify browser compatibility

---

Congratulations! You now have the Synthos-OS Web UI installed and accessible. Enjoy the full Synthos-OS experience through your web browser!