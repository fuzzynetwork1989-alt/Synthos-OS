// Custom hook for model gateway integration
import { useState, useEffect, useCallback } from 'react';
import { modelGatewayService, GenerationRequest, GenerationResponse } from '../services/modelGateway';

export function useModelGateway() {
  const [availableModels, setAvailableModels] = useState<any[]>([]);
  const [preferredModel, setPreferredModel] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [localModelHealthy, setLocalModelHealthy] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    initialize();
  }, []);

  const initialize = async () => {
    try {
      setLoading(true);
      const models = await modelGatewayService.getAvailableModels();
      setAvailableModels(models);
      setPreferredModel(modelGatewayService.getPreferredModel());
      
      const healthy = await modelGatewayService.checkLocalModelHealth();
      setLocalModelHealthy(healthy);
    } catch (error) {
      console.error('Model gateway initialization failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateResponse = useCallback(async (request: GenerationRequest): Promise<GenerationResponse> => {
    try {
      setIsGenerating(true);
      return await modelGatewayService.generateResponse(request);
    } catch (error) {
      console.error('Generation failed:', error);
      throw error;
    } finally {
      setIsGenerating(false);
    }
  }, []);

  const streamResponse = useCallback(async (
    request: GenerationRequest,
    onChunk: (chunk: string) => void
  ): Promise<GenerationResponse> => {
    try {
      setIsGenerating(true);
      return await modelGatewayService.streamResponse(request, onChunk);
    } catch (error) {
      console.error('Streaming failed:', error);
      throw error;
    } finally {
      setIsGenerating(false);
    }
  }, []);

  const setModelPreference = useCallback(async (modelId: string) => {
    try {
      await modelGatewayService.setPreferredModel(modelId);
      setPreferredModel(modelId);
    } catch (error) {
      console.error('Failed to set model preference:', error);
    }
  }, []);

  const pullModel = useCallback(async (modelName: string) => {
    try {
      await modelGatewayService.pullModel(modelName);
      await initialize(); // Refresh available models
    } catch (error) {
      console.error('Failed to pull model:', error);
      throw error;
    }
  }, []);

  const refreshModels = useCallback(async () => {
    await initialize();
  }, []);

  return {
    availableModels,
    preferredModel,
    isGenerating,
    localModelHealthy,
    loading,
    generateResponse,
    streamResponse,
    setModelPreference,
    pullModel,
    refreshModels,
  };
}