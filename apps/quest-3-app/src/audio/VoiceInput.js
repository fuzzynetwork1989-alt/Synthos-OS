/**
 * SynthOS Voice Input System
 * Natural speech recognition and voice command processing for Quest 3
 */

const EventEmitter = require('eventemitter3');

class VoiceInput extends EventEmitter {
  constructor(spatialSystem) {
    super();
    this.spatial = spatialSystem;
    this.recognition = null;
    this.isListening = false;
    this.isInitialized = false;
    this.currentLanguage = 'en-US';
    this.continuousMode = false;
    this.interimResults = false;
    this.commandPatterns = new Map();
    this.voiceProfile = null;
  }

  async initialize() {
    console.log('🎤 Initializing voice input system...');

    try {
      // Initialize speech recognition
      await this.initializeSpeechRecognition();

      // Set up command patterns
      this.setupCommandPatterns();

      // Initialize voice profile
      await this.initializeVoiceProfile();

      this.isInitialized = true;
      console.log('✅ Voice input system initialized successfully!');

    } catch (error) {
      console.error('❌ Failed to initialize voice input:', error);
      throw error;
    }
  }

  async initializeSpeechRecognition() {
    console.log('🔊 Setting up speech recognition...');

    // In production, this would use Meta Spatial SDK's speech recognition
    // For now, we'll create a simulated recognition system
    this.recognition = {
      lang: this.currentLanguage,
      continuous: this.continuousMode,
      interimResults: this.interimResults,
      maxAlternatives: 3,

      start: () => {
        this.isListening = true;
        console.log('🎙️ Voice recognition started');
        this.emit('listeningStarted');
      },

      stop: () => {
        this.isListening = false;
        console.log('🔇 Voice recognition stopped');
        this.emit('listeningStopped');
      },

      onresult: (event) => {
        this.handleRecognitionResult(event);
      },

      onerror: (error) => {
        this.handleRecognitionError(error);
      },

      onend: () => {
        if (this.continuousMode && this.isListening) {
          this.recognition.start();
        } else {
          this.isListening = false;
          this.emit('listeningEnded');
        }
      }
    };

    console.log('✅ Speech recognition initialized');
  }

  setupCommandPatterns() {
    console.log('📝 Setting up voice command patterns...');

    // Navigation commands
    this.commandPatterns.set('navigation', [
      { pattern: /go to|navigate to|take me to/i, action: 'navigate' },
      { pattern: /where is|find|locate/i, action: 'locate' },
      { pattern: /show me|display/i, action: 'show' }
    ]);

    // Object interaction commands
    this.commandPatterns.set('interaction', [
      { pattern: /grab|pick up|take/i, action: 'grab' },
      { pattern: /move|place|put/i, action: 'move' },
      { pattern: /drop|release|let go/i, action: 'drop' },
      { pattern: /rotate|turn|spin/i, action: 'rotate' }
    ]);

    // System commands
    this.commandPatterns.set('system', [
      { pattern: /open|launch|start/i, action: 'open' },
      { pattern: /close|exit|quit/i, action: 'close' },
      { pattern: /settings|preferences|options/i, action: 'settings' },
      { pattern: /help|assist|what can you do/i, action: 'help' }
    ]);

    // AI commands
    this.commandPatterns.set('ai', [
      { pattern: /tell me|explain|describe/i, action: 'explain' },
      { pattern: /remember|save|keep/i, action: 'remember' },
      { pattern: /search|look for|find information/i, action: 'search' },
      { pattern: /create|make|generate/i, action: 'create' }
    ]);

    console.log('✅ Command patterns set up');
  }

  async initializeVoiceProfile() {
    console.log('👤 Initializing voice profile...');

    // Voice profile for personalized recognition
    this.voiceProfile = {
      userId: 'default_user',
      language: this.currentLanguage,
      accent: 'neutral',
      pitch: 'normal',
      speed: 'normal',
      adaptationLevel: 0.5,
      lastCalibration: Date.now()
    };

    console.log('✅ Voice profile initialized');
  }

  async startListening(options = {}) {
    if (!this.isInitialized) {
      throw new Error('Voice input not initialized');
    }

    const {
      continuous = false,
      interimResults = false,
      language = this.currentLanguage
    } = options;

    this.continuousMode = continuous;
    this.interimResults = interimResults;
    this.currentLanguage = language;

    if (this.recognition) {
      this.recognition.lang = language;
      this.recognition.continuous = continuous;
      this.recognition.interimResults = interimResults;
      this.recognition.start();
    }
  }

  async stopListening() {
    if (this.recognition && this.isListening) {
      this.recognition.stop();
    }
  }

  handleRecognitionResult(event) {
    // In production, this would handle actual speech recognition results
    // For simulation, we'll generate mock results

    const result = {
      transcript: this.generateMockTranscript(),
      confidence: 0.85 + Math.random() * 0.14,
      isFinal: true,
      alternatives: [
        { transcript: this.generateMockTranscript(), confidence: 0.75 },
        { transcript: this.generateMockTranscript(), confidence: 0.65 }
      ],
      timestamp: Date.now()
    };

    this.emit('speechResult', result);

    // Process for commands
    const command = this.parseCommand(result.transcript);
    if (command) {
      this.emit('voiceCommand', command);
    }
  }

  generateMockTranscript() {
    const samplePhrases = [
      'Show me the nearest object',
      'Navigate to the table',
      'Tell me about my surroundings',
      'Create a new panel',
      'Open settings',
      'What can you see',
      'Help me with this task',
      'Remember this location'
    ];
    return samplePhrases[Math.floor(Math.random() * samplePhrases.length)];
  }

  parseCommand(transcript) {
    const lowerTranscript = transcript.toLowerCase();

    for (const [category, patterns] of this.commandPatterns) {
      for (const { pattern, action } of patterns) {
        if (pattern.test(lowerTranscript)) {
          return {
            category,
            action,
            transcript,
            confidence: 0.9,
            timestamp: Date.now()
          };
        }
      }
    }

    // If no specific command, treat as general query
    return {
      category: 'query',
      action: 'general',
      transcript,
      confidence: 0.8,
      timestamp: Date.now()
    };
  }

  handleRecognitionError(error) {
    console.error('Speech recognition error:', error);

    const errorTypes = {
      'no-speech': 'No speech detected',
      'audio-capture': 'Audio capture failed',
      'not-allowed': 'Microphone permission denied',
      'network': 'Network error',
      'aborted': 'Recognition aborted'
    };

    const errorMessage = errorTypes[error.error] || 'Unknown error';
    this.emit('recognitionError', { error: error.error, message: errorMessage });
  }

  async calibrateVoice() {
    console.log('🎚️ Calibrating voice recognition...');

    // Simulate voice calibration process
    await new Promise(resolve => setTimeout(resolve, 2000));

    this.voiceProfile.adaptationLevel = 0.8;
    this.voiceProfile.lastCalibration = Date.now();

    console.log('✅ Voice calibration complete');
    this.emit('voiceCalibrated', this.voiceProfile);
  }

  async setLanguage(language) {
    console.log(`🌍 Setting language to: ${language}`);

    this.currentLanguage = language;
    this.voiceProfile.language = language;

    if (this.recognition) {
      this.recognition.lang = language;
    }

    this.emit('languageChanged', language);
  }

  async enableContinuousMode(enabled) {
    this.continuousMode = enabled;

    if (this.recognition) {
      this.recognition.continuous = enabled;
    }

    console.log(`Continuous mode: ${enabled ? 'enabled' : 'disabled'}`);
  }

  getVoiceProfile() {
    return { ...this.voiceProfile };
  }

  async update() {
    if (!this.isInitialized) return;

    try {
      // Update voice recognition state
      if (this.isListening && this.continuousMode) {
        // Continuous listening updates
      }

    } catch (error) {
      console.error('Error updating voice input:', error);
    }
  }

  async shutdown() {
    console.log('🛑 Shutting down voice input system...');

    if (this.isListening) {
      await this.stopListening();
    }

    this.isInitialized = false;
    this.commandPatterns.clear();
    this.voiceProfile = null;

    console.log('✅ Voice input system shut down');
  }
}

module.exports = { VoiceInput };