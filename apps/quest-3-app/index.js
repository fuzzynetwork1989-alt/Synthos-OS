/**
 * SynthOS Quest 3 - Main Entry Point
 * Meta XR/AR/VR Application with Spatial AI
 */

const { SynthOSSpatial } = require('./src/spatial/SynthOSSpatial');
const { SynthOSAI } = require('./src/ai/SynthOSAI');
const { HolographicUI } = require('./src/ui/HolographicUI');
const { PerformanceManager } = require('./src/performance/PerformanceManager');

class SynthOSQuest3 {
  constructor() {
    this.spatial = null;
    this.ai = null;
    this.ui = null;
    this.performance = null;
    this.isInitialized = false;
  }

  async initialize() {
    console.log('🚀 Initializing SynthOS Quest 3...');

    try {
      // Initialize performance manager first
      this.performance = new PerformanceManager();
      await this.performance.initialize();

      // Initialize spatial computing
      console.log('📍 Initializing spatial computing...');
      this.spatial = new SynthOSSpatial(this.performance);
      await this.spatial.initialize();

      // Initialize AI integration
      console.log('🧠 Initializing AI integration...');
      this.ai = new SynthOSAI(this.spatial);
      await this.ai.initialize();

      // Initialize holographic UI
      console.log('🎨 Initializing holographic UI...');
      this.ui = new HolographicUI(this.spatial, this.ai);
      await this.ui.initialize();

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

  async shutdown() {
    console.log('🛑 Shutting down SynthOS Quest 3...');

    if (this.ui) await this.ui.shutdown();
    if (this.ai) await this.ai.shutdown();
    if (this.spatial) await this.spatial.shutdown();
    if (this.performance) await this.performance.shutdown();

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