<script lang="ts">
  import { onMount } from 'svelte';
  import { invoke } from '@tauri-apps/api/tauri';
  import { open } from '@tauri-apps/api/shell';
  import { apiService } from './services/api';
  import { modelGatewayService } from './services/modelGateway';
  import { authService } from './services/auth';

  let systemStatus = {
    localModel: false,
    memoryEngine: false,
    toolGateway: false,
    cpuUsage: 0,
    memoryUsage: 0
  };

  let currentView = 'home';
  let sidebarOpen = true;
  let isAuthenticated = false;
  let currentUser = null;
  let availableModels = [];
  let preferredModel = null;

  const views = ['home', 'chat', 'memory', 'tools', 'settings'];

  onMount(async () => {
    try {
      // Initialize auth
      await authService.initialize();
      isAuthenticated = authService.isAuthenticated();
      currentUser = authService.getCurrentUser();

      // Try to get system status from Tauri backend
      try {
        const status = await invoke('get_system_status');
        systemStatus = status as typeof systemStatus;
      } catch (error) {
        console.error('Failed to get system status from Tauri:', error);
        // Fallback to web-based status checking
        await checkWebStatus();
      }

      // Load model information
      availableModels = await modelGatewayService.getAvailableModels();
      preferredModel = modelGatewayService.getPreferredModel();
    } catch (error) {
      console.error('Initialization failed:', error);
    }
  });

  async function checkWebStatus() {
    try {
      const modelHealthy = await modelGatewayService.checkLocalModelHealth();
      systemStatus.localModel = modelHealthy;
      systemStatus.memoryEngine = true; // Assume memory engine is available
      systemStatus.toolGateway = true; // Assume tool gateway is available
    } catch (error) {
      console.error('Web status check failed:', error);
    }
  }

  function getStatusColor(status: boolean) {
    return status ? '#4CAF50' : '#F44336';
  }

  async function handleLogout() {
    await authService.logout();
    isAuthenticated = false;
    currentUser = null;
    currentView = 'home';
  }
</script>

<div class="app-container">
  {#if sidebarOpen}
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1>Synthos OS</h1>
        <p class="subtitle">Desktop Shell</p>
      </div>

      <nav class="sidebar-nav">
        {#each views as view}
          <button 
            class="nav-item" 
            class:active={currentView === view}
            on:click={() => currentView = view}
          >
            {view.charAt(0).toUpperCase() + view.slice(1)}
          </button>
        {/each}
      </nav>

      <div class="sidebar-footer">
        {#if isAuthenticated && currentUser}
          <div class="user-info">
            <div class="user-avatar">
              {currentUser.name ? currentUser.name.charAt(0).toUpperCase() : currentUser.email.charAt(0).toUpperCase()}
            </div>
            <div class="user-details">
              <span class="user-name">{currentUser.name || 'User'}</span>
              <span class="user-email">{currentUser.email}</span>
            </div>
          </div>
        {/if}
        <div class="status-indicator">
          <div class="status-dot" style="background-color: {getStatusColor(systemStatus.localModel)}"></div>
          <span>Local Model</span>
        </div>
        <div class="status-indicator">
          <div class="status-dot" style="background-color: {getStatusColor(systemStatus.memoryEngine)}"></div>
          <span>Memory Engine</span>
        </div>
        {#if isAuthenticated}
          <button class="logout-button" on:click={handleLogout}>Logout</button>
        {/if}
      </div>
    </aside>
  {/if}

  <main class="main-content">
    <header class="top-bar">
      <button class="toggle-sidebar" on:click={() => sidebarOpen = !sidebarOpen}>
        {sidebarOpen ? '◀' : '▶'}
      </button>
      <h2>{currentView.charAt(0).toUpperCase() + currentView.slice(1)}</h2>
      <div class="resource-usage">
        <span>CPU: {systemStatus.cpuUsage}%</span>
        <span>Memory: {systemStatus.memoryUsage}%</span>
      </div>
    </header>

    <div class="content-area">
      {#if currentView === 'home'}
        <div class="home-view">
          <div class="welcome-section">
            <h3>Welcome to Synthos OS</h3>
            <p>Next-Generation AI Operating System</p>
          </div>

          <div class="quick-actions">
            <div class="action-card" on:click={() => currentView = 'chat'}>
              <h4>Start Chat</h4>
              <p>Begin a conversation with your AI assistant</p>
            </div>
            <div class="action-card" on:click={() => currentView = 'memory'}>
              <h4>Memory</h4>
              <p>View and manage your stored memories</p>
            </div>
            <div class="action-card" on:click={() => currentView = 'tools'}>
              <h4>Tools</h4>
              <p>Access available tools and capabilities</p>
            </div>
            <div class="action-card" on:click={() => currentView = 'settings'}>
              <h4>Settings</h4>
              <p>Configure your Synthos OS experience</p>
            </div>
          </div>

          <div class="system-status">
            <h4>System Status</h4>
            <div class="status-grid">
              <div class="status-item">
                <span class="status-label">Local Model</span>
                <span class="status-value" style="color: {getStatusColor(systemStatus.localModel)}">
                  {systemStatus.localModel ? 'Online' : 'Offline'}
                </span>
              </div>
              <div class="status-item">
                <span class="status-label">Memory Engine</span>
                <span class="status-value" style="color: {getStatusColor(systemStatus.memoryEngine)}">
                  {systemStatus.memoryEngine ? 'Active' : 'Inactive'}
                </span>
              </div>
              <div class="status-item">
                <span class="status-label">Tool Gateway</span>
                <span class="status-value" style="color: {getStatusColor(systemStatus.toolGateway)}">
                  {systemStatus.toolGateway ? 'Ready' : 'Unavailable'}
                </span>
              </div>
            </div>
          </div>
        </div>
      {:else if currentView === 'chat'}
        <div class="chat-view">
          <div class="chat-messages">
            <div class="message assistant">
              <div class="message-content">
                <p>Hello! I am your Synthos OS assistant. How can I help you today?</p>
              </div>
            </div>
          </div>
          <div class="chat-input">
            <input type="text" placeholder="Type your message..." />
            <button>Send</button>
          </div>
        </div>
      {:else if currentView === 'memory'}
        <div class="memory-view">
          <h3>Memory Management</h3>
          <div class="memory-stats">
            <div class="stat-card">
              <span class="stat-number">24</span>
              <span class="stat-label">Episodic</span>
            </div>
            <div class="stat-card">
              <span class="stat-number">156</span>
              <span class="stat-label">Semantic</span>
            </div>
            <div class="stat-card">
              <span class="stat-number">12</span>
              <span class="stat-label">Procedural</span>
            </div>
          </div>
          <div class="memory-list">
            <div class="memory-item">
              <span class="memory-type">Episodic</span>
              <span class="memory-title">Previous conversation about project planning</span>
              <span class="memory-date">2024-09-25</span>
            </div>
            <div class="memory-item">
              <span class="memory-type">Semantic</span>
              <span class="memory-title">Best practices for React Native development</span>
              <span class="memory-date">2024-09-24</span>
            </div>
          </div>
          <button class="add-memory-button">+ Add Memory</button>
        </div>
      {:else if currentView === 'tools'}
        <div class="tools-view">
          <h3>Tools Panel</h3>
          <div class="tools-grid">
            <div class="tool-card">
              <h4>File Manager</h4>
              <p>Manage local files and directories</p>
            </div>
            <div class="tool-card">
              <h4>Code Editor</h4>
              <p>Edit code with syntax highlighting</p>
            </div>
            <div class="tool-card">
              <h4>Terminal</h4>
              <p>Execute shell commands</p>
            </div>
            <div class="tool-card">
              <h4>Browser</h4>
              <p>Web browsing capabilities</p>
            </div>
          </div>
        </div>
      {:else if currentView === 'settings'}
        <div class="settings-view">
          <h3>Settings</h3>
          <div class="settings-section">
            <h4>AI Model Configuration</h4>
            <div class="setting-item">
              <span>Preferred Model</span>
              <select>
                {#each availableModels as model}
                  <option value={model.id}>{model.name}</option>
                {/each}
              </select>
            </div>
            <div class="setting-item">
              <span>Temperature</span>
              <input type="range" min="0" max="1" step="0.1" value="0.7" />
            </div>
          </div>
          <div class="settings-section">
            <h4>Privacy & Security</h4>
            <div class="setting-item">
              <span>Local Processing</span>
              <input type="checkbox" checked />
            </div>
            <div class="setting-item">
              <span>Offline Mode</span>
              <input type="checkbox" />
            </div>
          </div>
          <div class="settings-section">
            <h4>Appearance</h4>
            <div class="setting-item">
              <span>Theme</span>
              <select>
                <option>Dark</option>
                <option>Light</option>
                <option>System</option>
              </select>
            </div>
          </div>
        </div>
      {/if}
    </div>
  </main>
</div>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background-color: #1a1a1a;
    color: #ffffff;
  }

  .app-container {
    display: flex;
    height: 100vh;
    overflow: hidden;
  }

  .sidebar {
    width: 250px;
    background-color: #2d2d2d;
    display: flex;
    flex-direction: column;
    border-right: 1px solid #3d3d3d;
  }

  .sidebar-header {
    padding: 20px;
    border-bottom: 1px solid #3d3d3d;
  }

  .sidebar-header h1 {
    margin: 0;
    font-size: 20px;
    color: #ffffff;
  }

  .subtitle {
    margin: 5px 0 0 0;
    font-size: 12px;
    color: #888;
  }

  .sidebar-nav {
    flex: 1;
    padding: 10px;
  }

  .nav-item {
    width: 100%;
    padding: 12px;
    margin-bottom: 5px;
    background: none;
    border: none;
    color: #888;
    text-align: left;
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.2s;
  }

  .nav-item:hover {
    background-color: #3d3d3d;
    color: #ffffff;
  }

  .nav-item.active {
    background-color: #007AFF;
    color: #ffffff;
  }

  .sidebar-footer {
    padding: 15px;
    border-top: 1px solid #3d3d3d;
  }

  .user-info {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    padding: 10px;
    background-color: #1a1a1a;
    border-radius: 8px;
  }

  .user-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: #007AFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    margin-right: 10px;
  }

  .user-details {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .user-name {
    font-size: 14px;
    color: #ffffff;
    font-weight: 600;
  }

  .user-email {
    font-size: 12px;
    color: #888;
  }

  .status-indicator {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
    font-size: 12px;
    color: #888;
  }

  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 8px;
  }

  .logout-button {
    width: 100%;
    padding: 8px;
    background-color: #FF3B30;
    border: none;
    border-radius: 5px;
    color: #ffffff;
    cursor: pointer;
    font-size: 12px;
    margin-top: 10px;
  }

  .logout-button:hover {
    background-color: #d32f2f;
  }

  .main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: #1a1a1a;
  }

  .top-bar {
    display: flex;
    align-items: center;
    padding: 15px 20px;
    background-color: #2d2d2d;
    border-bottom: 1px solid #3d3d3d;
  }

  .toggle-sidebar {
    background: none;
    border: none;
    color: #888;
    font-size: 16px;
    cursor: pointer;
    margin-right: 15px;
  }

  .top-bar h2 {
    margin: 0;
    flex: 1;
    font-size: 18px;
    color: #ffffff;
  }

  .resource-usage {
    display: flex;
    gap: 20px;
    font-size: 12px;
    color: #888;
  }

  .content-area {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
  }

  .home-view {
    max-width: 800px;
    margin: 0 auto;
  }

  .welcome-section {
    text-align: center;
    margin-bottom: 40px;
  }

  .welcome-section h3 {
    margin: 0 0 10px 0;
    font-size: 24px;
    color: #ffffff;
  }

  .welcome-section p {
    margin: 0;
    color: #888;
  }

  .quick-actions {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-bottom: 30px;
  }

  .action-card {
    background-color: #2d2d2d;
    padding: 20px;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s;
    border: 1px solid #3d3d3d;
  }

  .action-card:hover {
    background-color: #3d3d3d;
  }

  .action-card h4 {
    margin: 0 0 8px 0;
    color: #ffffff;
  }

  .action-card p {
    margin: 0;
    color: #888;
    font-size: 14px;
  }

  .system-status {
    background-color: #2d2d2d;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #3d3d3d;
  }

  .system-status h4 {
    margin: 0 0 15px 0;
    color: #ffffff;
  }

  .status-grid {
    display: grid;
    gap: 10px;
  }

  .status-item {
    display: flex;
    justify-content: space-between;
    padding: 10px;
    background-color: #1a1a1a;
    border-radius: 5px;
  }

  .status-label {
    color: #888;
  }

  .status-value {
    font-weight: 600;
  }

  .chat-view {
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
  }

  .message {
    margin-bottom: 15px;
  }

  .message.assistant {
    display: flex;
    justify-content: flex-start;
  }

  .message-content {
    background-color: #2d2d2d;
    padding: 15px;
    border-radius: 8px;
    max-width: 70%;
  }

  .message-content p {
    margin: 0;
    color: #ffffff;
  }

  .chat-input {
    display: flex;
    padding: 20px;
    background-color: #2d2d2d;
    border-top: 1px solid #3d3d3d;
  }

  .chat-input input {
    flex: 1;
    padding: 12px;
    background-color: #1a1a1a;
    border: 1px solid #3d3d3d;
    border-radius: 5px;
    color: #ffffff;
    margin-right: 10px;
  }

  .chat-input button {
    padding: 12px 20px;
    background-color: #007AFF;
    border: none;
    border-radius: 5px;
    color: #ffffff;
    cursor: pointer;
  }

  .memory-view,
  .tools-view,
  .settings-view {
    max-width: 800px;
    margin: 0 auto;
  }

  .memory-view h3,
  .tools-view h3,
  .settings-view h3 {
    margin: 0 0 20px 0;
    color: #ffffff;
  }

  .memory-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-bottom: 30px;
  }

  .stat-card {
    background-color: #2d2d2d;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    border: 1px solid #3d3d3d;
  }

  .stat-number {
    display: block;
    font-size: 24px;
    font-weight: bold;
    color: #007AFF;
    margin-bottom: 5px;
  }

  .stat-label {
    font-size: 12px;
    color: #888;
  }

  .memory-list {
    background-color: #2d2d2d;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 20px;
    border: 1px solid #3d3d3d;
  }

  .memory-item {
    display: flex;
    align-items: center;
    padding: 12px;
    border-bottom: 1px solid #3d3d3d;
  }

  .memory-item:last-child {
    border-bottom: none;
  }

  .memory-type {
    background-color: #007AFF;
    color: #ffffff;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    margin-right: 12px;
  }

  .memory-title {
    flex: 1;
    color: #ffffff;
  }

  .memory-date {
    color: #888;
    font-size: 12px;
  }

  .add-memory-button {
    width: 100%;
    padding: 12px;
    background-color: #007AFF;
    border: none;
    border-radius: 8px;
    color: #ffffff;
    cursor: pointer;
    font-size: 14px;
  }

  .add-memory-button:hover {
    background-color: #0056b3;
  }

  .tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
  }

  .tool-card {
    background-color: #2d2d2d;
    padding: 20px;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s;
    border: 1px solid #3d3d3d;
  }

  .tool-card:hover {
    background-color: #3d3d3d;
  }

  .tool-card h4 {
    margin: 0 0 8px 0;
    color: #ffffff;
  }

  .tool-card p {
    margin: 0;
    color: #888;
    font-size: 14px;
  }

  .settings-section {
    background-color: #2d2d2d;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    border: 1px solid #3d3d3d;
  }

  .settings-section h4 {
    margin: 0 0 15px 0;
    color: #ffffff;
  }

  .setting-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #3d3d3d;
  }

  .setting-item:last-child {
    border-bottom: none;
  }

  .setting-item span {
    color: #ffffff;
  }

  .setting-item select,
  .setting-item input[type="range"] {
    background-color: #1a1a1a;
    border: 1px solid #3d3d3d;
    color: #ffffff;
    padding: 8px;
    border-radius: 4px;
  }

  .setting-item input[type="checkbox"] {
    width: 20px;
    height: 20px;
  }
</style>
