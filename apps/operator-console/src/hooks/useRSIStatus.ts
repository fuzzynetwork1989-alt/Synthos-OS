// Custom hook for RSI (Recursive Self-Improvement) status monitoring
import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

interface RSIStatus {
  is_active: boolean;
  current_cycle: number;
  total_cycles: number;
  last_improvement: string;
  goal_drift_index: number;
  safety_status: string;
}

export function useRSIStatus() {
  const [rsiStatus, setRSIStatus] = useState<RSIStatus>({
    is_active: false,
    current_cycle: 0,
    total_cycles: 0,
    last_improvement: '',
    goal_drift_index: 0,
    safety_status: 'healthy',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRSIStatus = async () => {
      try {
        setLoading(true);
        const status = await apiService.getRSIStatus();
        setRSIStatus(status);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch RSI status:', err);
        setError('Failed to fetch RSI status');
        // Set default values on error
        setRSIStatus({
          is_active: false,
          current_cycle: 0,
          total_cycles: 0,
          last_improvement: 'Never',
          goal_drift_index: 0,
          safety_status: 'unknown',
        });
      } finally {
        setLoading(false);
      }
    };

    fetchRSIStatus();
    const interval = setInterval(fetchRSIStatus, 10000); // Update every 10 seconds

    return () => clearInterval(interval);
  }, []);

  const startImprovementCycle = async (triggerReason: string, autoApprove: boolean = false) => {
    try {
      const result = await apiService.startRSICycle(triggerReason, autoApprove);
      // Refresh status after starting cycle
      const status = await apiService.getRSIStatus();
      setRSIStatus(status);
      return result;
    } catch (err) {
      console.error('Failed to start improvement cycle:', err);
      throw err;
    }
  };

  const emergencyStop = async () => {
    try {
      const result = await apiService.emergencyStop();
      // Refresh status after emergency stop
      const status = await apiService.getRSIStatus();
      setRSIStatus(status);
      return result;
    } catch (err) {
      console.error('Failed to execute emergency stop:', err);
      throw err;
    }
  };

  const getGoalDriftIndex = async () => {
    try {
      const gdi = await apiService.getGoalDriftIndex();
      return gdi;
    } catch (err) {
      console.error('Failed to fetch goal drift index:', err);
      throw err;
    }
  };

  return { rsiStatus, loading, error, startImprovementCycle, emergencyStop, getGoalDriftIndex };
}