// Custom hook for offline functionality
import { useState, useEffect, useCallback } from 'react';
import { offlineService } from '../services/offline';

export function useOffline() {
  const [isOnline, setIsOnline] = useState(true);
  const [queueSize, setQueueSize] = useState(0);
  const [syncStatus, setSyncStatus] = useState<'idle' | 'syncing' | 'completed' | 'failed'>('idle');
  const [cacheSize, setCacheSize] = useState(0);

  useEffect(() => {
    initialize();
    const interval = setInterval(checkStatus, 5000); // Check every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const initialize = async () => {
    try {
      const online = await offlineService.isAvailable();
      setIsOnline(online);
      
      const queue = await offlineService.getQueue();
      setQueueSize(queue.length);
      
      const status = await offlineService.getSyncStatus();
      if (status) {
        setSyncStatus(status.status as any);
      }
      
      const size = await offlineService.getStorageSize();
      setCacheSize(size);
    } catch (error) {
      console.error('Offline service initialization failed:', error);
    }
  };

  const checkStatus = async () => {
    try {
      const online = await offlineService.isAvailable();
      setIsOnline(online);
      
      const queue = await offlineService.getQueue();
      setQueueSize(queue.length);
      
      const status = await offlineService.getSyncStatus();
      if (status) {
        setSyncStatus(status.status as any);
      }
    } catch (error) {
      console.error('Status check failed:', error);
    }
  };

  const cacheData = useCallback(async (key: string, data: any, ttl?: number) => {
    try {
      await offlineService.cacheData(key, data, ttl);
      const size = await offlineService.getStorageSize();
      setCacheSize(size);
    } catch (error) {
      console.error('Failed to cache data:', error);
    }
  }, []);

  const getCachedData = useCallback(async (key: string) => {
    try {
      return await offlineService.getCachedData(key);
    } catch (error) {
      console.error('Failed to get cached data:', error);
      return null;
    }
  }, []);

  const storeLocally = useCallback(async (key: string, data: any) => {
    try {
      await offlineService.storeLocally(key, data);
      const size = await offlineService.getStorageSize();
      setCacheSize(size);
    } catch (error) {
      console.error('Failed to store locally:', error);
    }
  }, []);

  const retrieveLocally = useCallback(async (key: string) => {
    try {
      return await offlineService.retrieveLocally(key);
    } catch (error) {
      console.error('Failed to retrieve locally:', error);
      return null;
    }
  }, []);

  const syncNow = useCallback(async () => {
    try {
      setSyncStatus('syncing');
      await offlineService.syncOfflineData();
      await checkStatus();
    } catch (error) {
      console.error('Sync failed:', error);
      setSyncStatus('failed');
    }
  }, []);

  const clearCache = useCallback(async () => {
    try {
      await offlineService.clearCache();
      const size = await offlineService.getStorageSize();
      setCacheSize(size);
    } catch (error) {
      console.error('Failed to clear cache:', error);
    }
  }, []);

  const clearExpiredCache = useCallback(async () => {
    try {
      await offlineService.clearExpiredCache();
      const size = await offlineService.getStorageSize();
      setCacheSize(size);
    } catch (error) {
      console.error('Failed to clear expired cache:', error);
    }
  }, []);

  return {
    isOnline,
    queueSize,
    syncStatus,
    cacheSize,
    cacheData,
    getCachedData,
    storeLocally,
    retrieveLocally,
    syncNow,
    clearCache,
    clearExpiredCache,
  };
}