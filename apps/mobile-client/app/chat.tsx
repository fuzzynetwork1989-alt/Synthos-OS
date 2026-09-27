import { View, Text, StyleSheet, TextInput, TouchableOpacity, ScrollView, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { useState } from 'react';
import { useModelGateway } from '../hooks/useModelGateway';
import { useOffline } from '../hooks/useOffline';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp?: number;
}

export default function ChatScreen() {
  const router = useRouter();
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, role: 'assistant', content: 'Hello! I am your Synthos OS assistant. How can I help you today?' }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  
  const { generateResponse, isGenerating, localModelHealthy } = useModelGateway();
  const { isOnline, storeLocally } = useOffline();

  const sendMessage = async () => {
    if (message.trim()) {
      const userMessage: Message = {
        id: Date.now(),
        role: 'user',
        content: message,
        timestamp: Date.now(),
      };

      setMessages(prev => [...prev, userMessage]);
      setMessage('');
      setIsTyping(true);

      try {
        // Try to generate response using model gateway
        const response = await generateResponse({
          prompt: message,
          temperature: 0.7,
          maxTokens: 2048,
        });

        const assistantMessage: Message = {
          id: Date.now() + 1,
          role: 'assistant',
          content: response.content,
          timestamp: Date.now(),
        };

        setMessages(prev => [...prev, assistantMessage]);

        // Store conversation locally for offline access
        await storeLocally('chat_history', messages);
      } catch (error) {
        console.error('Generation failed:', error);
        
        // Fallback response if generation fails
        const fallbackMessage: Message = {
          id: Date.now() + 1,
          role: 'assistant',
          content: isOnline 
            ? 'I apologize, but I encountered an error processing your request. Please try again.'
            : 'I\'m currently offline. Your message has been saved and will be processed when connectivity is restored.',
          timestamp: Date.now(),
        };

        setMessages(prev => [...prev, fallbackMessage]);
      } finally {
        setIsTyping(false);
      }
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}>
          <Text style={styles.backButton}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Chat</Text>
        <View style={styles.statusContainer}>
          <View style={[
            styles.statusDot,
            { backgroundColor: localModelHealthy ? '#4CAF50' : '#FF9800' }
          ]} />
        </View>
      </View>

      <ScrollView style={styles.messagesContainer}>
        {messages.map((msg) => (
          <View 
            key={msg.id} 
            style={[
              styles.messageBubble,
              msg.role === 'user' ? styles.userMessage : styles.assistantMessage
            ]}
          >
            <Text style={[
              styles.messageText,
              msg.role === 'user' ? styles.userMessageText : styles.assistantMessageText
            ]}>
              {msg.content}
            </Text>
            {msg.timestamp && (
              <Text style={styles.timestamp}>
                {new Date(msg.timestamp).toLocaleTimeString()}
              </Text>
            )}
          </View>
        ))}
        {isTyping && (
          <View style={[styles.messageBubble, styles.assistantMessage]}>
            <ActivityIndicator size="small" color="#007AFF" />
            <Text style={styles.typingText}>Thinking...</Text>
          </View>
        )}
      </ScrollView>

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={message}
          onChangeText={setMessage}
          placeholder="Type your message..."
          multiline
          editable={!isGenerating}
        />
        <TouchableOpacity 
          style={[styles.sendButton, isGenerating && styles.sendButtonDisabled]} 
          onPress={sendMessage}
          disabled={isGenerating || !message.trim()}
        >
          {isGenerating ? (
            <ActivityIndicator size="small" color="#ffffff" />
          ) : (
            <Text style={styles.sendButtonText}>Send</Text>
          )}
        </TouchableOpacity>
      </View>
      
      {!isOnline && (
        <View style={styles.offlineBanner}>
          <Text style={styles.offlineText}>Offline Mode - Messages will sync when connected</Text>
        </View>
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
  statusContainer: {
    width: 24,
    height: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
  statusDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
  },
  messagesContainer: {
    flex: 1,
    padding: 16,
  },
  messageBubble: {
    maxWidth: '80%',
    padding: 12,
    borderRadius: 16,
    marginBottom: 8,
  },
  userMessage: {
    backgroundColor: '#007AFF',
    alignSelf: 'flex-end',
  },
  assistantMessage: {
    backgroundColor: '#ffffff',
    alignSelf: 'flex-start',
  },
  messageText: {
    fontSize: 16,
  },
  userMessageText: {
    color: '#ffffff',
  },
  assistantMessageText: {
    color: '#1a1a1a',
  },
  timestamp: {
    fontSize: 12,
    color: '#999',
    marginTop: 4,
  },
  typingText: {
    fontSize: 14,
    color: '#666',
    marginLeft: 8,
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 16,
    backgroundColor: '#ffffff',
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  input: {
    flex: 1,
    backgroundColor: '#f0f0f0',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 12,
    marginRight: 8,
    maxHeight: 100,
  },
  sendButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 20,
    minWidth: 70,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: '#ccc',
  },
  sendButtonText: {
    color: '#ffffff',
    fontWeight: '600',
  },
  offlineBanner: {
    backgroundColor: '#FF9800',
    padding: 8,
    alignItems: 'center',
  },
  offlineText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: '600',
  },
});
