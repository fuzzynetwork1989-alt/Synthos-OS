/**
 * SynthOS Spatial Audio System
 * 3D positional audio for immersive XR experiences on Quest 3
 */

const EventEmitter = require('eventemitter3');

class SpatialAudio extends EventEmitter {
  constructor(spatialSystem) {
    super();
    this.spatial = spatialSystem;
    this.audioContext = null;
    this.listener = null;
    this.soundSources = new Map();
    this.isInitialized = false;
    this.masterVolume = 1.0;
    this.spatialEnabled = true;
    this.hrtfEnabled = true;
    this.reverbEnabled = true;
    this.acousticModel = 'room';
  }

  async initialize() {
    console.log('🔊 Initializing spatial audio system...');

    try {
      // Initialize Web Audio API
      await this.initializeAudioContext();

      // Set up spatial audio listener
      await this.setupListener();

      // Initialize acoustic environments
      await this.initializeAcoustics();

      this.isInitialized = true;
      console.log('✅ Spatial audio system initialized successfully!');

    } catch (error) {
      console.error('❌ Failed to initialize spatial audio:', error);
      throw error;
    }
  }

  async initializeAudioContext() {
    console.log('🎵 Setting up audio context...');

    // In production, this would use Web Audio API with Meta Spatial SDK integration
    this.audioContext = {
      state: 'running',
      sampleRate: 48000,
      currentTime: 0,

      createBuffer: (channels, length, sampleRate) => {
        return {
          numberOfChannels: channels,
          length: length,
          sampleRate: sampleRate,
          duration: length / sampleRate,
          getChannelData: (channel) => new Float32Array(length)
        };
      },

      createBufferSource: () => {
        return {
          buffer: null,
          loop: false,
          playbackRate: 1.0,
          gain: 1.0,
          panner: null,
          start: (when) => {},
          stop: (when) => {}
        };
      },

      createPanner: () => {
        return {
          panningModel: 'HRTF',
          distanceModel: 'inverse',
          refDistance: 1.0,
          maxDistance: 10000.0,
          rolloffFactor: 1.0,
          coneInnerAngle: 360,
          coneOuterAngle: 360,
          coneOuterGain: 0.0,
          positionX: { value: 0 },
          positionY: { value: 0 },
          positionZ: { value: 0 },
          orientationX: { value: 0 },
          orientationY: { value: 0 },
          orientationZ: { value: 0 }
        };
      },

      createGain: () => {
        return {
          gain: { value: 1.0 },
          connect: (destination) => {},
          disconnect: () => {}
        };
      },

      createConvolver: () => {
        return {
          buffer: null,
          connect: (destination) => {},
          disconnect: () => {}
        };
      },

      resume: async () => {
        this.audioContext.state = 'running';
      },

      suspend: async () => {
        this.audioContext.state = 'suspended';
      }
    };

    console.log('✅ Audio context initialized');
  }

  async setupListener() {
    console.log('👂 Setting up spatial audio listener...');

    // Audio listener represents the user's head position/orientation
    this.listener = {
      position: { x: 0, y: 1.6, z: 0 },
      forward: { x: 0, y: 0, z: -1 },
      up: { x: 0, y: 1, z: 0 },

      setPosition: (x, y, z) => {
        this.listener.position = { x, y, z };
        this.emit('listenerPositionChanged', { x, y, z });
      },

      setOrientation: (forwardX, forwardY, forwardZ, upX, upY, upZ) => {
        this.listener.forward = { x: forwardX, y: forwardY, z: forwardZ };
        this.listener.up = { x: upX, y: upY, z: upZ };
        this.emit('listenerOrientationChanged', { forward: this.listener.forward, up: this.listener.up });
      }
    };

    console.log('✅ Spatial audio listener set up');
  }

  async initializeAcoustics() {
    console.log('🏠 Initializing acoustic environments...');

    // Predefined acoustic environments
    this.acousticEnvironments = {
      room: {
        name: 'Room',
        reverbTime: 0.8,
        reflections: 3,
        diffusion: 0.5,
        description: 'Standard room acoustics'
      },
      hall: {
        name: 'Hall',
        reverbTime: 2.0,
        reflections: 5,
        diffusion: 0.7,
        description: 'Large hall with longer reverb'
      },
      outdoor: {
        name: 'Outdoor',
        reverbTime: 0.2,
        reflections: 1,
        diffusion: 0.3,
        description: 'Outdoor environment with minimal reverb'
      },
      studio: {
        name: 'Studio',
        reverbTime: 0.4,
        reflections: 2,
        diffusion: 0.4,
        description: 'Dry studio environment'
      }
    };

    this.currentAcoustic = this.acousticEnvironments.room;

    console.log('✅ Acoustic environments initialized');
  }

  async createSoundSource(config) {
    const {
      id = `sound_${Date.now()}`,
      position = { x: 0, y: 0, z: 0 },
      volume = 1.0,
      loop = false,
      spatial = true,
      distance = 5.0,
      cone = { innerAngle: 360, outerAngle: 360, outerGain: 0.0 }
    } = config;

    console.log(`🔊 Creating sound source: ${id}`);

    const soundSource = {
      id,
      position: { ...position },
      volume,
      loop,
      spatial,
      distance,
      cone: { ...cone },
      isPlaying: false,
      buffer: null,
      sourceNode: null,
      pannerNode: null,
      gainNode: null,

      setPosition: (x, y, z) => {
        soundSource.position = { x, y, z };
        if (soundSource.pannerNode) {
          soundSource.pannerNode.positionX.value = x;
          soundSource.pannerNode.positionY.value = y;
          soundSource.pannerNode.positionZ.value = z;
        }
      },

      setVolume: (vol) => {
        soundSource.volume = vol;
        if (soundSource.gainNode) {
          soundSource.gainNode.gain.value = vol * this.masterVolume;
        }
      },

      play: async () => {
        if (soundSource.buffer) {
          soundSource.isPlaying = true;
          this.emit('soundStarted', { id: soundSource.id });
        }
      },

      pause: () => {
        soundSource.isPlaying = false;
        this.emit('soundPaused', { id: soundSource.id });
      },

      stop: () => {
        soundSource.isPlaying = false;
        this.emit('soundStopped', { id: soundSource.id });
      }
    };

    // Create audio nodes if spatial audio is enabled
    if (this.spatialEnabled && spatial) {
      soundSource.pannerNode = this.audioContext.createPanner();
      soundSource.pannerNode.panningModel = this.hrtfEnabled ? 'HRTF' : 'equalpower';
      soundSource.pannerNode.distanceModel = 'inverse';
      soundSource.pannerNode.refDistance = 1.0;
      soundSource.pannerNode.maxDistance = distance;
      soundSource.pannerNode.coneInnerAngle = cone.innerAngle;
      soundSource.pannerNode.coneOuterAngle = cone.outerAngle;
      soundSource.pannerNode.coneOuterGain = cone.outerGain;

      soundSource.pannerNode.positionX.value = position.x;
      soundSource.pannerNode.positionY.value = position.y;
      soundSource.pannerNode.positionZ.value = position.z;
    }

    soundSource.gainNode = this.audioContext.createGain();
    soundSource.gainNode.gain.value = volume * this.masterVolume;

    this.soundSources.set(id, soundSource);
    return soundSource;
  }

  async loadSound(id, audioData) {
    console.log(`📥 Loading sound: ${id}`);

    const soundSource = this.soundSources.get(id);
    if (!soundSource) {
      throw new Error(`Sound source ${id} not found`);
    }

    // In production, this would decode actual audio data
    soundSource.buffer = this.audioContext.createBuffer(2, 48000, 48000);

    console.log(`✅ Sound loaded: ${id}`);
    this.emit('soundLoaded', { id });
  }

  async playSound(id) {
    const soundSource = this.soundSources.get(id);
    if (!soundSource) {
      throw new Error(`Sound source ${id} not found`);
    }

    await soundSource.play();
  }

  async stopSound(id) {
    const soundSource = this.soundSources.get(id);
    if (!soundSource) {
      throw new Error(`Sound source ${id} not found`);
    }

    soundSource.stop();
  }

  async removeSoundSource(id) {
    const soundSource = this.soundSources.get(id);
    if (soundSource) {
      soundSource.stop();
      this.soundSources.delete(id);
      this.emit('soundRemoved', { id });
    }
  }

  async updateListenerPosition(position, orientation) {
    if (!this.listener) return;

    this.listener.setPosition(position.x, position.y, position.z);

    if (orientation) {
      this.listener.setOrientation(
        orientation.forward.x,
        orientation.forward.y,
        orientation.forward.z,
        orientation.up.x,
        orientation.up.y,
        orientation.up.z
      );
    }
  }

  async setAcousticEnvironment(environmentName) {
    const environment = this.acousticEnvironments[environmentName];
    if (environment) {
      this.currentAcoustic = environment;
      this.acousticModel = environmentName;
      console.log(`🏠 Acoustic environment set to: ${environment.name}`);
      this.emit('acousticEnvironmentChanged', environment);
    }
  }

  setMasterVolume(volume) {
    this.masterVolume = Math.max(0, Math.min(1, volume));

    // Update all sound sources
    for (const soundSource of this.soundSources.values()) {
      soundSource.setVolume(soundSource.volume);
    }

    console.log(`🔊 Master volume set to: ${this.masterVolume}`);
    this.emit('masterVolumeChanged', this.masterVolume);
  }

  enableSpatialAudio(enabled) {
    this.spatialEnabled = enabled;
    console.log(`🎧 Spatial audio: ${enabled ? 'enabled' : 'disabled'}`);
    this.emit('spatialAudioToggled', enabled);
  }

  enableHRTF(enabled) {
    this.hrtfEnabled = enabled;

    // Update all panner nodes
    for (const soundSource of this.soundSources.values()) {
      if (soundSource.pannerNode) {
        soundSource.pannerNode.panningModel = enabled ? 'HRTF' : 'equalpower';
      }
    }

    console.log(`🎧 HRTF: ${enabled ? 'enabled' : 'disabled'}`);
    this.emit('hrtfToggled', enabled);
  }

  async update() {
    if (!this.isInitialized) return;

    try {
      // Update listener position based on spatial context
      if (this.spatial && this.spatial.spatialContext) {
        const context = this.spatial.spatialContext;
        // In production, this would use actual head tracking data
        // await this.updateListenerPosition(headPosition, headOrientation);
      }

      // Update sound source positions if they're moving
      for (const soundSource of this.soundSources.values()) {
        if (soundSource.isPlaying && soundSource.spatial) {
          // Update spatialization based on listener position
        }
      }

    } catch (error) {
      console.error('Error updating spatial audio:', error);
    }
  }

  getAudioStatus() {
    return {
      isInitialized: this.isInitialized,
      masterVolume: this.masterVolume,
      spatialEnabled: this.spatialEnabled,
      hrtfEnabled: this.hrtfEnabled,
      acousticModel: this.acousticModel,
      activeSounds: this.soundSources.size,
      soundSources: Array.from(this.soundSources.keys())
    };
  }

  async shutdown() {
    console.log('🛑 Shutting down spatial audio system...');

    // Stop all sounds
    for (const soundSource of this.soundSources.values()) {
      soundSource.stop();
    }

    this.soundSources.clear();

    if (this.audioContext) {
      await this.audioContext.suspend();
    }

    this.isInitialized = false;

    console.log('✅ Spatial audio system shut down');
  }
}

module.exports = { SpatialAudio };