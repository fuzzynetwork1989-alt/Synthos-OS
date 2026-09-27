/**
 * API Service for Operator Console
 * Handles communication with Synthos-OS backend services
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const MODEL_GATEWAY_URL = process.env.NEXT_PUBLIC_MODEL_GATEWAY_URL || 'http://localhost:8002';
const MEMORY_ENGINE_URL = process.env.NEXT_PUBLIC_MEMORY_ENGINE_URL || 'http://localhost:8003';
const RSI_ENGINE_URL = process.env.NEXT_PUBLIC_RSI_ENGINE_URL || 'http://localhost:8004';
const COGNITIVE_ENGINE_URL = process.env.NEXT_PUBLIC_COGNITIVE_ENGINE_URL || 'http://localhost:8005';
const TOOL_EXECUTION_URL = process.env.NEXT_PUBLIC_TOOL_EXECUTION_URL || 'http://localhost:8006';
const WORKFLOW_ENGINE_URL = process.env.NEXT_PUBLIC_WORKFLOW_ENGINE_URL || 'http://localhost:8007';
const POLICY_ENGINE_URL = process.env.NEXT_PUBLIC_POLICY_ENGINE_URL || 'http://localhost:8008';
const EVALUATION_ENGINE_URL = process.env.NEXT_PUBLIC_EVALUATION_ENGINE_URL || 'http://localhost:8009';
const DEVICE_GATEWAY_URL = process.env.NEXT_PUBLIC_DEVICE_GATEWAY_URL || 'http://localhost:8010';

interface HealthStatus {
  status: string;
  services?: Record<string, string>;
  timestamp?: string;
}

interface SystemMetrics {
  cpuUsage: number;
  memoryUsage: number;
  activeConnections: number;
  responseTime: number;
  localModel: boolean;
  memoryEngine: boolean;
  toolGateway: boolean;
}

interface ModelInfo {
  name: string;
  provider: string;
  capabilities: string[];
  context_length: number;
  parameters: string;
}

interface ChatMessage {
  role: string;
  content: string;
}

interface ChatRequest {
  messages: ChatMessage[];
  model?: string;
  provider?: string;
  temperature?: number;
  max_tokens?: number;
  stream?: boolean;
}

interface ChatResponse {
  content: string;
  model: string;
  provider: string;
  tokens_used: number;
  finish_reason: string;
}

interface MemoryEntry {
  id?: string;
  content: string;
  embedding?: number[];
  metadata?: Record<string, any>;
  tags?: string[];
  created_at?: string;
  updated_at?: string;
  ttl?: number;
}

interface MemorySearchRequest {
  query: string;
  query_embedding?: number[];
  limit?: number;
  filters?: Record<string, any>;
}

interface MemorySearchResponse {
  results: MemoryEntry[];
  total_count: number;
  search_time_ms: number;
}

class APIService {
  private baseUrl: string;
  private modelGatewayUrl: string;
  private memoryEngineUrl: string;
  private rsiEngineUrl: string;
  private cognitiveEngineUrl: string;
  private toolExecutionUrl: string;
  private workflowEngineUrl: string;
  private policyEngineUrl: string;
  private evaluationEngineUrl: string;
  private deviceGatewayUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
    this.modelGatewayUrl = MODEL_GATEWAY_URL;
    this.memoryEngineUrl = MEMORY_ENGINE_URL;
    this.rsiEngineUrl = RSI_ENGINE_URL;
    this.cognitiveEngineUrl = COGNITIVE_ENGINE_URL;
    this.toolExecutionUrl = TOOL_EXECUTION_URL;
    this.workflowEngineUrl = WORKFLOW_ENGINE_URL;
    this.policyEngineUrl = POLICY_ENGINE_URL;
    this.evaluationEngineUrl = EVALUATION_ENGINE_URL;
    this.deviceGatewayUrl = DEVICE_GATEWAY_URL;
  }

  private async request<T>(
    url: string,
    options: RequestInit = {}
  ): Promise<T> {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // API Gateway Endpoints
  async getHealth(): Promise<HealthStatus> {
    return this.request<HealthStatus>(`${this.baseUrl}/api/v1/health`);
  }

  async getSystemMetrics(): Promise<SystemMetrics> {
    // In production, this would come from actual metrics service
    return {
      cpuUsage: 45.2 + Math.random() * 10,
      memoryUsage: 62.8 + Math.random() * 5,
      activeConnections: 156 + Math.floor(Math.random() * 20),
      responseTime: 120 + Math.floor(Math.random() * 30),
      localModel: true,
      memoryEngine: true,
      toolGateway: true,
    };
  }

  // Model Gateway Endpoints
  async getModels(): Promise<{ models: ModelInfo[] }> {
    return this.request<{ models: ModelInfo[] }>(`${this.modelGatewayUrl}/models`);
  }

  async getProviders(): Promise<{ providers: any[] }> {
    return this.request<{ providers: any[] }>(`${this.modelGatewayUrl}/providers`);
  }

  async chatCompletion(request: ChatRequest): Promise<ChatResponse> {
    return this.request<ChatResponse>(
      `${this.modelGatewayUrl}/chat/completions`,
      {
        method: 'POST',
        body: JSON.stringify(request),
      }
    );
  }

  // Memory Engine Endpoints
  async createMemory(entry: MemoryEntry): Promise<MemoryEntry> {
    return this.request<MemoryEntry>(
      `${this.memoryEngineUrl}/memory`,
      {
        method: 'POST',
        body: JSON.stringify(entry),
      }
    );
  }

  async getMemory(memoryId: string): Promise<MemoryEntry> {
    return this.request<MemoryEntry>(`${this.memoryEngineUrl}/memory/${memoryId}`);
  }

  async searchMemory(request: MemorySearchRequest): Promise<MemorySearchResponse> {
    return this.request<MemorySearchResponse>(
      `${this.memoryEngineUrl}/memory/search`,
      {
        method: 'POST',
        body: JSON.stringify(request),
      }
    );
  }

  async deleteMemory(memoryId: string): Promise<{ status: string; id: string }> {
    return this.request<{ status: string; id: string }>(
      `${this.memoryEngineUrl}/memory/${memoryId}`,
      {
        method: 'DELETE',
      }
    );
  }

  // RSI Engine Endpoints
  async getRSIStatus(): Promise<any> {
    return this.request<any>(`${this.rsiEngineUrl}/rsi/status`);
  }

  async startRSICycle(triggerReason: string, autoApprove: boolean = false): Promise<any> {
    return this.request<any>(
      `${this.rsiEngineUrl}/rsi/cycle/start`,
      {
        method: 'POST',
        body: JSON.stringify({ trigger_reason: triggerReason, auto_approve: autoApprove }),
      }
    );
  }

  async emergencyStop(): Promise<any> {
    return this.request<any>(
      `${this.rsiEngineUrl}/rsi/emergency-stop`,
      {
        method: 'POST',
      }
    );
  }

  async getGoalDriftIndex(): Promise<any> {
    return this.request<any>(`${this.rsiEngineUrl}/safety/gdi`);
  }

  // Cognitive Engine Endpoints
  async getCognitiveCapabilities(): Promise<any> {
    return this.request<any>(`${this.cognitiveEngineUrl}/capabilities`);
  }

  async performReasoning(query: string, reasoningMethod: string = 'chain_of_thought'): Promise<any> {
    return this.request<any>(
      `${this.cognitiveEngineUrl}/reasoning`,
      {
        method: 'POST',
        body: JSON.stringify({ query, reasoning_method: reasoningMethod }),
      }
    );
  }

  async generatePlanning(goal: string, currentState: Record<string, any>): Promise<any> {
    return this.request<any>(
      `${this.cognitiveEngineUrl}/planning`,
      {
        method: 'POST',
        body: JSON.stringify({ goal, current_state: currentState }),
      }
    );
  }

  // Tool Execution Endpoints
  async getAvailableTools(): Promise<any> {
    return this.request<any>(`${this.toolExecutionUrl}/tools`);
  }

  async executeTool(toolName: string, parameters: Record<string, any>): Promise<any> {
    return this.request<any>(
      `${this.toolExecutionUrl}/tools/${toolName}/execute`,
      {
        method: 'POST',
        body: JSON.stringify(parameters),
      }
    );
  }

  // Workflow Engine Endpoints
  async getWorkflows(): Promise<any> {
    return this.request<any>(`${this.workflowEngineUrl}/workflows`);
  }

  async executeWorkflow(workflowId: string, inputs: Record<string, any>): Promise<any> {
    return this.request<any>(
      `${this.workflowEngineUrl}/workflows/${workflowId}/execute`,
      {
        method: 'POST',
        body: JSON.stringify(inputs),
      }
    );
  }

  // Policy Engine Endpoints
  async getPolicies(): Promise<any> {
    return this.request<any>(`${this.policyEngineUrl}/policies`);
  }

  async evaluatePolicy(policyId: string, context: Record<string, any>): Promise<any> {
    return this.request<any>(
      `${this.policyEngineUrl}/policies/${policyId}/evaluate`,
      {
        method: 'POST',
        body: JSON.stringify(context),
      }
    );
  }

  // Evaluation Engine Endpoints
  async getBenchmarks(): Promise<any> {
    return this.request<any>(`${this.evaluationEngineUrl}/benchmarks`);
  }

  async runBenchmark(benchmarkId: string): Promise<any> {
    return this.request<any>(
      `${this.evaluationEngineUrl}/benchmarks/${benchmarkId}/run`,
      {
        method: 'POST',
      }
    );
  }

  // Device Gateway Endpoints
  async getConnectedDevices(): Promise<any> {
    return this.request<any>(`${this.deviceGatewayUrl}/devices`);
  }

  async getDeviceStatus(deviceId: string): Promise<any> {
    return this.request<any>(`${this.deviceGatewayUrl}/devices/${deviceId}/status`);
  }
}

// Export singleton instance
export const apiService = new APIService();
export default apiService;