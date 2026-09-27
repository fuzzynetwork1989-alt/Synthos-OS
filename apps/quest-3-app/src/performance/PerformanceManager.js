/**
 * SynthOS Performance Manager
 * Optimizes GPU, memory, and power usage for Quest 3
 */

class PerformanceManager {
  constructor() {
    this.metrics = {
      fps: 0,
      frameTime: 0,
      cpuUsage: 0,
      memoryUsage: 0,
      gpuUsage: 0,
      batteryLevel: 100,
      thermalState: 'normal'
    };
    
    this.settings = {
      targetFPS: 90,
      maxFrameTime: 11.11, // 1000ms / 90fps
      memoryLimit: 2048, // 2GB
      batteryThreshold: 20,
      thermalThreshold: 0.8
    };
    
    this.frameCount = 0;
    this.lastFrameTime = 0;
    this.frameTimes = [];
    this.isInitialized = false;
  }

  async initialize() {
    console.log('⚡ Initializing performance manager...');

    try {
      // Start performance monitoring
      this.startMonitoring();

      // Set up adaptive quality
      this.setupAdaptiveQuality();

      this.isInitialized = true;
      console.log('✅ Performance manager initialized successfully!');

    } catch (error) {
      console.error('❌ Failed to initialize performance manager:', error);
      throw error;
    }
  }

  startMonitoring() {
    // Monitor performance metrics
    setInterval(() => {
      this.updateMetrics();
    }, 1000);
  }

  setupAdaptiveQuality() {
    // Set up adaptive quality based on performance
    setInterval(() => {
      this.adjustQuality();
    }, 5000);
  }

  updateFrame(timestamp) {
    const currentTime = performance.now();
    const deltaTime = currentTime - this.lastFrameTime;
    
    this.frameCount++;
    this.frameTimes.push(deltaTime);
    
    // Keep only last 60 frame times
    if (this.frameTimes.length > 60) {
      this.frameTimes.shift();
    }
    
    // Calculate FPS
    const avgFrameTime = this.frameTimes.reduce((a, b) => a + b, 0) / this.frameTimes.length;
    this.metrics.fps = 1000 / avgFrameTime;
    this.metrics.frameTime = avgFrameTime;
    
    this.lastFrameTime = currentTime;
  }

  updateMetrics() {
    // Simulated metrics (replace with actual device metrics)
    this.metrics.cpuUsage = 30 + Math.random() * 20;
    this.metrics.memoryUsage = 1024 + Math.random() * 512;
    this.metrics.gpuUsage = 40 + Math.random() * 30;
    this.metrics.batteryLevel = Math.max(0, this.metrics.batteryLevel - 0.1);
    this.metrics.thermalState = this.getThermalState();
  }

  getThermalState() {
    const gpuUsage = this.metrics.gpuUsage;
    
    if (gpuUsage > 90) return 'critical';
    if (gpuUsage > 75) return 'high';
    if (gpuUsage > 60) return 'moderate';
    return 'normal';
  }

  adjustQuality() {
    const fps = this.metrics.fps;
    const targetFPS = this.settings.targetFPS;
    
    if (fps < targetFPS * 0.8) {
      // Reduce quality
      this.reduceQuality();
    } else if (fps > targetFPS * 1.2) {
      // Increase quality
      this.increaseQuality();
    }
  }

  reduceQuality() {
    console.log('📉 Reducing quality to maintain performance');
    // In production, this would adjust rendering quality, texture resolution, etc.
  }

  increaseQuality() {
    console.log('📈 Increasing quality for better visuals');
    // In production, this would enhance rendering quality
  }

  getPerformanceReport() {
    return {
      ...this.metrics,
      quality: this.getCurrentQuality(),
      recommendations: this.getRecommendations()
    };
  }

  getCurrentQuality() {
    const fps = this.metrics.fps;
    
    if (fps >= 85) return 'high';
    if (fps >= 60) return 'medium';
    return 'low';
  }

  getRecommendations() {
    const recommendations = [];
    
    if (this.metrics.fps < 60) {
      recommendations.push('Consider reducing visual quality');
    }
    
    if (this.metrics.memoryUsage > this.settings.memoryLimit * 0.9) {
      recommendations.push('Memory usage is high, consider asset streaming');
    }
    
    if (this.metrics.batteryLevel < this.settings.batteryThreshold) {
      recommendations.push('Battery level low, enable power saving mode');
    }
    
    if (this.metrics.thermalState === 'critical') {
      recommendations.push('Device overheating, reduce graphics intensity');
    }
    
    return recommendations;
  }

  async shutdown() {
    console.log('🛑 Shutting down performance manager...');

    this.isInitialized = false;
    this.frameTimes = [];

    console.log('✅ Performance manager shut down');
  }
}

module.exports = { PerformanceManager };