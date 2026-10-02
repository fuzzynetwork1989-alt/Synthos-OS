/**
 * SynthOS Holographic UI System
 * 3D spatial interface elements positioned in physical space
 */

const EventEmitter = require('eventemitter3');

class HolographicUI extends EventEmitter {
  constructor(spatialSystem, aiSystem) {
    super();
    this.spatial = spatialSystem;
    this.ai = aiSystem;
    this.uiElements = new Map();
    this.activePanel = null;
    this.isInitialized = false;
    this.interactionMode = 'gesture'; // gesture, gaze, controller
  }

  async initialize() {
    console.log('🎨 Initializing holographic UI system...');

    try {
      // Initialize UI components
      await this.initializeUIComponents();

      // Set up interaction handlers
      await this.setupInteractionHandlers();

      // Create default UI layout
      await this.createDefaultLayout();

      this.isInitialized = true;
      console.log('✅ Holographic UI initialized successfully!');

    } catch (error) {
      console.error('❌ Failed to initialize holographic UI:', error);
      throw error;
    }
  }

  async initializeUIComponents() {
    console.log('🔧 Initializing UI components...');

    // In production, this would initialize 3D rendering, etc.
    this.uiComponents = {
      panels: new Map(),
      buttons: new Map(),
      textFields: new Map(),
      sliders: new Map(),
      menus: new Map()
    };

    console.log('✅ UI components initialized');
  }

  async setupInteractionHandlers() {
    console.log('👆 Setting up interaction handlers...');

    // Hand gesture interactions
    this.spatial.on('contextUpdate', (context) => {
      this.handleGestureInteractions(context);
    });

    // Gaze interactions
    this.spatial.on('contextUpdate', (context) => {
      this.handleGazeInteractions(context);
    });

    console.log('✅ Interaction handlers set up');
  }

  async createDefaultLayout() {
    console.log('📐 Creating default UI layout...');

    // Create main control panel
    await this.createControlPanel();

    // Create AI assistant panel
    await this.createAIAssistantPanel();

    // Create status display
    await this.createStatusDisplay();

    console.log('✅ Default UI layout created');
  }

  async createControlPanel() {
    const panel = {
      id: 'control_panel',
      type: 'panel',
      position: { x: 0, y: 1.2, z: -1.5 },
      rotation: { x: 0, y: 0, z: 0 },
      size: { width: 0.4, height: 0.3 },
      title: 'SynthOS Controls',
      buttons: [
        { id: 'btn_voice', label: 'Voice', position: { x: -0.15, y: 0.1, z: 0 } },
        { id: 'btn_gesture', label: 'Gesture', position: { x: 0, y: 0.1, z: 0 } },
        { id: 'btn_settings', label: 'Settings', position: { x: 0.15, y: 0.1, z: 0 } }
      ]
    };

    this.uiComponents.panels.set(panel.id, panel);
    this.uiElements.set(panel.id, panel);
  }

  async createAIAssistantPanel() {
    const panel = {
      id: 'ai_assistant_panel',
      type: 'panel',
      position: { x: 0.3, y: 1.0, z: -1.2 },
      rotation: { x: 0, y: -0.3, z: 0 },
      size: { width: 0.35, height: 0.5 },
      title: 'AI Assistant',
      content: {
        type: 'text',
        text: 'Hello! I\'m your spatial AI assistant. How can I help you today?',
        editable: true
      },
      buttons: [
        { id: 'btn_send', label: 'Send', position: { x: 0, y: -0.2, z: 0 } }
      ]
    };

    this.uiComponents.panels.set(panel.id, panel);
    this.uiElements.set(panel.id, panel);
  }

  async createStatusDisplay() {
    const panel = {
      id: 'status_display',
      type: 'panel',
      position: { x: -0.3, y: 1.3, z: -1.2 },
      rotation: { x: 0, y: 0.3, z: 0 },
      size: { width: 0.25, height: 0.2 },
      title: 'System Status',
      content: {
        type: 'status',
        items: [
          { label: 'Spatial', value: 'Active' },
          { label: 'AI', value: 'Ready' },
          { label: 'Hands', value: 'Tracking' },
          { label: 'Gaze', value: 'Tracking' }
        ]
      }
    };

    this.uiComponents.panels.set(panel.id, panel);
    this.uiElements.set(panel.id, panel);
  }

  async update() {
    if (!this.isInitialized) return;

    try {
      // Update UI element positions based on spatial context
      await this.updateUIPositions();

      // Update UI content
      await this.updateUIContent();

      // Handle animations
      await this.updateAnimations();

    } catch (error) {
      console.error('Error updating UI:', error);
    }
  }

  async updateUIPositions() {
    // Update UI positions based on user movement
    // In production, this would anchor UI elements to spatial anchors
  }

  async updateUIContent() {
    // Update dynamic content like AI responses, status, etc.
    const statusPanel = this.uiComponents.panels.get('status_display');
    if (statusPanel && this.spatial.spatialContext) {
      // Update status based on spatial context
    }
  }

  async updateAnimations() {
    // Update UI animations and transitions
  }

  handleGestureInteractions(context) {
    if (!context.hands) return;

    // Detect pinch gestures for button presses
    context.hands.forEach(hand => {
      if (this.detectPinchGesture(hand)) {
        this.handlePinchInteraction(hand);
      }
    });
  }

  handleGazeInteractions(context) {
    if (!context.gaze) return;

    // Detect gaze-based selections
    const gazedElement = this.findElementAtGazePoint(context.gaze.point);
    if (gazedElement) {
      this.handleGazeSelection(gazedElement);
    }
  }

  detectPinchGesture(hand) {
    // Simulated pinch detection
    const thumb = hand.fingers.find(f => f.name === 'thumb');
    const index = hand.fingers.find(f => f.name === 'index');

    if (thumb && index && thumb.extended && index.extended) {
      const distance = Math.sqrt(
        Math.pow(thumb.position.x - index.position.x, 2) +
        Math.pow(thumb.position.y - index.position.y, 2) +
        Math.pow(thumb.position.z - index.position.z, 2)
      );
      return distance < 0.05; // 5cm threshold
    }

    return false;
  }

  handlePinchInteraction(hand) {
    const interactedElement = this.findElementAtHandPosition(hand.position);
    if (interactedElement) {
      this.emit('elementInteracted', {
        element: interactedElement,
        interaction: 'pinch',
        hand: hand.id
      });
    }
  }

  findElementAtGazePoint(gazePoint) {
    // Find UI element at gaze point
    for (const [id, element] of this.uiElements) {
      if (this.isPointInElement(gazePoint, element)) {
        return element;
      }
    }
    return null;
  }

  findElementAtHandPosition(handPosition) {
    // Find UI element at hand position
    for (const [id, element] of this.uiElements) {
      if (this.isPointInElement(handPosition, element)) {
        return element;
      }
    }
    return null;
  }

  isPointInElement(point, element) {
    // Simple bounding box check
    if (!element.position || !element.size) return false;

    const halfWidth = element.size.width / 2;
    const halfHeight = element.size.height / 2;

    return (
      point.x >= element.position.x - halfWidth &&
      point.x <= element.position.x + halfWidth &&
      point.y >= element.position.y - halfHeight &&
      point.y <= element.position.y + halfHeight
    );
  }

  handleGazeSelection(element) {
    this.emit('elementGazed', {
      element: element,
      duration: 1000 // 1 second gaze duration
    });
  }

  async createPanel(config) {
    const panel = {
      id: config.id || `panel_${Date.now()}`,
      type: 'panel',
      position: config.position || { x: 0, y: 1.0, z: -1.0 },
      rotation: config.rotation || { x: 0, y: 0, z: 0 },
      size: config.size || { width: 0.3, height: 0.2 },
      title: config.title || 'Panel',
      content: config.content || null,
      buttons: config.buttons || []
    };

    this.uiComponents.panels.set(panel.id, panel);
    this.uiElements.set(panel.id, panel);

    return panel;
  }

  async removePanel(panelId) {
    this.uiComponents.panels.delete(panelId);
    this.uiElements.delete(panelId);
  }

  async showAIResponse(response) {
    const aiPanel = this.uiComponents.panels.get('ai_assistant_panel');
    if (aiPanel && aiPanel.content) {
      aiPanel.content.text = response;
      this.emit('uiUpdated', { panel: aiPanel });
    }
  }

  async setInteractionMode(mode) {
    this.interactionMode = mode;
    console.log(`Interaction mode set to: ${mode}`);
  }

  async shutdown() {
    console.log('🛑 Shutting down holographic UI...');

    this.isInitialized = false;
    this.uiElements.clear();
    this.uiComponents.panels.clear();
    this.uiComponents.buttons.clear();
    this.uiComponents.textFields.clear();
    this.uiComponents.sliders.clear();
    this.uiComponents.menus.clear();

    console.log('✅ Holographic UI shut down');
  }
}

module.exports = { HolographicUI };