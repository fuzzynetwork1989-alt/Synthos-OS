import { View, Text, StyleSheet, TouchableOpacity, Switch, ScrollView, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useOffline } from '../hooks/useOffline';
import { useModelGateway } from '../hooks/useModelGateway';
import * as LocalAuthentication from 'expo-local-authentication';

export default function SettingsScreen() {
  const router = useRouter();
  const { user, logout, isAuthenticated } = useAuth();
  const { isOnline, cacheSize, clearCache } = useOffline();
  const { localModelHealthy, availableModels, setModelPreference, preferredModel } = useModelGateway();
  
  const [localProcessing, setLocalProcessing] = useState(true);
  const [biometricAuth, setBiometricAuth] = useState(false);
  const [notifications, setNotifications] = useState(true);
  const [cloudSync, setCloudSync] = useState(false);
  const [biometricAvailable, setBiometricAvailable] = useState(false);

  useEffect(() => {
    checkBiometricAvailability();
  }, []);

  const checkBiometricAvailability = async () => {
    try {
      const available = await LocalAuthentication.hasHardwareAsync();
      const enrolled = await LocalAuthentication.isEnrolledAsync();
      setBiometricAvailable(available && enrolled);
    } catch (error) {
      console.error('Biometric check failed:', error);
    }
  };

  const handleBiometricToggle = async (value: boolean) => {
    if (value) {
      try {
        const result = await LocalAuthentication.authenticateAsync({
          promptMessage: 'Enable biometric authentication',
          fallbackLabel: 'Use password',
        });
        if (result.success) {
          setBiometricAuth(true);
        }
      } catch (error) {
        console.error('Biometric setup failed:', error);
      }
    } else {
      setBiometricAuth(false);
    }
  };

  const handleLogout = () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Logout', 
          style: 'destructive',
          onPress: async () => {
            await logout();
            router.replace('/');
          }
        }
      ]
    );
  };

  const handleClearCache = () => {
    Alert.alert(
      'Clear Cache',
      'This will clear all cached data. Are you sure?',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Clear', 
          style: 'destructive',
          onPress: async () => {
            await clearCache();
            Alert.alert('Success', 'Cache cleared successfully');
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
        <Text style={styles.headerTitle}>Settings</Text>
        <View style={{ width: 50 }} />
      </View>

      <ScrollView style={styles.content}>
        {isAuthenticated && user && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Account</Text>
            <View style={styles.settingItem}>
              <View style={styles.settingInfo}>
                <Text style={styles.settingLabel}>Email</Text>
                <Text style={styles.settingDescription}>{user.email}</Text>
              </View>
            </View>
            <TouchableOpacity style={styles.settingItem} onPress={handleLogout}>
              <Text style={[styles.settingLabel, styles.logoutText]}>Logout</Text>
            </TouchableOpacity>
          </View>
        )}

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Privacy & Security</Text>
          
          <View style={styles.settingItem}>
            <View style={styles.settingInfo}>
              <Text style={styles.settingLabel}>Local Processing</Text>
              <Text style={styles.settingDescription}>Process data locally when possible</Text>
            </View>
            <Switch
              value={localProcessing}
              onValueChange={setLocalProcessing}
              trackColor={{ false: '#767577', true: '#007AFF' }}
            />
          </View>

          {biometricAvailable && (
            <View style={styles.settingItem}>
              <View style={styles.settingInfo}>
                <Text style={styles.settingLabel}>Biometric Authentication</Text>
                <Text style={styles.settingDescription}>Use Face ID or fingerprint</Text>
              </View>
              <Switch
                value={biometricAuth}
                onValueChange={handleBiometricToggle}
                trackColor={{ false: '#767577', true: '#007AFF' }}
              />
            </View>
          )}
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>AI Model</Text>
          
          <View style={styles.settingItem}>
            <View style={styles.settingInfo}>
              <Text style={styles.settingLabel}>Local Model Status</Text>
              <Text style={styles.settingDescription}>
                {localModelHealthy ? 'Online' : 'Offline'}
              </Text>
            </View>
            <View style={[
              styles.statusDot,
              { backgroundColor: localModelHealthy ? '#4CAF50' : '#FF9800' }
            ]} />
          </View>

          {availableModels.length > 0 && (
            <View style={styles.settingItem}>
              <View style={styles.settingInfo}>
                <Text style={styles.settingLabel}>Preferred Model</Text>
                <Text style={styles.settingDescription}>{preferredModel || 'Default'}</Text>
              </View>
            </View>
          )}
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Data & Sync</Text>
          
          <View style={styles.settingItem}>
            <View style={styles.settingInfo}>
              <Text style={styles.settingLabel}>Connection Status</Text>
              <Text style={styles.settingDescription}>{isOnline ? 'Online' : 'Offline'}</Text>
            </View>
            <View style={[
              styles.statusDot,
              { backgroundColor: isOnline ? '#4CAF50' : '#FF9800' }
            ]} />
          </View>

          <View style={styles.settingItem}>
            <View style={styles.settingInfo}>
              <Text style={styles.settingLabel}>Cloud Sync</Text>
              <Text style={styles.settingDescription}>Sync data to cloud storage</Text>
            </View>
            <Switch
              value={cloudSync}
              onValueChange={setCloudSync}
              trackColor={{ false: '#767577', true: '#007AFF' }}
            />
          </View>

          <TouchableOpacity style={styles.settingItem} onPress={handleClearCache}>
            <View style={styles.settingInfo}>
              <Text style={styles.settingLabel}>Clear Cache</Text>
              <Text style={styles.settingDescription}>Free {(cacheSize / 1024).toFixed(2)} KB</Text>
            </View>
            <Text style={styles.settingValue}>Clear</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Notifications</Text>
          
          <View style={styles.settingItem}>
            <View style={styles.settingInfo}>
              <Text style={styles.settingLabel}>Push Notifications</Text>
              <Text style={styles.settingDescription}>Receive system notifications</Text>
            </View>
            <Switch
              value={notifications}
              onValueChange={setNotifications}
              trackColor={{ false: '#767577', true: '#007AFF' }}
            />
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>About</Text>
          
          <TouchableOpacity style={styles.settingItem}>
            <Text style={styles.settingLabel}>Version</Text>
            <Text style={styles.settingValue}>0.1.0</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.settingItem}>
            <Text style={styles.settingLabel}>Privacy Policy</Text>
            <Text style={styles.settingValue}>→</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.settingItem}>
            <Text style={styles.settingLabel}>Terms of Service</Text>
            <Text style={styles.settingValue}>→</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.settingItem}>
            <Text style={styles.settingLabel}>Open Source License</Text>
            <Text style={styles.settingValue}>→</Text>
          </TouchableOpacity>
        </View>
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
  content: {
    flex: 1,
  },
  section: {
    backgroundColor: '#ffffff',
    marginTop: 20,
    paddingVertical: 8,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    paddingHorizontal: 16,
    paddingVertical: 8,
    textTransform: 'uppercase',
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  settingInfo: {
    flex: 1,
  },
  settingLabel: {
    fontSize: 16,
    color: '#1a1a1a',
    marginBottom: 4,
  },
  settingDescription: {
    fontSize: 14,
    color: '#666',
  },
  settingValue: {
    fontSize: 16,
    color: '#007AFF',
  },
  statusDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
  },
  logoutText: {
    color: '#FF3B30',
  },
});
