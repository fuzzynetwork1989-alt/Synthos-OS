import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function RootLayout() {
  return (
    <>
      <StatusBar style="auto" />
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="index" options={{ title: 'Home' }} />
        <Stack.Screen name="chat" options={{ title: 'Chat' }} />
        <Stack.Screen name="settings" options={{ title: 'Settings' }} />
        <Stack.Screen name="memory" options={{ title: 'Memory' }} />
        <Stack.Screen name="tools" options={{ title: 'Tools' }} />
      </Stack>
    </>
  );
}
