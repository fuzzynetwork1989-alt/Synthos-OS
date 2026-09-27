/**
 * SynthOS AI Integration for Quest 3
 * Spatial AI assistant with environmental understanding and context-aware responses
 */

const EventEmitter = require('eventemitter3');
const axios = require('axios');

class SynthOSAI extends EventEmitter {
  constructor(spatialSystem) {
    super();
    this.spatial = spatialSystem;
    this.ollamaClient = null;
    this.contextMemory = [];
    this.spatialContext = null;
    this.isInitialized = false;
    this.currentModel = 'synthos-enhanced-20b';
    this.responseCache = new Map();
  }

  async initialize() {
    console.log('🧠 Initializing AI integration...');

    try {
      // Initialize Ollama client
      await this.initializeOllamaClient();

      // Set up spatial context listener
      this.spatial.on('contextUpdate', (context) => {
        this.spatialContext = context;
      });

      this.isInitialized = true;
      console.log('✅ AI integration initialized successfully!');

    } catch (error) {
      console.error('❌ Failed to initialize AI integration:', error);
      throw error;
    }
  }

  async initializeOllamaClient() {
    console.log('🔌 Connecting to Ollama service...');
    
    // In production, this would connect to the actual Ollama service
    this.ollamaClient = {
      baseURL: 'http://localhost:11434',
      model: this.currentModel,
      
      async chat(messages, options = {}) {
        // Simulated AI response (replace with actual Ollama API call)
        return this.simulateAIResponse(messages, options);
      },

      async generate(prompt, options = {}) {
        // Simulated text generation
        return this.simulateGeneration(prompt, options);
      }
    };

    console.log('✅ Ollama client initialized');
  }

  async update() {
    if (!this.isInitialized) return;

    try {
      // Process any pending AI tasks
      await this.processPendingTasks();
      
    } catch (error) {
      console.error('Error updating AI system:', error);
    }
  }

  async processSpatialQuery(query, options = {}) {
    if (!this.isInitialized) {
      throw new Error('AI system not initialized');
    }

    try {
      // Build context-aware messages
      const messages = this.buildContextualMessages(query);
      
      // Add spatial context to options
      const enhancedOptions = {
        ...options,
        spatial: true,
        context: this.spatialContext,
        environment: await this.getEnvironmentContext()
      };

      // Get AI response
      const response = await this.ollamaClient.chat(messages, enhancedOptions);
      
      // Cache response
      this.cacheResponse(query, response);
      
      // Add to context memory
      this.addToContextMemory(query, response);
      
      return response;
      
    } catch (error) {
      console.error('Error processing spatial query:', error);
      throw error;
    }
  }

  buildContextualMessages(query) {
    const systemMessage = {
      role: 'system',
      content: this.buildSystemPrompt()
    };

    const userMessage = {
      role: 'user',
      content: this.buildUserPrompt(query)
    };

    // Include recent context
    const contextMessages = this.getRecentContext().map(msg => ({
      role: msg.role,
      content: msg.content
    }));

    return [systemMessage, ...contextMessages, userMessage];
  }

  buildSystemPrompt() {
    let prompt = `You are SynthOS, a spatial AI assistant with full understanding of 3D environments. You help users in immersive XR/AR/VR spaces.`;

    if (this.spatialContext) {
      prompt += `\n\nCurrent Spatial Context:\n`;
      prompt += `Environment: ${JSON.stringify(this.spatialContext.environment)}\n`;
      prompt += `Nearby Objects: ${JSON.stringify(this.spatialContext.objects)}\n`;
      prompt += `Hand Position: ${JSON.stringify(this.spatialContext.hands)}\n`;
      prompt += `Gaze Direction: ${JSON.stringify(this.spatialContext.gaze)}\n`;
    }

    prompt += `\n\nYou can:\n`;
    prompt += `- Understand and operate in 3D space\n`;
    prompt += `- Provide contextual assistance based on surroundings\n`;
    prompt += `- Manipulate virtual objects in physical environment\n`;
    prompt += `- Give spatial directions and guidance\n`;
    prompt += `- Recognize and interact with real-world objects\n`;
    prompt += `- Adapt responses based on user's spatial position and gaze\n`;

    return prompt;
  }

  buildUserPrompt(query) {
    let prompt = query;

    if (this.spatialContext && this.spatialContext.gaze) {
      prompt += `\n\nI am currently looking at: ${JSON.stringify(this.spatialContext.gaze.point)}`;
    }

    if (this.spatialContext && this.spatialContext.hands) {
      prompt += `\n\nMy hands are positioned at: ${JSON.stringify(this.spatialContext.hands.map(h => h.position))}`;
    }

    return prompt;
  }

  async getEnvironmentContext() {
    if (!this.spatialContext) {
      return {};
    }

    return {
      room: this.spatialContext.environment,
      objects: this.spatialContext.objects,
      lighting: this.spatialContext.environment?.lighting,
      surfaces: this.spatialContext.environment?.surfaces
    };
  }

  getRecentContext(limit = 5) {
    return this.contextMemory.slice(-limit);
  }

  addToContextMemory(query, response) {
    this.contextMemory.push({
      role: 'user',
      content: query,
      timestamp: Date.now()
    });

    this.contextMemory.push({
      role: 'assistant',
      content: response.content || response,
      timestamp: Date.now()
    });

    // Keep memory size manageable
    if (this.contextMemory.length > 20) {
      this.contextMemory = this.contextMemory.slice(-10);
    }
  }

  cacheResponse(query, response) {
    const cacheKey = this.generateCacheKey(query);
    this.responseCache.set(cacheKey, {
      response,
      timestamp: Date.now()
    });

    // Clean old cache entries
    if (this.responseCache.size > 100) {
      const oldestKey = this.responseCache.keys().next().value;
      this.responseCache.delete(oldestKey);
    }
  }

  generateCacheKey(query) {
    return query.toLowerCase().trim().substring(0, 50);
  }

  getCachedResponse(query) {
    const cacheKey = this.generateCacheKey(query);
    const cached = this.responseCache.get(cacheKey);
    
    if (cached) {
      const age = Date.now() - cached.timestamp;
      // Cache expires after 5 minutes
      if (age < 300000) {
        return cached.response;
      }
    }
    
    return null;
  }

  async processPendingTasks() {
    // Process any background AI tasks
    // This could include proactive suggestions, environment analysis, etc.
  }

  // Simulation methods (replace with actual Ollama API calls)
  async simulateAIResponse(messages, options) {
    const userQuery = messages[messages.length - 1].content;
    
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 100 + Math.random() * 200));

    // Generate contextual response based on query
    const response = this.generateContextualResponse(userQuery, options);
    
    return {
      content: response,
      model: this.currentModel,
      timestamp: Date.now(),
      spatial: options.spatial || false
    };
  }

  generateContextualResponse(query, options) {
    const lowerQuery = query.toLowerCase();
    
    // Spatial navigation responses
    if (lowerQuery.includes('where') || lowerQuery.includes('find') || lowerQuery.includes('locate')) {
      return this.generateNavigationResponse(query);
    }
    
    // Object interaction responses
    if (lowerQuery.includes('grab') || lowerQuery.includes('pick') || lowerQuery.includes('move')) {
      return this.generateInteractionResponse(query);
    }
    
    // Information responses
    if (lowerQuery.includes('what') || lowerQuery.includes('tell') || lowerQuery.includes('explain')) {
      return this.generateInformationResponse(query);
    }
    
    // Default response
    return this.generateDefaultResponse(query);
  }

  generateNavigationResponse(query) {
    if (this.spatialContext && this.spatialContext.objects) {
      const objects = this.spatialContext.objects;
      const nearestObject = objects[0];
      
      if (nearestObject) {
        return `I can see a ${nearestObject.type} located at ${JSON.stringify(nearestObject.position)}. Would you like me to guide you there or help you interact with it?`;
      }
    }
    
    return "I'm scanning your environment to help you navigate. I can see your surroundings and can guide you to any object or location you're looking for.";
  }

  generateInteractionResponse(query) {
    if (this.spatialContext && this.spatialContext.hands) {
      const handPosition = this.spatialContext.hands[0]?.position;
      
      if (handPosition) {
        return `Your hands are currently at ${JSON.stringify(handPosition)}. I can help you interact with nearby objects. What would you like to grab or manipulate?`;
      }
    }
    
    return "I can help you interact with objects in your environment. I can guide your hands to the right position and assist with manipulation tasks.";
  }

  generateInformationResponse(query) {
    if (this.spatialContext && this.spatialContext.environment) {
      const env = this.spatialContext.environment;
      
      return `Based on your current environment, I can see you're in a space with dimensions ${JSON.stringify(env.roomBounds)}. The lighting conditions are ${env.lighting.ambient * 100}% ambient with directional lighting. Would you like more specific information about anything in your surroundings?`;
    }
    
    return "I'm analyzing your environment to provide you with relevant information. I can tell you about objects, spatial relationships, and help you understand your surroundings.";
  }

  generateDefaultResponse(query) {
    return `I understand you're asking about "${query}". As your spatial AI assistant, I can help you navigate your environment, interact with objects, and provide contextual information based on your current spatial context. How can I assist you further?`;
  }

  async simulateGeneration(prompt, options) {
    // Simulate text generation
    await new Promise(resolve => setTimeout(resolve, 150 + Math.random() * 100));
    
    return {
      text: `Generated response for: ${prompt}`,
      model: this.currentModel,
      timestamp: Date.now()
    };
  }

  async shutdown() {
    console.log('🛑 Shutting down AI integration...');
    
    this.isInitialized = false;
    this.contextMemory = [];
    this.responseCache.clear();
    
    console.log('✅ AI integration shut down');
  }
}

module.exports = { SynthOSAI };