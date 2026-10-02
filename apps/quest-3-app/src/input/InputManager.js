/**
 * SynthOS Input Manager
 * Unified input handling for gesture, gaze, controller, and voice input
 */

const EventEmitter = require('eventemitter3');

class InputManager extends EventEmitter {
  constructor(spatialSystem, voiceInput) {
    super();
    this.spatial = spatialSystem;
    this.voice = voiceInput;
    this.inputState = {
      gestures: [],
      gaze: null,
      controllers: [],
      voice: null,
      combined: []
    };
    this.inputMode = 'mixed'; // gesture, gaze, controller, voice, mixed
    this.gestureThresholds = {
      pinch: 0.05,
      grab: 0.08,
      point: 0.1
    };
    this.gazeDwellTime = 1000; // 1 second
    this.isInitialized = false;
    this.activeInputs = new Set();
  }

  async initialize() {
    console.log('🎮 Initializing input manager...');

    try {
      // Set up gesture input handlers
      await this.setupGestureHandlers();

      // Set up gaze input handlers
      await this.setupGazeHandlers();

      // Set up controller input handlers
      await this.setupControllerHandlers();

      // Set up voice input handlers
      await this.setupVoiceHandlers();

      // Set up combined input processing
      await this.setupCombinedInput();

      this.isInitialized = true;
      console.log('✅ Input manager initialized successfully!');

    } catch (error) {
      console.error('❌ Failed to initialize input manager:', error);
      throw error;
    }
  }

  async setupGestureHandlers() {
    console.log('👆 Setting up gesture handlers...');

    this.spatial.on('contextUpdate', (context) => {
      if (context.hands) {
        this.processGestures(context.hands);
      }
    });

    console.log('✅ Gesture handlers set up');
  }

  async setupGazeHandlers() {
    console.log('👁️ Setting up gaze handlers...');

    this.spatial.on('contextUpdate', (context) => {
      if (context.gaze) {
        this.processGaze(context.gaze);
      }
    });

    console.log('✅ Gaze handlers set up');
  }

  async setupControllerHandlers() {
    console.log('🎮 Setting up controller handlers...');

    // In production, this would set up actual controller input
    this.controllerState = {
      left: {
        connected: true,
        position: { x: -0.2, y: 0.5, z: -0.3 },
        rotation: { x: 0, y: 0, z: 0 },
        buttons: {
          trigger: 0,
          grip: 0,
          a: false,
          b: false,
          x: false,
          y: false,
          joystick: { x: 0, y: 0 }
        }
      },
      right: {
        connected: true,
        position: { x: 0.2, y: 0.5, z: -0.3 },
        rotation: { x: 0, y: 0, z: 0 },
        buttons: {
          trigger: 0,
          grip: 0,
          a: false,
          b: false,
          x: false,
          y: false,
          joystick: { x: 0, y: 0 }
        }
      }
    };

    console.log('✅ Controller handlers set up');
  }

  async setupVoiceHandlers() {
    console.log('🎤 Setting up voice handlers...');

    this.voice.on('voiceCommand', (command) => {
      this.processVoiceCommand(command);
    });

    this.voice.on('speechResult', (result) => {
      this.processSpeechResult(result);
    });

    console.log('✅ Voice handlers set up');
  }

  async setupCombinedInput() {
    console.log('🔗 Setting up combined input processing...');

    // Process multi-modal input combinations
    setInterval(() => {
      this.processCombinedInput();
    }, 100);

    console.log('✅ Combined input processing set up');
  }

  processGestures(hands) {
    const gestures = [];

    hands.forEach(hand => {
      const gesture = this.detectGesture(hand);
      if (gesture) {
        gestures.push({
          type: gesture.type,
          hand: hand.id,
          confidence: gesture.confidence,
          position: hand.position,
          timestamp: Date.now()
        });
      }
    });

    this.inputState.gestures = gestures;

    if (gestures.length > 0) {
      this.emit('gestureInput', gestures);
      this.activeInputs.add('gesture');
    }
  }

  detectGesture(hand) {
    const thumb = hand.fingers.find(f => f.name === 'thumb');
    const index = hand.fingers.find(f => f.name === 'index');
    const middle = hand.fingers.find(f => f.name === 'middle');
    const ring = hand.fingers.find(f => f.name === 'ring');
    const pinky = hand.fingers.find(f => f.name === 'pinky');

    if (!thumb || !index) return null;

    // Pinch gesture
    if (thumb.extended && index.extended) {
      const distance = Math.sqrt(
        Math.pow(thumb.position.x - index.position.x, 2) +
        Math.pow(thumb.position.y - index.position.y, 2) +
        Math.pow(thumb.position.z - index.position.z, 2)
      );

      if (distance < this.gestureThresholds.pinch) {
        return { type: 'pinch', confidence: 0.9 };
      }
    }

    // Point gesture
    if (index.extended && !middle.extended && !ring.extended && !pinky.extended) {
      return { type: 'point', confidence: 0.85 };
    }

    // Grab gesture
    if (thumb.extended && index.extended && middle.extended && ring.extended && pinky.extended) {
      return { type: 'grab', confidence: 0.8 };
    }

    // Thumbs up
    if (thumb.extended && !index.extended && !middle.extended && !ring.extended && !pinky.extended) {
      return { type: 'thumbs-up', confidence: 0.9 };
    }

    // Wave (detected over time)
    if (hand.confidence > 0.8) {
      return { type: 'wave', confidence: 0.75 };
    }

    return null;
  }

  processGaze(gaze) {
    this.inputState.gaze = {
      point: gaze.point,
      direction: gaze.direction,
      confidence: gaze.confidence,
      timestamp: gaze.timestamp
    };

    this.emit('gazeInput', this.inputState.gaze);
    this.activeInputs.add('gaze');
  }

  processVoiceCommand(command) {
    this.inputState.voice = {
      type: 'command',
      category: command.category,
      action: command.action,
      transcript: command.transcript,
      confidence: command.confidence,
      timestamp: command.timestamp
    };

    this.emit('voiceInput', this.inputState.voice);
    this.activeInputs.add('voice');
  }

  processSpeechResult(result) {
    if (!this.inputState.voice || this.inputState.voice.type !== 'command') {
      this.inputState.voice = {
        type: 'speech',
        transcript: result.transcript,
        confidence: result.confidence,
        timestamp: result.timestamp
      };

      this.emit('voiceInput', this.inputState.voice);
      this.activeInputs.add('voice');
    }
  }

  processCombinedInput() {
    const combined = [];

    // Gesture + Gaze combination
    if (this.inputState.gestures.length > 0 && this.inputState.gaze) {
      this.inputState.gestures.forEach(gesture => {
        combined.push({
          type: 'gesture_gaze',
          gesture: gesture.type,
          gazePoint: this.inputState.gaze.point,
          handPosition: gesture.position,
          timestamp: Date.now()
        });
      });
    }

    // Voice + Gesture combination
    if (this.inputState.voice && this.inputState.gestures.length > 0) {
      combined.push({
        type: 'voice_gesture',
        voice: this.inputState.voice.transcript,
        gesture: this.inputState.gestures[0].type,
        timestamp: Date.now()
      });
    }

    // Controller + Gaze combination
    if (this.controllerState && this.inputState.gaze) {
      combined.push({
        type: 'controller_gaze',
        controllerPosition: this.controllerState.right.position,
        gazePoint: this.inputState.gaze.point,
        timestamp: Date.now()
      });
    }

    this.inputState.combined = combined;

    if (combined.length > 0) {
      this.emit('combinedInput', combined);
    }
  }

  setInputMode(mode) {
    const validModes = ['gesture', 'gaze', 'controller', 'voice', 'mixed'];
    if (validModes.includes(mode)) {
      this.inputMode = mode;
      console.log(`Input mode set to: ${mode}`);
      this.emit('inputModeChanged', mode);
    }
  }

  setGestureThreshold(gesture, threshold) {
    if (this.gestureThresholds[gesture] !== undefined) {
      this.gestureThresholds[gesture] = threshold;
      console.log(`Gesture threshold for ${gesture} set to: ${threshold}`);
    }
  }

  setGazeDwellTime(time) {
    this.gazeDwellTime = time;
    console.log(`Gaze dwell time set to: ${time}ms`);
  }

  getControllerState(controller) {
    return this.controllerState[controller] || null;
  }

  updateControllerButton(controller, button, value) {
    if (this.controllerState[controller]) {
      this.controllerState[controller].buttons[button] = value;
      this.emit('controllerInput', {
        controller,
        button,
        value,
        timestamp: Date.now()
      });
      this.activeInputs.add('controller');
    }
  }

  updateControllerPosition(controller, position, rotation) {
    if (this.controllerState[controller]) {
      this.controllerState[controller].position = position;
      this.controllerState[controller].rotation = rotation;
      this.emit('controllerMove', {
        controller,
        position,
        rotation,
        timestamp: Date.now()
      });
    }
  }

  getInputState() {
    return {
      ...this.inputState,
      inputMode: this.inputMode,
      activeInputs: Array.from(this.activeInputs)
    };
  }

  async startVoiceListening(options = {}) {
    await this.voice.startListening(options);
  }

  async stopVoiceListening() {
    await this.voice.stopListening();
  }

  async update() {
    if (!this.isInitialized) return;

    try {
      // Update controller state (in production, this would poll actual controllers)
      // Poll controller inputs...

      // Process any buffered inputs
      this.processCombinedInput();

    } catch (error) {
      console.error('Error updating input manager:', error);
    }
  }

  isInputActive(inputType) {
    return this.activeInputs.has(inputType);
  }

  getActiveInputs() {
    return Array.from(this.activeInputs);
  }

  async shutdown() {
    console.log('🛑 Shutting down input manager...');

    this.activeInputs.clear();
    this.inputState = {
      gestures: [],
      gaze: null,
      controllers: [],
      voice: null,
      combined: []
    };

    this.isInitialized = false;

    console.log('✅ Input manager shut down');
  }
}

module.exports = { InputManager };