// Custom hook for authentication
import { useState, useEffect, useCallback } from 'react';
import { authService, AuthUser } from '../services/auth';

export function useAuth() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    initializeAuth();
  }, []);

  const initializeAuth = async () => {
    try {
      await authService.initialize();
      const currentUser = authService.getCurrentUser();
      setUser(currentUser);
      setIsAuthenticated(authService.isAuthenticated());
    } catch (error) {
      console.error('Auth initialization failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = useCallback(async (email: string, password: string) => {
    try {
      const loggedInUser = await authService.login(email, password);
      setUser(loggedInUser);
      setIsAuthenticated(true);
      return loggedInUser;
    } catch (error) {
      throw error;
    }
  }, []);

  const register = useCallback(async (email: string, password: string, name: string) => {
    try {
      const registeredUser = await authService.register(email, password, name);
      setUser(registeredUser);
      setIsAuthenticated(true);
      return registeredUser;
    } catch (error) {
      throw error;
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      await authService.logout();
      setUser(null);
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Logout failed:', error);
    }
  }, []);

  const refreshToken = useCallback(async () => {
    try {
      await authService.refreshToken();
      const currentUser = authService.getCurrentUser();
      setUser(currentUser);
    } catch (error) {
      console.error('Token refresh failed:', error);
    }
  }, []);

  return {
    user,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
    refreshToken,
  };
}