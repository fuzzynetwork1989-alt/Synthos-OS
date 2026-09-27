// Model Gateway Service for AI model integration
import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-community/netinfo';

const MODEL_GATEWAY_URL = process.env.MODEL_GATEWAY_URL || 'https://model-gateway.synthos-os.local';
const OLLAMA_BASE_URL = process.env.OLLAMA_BASE_URL || 'http://localhost:11434';

interface ModelConfig {
  id: string;
  name: string;
  provider: 'ollama' | 'openai' | 'anthropic' | 'local';
  type: 'chat' | 'completion' | 'embedding';
  parameters?: {
    temperature?: number;
    maxTokens?: number;
    topP?: number;
    frequencyPenalty?: number;
    presencePenalty?: number;
  };
}

interface GenerationRequest {
  prompt: string;
  modelId?: string;
  temperature?: number;
  maxTokens?: number;
  stream?: boolean;
}

interface GenerationResponse {
  content: string;
  model: string;
  tokens: number;
  latency: number;
}

class ModelGatewayService {
  private gatewayUrl: string;
  private ollamaUrl: string;
  private preferredModel: string | null = null;

  constructor() {
    this.gatewayUrl = MODEL_GATEWAY_URL;
    this.ollamaUrl = OLLAMA_BASE_URL;
    this.loadPreferences();
  }

  private async loadPreferences(): Promise<void> {
    try {
      this.preferredModel = await AsyncStorage.getItem('preferred_model');
    } catch (error) {
      console.error('Failed to load model preferences:', error);
    }
  }

  private async savePreferences(modelId: string): Promise<void> {
    try {
      this.preferredModel = modelId;
      await AsyncStorage.setItem('preferred_model', modelId);
    } catch (error) {
      console.error('Failed to save model preferences:', error);
    }
  }

  private async isOnline(): Promise<boolean> {
    const state = await NetInfo.fetch();
    return state.isConnected ?? false;
  }

  async getAvailableModels(): Promise<ModelConfig[]> {
    try {
      const online = await this.isOnline();
      
      if (online) {
        // Try cloud gateway first
        try {
          const response = await fetch(`${this.gatewayUrl}/models`);
          if (response.ok) {
            return await response.json();
          }
        } catch (error) {
          console.warn('Cloud gateway unavailable, falling back to local');
        }
      }

      // Fall back to local Ollama
      try {
        const response = await fetch(`${this.ollamaUrl}/api/tags`);
        if (response.ok) {
          const data = await response.json();
          return data.models.map((model: any) => ({
            id: model.name,
            name: model.name,
            provider: 'ollama' as const,
            type: 'chat' as const,
          }));
        }
      } catch (error) {
        console.error('Local Ollama unavailable:', error);
      }

      return [];
    } catch (error) {
      console.error('Failed to get available models:', error);
      return [];
    }
  }

  async generateResponse(request: GenerationRequest): Promise<GenerationResponse> {
    const startTime = Date.now();
    const modelId = request.modelId || this.preferredModel || 'llama2';

    try {
      const online = await this.isOnline();
      
      if (online) {
        // Try cloud gateway first
        try {
          const response = await fetch(`${this.gatewayUrl}/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              prompt: request.prompt,
              model: modelId,
              temperature: request.temperature || 0.7,
              max_tokens: request.maxTokens || 2048,
              stream: request.stream || false,
            }),
          });

          if (response.ok) {
            const data = await response.json();
            return {
              content: data.content,
              model: data.model,
              tokens: data.tokens || 0,
              latency: Date.now() - startTime,
            };
          }
        } catch (error) {
          console.warn('Cloud generation failed, falling back to local');
        }
      }

      // Fall back to local Ollama
      const response = await fetch(`${this.ollamaUrl}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: modelId,
          prompt: request.prompt,
          stream: false,
          options: {
            temperature: request.temperature || 0.7,
            num_predict: request.maxTokens || 2048,
          },
        }),
      });

      if (!response.ok) {
        throw new Error(`Local model generation failed: ${response.status}`);
      }

      const data = await response.json();
      return {
        content: data.response,
        model: data.model,
        tokens: data.eval_count || 0,
        latency: Date.now() - startTime,
      };
    } catch (error) {
      console.error('Generation failed:', error);
      throw new Error('Failed to generate response. Please check your connection.');
    }
  }

  async streamResponse(
    request: GenerationRequest,
    onChunk: (chunk: string) => void
  ): Promise<GenerationResponse> {
    const startTime = Date.now();
    const modelId = request.modelId || this.preferredModel || 'llama2';
    let fullContent = '';

    try {
      const online = await this.isOnline();
      
      if (online) {
        // Try cloud gateway streaming
        try {
          const response = await fetch(`${this.gatewayUrl}/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              prompt: request.prompt,
              model: modelId,
              temperature: request.temperature || 0.7,
              max_tokens: request.maxTokens || 2048,
              stream: true,
            }),
          });

          if (response.ok && response.body) {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
              const { done, value } = await reader.read();
              if (done) break;

              const chunk = decoder.decode(value);
              // Parse SSE format
              const lines = chunk.split('\n');
              for (const line of lines) {
                if (line.startsWith('data: ')) {
                  const data = JSON.parse(line.slice(6));
                  if (data.content) {
                    fullContent += data.content;
                    onChunk(data.content);
                  }
                }
              }
            }

            return {
              content: fullContent,
              model: modelId,
              tokens: fullContent.split(' ').length,
              latency: Date.now() - startTime,
            };
          }
        } catch (error) {
          console.warn('Cloud streaming failed, falling back to local');
        }
      }

      // Fall back to local Ollama streaming
      const response = await fetch(`${this.ollamaUrl}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: modelId,
          prompt: request.prompt,
          stream: true,
          options: {
            temperature: request.temperature || 0.7,
            num_predict: request.maxTokens || 2048,
          },
        }),
      });

      if (!response.ok || !response.body) {
        throw new Error('Local streaming failed');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        for (const line of lines) {
          try {
            const data = JSON.parse(line);
            if (data.response) {
              fullContent += data.response;
              onChunk(data.response);
            }
          } catch (e) {
            // Skip invalid JSON
          }
        }
      }

      return {
        content: fullContent,
        model: modelId,
        tokens: fullContent.split(' ').length,
        latency: Date.now() - startTime,
      };
    } catch (error) {
      console.error('Streaming failed:', error);
      throw new Error('Failed to stream response');
    }
  }

  async setPreferredModel(modelId: string): Promise<void> {
    await this.savePreferences(modelId);
  }

  getPreferredModel(): string | null {
    return this.preferredModel;
  }

  async checkLocalModelHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${this.ollamaUrl}/api/tags`, {
        method: 'GET',
      });
      return response.ok;
    } catch (error) {
      return false;
    }
  }

  async pullModel(modelName: string): Promise<void> {
    try {
      const response = await fetch(`${this.ollamaUrl}/api/pull`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: modelName, stream: false }),
      });

      if (!response.ok) {
        throw new Error(`Failed to pull model: ${response.status}`);
      }
    } catch (error) {
      console.error('Model pull failed:', error);
      throw new Error('Failed to download model');
    }
  }
}

export const modelGatewayService = new ModelGatewayService();
export default ModelGatewayService;