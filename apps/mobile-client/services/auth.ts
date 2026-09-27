// Authentication Service
import * as SecureStore from 'expo-secure-store';
import * as LocalAuthentication from 'expo-local-authentication';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { apiService } from './api';

interface AuthUser {
  id: string;
  email: string;
  name: string;
  createdAt: string;
}

interface AuthSession {
  token: string;
  user: AuthUser;
  expiresAt: string;
}

class AuthService {
  private static readonly TOKEN_KEY = 'auth_token';
  private static readonly USER_KEY = 'auth_user';
  private static readonly SESSION_KEY = 'auth_session';
  private static readonly BIOMETRIC_ENABLED_KEY = 'biometric_enabled';

  private currentUser: AuthUser | null = null;
  private session: AuthSession | null = null;

  async initialize(): Promise<void> {
    try {
      // Load session from secure storage
      const sessionData = await SecureStore.getItemAsync(this.SESSION_KEY);
      if (sessionData) {
        this.session = JSON.parse(sessionData);
        this.currentUser = this.session.user;

        // Check if session is expired
        if (new Date(this.session.expiresAt) < new Date()) {
          await this.logout();
        }
      }
    } catch (error) {
      console.error('Failed to initialize auth service:', error);
    }
  }

  async login(email: string, password: string): Promise<AuthUser> {
    try {
      const response = await apiService.login(email, password);
      
      const session: AuthSession = {
        token: response.token,
        user: response.user,
        expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(), // 24 hours
      };

      await this.saveSession(session);
      this.currentUser = response.user;
      this.session = session;

      return response.user;
    } catch (error) {
      console.error('Login failed:', error);
      throw new Error('Authentication failed. Please check your credentials.');
    }
  }

  async register(email: string, password: string, name: string): Promise<AuthUser> {
    try {
      const response = await apiService.register(email, password, name);
      
      const session: AuthSession = {
        token: response.token,
        user: response.user,
        expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
      };

      await this.saveSession(session);
      this.currentUser = response.user;
      this.session = session;

      return response.user;
    } catch (error) {
      console.error('Registration failed:', error);
      throw new Error('Registration failed. Please try again.');
    }
  }

  async logout(): Promise<void> {
    try {
      await apiService.logout();
      await this.clearSession();
      this.currentUser = null;
      this.session = null;
    } catch (error) {
      console.error('Logout failed:', error);
      // Clear local session even if API call fails
      await this.clearSession();
      this.currentUser = null;
      this.session = null;
    }
  }

  private async saveSession(session: AuthSession): Promise<void> {
    try {
      await SecureStore.setItemAsync(this.TOKEN_KEY, session.token);
      await SecureStore.setItemAsync(this.USER_KEY, JSON.stringify(session.user));
      await SecureStore.setItemAsync(this.SESSION_KEY, JSON.stringify(session));
    } catch (error) {
      console.error('Failed to save session:', error);
      throw new Error('Failed to save authentication session');
    }
  }

  private async clearSession(): Promise<void> {
    try {
      await SecureStore.deleteItemAsync(this.TOKEN_KEY);
      await SecureStore.deleteItemAsync(this.USER_KEY);
      await SecureStore.deleteItemAsync(this.SESSION_KEY);
    } catch (error) {
      console.error('Failed to clear session:', error);
    }
  }

  getCurrentUser(): AuthUser | null {
    return this.currentUser;
  }

  isAuthenticated(): boolean {
    return this.currentUser !== null && this.session !== null;
  }

  getToken(): string | null {
    return this.session?.token || null;
  }

  async refreshToken(): Promise<void> {
    try {
      const user = await apiService.getCurrentUser();
      if (user) {
        this.currentUser = user;
        if (this.session) {
          this.session.user = user;
          await this.saveSession(this.session);
        }
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
      await this.logout();
    }
  }

  // Biometric Authentication
  async isBiometricAvailable(): Promise<boolean> {
    try {
      const compatible = await LocalAuthentication.hasHardwareAsync();
      const enrolled = await LocalAuthentication.isEnrolledAsync();
      return compatible && enrolled;
    } catch (error) {
      console.error('Biometric check failed:', error);
      return false;
    }
  }

  async authenticateBiometric(): Promise<boolean> {
    try {
      const result = await LocalAuthentication.authenticateAsync({
        promptMessage: 'Authenticate to access Synthos OS',
        fallbackLabel: 'Use password',
        cancelLabel: 'Cancel',
      });

      return result.success;
    } catch (error) {
      console.error('Biometric authentication failed:', error);
      return false;
    }
  }

  async setBiometricEnabled(enabled: boolean): Promise<void> {
    try {
      await AsyncStorage.setItem(this.BIOMETRIC_ENABLED_KEY, enabled.toString());
    } catch (error) {
      console.error('Failed to set biometric preference:', error);
    }
  }

  async isBiometricEnabled(): Promise<boolean> {
    try {
      const enabled = await AsyncStorage.getItem(this.BIOMETRIC_ENABLED_KEY);
      return enabled === 'true';
    } catch (error) {
      console.error('Failed to get biometric preference:', error);
      return false;
    }
  }

  // Password management
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    try {
      await apiService.post('/auth/change-password', {
        currentPassword,
        newPassword,
      });
    } catch (error) {
      console.error('Password change failed:', error);
      throw new Error('Failed to change password');
    }
  }

  async resetPassword(email: string): Promise<void> {
    try {
      await apiService.post('/auth/reset-password', { email });
    } catch (error) {
      console.error('Password reset failed:', error);
      throw new Error('Failed to initiate password reset');
    }
  }

  // Session management
  async getSessionInfo(): Promise<{ userId: string; expiresAt: string } | null> {
    if (!this.session) return null;
    return {
      userId: this.session.user.id,
      expiresAt: this.session.expiresAt,
    };
  }

  async extendSession(): Promise<void> {
    if (this.session) {
      this.session.expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
      await this.saveSession(this.session);
    }
  }
}

export const authService = new AuthService();
export default AuthService;