import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Alert, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { useOffline } from '../hooks/useOffline';

interface Memory {
  id: string;
  type: 'Episodic' | 'Semantic' | 'Procedural';
  title: string;
  content: string;
  date: string;
  metadata?: any;
}

export default function MemoryScreen() {
  const router = useRouter();
  const { isOnline, retrieveLocally, storeLocally } = useOffline();
  
  const [memories, setMemories] = useState<Memory[]>([]);
  const [loading, setLoading] = useState(true);
  const [memoryStats, setMemoryStats] = useState({
    episodic: 0,
    semantic: 0,
    procedural: 0,
  });

  useEffect(() => {
    loadMemories();
  }, []);

  const loadMemories = async () => {
    try {
      setLoading(true);
      
      if (isOnline) {
        try {
          const remoteMemories = await apiService.getMemories();
          setMemories(remoteMemories);
          // Cache locally for offline access
          await storeLocally('cached_memories', remoteMemories);
        } catch (error) {
          console.error('Failed to load remote memories:', error);
          // Fall back to local cache
          const cachedMemories = await retrieveLocally('cached_memories');
          if (cachedMemories) {
            setMemories(cachedMemories);
          }
        }
      } else {
        // Load from local cache
        const cachedMemories = await retrieveLocally('cached_memories');
        if (cachedMemories) {
          setMemories(cachedMemories);
        }
      }

      // Calculate stats
      const stats = memories.reduce((acc, memory) => {
        const type = memory.type.toLowerCase();
        if (type in acc) {
          acc[type as keyof typeof acc]++;
        }
        return acc;
      }, { episodic: 0, semantic: 0, procedural: 0 });
      
      setMemoryStats(stats);
    } catch (error) {
      console.error('Failed to load memories:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateMemory = () => {
    // Navigate to memory creation screen
    router.push('/memory-create');
  };

  const handleClearMemories = () => {
    Alert.alert(
      'Clear All Memories',
      'This will permanently delete all stored memories. Are you sure?',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Clear', 
          style: 'destructive',
          onPress: async () => {
            try {
              // Clear from backend if online
              if (isOnline) {
                for (const memory of memories) {
                  await apiService.deleteMemory(memory.id);
                }
              }
              // Clear local cache
              await storeLocally('cached_memories', []);
              setMemories([]);
              setMemoryStats({ episodic: 0, semantic: 0, procedural: 0 });
              Alert.alert('Success', 'All memories cleared');
            } catch (error) {
              console.error('Failed to clear memories:', error);
              Alert.alert('Error', 'Failed to clear memories');
            }
          }
        }
      ]
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}>
          <Text style={styles.backButton}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Memory</Text>
        <TouchableOpacity onPress={handleCreateMemory}>
          <Text style={styles.addButton}>+ Add</Text>
        </TouchableOpacity>
      </View>

      {loading ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#007AFF" />
          <Text style={styles.loadingText}>Loading memories...</Text>
        </View>
      ) : (
        <ScrollView style={styles.content}>
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Memory Types</Text>
            
            <View style={styles.memoryTypes}>
              <View style={styles.memoryTypeCard}>
                <Text style={styles.memoryTypeCount}>{memoryStats.episodic}</Text>
                <Text style={styles.memoryTypeLabel}>Episodic</Text>
              </View>
              <View style={styles.memoryTypeCard}>
                <Text style={styles.memoryTypeCount}>{memoryStats.semantic}</Text>
                <Text style={styles.memoryTypeLabel}>Semantic</Text>
              </View>
              <View style={styles.memoryTypeCard}>
                <Text style={styles.memoryTypeCount}>{memoryStats.procedural}</Text>
                <Text style={styles.memoryTypeLabel}>Procedural</Text>
              </View>
            </View>
          </View>

          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Recent Memories</Text>
            
            {memories.length === 0 ? (
              <View style={styles.emptyState}>
                <Text style={styles.emptyText}>No memories stored yet</Text>
                <TouchableOpacity style={styles.emptyButton} onPress={handleCreateMemory}>
                  <Text style={styles.emptyButtonText}>Create First Memory</Text>
                </TouchableOpacity>
              </View>
            ) : (
              memories.map((memory) => (
                <TouchableOpacity key={memory.id} style={styles.memoryCard}>
                  <View style={styles.memoryTypeBadge}>
                    <Text style={styles.memoryTypeText}>{memory.type}</Text>
                  </View>
                  <Text style={styles.memoryTitle}>{memory.title}</Text>
                  <Text style={styles.memoryDate}>{new Date(memory.date).toLocaleDateString()}</Text>
                </TouchableOpacity>
              ))
            )}
          </View>

          {memories.length > 0 && (
            <TouchableOpacity style={styles.clearButton} onPress={handleClearMemories}>
              <Text style={styles.clearButtonText}>Clear All Memories</Text>
            </TouchableOpacity>
          )}
          
          {!isOnline && (
            <View style={styles.offlineBanner}>
              <Text style={styles.offlineText}>Offline Mode - Showing cached memories</Text>
            </View>
          )}
        </ScrollView>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    backgroundColor: '#ffffff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  backButton: {
    fontSize: 16,
    color: '#007AFF',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1a1a1a',
  },
  addButton: {
    fontSize: 16,
    color: '#007AFF',
    fontWeight: '600',
  },
  content: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 12,
    fontSize: 16,
    color: '#666',
  },
  section: {
    backgroundColor: '#ffffff',
    marginTop: 20,
    padding: 16,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    marginBottom: 12,
    textTransform: 'uppercase',
  },
  memoryTypes: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  memoryTypeCard: {
    flex: 1,
    backgroundColor: '#f0f0f0',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    marginHorizontal: 4,
  },
  memoryTypeCount: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#007AFF',
    marginBottom: 4,
  },
  memoryTypeLabel: {
    fontSize: 12,
    color: '#666',
  },
  memoryCard: {
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    padding: 12,
    marginBottom: 8,
  },
  memoryTypeBadge: {
    alignSelf: 'flex-start',
    backgroundColor: '#007AFF',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
    marginBottom: 8,
  },
  memoryTypeText: {
    fontSize: 12,
    color: '#ffffff',
    fontWeight: '600',
  },
  memoryTitle: {
    fontSize: 16,
    color: '#1a1a1a',
    marginBottom: 4,
  },
  memoryDate: {
    fontSize: 14,
    color: '#666',
  },
  emptyState: {
    padding: 40,
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 16,
    color: '#666',
    marginBottom: 16,
  },
  emptyButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  emptyButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
  clearButton: {
    backgroundColor: '#FF3B30',
    borderRadius: 8,
    padding: 16,
    margin: 20,
    alignItems: 'center',
  },
  clearButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
  offlineBanner: {
    backgroundColor: '#FF9800',
    padding: 12,
    alignItems: 'center',
    margin: 20,
    borderRadius: 8,
  },
  offlineText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '600',
  },
});
