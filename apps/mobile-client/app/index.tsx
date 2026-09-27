import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import { useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useOffline } from '../hooks/useOffline';
import { useModelGateway } from '../hooks/useModelGateway';

export default function HomeScreen() {
  const router = useRouter();
  const { isAuthenticated, user } = useAuth();
  const { isOnline } = useOffline();
  const { localModelHealthy } = useModelGateway();

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace('/login');
    }
  }, [isAuthenticated, router]);

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.title}>Synthos OS</Text>
          <Text style={styles.subtitle}>Next-Generation AI Operating System</Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Quick Actions</Text>
          
          <TouchableOpacity 
            style={styles.card}
            onPress={() => router.push('/chat')}
          >
            <Text style={styles.cardTitle}>Start Chat</Text>
            <Text style={styles.cardDescription}>Begin a conversation with your AI assistant</Text>
          </TouchableOpacity>

          <TouchableOpacity 
            style={styles.card}
            onPress={() => router.push('/memory')}
          >
            <Text style={styles.cardTitle}>Memory</Text>
            <Text style={styles.cardDescription}>View and manage your stored memories</Text>
          </TouchableOpacity>

          <TouchableOpacity 
            style={styles.card}
            onPress={() => router.push('/tools')}
          >
            <Text style={styles.cardTitle}>Tools</Text>
            <Text style={styles.cardDescription}>Access available tools and capabilities</Text>
          </TouchableOpacity>

          <TouchableOpacity 
            style={styles.card}
            onPress={() => router.push('/settings')}
          >
            <Text style={styles.cardTitle}>Settings</Text>
            <Text style={styles.cardDescription}>Configure your Synthos OS experience</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>System Status</Text>
          <View style={styles.statusCard}>
            <View style={styles.statusItem}>
              <View style={[styles.statusIndicator, localModelHealthy ? styles.statusOnline : styles.statusOffline]} />
              <Text style={styles.statusText}>Local Model: {localModelHealthy ? 'Online' : 'Offline'}</Text>
            </View>
            <View style={styles.statusItem}>
              <View style={[styles.statusIndicator, isOnline ? styles.statusOnline : styles.statusOffline]} />
              <Text style={styles.statusText}>Network: {isOnline ? 'Connected' : 'Offline'}</Text>
            </View>
            <View style={styles.statusItem}>
              <View style={[styles.statusIndicator, isAuthenticated ? styles.statusOnline : styles.statusOffline]} />
              <Text style={styles.statusText}>Authentication: {isAuthenticated ? 'Active' : 'Inactive'}</Text>
            </View>
          </View>
        </View>

        {user && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Welcome Back</Text>
            <View style={styles.userCard}>
              <Text style={styles.userGreeting}>Hello, {user.name || user.email}</Text>
              <Text style={styles.userSubtext}>Your Synthos OS is ready</Text>
            </View>
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
  scrollContent: {
    padding: 20,
  },
  header: {
    alignItems: 'center',
    marginBottom: 30,
    paddingTop: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#1a1a1a',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 12,
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 4,
  },
  cardDescription: {
    fontSize: 14,
    color: '#666',
  },
  statusCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statusItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  statusIndicator: {
    width: 10,
    height: 10,
    borderRadius: 5,
    marginRight: 12,
  },
  statusOnline: {
    backgroundColor: '#4CAF50',
  },
  statusOffline: {
    backgroundColor: '#FF9800',
  },
  statusText: {
    fontSize: 14,
    color: '#1a1a1a',
  },
  userCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  userGreeting: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 4,
  },
  userSubtext: {
    fontSize: 14,
    color: '#666',
  },
});
