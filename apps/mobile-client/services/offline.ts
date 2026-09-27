// Offline Service for local storage and sync
import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-community/netinfo';

interface OfflineQueueItem {
  id: string;
  type: 'api_call' | 'memory' | 'tool_execution';
  endpoint?: string;
  method?: string;
  data?: any;
  timestamp: number;
  retryCount: number;
}

interface CachedData {
  key: string;
  data: any;
  timestamp: number;
  ttl: number; // Time to live in milliseconds
}

class OfflineService {
  private static readonly QUEUE_KEY = 'offline_queue';
  private static readonly CACHE_KEY = 'offline_cache';
  private static readonly SYNC_STATUS_KEY = 'sync_status';
  private isOnline: boolean = true;
  private syncInProgress: boolean = false;

  constructor() {
    this.initializeNetworkListener();
  }

  private initializeNetworkListener(): void {
    NetInfo.addEventListener(state => {
      this.isOnline = state.isConnected ?? false;
      if (this.isOnline && !this.syncInProgress) {
        this.syncOfflineData();
      }
    });
  }

  async isAvailable(): Promise<boolean> {
    const state = await NetInfo.fetch();
    return state.isConnected ?? false;
  }

  // Queue management
  async addToQueue(item: Omit<OfflineQueueItem, 'id' | 'timestamp' | 'retryCount'>): Promise<void> {
    try {
      const queue = await this.getQueue();
      const queueItem: OfflineQueueItem = {
        ...item,
        id: Date.now().toString(),
        timestamp: Date.now(),
        retryCount: 0,
      };
      queue.push(queueItem);
      await AsyncStorage.setItem(this.QUEUE_KEY, JSON.stringify(queue));
    } catch (error) {
      console.error('Failed to add to queue:', error);
    }
  }

  async getQueue(): Promise<OfflineQueueItem[]> {
    try {
      const queueData = await AsyncStorage.getItem(this.QUEUE_KEY);
      return queueData ? JSON.parse(queueData) : [];
    } catch (error) {
      console.error('Failed to get queue:', error);
      return [];
    }
  }

  async clearQueue(): Promise<void> {
    try {
      await AsyncStorage.removeItem(this.QUEUE_KEY);
    } catch (error) {
      console.error('Failed to clear queue:', error);
    }
  }

  async removeFromQueue(itemId: string): Promise<void> {
    try {
      const queue = await this.getQueue();
      const filteredQueue = queue.filter(item => item.id !== itemId);
      await AsyncStorage.setItem(this.QUEUE_KEY, JSON.stringify(filteredQueue));
    } catch (error) {
      console.error('Failed to remove from queue:', error);
    }
  }

  // Cache management
  async cacheData(key: string, data: any, ttl: number = 3600000): Promise<void> {
    try {
      const cache = await this.getCache();
      const cacheItem: CachedData = {
        key,
        data,
        timestamp: Date.now(),
        ttl,
      };
      cache[key] = cacheItem;
      await AsyncStorage.setItem(this.CACHE_KEY, JSON.stringify(cache));
    } catch (error) {
      console.error('Failed to cache data:', error);
    }
  }

  async getCachedData(key: string): Promise<any | null> {
    try {
      const cache = await this.getCache();
      const item = cache[key];

      if (!item) return null;

      // Check if cache is expired
      if (Date.now() - item.timestamp > item.ttl) {
        await this.removeCachedData(key);
        return null;
      }

      return item.data;
    } catch (error) {
      console.error('Failed to get cached data:', error);
      return null;
    }
  }

  async getCache(): Promise<Record<string, CachedData>> {
    try {
      const cacheData = await AsyncStorage.getItem(this.CACHE_KEY);
      return cacheData ? JSON.parse(cacheData) : {};
    } catch (error) {
      console.error('Failed to get cache:', error);
      return {};
    }
  }

  async removeCachedData(key: string): Promise<void> {
    try {
      const cache = await this.getCache();
      delete cache[key];
      await AsyncStorage.setItem(this.CACHE_KEY, JSON.stringify(cache));
    } catch (error) {
      console.error('Failed to remove cached data:', error);
    }
  }

  async clearCache(): Promise<void> {
    try {
      await AsyncStorage.removeItem(this.CACHE_KEY);
    } catch (error) {
      console.error('Failed to clear cache:', error);
    }
  }

  async clearExpiredCache(): Promise<void> {
    try {
      const cache = await this.getCache();
      const now = Date.now();
      const filteredCache: Record<string, CachedData> = {};

      for (const [key, item] of Object.entries(cache)) {
        if (now - item.timestamp <= item.ttl) {
          filteredCache[key] = item;
        }
      }

      await AsyncStorage.setItem(this.CACHE_KEY, JSON.stringify(filteredCache));
    } catch (error) {
      console.error('Failed to clear expired cache:', error);
    }
  }

  // Sync functionality
  async syncOfflineData(): Promise<void> {
    if (this.syncInProgress || !this.isOnline) return;

    this.syncInProgress = true;
    try {
      const queue = await this.getQueue();
      const failedItems: OfflineQueueItem[] = [];

      for (const item of queue) {
        try {
          await this.processQueueItem(item);
        } catch (error) {
          console.error('Failed to process queue item:', error);
          item.retryCount++;
          if (item.retryCount < 3) {
            failedItems.push(item);
          }
        }
      }

      // Update queue with failed items
      await AsyncStorage.setItem(this.QUEUE_KEY, JSON.stringify(failedItems));

      // Update sync status
      await this.setSyncStatus('completed', Date.now());
    } catch (error) {
      console.error('Sync failed:', error);
      await this.setSyncStatus('failed', Date.now());
    } finally {
      this.syncInProgress = false;
    }
  }

  private async processQueueItem(item: OfflineQueueItem): Promise<void> {
    // This would integrate with the API service
    // For now, this is a placeholder implementation
    switch (item.type) {
      case 'api_call':
        if (item.endpoint && item.method && item.data) {
          // Process API call
          console.log('Processing API call:', item.endpoint);
        }
        break;
      case 'memory':
        // Sync memory item
        console.log('Processing memory sync');
        break;
      case 'tool_execution':
        // Sync tool execution
        console.log('Processing tool execution sync');
        break;
    }
  }

  async setSyncStatus(status: 'idle' | 'syncing' | 'completed' | 'failed', timestamp: number): Promise<void> {
    try {
      await AsyncStorage.setItem(
        this.SYNC_STATUS_KEY,
        JSON.stringify({ status, timestamp })
      );
    } catch (error) {
      console.error('Failed to set sync status:', error);
    }
  }

  async getSyncStatus(): Promise<{ status: string; timestamp: number } | null> {
    try {
      const statusData = await AsyncStorage.getItem(this.SYNC_STATUS_KEY);
      return statusData ? JSON.parse(statusData) : null;
    } catch (error) {
      console.error('Failed to get sync status:', error);
      return null;
    }
  }

  // Local storage helpers
  async storeLocally(key: string, data: any): Promise<void> {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
      console.error('Failed to store locally:', error);
    }
  }

  async retrieveLocally(key: string): Promise<any | null> {
    try {
      const data = await AsyncStorage.getItem(key);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('Failed to retrieve locally:', error);
      return null;
    }
  }

  async removeLocally(key: string): Promise<void> {
    try {
      await AsyncStorage.removeItem(key);
    } catch (error) {
      console.error('Failed to remove locally:', error);
    }
  }

  // Storage management
  async getStorageSize(): Promise<number> {
    try {
      const keys = await AsyncStorage.getAllKeys();
      let totalSize = 0;

      for (const key of keys) {
        const data = await AsyncStorage.getItem(key);
        if (data) {
          totalSize += data.length;
        }
      }

      return totalSize;
    } catch (error) {
      console.error('Failed to get storage size:', error);
      return 0;
    }
  }

  async clearAllStorage(): Promise<void> {
    try {
      await AsyncStorage.clear();
    } catch (error) {
      console.error('Failed to clear storage:', error);
    }
  }
}

export const offlineService = new OfflineService();
export default OfflineService;