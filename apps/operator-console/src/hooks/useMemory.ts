// Custom hook for memory management
import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

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

interface MemoryStats {
  totalMemories: number;
  storageUsed: string;
  retentionRate: number;
  distribution: {
    episodic: number;
    semantic: number;
    procedural: number;
  };
}

export function useMemory() {
  const [memories, setMemories] = useState<MemoryEntry[]>([]);
  const [stats, setStats] = useState<MemoryStats>({
    totalMemories: 0,
    storageUsed: '0 GB',
    retentionRate: 0,
    distribution: {
      episodic: 0,
      semantic: 0,
      procedural: 0,
    },
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createMemory = async (entry: MemoryEntry) => {
    try {
      setLoading(true);
      const newMemory = await apiService.createMemory(entry);
      setMemories(prev => [...prev, newMemory]);
      setError(null);
      return newMemory;
    } catch (err) {
      console.error('Failed to create memory:', err);
      setError('Failed to create memory');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getMemory = async (memoryId: string) => {
    try {
      setLoading(true);
      const memory = await apiService.getMemory(memoryId);
      setError(null);
      return memory;
    } catch (err) {
      console.error('Failed to get memory:', err);
      setError('Failed to get memory');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const searchMemory = async (query: string, limit: number = 10) => {
    try {
      setLoading(true);
      const results = await apiService.searchMemory({ query, limit });
      setMemories(results.results);
      setError(null);
      return results;
    } catch (err) {
      console.error('Failed to search memory:', err);
      setError('Failed to search memory');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteMemory = async (memoryId: string) => {
    try {
      setLoading(true);
      await apiService.deleteMemory(memoryId);
      setMemories(prev => prev.filter(m => m.id !== memoryId));
      setError(null);
    } catch (err) {
      console.error('Failed to delete memory:', err);
      setError('Failed to delete memory');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const loadMemoryStats = async () => {
    try {
      // In production, this would come from actual stats endpoint
      setStats({
        totalMemories: 12458,
        storageUsed: '2.4 GB',
        retentionRate: 94.2,
        distribution: {
          episodic: 4521,
          semantic: 6234,
          procedural: 1703,
        },
      });
    } catch (err) {
      console.error('Failed to load memory stats:', err);
    }
  };

  useEffect(() => {
    loadMemoryStats();
  }, []);

  return {
    memories,
    stats,
    loading,
    error,
    createMemory,
    getMemory,
    searchMemory,
    deleteMemory,
    loadMemoryStats,
  };
}