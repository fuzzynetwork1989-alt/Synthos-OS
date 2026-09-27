# Synthos-OS Beginner's Quick Start Guide
## Get Started in 30 Minutes - No Experience Required

## Overview
This guide is designed for complete beginners who have never used Synthos-OS before. We'll walk you through everything from installation to your first AI conversation in simple, easy-to-follow steps.

## Table of Contents
1. [What is Synthos-OS?](#what-is-synthos-os)
2. [What You'll Need](#what-youll-need)
3. [Quick Installation (5 Minutes)](#quick-installation-5-minutes)
4. [Start Using Synthos-OS (10 Minutes)](#start-using-synthos-os-10-minutes)
5. [Basic Features (10 Minutes)](#basic-features-10-minutes)
6. [Next Steps](#next-steps)
7. [Where to Get Help](#where-to-get-help)

---

## What is Synthos-OS?

### In Simple Terms
Synthos-OS is like having a super-smart AI assistant that:
- Can answer your questions
- Help you write documents
- Write code for you
- Remember what you tell it
- Improve itself over time
- Works on your computer, phone, and VR headset

### What Makes It Special
- **Runs Locally**: Your data stays on your computer (private and secure)
- **Multi-Platform**: Works on Desktop, Web, Mobile, and Meta Quest 3
- **Self-Improving**: It gets better at helping you over time
- **System-Wide**: On Quest 3, it replaces Meta AI and works throughout the entire system

### What You Can Do With It
- **Chat**: Have conversations on any topic
- **Write**: Create documents, emails, stories
- **Code**: Get help with programming
- **Research**: Look up information and analyze data
- **Remember**: It remembers important things you tell it
- **Automate**: It can help you automate tasks

---

## What You'll Need

### For Desktop/Web Version (Recommended for Beginners)

#### Hardware
- **Computer**: Windows 10/11, Mac, or Linux
- **Memory**: 8GB RAM minimum (16GB recommended)
- **Storage**: 50GB free space
- **Internet**: For initial setup only

#### Software (We'll help you install these)
- Git (for downloading)
- Docker Desktop (for running services)
- Python 3.10+ (for backend)
- Node.js (optional, for some features)

### For Mobile Version
- **Android phone** or **iPhone**
- **Internet connection**
- **Synthos-OS backend running on your computer** (first)

### For Quest 3 Version
- **Meta Quest 3 headset**
- **Computer with Synthos-OS backend running**
- **Same network connection**

---

## Quick Installation (5 Minutes)

### Step 1: Check Your Computer (1 Minute)

#### Check Operating System
- **Windows**: Click Start → Settings → System → About
- **Mac**: Click Apple menu → About This Mac
- **Linux**: Open terminal and type: `uname -a`

**You need:** Windows 10+, macOS 10.15+, or modern Linux

#### Check RAM
- **Windows**: Task Manager → Performance → Memory
- **Mac**: About This Mac → Memory
- **Linux**: Open terminal and type: `free -h`

**You need:** 8GB minimum, 16GB recommended

#### Check Disk Space
- **Windows**: File Explorer → This PC
- **Mac**: About This Mac → Storage
- **Linux**: Open terminal and type: `df -h`

**You need:** 50GB free space

### Step 2: Install Required Software (2 Minutes)

#### Install Git
1. Go to: https://git-scm.com/download/win (Windows) or https://git-scm.com/download/mac (Mac)
2. Download and run the installer
3. **IMPORTANT**: Check "Add Git to PATH" during installation
4. Click through and finish

**Verify:** Open Command Prompt/Terminal and type: `git --version`
You should see something like: `git version 2.40.0`

#### Install Docker Desktop
1. Go to: https://www.docker.com/products/docker-desktop
2. Download and run the installer
3. Restart your computer when asked
4. After restart, open Docker Desktop from your Start menu
5. Wait for the whale icon to appear steady in the bottom right corner

**Verify:** Open Command Prompt/Terminal and type: `docker --version`
You should see something like: `Docker version 24.0.0`

#### Install Python
1. Go to: https://www.python.org/downloads/
2. Download Python 3.10.x (choose the latest 3.10 version)
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH"
5. Click "Install Now"

**Verify:** Open Command Prompt/Terminal and type: `python --version`
You should see something like: `Python 3.10.11`

### Step 3: Download Synthos-OS (1 Minute)

#### Method 1: Download ZIP (Easiest)
1. Go to: https://github.com/fuzzynetwork1989-alt/Synthos-OS
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to your Desktop
5. Rename the extracted folder to "Synthos-OS"

#### Method 2: Use Git (If you installed Git)
1. Open Command Prompt/Terminal
2. Type: `cd Desktop`
3. Type: `git clone https://github.com/fuzzynetwork1989-alt/Synthos-OS.git`

### Step 4: Run Setup Script (1 Minute)

#### Windows
1. Open the Synthos-OS folder on your Desktop
2. Double-click on `scripts` folder
3. Right-click on `setup-environment.ps1`
4. Select "Run with PowerShell"
5. If asked about execution policy, click "Run once"
6. Wait for it to complete (1-2 minutes)

#### Mac/Linux
1. Open Terminal
2. Type: `cd Desktop/Synthos-OS`
3. Type: `cp .env.example .env`
4. Type: `pip install -e .`

---

## Start Using Synthos-OS (10 Minutes)

### Step 5: Start the Services (2 Minutes)

#### Windows
1. Open Command Prompt
2. Type: `cd Desktop\Synthos-OS`
3. Type: `scripts\deploy.bat dev`
4. Wait for all services to start (2-5 minutes on first run)
5. You'll see "done" messages when ready

#### Mac/Linux
1. Open Terminal
2. Type: `cd Desktop/Synthos-OS`
3. Type: `./scripts/deploy.sh dev`
4. Wait for services to start

**What's happening:** Synthos-OS is starting all its backend services (database, AI models, etc.) in Docker containers.

### Step 6: Run Database Setup (1 Minute)

#### Windows
1. In the same Command Prompt window, type: `scripts\deploy.bat migrate`
2. Wait for "Migrations completed successfully!"

#### Mac/Linux
1. In the same Terminal window, type: `./scripts/deploy.sh migrate`
2. Wait for completion

**What's happening:** This sets up the database tables Synthos-OS needs to store your memories and data.

### Step 7: Download AI Models (5 Minutes)

#### Windows
1. In the same Command Prompt window, type: `scripts\pull-ollama-models.ps1`
2. Wait for all models to download (10-30 minutes depending on internet speed)
3. You'll see 5 models being downloaded:
   - Llama2 (general purpose)
   - Mistral (high performance)
   - Neural Chat (conversations)
   - Code Llama (programming)
   - Phi (lightweight)

#### Mac/Linux
1. In the same Terminal window, type:
   ```
   docker exec -it synthos-ollama bash
   ollama pull llama2 mistral neural-chat codellama phi
   exit
   ```

**What's happening:** Synthos-OS is downloading the AI models it uses to think and respond. These are large files (several GB each).

**Tip:** This is a one-time setup. After this, the models stay on your computer.

### Step 8: Start the Web Interface (2 Minutes)

#### Option 1: Use Web UI (Easiest)
1. Keep the Command Prompt/Terminal window open (services must stay running)
2. Open your web browser (Chrome, Firefox, Edge, Safari)
3. Go to: http://localhost:3000
4. You should see the Synthos-OS login screen

#### Option 2: Start Development Server (For Customization)
1. Open a NEW Command Prompt/Terminal window
2. Type: `cd Desktop\Synthos-OS\apps\operator-console`
3. Type: `npm install` (first time only)
4. Type: `npm run dev`
5. Open browser to: http://localhost:3000

**What's happening:** The web interface is the easiest way to use Synthos-OS. It works in any browser.

---

## Basic Features (10 Minutes)

### Step 9: First Login (1 Minute)

1. On the login screen, enter:
   - **Username**: `admin`
   - **Password**: `admin`
2. Click "Login"
3. You'll see the main Synthos-OS dashboard

**Important:** Change this password later in Settings for security!

### Step 10: Your First Conversation (3 Minutes)

#### Send Your First Message
1. Click on "Chat" in the left sidebar
2. In the text box at the bottom, type: "Hello, can you introduce yourself?"
3. Click "Send" or press Enter
4. Wait for the AI response (5-30 seconds)

#### Try Different Questions
Ask the AI anything:
- "What can you help me with?"
- "Explain how computers work"
- "Write a short story about a robot"
- "Help me write an email"

**Tip:** The AI responds based on the model you selected. Try different models in Settings!

### Step 11: Explore the Interface (2 Minutes)

#### Navigation
- **Chat**: Talk to the AI
- **Memory**: See what the AI remembers
- **Settings**: Configure Synthos-OS
- **Tools**: Use special tools (web search, file operations)
- **RSI**: See self-improvement activities
- **System Status**: Check if everything is working

#### Chat Features
- **New Chat**: Start a fresh conversation
- **Clear Chat**: Clear current conversation
- **Export Chat**: Download conversation as text file
- **Voice Input**: Use microphone (if enabled)

### Step 12: Configure Basic Settings (2 Minutes)

#### Change Model
1. Click "Settings" in the sidebar
2. Click "Model" tab
3. Choose a different model:
   - **Llama2**: Good all-around
   - **Mistral**: Faster, higher quality
   - **Neural Chat**: Best for conversations
   - **Phi**: Lightweight, good for older computers
4. Click "Save"

#### Adjust Response Length
1. In Settings → Model
2. Change "Max Tokens":
   - **128**: Very short responses
   - **512**: Short (default)
   - **1024**: Medium
   - **2048**: Long
3. Click "Save"

#### Adjust Creativity
1. In Settings → Model
2. Change "Temperature":
   - **0.3**: Focused, factual responses
   - **0.7**: Balanced (default)
   - **0.9**: Creative, diverse responses
3. Click "Save"

### Step 13: Try Memory Features (2 Minutes)

#### Add a Memory
1. Click "Memory" in the sidebar
2. Click "Add Memory"
3. Type something you want the AI to remember:
   - "My name is [Your Name]"
   - "I work as a [Your Job]"
   - "I'm learning to code"
4. Click "Save"

#### Search Memories
1. In the Memory section
2. Type a search term in the search box
3. Click "Search"
4. The AI will find related memories

#### Memory Categories
Memories are organized by:
- **Conversations**: Chat history
- **Knowledge**: Learned information
- **Personal**: Personal information
- **Tasks**: Task-related memories

---

## Common First-Time Tasks

### Task 1: Get Help Writing an Email

1. Click "Chat"
2. Type: "Help me write a professional email to my boss asking for a meeting"
3. The AI will draft an email for you
4. You can ask for revisions: "Make it more formal" or "Add a deadline"

### Task 2: Get Help with Coding

1. Click "Chat"
2. Type: "Write a Python function that calculates the factorial of a number"
3. The AI will write the code for you
4. Ask for explanations: "Explain how this code works"

### Task 3: Research a Topic

1. Click "Chat"
2. Type: "Explain quantum computing in simple terms"
3. The AI will provide a clear explanation
4. Ask follow-up questions to learn more

### Task 4: Get Creative Help

1. Click "Chat"
2. Type: "Write a short poem about artificial intelligence"
3. The AI will create original content
4. Ask for different styles: "Make it funny" or "Make it in haiku format"

---

## Understanding the AI Models

### Which Model Should You Use?

#### Llama2 (Best for Beginners)
- **Good for**: General questions, writing, research
- **Performance**: Balanced speed and quality
- **Resource Use**: Medium
- **When to use**: Default choice for most tasks

#### Mistral (Best for Performance)
- **Good for**: Faster responses, higher quality
- **Performance**: Higher quality than Llama2
- **Resource Use**: Medium
- **When to use**: When you want better quality

#### Neural Chat (Best for Conversations)
- **Good for**: Dialogue, chat, questions
- **Performance**: Optimized for conversation
- **Resource Use**: Medium
- **When to use**: When having conversations

#### Phi (Best for Older Computers)
- **Good for**: Basic tasks on limited hardware
- **Performance**: Faster but simpler
- **Resource Use**: Low
- **When to use**: On older computers or for quick answers

#### Code Llama (Best for Programming)
- **Good for**: Writing and explaining code
- **Performance**: Optimized for code
- **Resource Use**: Medium
- **When to use**: When working with code

---

## Tips for Better Results

### Be Specific
- **Bad**: "Help me"
- **Good**: "Help me write a cover letter for a marketing job"

### Provide Context
- **Bad**: "Fix this code"
- **Good**: "This Python code is supposed to calculate a factorial but it's giving an error. Here's the code: [paste code]"

### Ask for Clarification
- If the AI doesn't understand, it will ask questions
- Answer them to get better results

### Iterate
- First response might not be perfect
- Ask for revisions: "Make it shorter" or "Explain it differently"

### Use Memory
- Tell the AI important things about you
- It will remember and use that information

---

## Stopping Synthos-OS

### When You're Done

#### Stop Services (Windows)
1. In the Command Prompt window, type: `scripts\deploy.bat stop`
2. Wait for services to stop
3. You can close the Command Prompt window

#### Stop Services (Mac/Linux)
1. In the Terminal window, type: `./scripts/deploy.sh stop`
2. Wait for services to stop
3. You can close the Terminal window

### Start Again Later

#### Quick Start (Windows)
1. Open Command Prompt
2. Type: `cd Desktop\Synthos-OS`
3. Type: `scripts\deploy.bat dev`
4. Open browser to: http://localhost:3000

#### Quick Start (Mac/Linux)
1. Open Terminal
2. Type: `cd Desktop/Synthos-OS`
3. Type: `./scripts/deploy.sh dev`
4. Open browser to: http://localhost:3000

**Note:** Models stay downloaded, so you don't need to pull them again.

---

## Next Steps

### Advanced Features to Try

#### Enable Voice Input
1. Go to Settings → Voice
2. Enable "Voice Input"
3. Grant microphone permission
4. Click the microphone icon to speak instead of type

#### Use Tools
1. Click "Tools" in the sidebar
2. Try "Web Search" to look up information
3. Try "File Operations" to read and write files
4. Try "Code Execution" to run code snippets

#### Explore RSI (Self-Improvement)
1. Click "RSI" in the sidebar
2. See how Synthos-OS improves itself
3. View "Cognitive DNA" to see learned patterns
4. Enable "Autonomous Mode" for continuous improvement

### Install on Other Devices

#### Mobile App
1. Follow the [Mobile Installation Guide](mobile-installation.md)
2. Install on your Android or iPhone
3. Connect to your Synthos-OS backend
4. Use Synthos-OS anywhere

#### Quest 3 App
1. Follow the [Quest 3 Installation Guide](quest3-installation.md)
2. Install on your Meta Quest 3
3. Enable system-wide integration
4. Replace Meta AI with Synthos-OS

### Customize Your Experience

#### Create Presets
1. Configure settings for different tasks
2. Save as presets (e.g., "Coding", "Writing", "Research")
3. Switch between presets easily

#### Customize System Prompt
1. Go to Settings → Advanced
2. Edit the system prompt
3. Make the AI behave how you want it to

---

## Common Questions

### Is my data private?
Yes! Synthos-OS runs locally on your computer. Your data doesn't leave your computer unless you enable cloud features.

### Does it need internet?
Only for initial setup and model downloads. After that, it works offline (except for web search features).

### Can I use it for free?
Yes! Synthos-OS is open-source and free to use. You only need your own computer.

### How much does it cost?
Nothing! It's completely free. You just need your own hardware.

### Can I use it for work?
Yes! It's great for productivity, coding, writing, and research.

### Is it safe?
Yes! It runs locally with your control. No data is sent to external servers by default.

### What if it makes mistakes?
AI can make mistakes. Always verify important information, especially for code, medical, or legal advice.

### Can I turn it off?
Yes! Just stop the services when you're done. It doesn't run in the background unless you configure it to.

---

## Troubleshooting Common Issues

### "Services won't start"
- Make sure Docker Desktop is running
- Check your internet connection
- Try restarting Docker Desktop

### "AI is slow to respond"
- Try a lighter model (Phi)
- Close other applications
- Check your computer's performance

### "Can't connect to backend"
- Make sure services are running
- Check you're on the right URL (http://localhost:3000)
- Restart the services

### "Models won't download"
- Check your internet connection
- Make sure Docker has enough disk space
- Try pulling models one at a time

### "Web UI won't load"
- Check services are running
- Try a different browser
- Clear browser cache

---

## Where to Get Help

### Documentation
- [Pre-Activation Setup Guide](pre-activation-setup.md) - Detailed setup instructions
- [Desktop Installation Guide](desktop-installation.md) - Desktop-specific help
- [Web UI Installation Guide](web-ui-installation.md) - Web interface help
- [Mobile Installation Guide](mobile-installation.md) - Mobile app help
- [Quest 3 Installation Guide](quest3-installation.md) - VR/AR help
- [Settings Guide](../configuration/settings-guide.md) - Configuration help

### Community
- [GitHub Issues](https://github.com/fuzzynetwork1989-alt/Synthos-OS/issues) - Report bugs
- [GitHub Discussions](https://github.com/fuzzynetwork1989-alt/Synthos-OS/discussions) - Ask questions

### Quick Help Commands
```bash
# Check service status
scripts\deploy.bat status  # Windows
./scripts/deploy.sh status  # Mac/Linux

# View logs
scripts\deploy.bat logs  # Windows
./scripts/deploy.sh logs  # Mac/Linux

# Restart services
scripts\deploy.bat restart  # Windows
./scripts/deploy.sh restart  # Mac/Linux
```

---

## Cheat Sheet

### Essential Commands (Windows)
```batch
# Start Synthos-OS
cd Desktop\Synthos-OS
scripts\deploy.bat dev

# Stop Synthos-OS
scripts\deploy.bat stop

# Check status
scripts\deploy.bat status

# View logs
scripts\deploy.bat logs
```

### Essential Commands (Mac/Linux)
```bash
# Start Synthos-OS
cd Desktop/Synthos-OS
./scripts/deploy.sh dev

# Stop Synthos-OS
./scripts/deploy.sh stop

# Check status
./scripts/deploy.sh status

# View logs
./scripts/deploy.sh logs
```

### Important URLs
- **Web Interface**: http://localhost:3000
- **API Gateway**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

### Default Login
- **Username**: admin
- **Password**: admin
- **Change this in Settings!**

---

## What to Remember

### Key Points
- ✅ Synthos-OS runs locally (private and secure)
- ✅ It's free and open-source
- ✅ Works on Desktop, Web, Mobile, and Quest 3
- ✅ Can self-improve over time
- ✅ Replaces Meta AI on Quest 3

### Before You Start
- ✅ Install Git, Docker, and Python
- ✅ Download Synthos-OS
- ✅ Run setup script
- ✅ Start services
- ✅ Download models

### While Using
- ✅ Keep the services running in a terminal window
- ✅ Use the web interface at http://localhost:3000
- ✅ Try different models for different tasks
- ✅ Use memory to help the AI remember important things
- ✅ Explore settings to customize your experience

### When You're Done
- ✅ Stop services with `scripts\deploy.bat stop`
- ✅ Close the terminal window
- ✅ Models stay downloaded for next time

---

## You're Ready!

Congratulations! You now have Synthos-OS installed and running. You can:

- ✅ Have conversations with an AI
- ✅ Get help with writing and coding
- ✅ Research topics
- ✅ Remember important information
- ✅ Use tools for web search and file operations
- ✅ Watch it improve itself over time

### What to Do Next
1. **Explore**: Try different features and ask the AI anything
2. **Customize**: Adjust settings to your preferences
3. **Install Mobile**: Get it on your phone
4. **Install Quest 3**: Experience VR/AR AI
5. **Learn More**: Read the detailed documentation

### Have Fun!
Synthos-OS is a powerful AI system. Experiment with it, learn what it can do, and make it your own personal AI assistant!

---

**Need more help?** Check the detailed guides in the `docs/` directory or visit the GitHub repository for support.

---

*Last updated: 2024*
*Version: 1.0*