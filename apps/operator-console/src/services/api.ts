// API Service for operator console backend communication
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
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
      if (typeof window !== 'undefined') {
        const token = localStorage.getItem('auth_token');
        if (token) {
          this.token = token;
        }
      }
    } catch (error) {
      console.error('Failed to load auth token:', error);
    }
  }

  private async saveToken(token: string): Promise<void> {
    try {
      this.token = token;
      if (typeof window !== 'undefined') {
        localStorage.setItem('auth_token', token);
      }
    } catch (error) {
      console.error('Failed to save auth token:', error);
    }
  }

  private async clearToken(): Promise<void> {
    try {
      this.token = null;
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token');
      }
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

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
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

  // System monitoring methods
  async getSystemStatus(): Promise<any> {
    return this.get<any>('/system/status');
  }

  async getSystemMetrics(): Promise<any> {
    return this.get<any>('/system/metrics');
  }

  async getCognitiveEngineStats(): Promise<any> {
    return this.get<any>('/cognitive/stats');
  }

  async getMemorySystemStats(): Promise<any> {
    return this.get<any>('/memory/stats');
  }

  async getToolGatewayStats(): Promise<any> {
    return this.get<any>('/tools/stats');
  }

  // User management methods
  async getUsers(): Promise<any[]> {
    return this.get<any[]>('/users');
  }

  async createUser(userData: any): Promise<any> {
    return this.post<any>('/users', userData);
  }

  async updateUser(userId: string, userData: any): Promise<any> {
    return this.put<any>(`/users/${userId}`, userData);
  }

  async deleteUser(userId: string): Promise<void> {
    return this.delete<void>(`/users/${userId}`);
  }

  // Model management methods
  async getModels(): Promise<any[]> {
    return this.get<any[]>('/models');
  }

  async deployModel(modelConfig: any): Promise<any> {
    return this.post<any>('/models/deploy', modelConfig);
  }

  async updateModel(modelId: string, config: any): Promise<any> {
    return this.put<any>(`/models/${modelId}`, config);
  }

  async deleteModel(modelId: string): Promise<void> {
    return this.delete<void>(`/models/${modelId}`);
  }
}

export const apiService = new ApiService();
export default ApiService;