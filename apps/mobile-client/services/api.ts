// API Service for backend communication
import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-community/netinfo';

const API_BASE_URL = process.env.API_BASE_URL || 'https://api.synthos-os.local';
const API_TIMEOUT = 30000;

class ApiService {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
    this.loadToken();
  }

  private async loadToken(): Promise<void> {
    try {
      this.token = await AsyncStorage.getItem('auth_token');
    } catch (error) {
      console.error('Failed to load auth token:', error);
    }
  }

  private async saveToken(token: string): Promise<void> {
    try {
      this.token = token;
      await AsyncStorage.setItem('auth_token', token);
    } catch (error) {
      console.error('Failed to save auth token:', error);
    }
  }

  private async clearToken(): Promise<void> {
    try {
      this.token = null;
      await AsyncStorage.removeItem('auth_token');
    } catch (error) {
      console.error('Failed to clear auth token:', error);
    }
  }

  private getHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  private async isOnline(): Promise<boolean> {
    const state = await NetInfo.fetch();
    return state.isConnected ?? false;
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const online = await this.isOnline();
    if (!online) {
      throw new Error('Network unavailable. Please check your connection.');
    }

    const url = `${this.baseUrl}${endpoint}`;
    const config: RequestInit = {
      ...options,
      headers: {
        ...this.getHeaders(),
        ...options.headers,
      },
      signal: AbortSignal.timeout(API_TIMEOUT),
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        if (response.status === 401) {
          await this.clearToken();
          throw new Error('Authentication failed. Please login again.');
        }
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('An unexpected error occurred');
    }
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async put<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }

  // Authentication methods
  async login(email: string, password: string): Promise<{ token: string; user: any }> {
    const response = await this.post<{ token: string; user: any }>('/auth/login', {
      email,
      password,
    });
    await this.saveToken(response.token);
    return response;
  }

  async register(email: string, password: string, name: string): Promise<{ token: string; user: any }> {
    const response = await this.post<{ token: string; user: any }>('/auth/register', {
      email,
      password,
      name,
    });
    await this.saveToken(response.token);
    return response;
  }

  async logout(): Promise<void> {
    await this.clearToken();
  }

  async getCurrentUser(): Promise<any> {
    return this.get<any>('/auth/me');
  }

  // Memory methods
  async getMemories(): Promise<any[]> {
    return this.get<any[]>('/memory');
  }

  async createMemory(content: string, metadata?: any): Promise<any> {
    return this.post<any>('/memory', { content, metadata });
  }

  async updateMemory(id: string, content: string, metadata?: any): Promise<any> {
    return this.put<any>(`/memory/${id}`, { content, metadata });
  }

  async deleteMemory(id: string): Promise<void> {
    return this.delete<void>(`/memory/${id}`);
  }

  // Tool methods
  async getTools(): Promise<any[]> {
    return this.get<any[]>('/tools');
  }

  async executeTool(toolId: string, params: any): Promise<any> {
    return this.post<any>(`/tools/${toolId}/execute`, params);
  }

  // Model methods
  async getModels(): Promise<any[]> {
    return this.get<any[]>('/models');
  }

  async generateResponse(prompt: string, modelId?: string): Promise<any> {
    return this.post<any>('/models/generate', { prompt, modelId });
  }
}

export const apiService = new ApiService();
export default ApiService;