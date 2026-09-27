# Synthos-OS Settings and Configuration Guide
## Complete Guide to Customizing Your AI Experience

## Overview
This guide covers all settings and configuration options available in Synthos-OS across all platforms (Desktop, Web UI, Mobile, and Quest 3). Learn how to customize the AI models, configure system behavior, and make Synthos-OS truly your own.

## Table of Contents
1. [Settings Overview](#settings-overview)
2. [General Settings](#general-settings)
3. [Model Configuration](#model-configuration)
4. [Advanced Model Settings](#advanced-model-settings)
5. [Platform-Specific Settings](#platform-specific-settings)
6. [System Integration Settings](#system-integration-settings)
7. [RSI and Autonomy Settings](#rsi-and-autonomy-settings)
8. [Memory and Knowledge Settings](#memory-and-knowledge-settings)
9. [Security and Privacy Settings](#security-and-privacy-settings)
10. [Configuration Files](#configuration-files)

---

## Settings Overview

### Settings Structure
Synthos-OS has a hierarchical settings structure:

- **General Settings**: Basic configuration
- **Model Settings**: AI model selection and basic parameters
- **Advanced Settings**: Deep customization and expert options
- **Platform Settings**: Device-specific configuration
- **System Settings**: Backend and integration settings

### Accessing Settings

#### Desktop/Web UI
1. Click on "Settings" (gear icon)
2. Navigate through sidebar categories

#### Mobile
1. Tap menu button (≡)
2. Tap "Settings"
3. Navigate through categories

#### Quest 3
1. Open Synthos-OS menu
2. Tap "Settings"
3. Navigate through categories or use voice commands

---

## General Settings

### Interface Settings

#### Theme Selection
Choose your preferred visual appearance:

**Options:**
- **Light**: Light theme for bright environments
- **Dark**: Dark theme for low-light environments
- **Auto**: Automatically switches based on system theme

**Recommended:** Dark for extended use, reduces eye strain

#### Language
Set the interface language:

**Supported Languages:**
- English (US, UK, International)
- Spanish
- French
- German
- Chinese (Simplified, Traditional)
- Japanese
- Korean
- Portuguese (Brazilian, European)
- Russian
- And more...

**Note:** AI responses will be in the selected language when supported by the model.

#### Response Display
Configure how AI responses appear:

**Settings:**
- **Streaming**: Show responses as they're generated (real-time)
- **Complete**: Wait for full response before displaying
- **Typewriter Effect**: Show character-by-character typing effect
- **Response Length**: Maximum characters per response

**Recommended:** Streaming for better user experience

### Performance Settings

#### Resource Allocation
Configure system resource usage:

**Conservative Mode:**
- CPU: 1-2 cores
- Memory: 2-4GB
- Best for: Older computers, battery saving

**Balanced Mode:**
- CPU: 2-4 cores
- Memory: 4-8GB
- Best for: Most users, good balance

**Aggressive Mode:**
- CPU: 4-8 cores
- Memory: 8-16GB
- Best for: Powerful systems, maximum performance

#### Response Timeout
Set maximum time for AI responses:

**Settings:**
- **Short**: 30 seconds
- **Medium**: 60 seconds (default)
- **Long**: 120 seconds
- **Unlimited**: No timeout (not recommended)

**Recommended:** Medium for most tasks

### Notification Settings

#### Alert Configuration
Configure system notifications:

**Notification Types:**
- **Completion Alerts**: Notify when tasks complete
- **Error Alerts**: Notify when errors occur
- **Update Alerts**: Notify about system updates
- **RSI Alerts**: Notify about self-improvement activities

**Delivery Methods:**
- **In-App**: Show within Synthos-OS interface
- **System**: Use OS notification system
- **Sound**: Play notification sounds
- **None**: Disable notifications

---

## Model Configuration

### Model Selection

#### Primary Model
Choose your main AI model:

**Available Models:**

| Model | Size | Strengths | Best For | Resource Usage |
|-------|------|----------|----------|-----------------|
| **Llama2 7B** | 7B | Good all-around | General use | Medium |
| **Llama2 13B** | 13B | Better reasoning | Complex tasks | High |
| **Mistral 7B** | 7B | High performance | Speed + quality | Medium |
| **Neural Chat** | 7B | Conversational | Chat, dialogue | Medium |
| **Phi-3** | 3B | Lightweight | Low-end devices | Low |
| **Code Llama** | 7B | Code generation | Programming | Medium |
| **Custom Models** | Variable | Custom | Specialized | Variable |

**Selection Criteria:**
- **System RAM**: Choose model based on available memory
- **Use Case**: Different models excel at different tasks
- **Performance vs Quality**: Larger models generally better but slower
- **Hardware**: GPU acceleration allows larger models

#### Fallback Models
Configure backup models if primary fails:

**Configuration:**
1. **Primary Model**: First choice
2. **Fallback 1**: Second choice if primary fails
3. **Fallback 2**: Third choice if both fail
4. **Automatic Fallback**: Enable automatic switching

**Recommended:** Llama2 → Mistral → Phi

### Basic Model Parameters

#### Temperature
Controls randomness/creativity of responses:

**Scale:** 0.0 to 1.0

**Values:**
- **0.0 - 0.3**: Very focused, deterministic responses
- **0.4 - 0.7**: Balanced creativity and focus (recommended)
- **0.8 - 1.0**: Very creative, random responses

**Use Cases:**
- **Coding/Factual**: Lower temperature (0.1 - 0.3)
- **Creative Writing**: Higher temperature (0.7 - 0.9)
- **Conversation**: Medium temperature (0.5 - 0.7)

#### Max Tokens
Maximum length of AI responses:

**Scale:** 1 to 4096 tokens

**Values:**
- **128**: Very short responses
- **512**: Short responses (default)
- **1024**: Medium responses
- **2048**: Long responses
- **4096**: Maximum responses

**Note:** 1 token ≈ 4 characters in English

#### Top P (Nucleus Sampling)
Controls response diversity:

**Scale:** 0.0 to 1.0

**Values:**
- **0.0**: Always choose most likely token (deterministic)
- **0.9**: Sample from top 90% of likely tokens
- **1.0**: Sample from all tokens (very random)

**Recommended:** 0.9 for most use cases

#### Top K
Limits next token choices to top K options:

**Scale:** 1 to 100

**Values:**
- **1**: Always choose most likely token
- **10**: Choose from top 10 options
- **50**: Choose from top 50 options (recommended)
- **100**: Choose from top 100 options

**Recommended:** 40-50 for good balance

---

## Advanced Model Settings

### Expert Configuration

#### Repeat Penalty
Prevent the model from repeating itself:

**Scale:** 0.0 to 2.0

**Values:**
- **0.0**: No penalty
- **1.0**: Moderate penalty (recommended)
- **2.0**: Strong penalty

**Use Case:** Set to 1.0 - 1.2 for conversation to prevent loops

#### Presence Penalty
Encourage variety in responses:

**Scale:** -2.0 to 2.0

**Values:**
- **-2.0**: Encourage repetition
- **0.0**: No effect
- **0.5**: Encourage variety (recommended)
- **2.0**: Strong variety

**Use Case:** Set to 0.3 - 0.5 for more diverse responses

#### Frequency Penalty
Prevent word repetition:

**Scale:** 0.0 to 2.0

**Values:**
- **0.0**: No penalty
- **0.5**: Moderate penalty (recommended)
- **1.0**: Strong penalty

**Use Case:** Set to 0.5 - 0.7 for natural conversation

### Context Configuration

#### Context Window
Amount of previous conversation the model considers:

**Settings:**
- **Short**: 2048 tokens (≈ 8192 characters)
- **Medium**: 4096 tokens (≈ 16384 characters) - default
- **Long**: 8192 tokens (≈ 32768 characters)
- **Full**: 16384 tokens (≈ 65536 characters)

**Trade-offs:**
- **Short**: Faster, less memory, less context
- **Long**: Slower, more memory, more context

#### System Prompt
Customize the AI's personality and behavior:

**System Prompt Template:**
```
You are Synthos-OS, an advanced AI assistant. You are helpful, accurate, and safe. You provide clear, concise responses and ask clarifying questions when needed. You can help with a wide range of tasks including coding, writing, analysis, and problem-solving.
```

**Customization Examples:**
- **Formal**: "You are a professional, formal assistant..."
- **Casual**: "You are a friendly, casual assistant..."
- **Technical**: "You are a technical expert who provides detailed explanations..."
- **Creative**: "You are a creative assistant who thinks outside the box..."

#### User Identity
Tell the AI about you for personalized responses:

**Identity Settings:**
- **Name**: Your preferred name
- **Background**: Your profession or interests
- **Communication Style**: Preferred interaction style
- **Knowledge Areas**: Topics you're knowledgeable about
- **Learning Style**: How you prefer to learn

### Specialized Configurations

#### Coding Assistant Mode
Optimize for programming tasks:

**Settings:**
- **Temperature**: 0.1 - 0.3 (more deterministic)
- **Max Tokens**: 1024 - 2048 (longer for code)
- **System Prompt**: Focus on code accuracy and best practices
- **Model**: Code Llama or Mistral

#### Creative Writing Mode
Optimize for creative tasks:

**Settings:**
- **Temperature**: 0.7 - 0.9 (more creative)
- **Top P**: 0.95 (more diverse)
- **System Prompt**: Encourage creativity and originality
- **Model**: Llama2 or Mistral

#### Research Mode
Optimize for research and analysis:

**Settings:**
- **Temperature**: 0.3 - 0.5 (balanced)
- **Max Tokens**: 2048 - 4096 (detailed responses)
- **System Prompt**: Focus on accuracy and citations
- **Model**: Mistral or Llama2 13B

#### Conversation Mode
Optimize for dialogue:

**Settings:**
- **Temperature**: 0.5 - 0.7 (natural conversation)
- **Repeat Penalty**: 1.0 - 1.2 (prevent loops)
- **Max Tokens**: 512 - 1024 (natural length)
- **System Prompt**: Focus on natural dialogue
- **Model**: Neural Chat

---

## Platform-Specific Settings

### Desktop Settings

#### Window Behavior
Configure how the desktop app behaves:

**Settings:**
- **Start on Login**: Auto-start with computer
- **Minimize to Tray**: Minimize to system tray instead of taskbar
- **Always on Top**: Keep window visible
- **Multi-Monitor**: Configure display behavior

#### Keyboard Shortcuts
Customize keyboard shortcuts:

**Common Shortcuts:**
- **Ctrl + Enter**: Send message
- **Ctrl + N**: New conversation
- **Ctrl + /**: Focus search
- **Escape**: Stop generation
- **Ctrl + ,**: Open settings

**Customization:**
- Remap any shortcut to your preference
- Create custom shortcuts for common actions

#### Accessibility
Configure for accessibility:

**Settings:**
- **Font Size**: Increase/decrease text size
- **High Contrast**: Enable high contrast mode
- **Screen Reader**: Enable screen reader support
- **Voice Control**: Enable voice commands

### Web UI Settings

#### Browser Configuration
Web UI specific settings:

**Settings:**
- **Auto-Refresh**: Auto-refresh connection status
- **Notifications**: Browser notification preferences
- **PWA**: Install as desktop app (Progressive Web App)
- **Offline Mode**: Configure offline behavior

#### Layout Options
Customize web interface layout:

**Settings:**
- **Sidebar Position**: Left or right
- **Chat Layout**: Bubbles or inline
- **Panel Size**: Adjustable panel widths
- **Theme**: Light, dark, or auto

### Mobile Settings

#### Touch Interface
Configure touch interactions:

**Settings:**
- **Haptic Feedback**: Vibration on actions
- **Swipe Gestures**: Enable/disable swipe gestures
- **Long Press**: Configure long press actions
- **Keyboard**: Show/hide on-screen keyboard

#### Background Behavior
Configure background operation:

**Settings:**
- **Run in Background**: Allow AI to work when app is backgrounded
- **Notifications**: Configure background notifications
- **Battery Optimization**: Enable/disable battery optimization
- **Sync**: Configure background sync behavior

#### Orientation
Configure screen orientation:

**Settings:**
- **Auto-Rotate**: Allow automatic rotation
- **Portrait Lock**: Lock to portrait mode
- **Landscape Lock**: Lock to landscape mode
- **Sensor-Based**: Use sensor for rotation

### Quest 3 Settings

#### Spatial Interface
Configure VR/AR specific settings:

**Settings:**
- **AI Distance**: How far AI appears (1-10 meters)
- **AI Size**: Size of AI avatar (0.5x - 2x)
- **AI Placement**: Front, follow-gaze, or fixed position
- **Transparency**: How transparent the AI appears

#### Hand Tracking
Configure hand interaction:

**Settings:**
- **Gesture Sensitivity**: Sensitivity of gesture recognition
- **Hand Model**: Left hand, right hand, or both
- **Calibration**: Recalibrate hand tracking
- **Zone Sensitivity**: Set gesture detection zones

#### Passthrough Settings
Configure real-world integration:

**Settings:**
- **Passthrough Quality**: Balance quality and performance
- **AI Overlays**: Configure AI in real-world view
- **Depth Perception**: Enable/disable depth effects
- **Occlusion**: Real objects block AI

---

## System Integration Settings

### Backend Connection

#### Local Backend Configuration
Connect to Synthos-OS running on your local network:

**Settings:**
- **Backend Type**: Local
- **IP Address**: Your computer's IP address
- **Port**: 8000 (API Gateway)
- **Connection Timeout**: 30 seconds

**Find Your IP:**
- **Windows**: `ipconfig | findstr IPv4`
- **Mac**: `ifconfig | grep inet`
- **Linux**: `ip addr show`

#### Cloud Backend Configuration
Connect to cloud-hosted Synthos-OS:

**Settings:**
- **Backend Type**: Cloud
- **Cloud URL**: https://your-cloud-instance.com
- **API Key**: Your authentication key
- **Region**: Cloud region (if applicable)

#### Hybrid Mode
Use both local and cloud backends:

**Configuration:**
- **Primary Backend**: Local (for speed)
- **Secondary Backend**: Cloud (for advanced features)
- **Fallback Strategy**: When to use cloud
- **Data Routing**: Which features use which backend

### Service Configuration

#### API Gateway
Configure main API entry point:

**Settings:**
- **URL**: http://localhost:8000 (default)
- **Timeout**: 60 seconds
- **Retry Policy**: Number of retries on failure
- **Health Check**: Interval for health checks

#### Model Gateway
Configure AI model routing:

**Settings:**
- **URL**: http://localhost:8002 (default)
- **Default Provider**: ollama (or custom)
- **Model Fallback**: Fallback model configuration
- **Streaming**: Enable/disable response streaming

#### Memory Engine
Configure memory and knowledge storage:

**Settings:**
- **URL**: http://localhost:8003 (default)
- **Storage Limit**: Maximum memory entries
- **Retention Policy**: How long to keep memories
- **Indexing**: Configure search indexing

---

## RSI and Autonomy Settings

### Recursive Self-Improvement

#### RSI Configuration
Configure self-improvement behavior:

**Settings:**
- **Enable RSI**: Enable/disable recursive self-improvement
- **Strategy**: Improvement strategy (conservative, balanced, aggressive, adaptive)
- **Cycle Frequency**: How often to run improvement cycles
- **Resource Budget**: Maximum resources per cycle

#### Cognitive DNA
Configure the evolutionary improvement system:

**Settings:**
- **Gene Pool Size**: Maximum number of improvement genes
- **Evolution Interval**: How often to evolve genes
- **Learning Rate**: How quickly to adapt strategies
- **Exploration Rate**: How often to try new approaches

### Autonomous Mode

#### Continuous Operation
Configure autonomous improvement cycles:

**Settings:**
- **Enable Autonomous Mode**: Enable/disable self-triggering cycles
- **Trigger Conditions**: When to auto-trigger improvements
- **Auto-Approve**: Approve low-risk changes automatically
- **Emergency Stop**: Enable emergency stop capability

#### Safety Overrides
Configure safety constraints for autonomous mode:

**Settings:**
- **Safety Override Key**: Key for enhanced autonomy
- **Auto-Approve Threshold**: Risk level for auto-approval
- **Emergency Stop**: Configure emergency stop behavior
- **Human Oversight**: Configure human intervention requirements

---

## Memory and Knowledge Settings

### Memory Configuration

#### Storage Management
Configure how memories are stored:

**Settings:**
- **Storage Type**: Local only or cloud sync
- **Storage Limit**: Maximum memory entries
- **Retention Policy**: How long to keep memories
- **Compression**: Enable/disable memory compression

#### Memory Categories
Organize memories by category:

**Default Categories:**
- **Conversations**: Chat history
- **Knowledge**: Learned information
- **Tasks**: Task-related memories
- **Personal**: Personal information
- **Custom**: User-defined categories

#### Search Configuration
Configure memory search behavior:

**Settings:**
- **Search Method**: Keyword or vector search
- **Relevance Threshold**: Minimum relevance score
- **Max Results**: Maximum search results
- **Search Scope**: Which memory types to search

### Knowledge Base

#### External Knowledge
Configure external knowledge sources:

**Settings:**
- **Web Search**: Enable/disable web search capabilities
- **Knowledge Graph**: Enable knowledge graph integration
- **Document Access**: Configure document library access
- **API Integration**: Configure external API access

#### Learning Configuration
Configure how Synthos-OS learns:

**Settings:**
- **Learning Rate**: How quickly to adapt to your preferences
- **Forgetting Rate**: How quickly to forget unused information
- **Context Window**: How much context to consider
- **Update Frequency**: How often to update learned preferences

---

## Security and Privacy Settings

### Privacy Controls

#### Data Collection
Configure what data is collected:

**Settings:**
- **Usage Analytics**: Enable/disable usage analytics
- **Crash Reports**: Enable/disable crash reporting
- **Performance Data**: Enable/disable performance monitoring
- **Telemetry**: Enable/disable anonymous telemetry

#### Local vs Cloud
Configure data processing location:

**Settings:**
- **Local Processing**: Process all data locally (recommended)
- **Cloud Processing**: Use cloud for heavy processing
- **Hybrid**: Mix of local and cloud
- **Data Storage**: Where to store data

### Security Settings

#### Authentication
Configure access control:

**Settings:**
- **Local Auth**: Enable/disable local authentication
- **Password Policy**: Password requirements
- **Session Timeout**: Automatic logout timeout
- **Two-Factor**: Enable two-factor authentication

#### Access Control
Configure feature access:

**Settings:**
- **Tool Access**: Which tools can be used
- **File Access**: Which directories can be accessed
- **Network Access**: Which network operations are allowed
- **System Access**: Which system operations are allowed

---

## Configuration Files

### Environment Variables (.env)

#### Location
- **Desktop**: Root directory of Synthos-OS
- **Web UI**: `apps/operator-console/.env`
- **Mobile**: `apps/mobile-client/.env`
- **Quest 3**: `apps/quest-3-app/.env`

#### Common Variables
```bash
# Backend Configuration
API_GATEWAY_URL=http://localhost:8000
MODEL_GATEWAY_URL=http://localhost:8002
MEMORY_ENGINE_URL=http://localhost:8003
RSI_ENGINE_URL=http://localhost:8004

# Model Configuration
DEFAULT_MODEL=llama2
FALLBACK_MODELS=mistral,neural-chat
TEMPERATURE=0.7
MAX_TOKENS=512

# Resource Configuration
CPU_CORES=4
MEMORY_GB=8
ENABLE_GPU=false

# Feature Flags
ENABLE_VOICE=true
ENABLE_VISION=true
ENABLE_TOOLS=true
ENABLE_RSI=true
```

### Service Configuration Files

#### API Gateway
Location: `services/api-gateway/synthos_api_gateway/config.py`

#### Model Gateway
Location: `services/model-gateway/synthos_model_gateway/config.py`

#### Memory Engine
Location: `services/memory-engine/synthos_memory_engine/config.py`

#### RSI Engine
Location: `services/rsi-engine/synthos_rsi_engine/config.py`

### Docker Configuration

#### Docker Compose
Location: `docker-compose.yml`

Configure services, ports, volumes, and environment variables.

#### Kubernetes
Location: `infra/kubernetes/`

Configure deployments, services, and ingress for production.

---

## Reset to Defaults

### Reset Individual Settings

#### Reset Model Settings
1. Go to Settings → Model
2. Click "Reset to Defaults"
3. Confirm reset

#### Reset All Settings
1. Go to Settings → Advanced
2. Click "Factory Reset"
3. Confirm reset (this will reset ALL settings)

### Reset Configuration Files

#### Reset .env File
1. Delete `.env` file
2. Copy from `.env.example`
3. Restart services

#### Reset Service Config
1. Delete or rename service config file
2. Restart service (it will use defaults)

---

## Export/Import Settings

### Export Settings

#### Export All Settings
1. Go to Settings → Advanced
2. Click "Export Settings"
3. Choose file location
4. Save settings as JSON file

#### Export Specific Category
1. Go to Settings → [Category]
2. Click "Export [Category]"
3. Save settings as JSON file

### Import Settings

#### Import Settings
1. Go to Settings → Advanced
2. Click "Import Settings"
3. Select settings JSON file
4. Confirm import

#### Merge Settings
1. During import, choose "Merge" instead of "Replace"
2. Conflicting settings will keep current values
3. New settings will be added

---

## Presets

### Pre-Configured Presets

#### Productivity Preset
Optimized for work and productivity:
- **Model**: Mistral 7B
- **Temperature**: 0.3
- **Max Tokens**: 1024
- **System Prompt**: Professional and efficient

#### Creative Preset
Optimized for creative tasks:
- **Model**: Llama2 7B
- **Temperature**: 0.8
- **Max Tokens**: 2048
- **System Prompt**: Creative and imaginative

#### Coding Preset
Optimized for programming:
- **Model**: Code Llama
- **Temperature**: 0.1
- **Max Tokens**: 2048
- **System Prompt**: Technical and precise

#### Conversation Preset
Optimized for dialogue:
- **Model**: Neural Chat
- **Temperature**: 0.6
- **Max Tokens**: 512
- **System Prompt**: Friendly and conversational

### Custom Presets

#### Create Custom Preset
1. Configure your ideal settings
2. Go to Settings → Presets
3. Click "Save as Preset"
4. Name your preset
5. Save preset

#### Manage Presets
- Edit existing presets
- Delete unused presets
- Share presets (export as JSON)
- Import presets from others

---

## Quick Reference

### Common Model Configurations

**Conservative (Safe, Deterministic):**
```
Temperature: 0.1 - 0.3
Top P: 0.8
Top K: 20
Repeat Penalty: 1.2
Max Tokens: 512
```

**Balanced (Recommended):**
```
Temperature: 0.5 - 0.7
Top P: 0.9
Top K: 50
Repeat Penalty: 1.0
Max Tokens: 1024
```

**Creative (Diverse, Imaginative):**
```
Temperature: 0.8 - 1.0
Top P: 0.95
Top K: 80
Repeat Penalty: 0.5
Max Tokens: 2048
```

### Important Settings Locations

**Desktop:**
- Settings UI: Gear icon in app
- Config file: `.env` in root directory
- Logs: `logs/` directory

**Web UI:**
- Settings UI: Gear icon in web interface
- Config file: `apps/operator-console/.env`
- Browser: LocalStorage

**Mobile:**
- Settings UI: Menu button → Settings
- Config file: `apps/mobile-client/.env`
- App storage: Device storage

**Quest 3:**
- Settings UI: Menu → Settings
- Config file: `apps/quest-3-app/.env`
- App storage: Quest 3 storage

---

## Support

If you need help with settings:

1. Check this guide for your specific issue
2. Try resetting to defaults if settings seem corrupted
3. Export your settings before major changes
4. Consult platform-specific troubleshooting guides
5. Check GitHub Issues for known issues

---

## Next Steps

After configuring your settings:

1. **Test Your Configuration**: Try different tasks to ensure settings work
2. **Create Presets**: Save configurations for different use cases
3. **Monitor Performance**: Adjust settings if performance is poor
4. **Experiment**: Try different settings to find your ideal configuration
5. **Stay Updated**: Keep settings updated with new features

---

Congratulations! You now have complete control over your Synthos-OS configuration. Customize it to be truly your own AI assistant!