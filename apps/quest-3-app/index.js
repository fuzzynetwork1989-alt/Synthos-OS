/**
 * SynthOS Quest 3 - Main Entry Point
 * Meta XR/AR/VR Application with Spatial AI
 */

const { SynthOSSpatial } = require('./src/spatial/SynthOSSpatial');
const { SynthOSAI } = require('./src/ai/SynthOSAI');
const { HolographicUI } = require('./src/ui/HolographicUI');
const { PerformanceManager } = require('./src/performance/PerformanceManager');
const { VoiceInput } = require('./src/audio/VoiceInput');
const { SpatialAudio } = require('./src/audio/SpatialAudio');
const { Renderer3D } = require('./src/rendering/Renderer3D');
const { InputManager } = require('./src/input/InputManager');
const { ConfigManager } = require('./src/config/ConfigManager');

class SynthOSQuest3 {
  constructor() {
    this.spatial = null;
    this.ai = null;
    this.ui = null;
    this.performance = null;
    this.voice = null;
    this.audio = null;
    this.renderer = null;
    this.input = null;
    this.config = null;
    this.isInitialized = false;
  }

  async initialize() {
    console.log('🚀 Initializing SynthOS Quest 3...');

    try {
      // Initialize configuration manager first
      console.log('⚙️ Initializing configuration manager...');
      this.config = new ConfigManager();
      await this.config.initialize();

      // Initialize performance manager
      this.performance = new PerformanceManager();
      await this.performance.initialize();

      // Initialize spatial computing
      console.log('📍 Initializing spatial computing...');
      this.spatial = new SynthOSSpatial(this.performance);
      await this.spatial.initialize();

      // Initialize 3D rendering
      console.log('🎨 Initializing 3D rendering...');
      this.renderer = new Renderer3D(this.spatial, this.performance);
      await this.renderer.initialize();

      // Initialize voice input
      console.log('🎤 Initializing voice input...');
      this.voice = new VoiceInput(this.spatial);
      await this.voice.initialize();

      // Initialize spatial audio
      console.log('🔊 Initializing spatial audio...');
      this.audio = new SpatialAudio(this.spatial);
      await this.audio.initialize();

      // Initialize input manager
      console.log('🎮 Initializing input manager...');
      this.input = new InputManager(this.spatial, this.voice);
      await this.input.initialize();

      // Initialize AI integration
      console.log('🧠 Initializing AI integration...');
      this.ai = new SynthOSAI(this.spatial);
      await this.ai.initialize();

      // Initialize holographic UI
      console.log('🎨 Initializing holographic UI...');
      this.ui = new HolographicUI(this.spatial, this.ai);
      await this.ui.initialize();

      // Apply configuration to systems
      await this.applyConfiguration();

      // Set up system event connections
      this.setupSystemConnections();

      this.isInitialized = true;
      console.log('✅ SynthOS Quest 3 initialized successfully!');

      // Start main loop
      this.startMainLoop();

    } catch (error) {
      console.error('❌ Failed to initialize SynthOS Quest 3:', error);
      throw error;
    }
  }

  startMainLoop() {
    const targetFPS = 90;
    const frameTime = 1000 / targetFPS;

    const loop = async (timestamp) => {
      const startTime = performance.now();

      try {
        // Update spatial tracking
        await this.spatial.update();

        // Update 3D rendering
        await this.renderer.update();

        // Update voice input
        await this.voice.update();

        // Update spatial audio
        await this.audio.update();

        // Update input manager
        await this.input.update();

        // Update configuration
        await this.config.update();

        // Update AI processing
        await this.ai.update();

        // Update UI rendering
        await this.ui.update();

        // Performance monitoring
        this.performance.updateFrame(timestamp);

      } catch (error) {
        console.error('Error in main loop:', error);
      }

      // Calculate remaining time for next frame
      const elapsed = performance.now() - startTime;
      const remaining = Math.max(0, frameTime - elapsed);

      setTimeout(() => {
        requestAnimationFrame(loop);
      }, remaining);
    };

    requestAnimationFrame(loop);
  }

  setupSystemConnections() {
    console.log('🔗 Setting up system connections...');

    // Connect voice commands to AI
    this.input.on('voiceInput', async (voiceData) => {
      if (voiceData.type === 'command') {
        await this.ai.processSpatialQuery(voiceData.transcript);
      }
    });

    // Connect gestures to UI
    this.input.on('gestureInput', (gestures) => {
      this.ui.emit('gestureInput', gestures);
    });

    // Connect gaze to UI
    this.input.on('gazeInput', (gazeData) => {
      this.ui.emit('gazeInput', gazeData);
    });

    // Connect AI responses to UI
    this.ai.on('response', (response) => {
      this.ui.showAIResponse(response.content);
    });

    // Connect spatial context to audio
    this.spatial.on('contextUpdate', (context) => {
      if (context.hands && context.hands.length > 0) {
        this.audio.updateListenerPosition(
          { x: 0, y: 1.6, z: 0 },
          { forward: { x: 0, y: 0, z: -1 }, up: { x: 0, y: 1, z: 0 } }
        );
      }
    });

    console.log('✅ System connections set up');
  }

  async applyConfiguration() {
    console.log('⚙️ Applying configuration to systems...');

    // Apply performance settings
    const targetFPS = this.config.get('performance.targetFPS', 90);
    this.performance.settings.targetFPS = targetFPS;

    const renderQuality = this.config.get('performance.renderQuality', 'high');
    this.renderer.setRenderQuality(renderQuality);

    // Apply audio settings
    const masterVolume = this.config.get('audio.masterVolume', 1.0);
    this.audio.setMasterVolume(masterVolume);

    const spatialAudio = this.config.get('audio.spatialAudio', true);
    this.audio.enableSpatialAudio(spatialAudio);

    const hrtf = this.config.get('audio.hrtf', true);
    this.audio.enableHRTF(hrtf);

    // Apply input settings
    const inputMode = this.config.get('input.mode', 'mixed');
    this.input.setInputMode(inputMode);

    // Apply voice settings
    const voiceEnabled = this.config.get('voice.enabled', true);
    if (voiceEnabled) {
      const voiceLanguage = this.config.get('voice.language', 'en-US');
      await this.voice.setLanguage(voiceLanguage);
    }

    console.log('✅ Configuration applied');
  }

  async shutdown() {
    console.log('🛑 Shutting down SynthOS Quest 3...');

    if (this.ui) await this.ui.shutdown();
    if (this.ai) await this.ai.shutdown();
    if (this.input) await this.input.shutdown();
    if (this.audio) await this.audio.shutdown();
    if (this.voice) await this.voice.shutdown();
    if (this.renderer) await this.renderer.shutdown();
    if (this.spatial) await this.spatial.shutdown();
    if (this.performance) await this.performance.shutdown();
    if (this.config) await this.config.shutdown();

    this.isInitialized = false;
    console.log('✅ SynthOS Quest 3 shut down successfully!');
  }
}

// Main entry point
if (require.main === module) {
  const app = new SynthOSQuest3();

  app.initialize()
    .then(() => {
      console.log('🎉 SynthOS Quest 3 is running!');
    })
    .catch((error) => {
      console.error('Failed to start SynthOS Quest 3:', error);
      process.exit(1);
    });

  // Handle graceful shutdown
  process.on('SIGINT', async () => {
    console.log('\nReceived SIGINT, shutting down gracefully...');
    await app.shutdown();
    process.exit(0);
  });
}

module.exports = { SynthOSQuest3 };