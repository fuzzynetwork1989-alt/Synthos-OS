import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';

export default function ToolsScreen() {
  const router = useRouter();

  const tools = [
    { id: 1, name: 'Web Search', description: 'Search the web for information', status: 'Available', risk: 'Low' },
    { id: 2, name: 'Code Execution', description: 'Execute code in sandboxed environment', status: 'Available', risk: 'Medium' },
    { id: 3, name: 'File Operations', description: 'Read and write local files', status: 'Available', risk: 'Medium' },
    { id: 4, name: 'API Integration', description: 'Connect to external APIs', status: 'Available', risk: 'Low' },
    { id: 5, name: 'Database Access', description: 'Query and modify databases', status: 'Restricted', risk: 'High' },
    { id: 6, name: 'System Commands', description: 'Execute system commands', status: 'Restricted', risk: 'High' },
  ];

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'Low': return '#4CAF50';
      case 'Medium': return '#FF9800';
      case 'High': return '#F44336';
      default: return '#666';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Available': return '#4CAF50';
      case 'Restricted': return '#FF9800';
      case 'Unavailable': return '#F44336';
      default: return '#666';
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}>
          <Text style={styles.backButton}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Tools</Text>
        <View style={{ width: 50 }} />
      </View>

      <ScrollView style={styles.content}>
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Available Tools</Text>
          
          {tools.map((tool) => (
            <TouchableOpacity key={tool.id} style={styles.toolCard}>
              <View style={styles.toolHeader}>
                <Text style={styles.toolName}>{tool.name}</Text>
                <View style={[
                  styles.statusBadge, 
                  { backgroundColor: getStatusColor(tool.status) }
                ]}>
                  <Text style={styles.statusText}>{tool.status}</Text>
                </View>
              </View>
              <Text style={styles.toolDescription}>{tool.description}</Text>
              <View style={styles.toolFooter}>
                <Text style={styles.riskLabel}>Risk Level:</Text>
                <Text style={[styles.riskValue, { color: getRiskColor(tool.risk) }]}>
                  {tool.risk}
                </Text>
              </View>
            </TouchableOpacity>
          ))}
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Tool Permissions</Text>
          
          <View style={styles.permissionCard}>
            <Text style={styles.permissionTitle}>Permission Matrix</Text>
            <Text style={styles.permissionDescription}>
              Tools are assigned based on capability requirements and risk assessment.
              High-risk tools require explicit user approval.
            </Text>
            <TouchableOpacity style={styles.manageButton}>
              <Text style={styles.manageButtonText}>Manage Permissions</Text>
            </TouchableOpacity>
          </View>
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
    padding: 16,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    marginBottom: 12,
    textTransform: 'uppercase',
  },
  toolCard: {
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    padding: 12,
    marginBottom: 8,
  },
  toolHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  toolName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1a1a1a',
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  statusText: {
    fontSize: 12,
    color: '#ffffff',
    fontWeight: '600',
  },
  toolDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  toolFooter: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  riskLabel: {
    fontSize: 12,
    color: '#666',
    marginRight: 4,
  },
  riskValue: {
    fontSize: 12,
    fontWeight: '600',
  },
  permissionCard: {
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    padding: 12,
  },
  permissionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 8,
  },
  permissionDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
  },
  manageButton: {
    backgroundColor: '#007AFF',
    borderRadius: 8,
    padding: 12,
    alignItems: 'center',
  },
  manageButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
});
