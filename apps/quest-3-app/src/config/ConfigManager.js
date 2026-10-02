/**
 * SynthOS Configuration Manager
 * Handles app settings, preferences, and user configuration
 */

const EventEmitter = require('eventemitter3');
const fs = require('fs').promises;
const path = require('path');

class ConfigManager extends EventEmitter {
  constructor(configPath = null) {
    super();
    this.configPath = configPath || path.join(process.cwd(), 'config', 'app-config.json');
    this.config = {};
    this.defaults = this.getDefaultConfig();
    this.isInitialized = false;
    this.autoSave = true;
  }

  getDefaultConfig() {
    return {
      // App settings
      app: {
        name: 'SynthOS Quest 3',
        version: '1.0.0',
        language: 'en-US',
        theme: 'dark',
        firstRun: true
      },

      // Performance settings
      performance: {
        targetFPS: 90,
        renderQuality: 'high',
        powerSaving: false,
        thermalThrottling: true,
        adaptiveQuality: true
      },

      // Audio settings
      audio: {
        masterVolume: 1.0,
        voiceVolume: 1.0,
        systemVolume: 0.8,
        spatialAudio: true,
        hrtf: true,
        reverbEnabled: true,
        acousticEnvironment: 'room'
      },

      // Voice settings
      voice: {
        enabled: true,
        language: 'en-US',
        continuousMode: false,
        wakeWord: 'Hey SynthOS',
        voiceProfile: 'default',
        sensitivity: 0.8
      },

      // Input settings
      input: {
        mode: 'mixed',
        gestureEnabled: true,
        gazeEnabled: true,
        controllerEnabled: true,
        voiceEnabled: true,
        gestureThresholds: {
          pinch: 0.05,
          grab: 0.08,
          point: 0.1
        },
        gazeDwellTime: 1000
      },

      // AI settings
      ai: {
        model: 'synthos-enhanced-20b',
        temperature: 0.7,
        maxTokens: 2048,
        contextWindow: 10,
        responseCache: true,
        spatialUnderstanding: true,
        proactiveAssistance: false
      },

      // UI settings
      ui: {
        holographicOpacity: 0.8,
        panelSize: 'medium',
        animationSpeed: 'normal',
        showStatus: true,
        showAI: true,
        showControls: true,
        customLayouts: []
      },

      // Spatial settings
      spatial: {
        passthroughQuality: 'high',
        handTrackingEnabled: true,
        eyeTrackingEnabled: true,
        sceneUnderstanding: true,
        spatialAnchors: true,
        roomScale: true
      },

      // Privacy settings
      privacy: {
        dataCollection: false,
        analytics: false,
        crashReports: true,
        voiceDataStorage: false,
        spatialDataStorage: false
      },

      // Accessibility settings
      accessibility: {
        textToSpeech: false,
        speechToText: true,
        highContrast: false,
        largeText: false,
        reducedMotion: false,
        colorBlindMode: 'none'
      },

      // Developer settings
      developer: {
        debugMode: false,
        showFPS: false,
        showMemory: false,
        logLevel: 'info',
        enableProfiler: false
      }
    };
  }

  async initialize() {
    console.log('⚙️ Initializing configuration manager...');

    try {
      // Load existing configuration or create default
      await this.loadConfig();

      // Ensure all default keys exist
      this.ensureDefaults();

      this.isInitialized = true;
      console.log('✅ Configuration manager initialized successfully!');

    } catch (error) {
      console.error('❌ Failed to initialize configuration manager:', error);
      throw error;
    }
  }

  async loadConfig() {
    try {
      const configData = await fs.readFile(this.configPath, 'utf8');
      this.config = JSON.parse(configData);
      console.log('📂 Configuration loaded from file');
    } catch (error) {
      if (error.code === 'ENOENT') {
        console.log('📝 No existing config found, using defaults');
        this.config = { ...this.defaults };
        await this.saveConfig();
      } else {
        throw error;
      }
    }
  }

  async saveConfig() {
    if (!this.autoSave) return;

    try {
      // Ensure directory exists
      const configDir = path.dirname(this.configPath);
      await fs.mkdir(configDir, { recursive: true });

      // Write config file
      const configData = JSON.stringify(this.config, null, 2);
      await fs.writeFile(this.configPath, configData, 'utf8');

      console.log('💾 Configuration saved');
      this.emit('configSaved', this.config);

    } catch (error) {
      console.error('❌ Failed to save configuration:', error);
      throw error;
    }
  }

  ensureDefaults() {
    const merged = { ...this.defaults };

    const deepMerge = (target, source) => {
      for (const key in source) {
        if (source[key] instanceof Object && key in target) {
          Object.assign(source[key], deepMerge(target[key], source[key]));
        }
      }
      Object.assign(target || {}, source);
      return target;
    };

    deepMerge(merged, this.config);
    this.config = merged;
  }

  get(path, defaultValue = null) {
    const keys = path.split('.');
    let value = this.config;

    for (const key of keys) {
      if (value && typeof value === 'object' && key in value) {
        value = value[key];
      } else {
        return defaultValue;
      }
    }

    return value;
  }

  set(path, value, save = true) {
    const keys = path.split('.');
    let current = this.config;

    for (let i = 0; i < keys.length - 1; i++) {
      const key = keys[i];
      if (!(key in current) || typeof current[key] !== 'object') {
        current[key] = {};
      }
      current = current[key];
    }

    const oldValue = current[keys[keys.length - 1]];
    current[keys[keys.length - 1]] = value;

    this.emit('configChanged', { path, value, oldValue });

    if (save) {
      this.saveConfig();
    }
  }

  reset(path = null) {
    if (path) {
      const keys = path.split('.');
      let current = this.config;
      let defaults = this.defaults;

      for (let i = 0; i < keys.length - 1; i++) {
        current = current[keys[i]];
        defaults = defaults[keys[i]];
      }

      current[keys[keys.length - 1]] = defaults[keys[keys.length - 1]];
    } else {
      this.config = { ...this.defaults };
    }

    this.emit('configReset', path);
    this.saveConfig();
  }

  getCategory(category) {
    return this.config[category] || {};
  }

  setCategory(category, values, save = true) {
    this.config[category] = { ...this.config[category], ...values };
    this.emit('categoryChanged', { category, values });
    if (save) {
      this.saveConfig();
    }
  }

  // Specific configuration methods
  setVolume(type, volume) {
    const path = `audio.${type}Volume`;
    this.set(path, Math.max(0, Math.min(1, volume)));
  }

  getVolume(type) {
    return this.get(`audio.${type}Volume`, 1.0);
  }

  setRenderQuality(quality) {
    const validQualities = ['low', 'medium', 'high'];
    if (validQualities.includes(quality)) {
      this.set('performance.renderQuality', quality);
    }
  }

  setInputMode(mode) {
    const validModes = ['gesture', 'gaze', 'controller', 'voice', 'mixed'];
    if (validModes.includes(mode)) {
      this.set('input.mode', mode);
    }
  }

  setLanguage(language) {
    this.set('app.language', language);
    this.set('voice.language', language);
  }

  enableFeature(feature, enabled) {
    const featurePaths = {
      spatialAudio: 'audio.spatialAudio',
      handTracking: 'spatial.handTrackingEnabled',
      eyeTracking: 'spatial.eyeTrackingEnabled',
      voiceInput: 'voice.enabled',
      gestureInput: 'input.gestureEnabled',
      gazeInput: 'input.gazeEnabled'
    };

    if (featurePaths[feature]) {
      this.set(featurePaths[feature], enabled);
    }
  }

  isFeatureEnabled(feature) {
    const featurePaths = {
      spatialAudio: 'audio.spatialAudio',
      handTracking: 'spatial.handTrackingEnabled',
      eyeTracking: 'spatial.eyeTrackingEnabled',
      voiceInput: 'voice.enabled',
      gestureInput: 'input.gestureEnabled',
      gazeInput: 'input.gazeEnabled'
    };

    return this.get(featurePaths[feature], false);
  }

  setDeveloperMode(enabled) {
    this.set('developer.debugMode', enabled);
  }

  isDeveloperMode() {
    return this.get('developer.debugMode', false);
  }

  exportConfig() {
    return JSON.stringify(this.config, null, 2);
  }

  async importConfig(configString) {
    try {
      const importedConfig = JSON.parse(configString);
      this.config = { ...this.defaults, ...importedConfig };
      await this.saveConfig();
      this.emit('configImported', this.config);
    } catch (error) {
      console.error('❌ Failed to import configuration:', error);
      throw error;
    }
  }

  getConfig() {
    return { ...this.config };
  }

  getDefaults() {
    return { ...this.defaults };
  }

  setAutoSave(enabled) {
    this.autoSave = enabled;
  }

  async update() {
    if (!this.isInitialized) return;

    try {
      // Auto-save if enabled and changes detected
      // In production, this could detect unsaved changes
    } catch (error) {
      console.error('Error updating configuration manager:', error);
    }
  }

  async shutdown() {
    console.log('🛑 Shutting down configuration manager...');

    // Final save
    await this.saveConfig();

    this.isInitialized = false;

    console.log('✅ Configuration manager shut down');
  }
}

module.exports = { ConfigManager };