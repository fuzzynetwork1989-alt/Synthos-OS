import { View, Text, StyleSheet, TextInput, TouchableOpacity, ScrollView, Alert, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { useState } from 'react';
import { apiService } from '../services/api';
import { useOffline } from '../hooks/useOffline';

export default function MemoryCreateScreen() {
  const router = useRouter();
  const { isOnline, storeLocally } = useOffline();
  
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [type, setType] = useState<'Episodic' | 'Semantic' | 'Procedural'>('Episodic');
  const [loading, setLoading] = useState(false);

  const handleSave = async () => {
    if (!title.trim() || !content.trim()) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    setLoading(true);
    try {
      const memoryData = {
        title: title.trim(),
        content: content.trim(),
        type,
        metadata: {
          createdAt: new Date().toISOString(),
          device: 'mobile',
        },
      };

      if (isOnline) {
        await apiService.createMemory(content.trim(), memoryData);
        Alert.alert('Success', 'Memory created successfully');
        router.back();
      } else {
        // Store locally for sync when online
        await storeLocally('pending_memory', memoryData);
        Alert.alert('Saved', 'Memory saved locally and will sync when online');
        router.back();
      }
    } catch (error) {
      console.error('Failed to create memory:', error);
      Alert.alert('Error', 'Failed to create memory');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}>
          <Text style={styles.backButton}>Cancel</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Create Memory</Text>
        <TouchableOpacity style={styles.saveButton} onPress={handleSave} disabled={loading}>
          {loading ? (
            <ActivityIndicator size="small" color="#ffffff" />
          ) : (
            <Text style={styles.saveButtonText}>Save</Text>
          )}
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content}>
        <View style={styles.section}>
          <Text style={styles.label}>Memory Type</Text>
          <View style={styles.typeSelector}>
            {(['Episodic', 'Semantic', 'Procedural'] as const).map((memoryType) => (
              <TouchableOpacity
                key={memoryType}
                style={[
                  styles.typeButton,
                  type === memoryType && styles.typeButtonActive,
                ]}
                onPress={() => setType(memoryType)}
              >
                <Text style={[
                  styles.typeButtonText,
                  type === memoryType && styles.typeButtonTextActive,
                ]}>
                  {memoryType}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.label}>Title</Text>
          <TextInput
            style={styles.input}
            value={title}
            onChangeText={setTitle}
            placeholder="Enter memory title"
            placeholderTextColor="#999"
          />
        </View>

        <View style={styles.section}>
          <Text style={styles.label}>Content</Text>
          <TextInput
            style={[styles.input, styles.textArea]}
            value={content}
            onChangeText={setContent}
            placeholder="Enter memory content"
            placeholderTextColor="#999"
            multiline
            numberOfLines={10}
            textAlignVertical="top"
          />
        </View>

        {!isOnline && (
          <View style={styles.offlineBanner}>
            <Text style={styles.offlineText}>
              Offline Mode - Memory will be synced when connected
            </Text>
          </View>
        )}
      </ScrollView>
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
  saveButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  saveButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
  content: {
    flex: 1,
    padding: 16,
  },
  section: {
    marginBottom: 24,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 8,
  },
  typeSelector: {
    flexDirection: 'row',
    gap: 8,
  },
  typeButton: {
    flex: 1,
    backgroundColor: '#ffffff',
    borderRadius: 8,
    padding: 12,
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  typeButtonActive: {
    backgroundColor: '#007AFF',
    borderColor: '#007AFF',
  },
  typeButtonText: {
    fontSize: 14,
    color: '#1a1a1a',
    textAlign: 'center',
  },
  typeButtonTextActive: {
    color: '#ffffff',
  },
  input: {
    backgroundColor: '#ffffff',
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  textArea: {
    height: 150,
  },
  offlineBanner: {
    backgroundColor: '#FF9800',
    padding: 12,
    borderRadius: 8,
    marginTop: 16,
  },
  offlineText: {
    color: '#ffffff',
    fontSize: 14,
    textAlign: 'center',
  },
});