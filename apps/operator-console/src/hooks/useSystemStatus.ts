// Custom hook for system status monitoring
import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

interface SystemStatus {
  localModel: boolean;
  memoryEngine: boolean;
  toolGateway: boolean;
  cpuUsage: number;
  memoryUsage: number;
  activeConnections: number;
  responseTime: number;
}

export function useSystemStatus() {
  const [status, setStatus] = useState<SystemStatus>({
    localModel: false,
    memoryEngine: false,
    toolGateway: false,
    cpuUsage: 0,
    memoryUsage: 0,
    activeConnections: 0,
    responseTime: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        setLoading(true);
        const systemStatus = await apiService.getSystemMetrics();
        setStatus(systemStatus);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch system status:', err);
        setError('Failed to fetch system status');
        // Set default values on error
        setStatus({
          localModel: false,
          memoryEngine: false,
          toolGateway: false,
          cpuUsage: 0,
          memoryUsage: 0,
          activeConnections: 0,
          responseTime: 0,
        });
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return { status, loading, error };
}