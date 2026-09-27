import React from 'react';
import { render, screen } from '@testing-library/react-native';
import IndexScreen from '../app/index';
import ChatScreen from '../app/chat';
import SettingsScreen from '../app/settings';
import MemoryScreen from '../app/memory';
import MemoryCreateScreen from '../app/memory-create';
import ToolsScreen from '../app/tools';
import LoginScreen from '../app/login';

describe('Screen Components', () => {
  describe('Index Screen', () => {
    it('renders without crashing', () => {
      render(<IndexScreen />);
    });

    it('has expected structure', () => {
      const { UNSAFE_root } = render(<IndexScreen />);
      expect(UNSAFE_root).toBeTruthy();
    });
  });

  describe('Chat Screen', () => {
    it('renders without crashing', () => {
      render(<ChatScreen />);
    });

    it('has expected structure', () => {
      const { UNSAFE_root } = render(<ChatScreen />);
      expect(UNSAFE_root).toBeTruthy();
    });
  });

  describe('Settings Screen', () => {
    it('renders without crashing', () => {
      render(<SettingsScreen />);
    });

    it('has expected structure', () => {
      const { UNSAFE_root } = render(<SettingsScreen />);
      expect(UNSAFE_root).toBeTruthy();
    });
  });

  describe('Memory Screen', () => {
    it('renders without crashing', () => {
      render(<MemoryScreen />);
    });

    it('has expected structure', () => {
      const { UNSAFE_root } = render(<MemoryScreen />);
      expect(UNSAFE_root).toBeTruthy();
    });
  });

  describe('Memory Create Screen', () => {
    it('renders without crashing', () => {
      render(<MemoryCreateScreen />);
    });

    it('has expected structure', () => {
      const { UNSAFE_root } = render(<MemoryCreateScreen />);
      expect(UNSAFE_root).toBeTruthy();
    });
  });

  describe('Tools Screen', () => {
    it('renders without crashing', () => {
      render(<ToolsScreen />);
    });

    it('has expected structure', () => {
      const { UNSAFE_root } = render(<ToolsScreen />);
      expect(UNSAFE_root).toBeTruthy();
    });
  });

  describe('Login Screen', () => {
    it('renders without crashing', () => {
      render(<LoginScreen />);
    });

    it('has expected structure', () => {
      const { UNSAFE_root } = render(<LoginScreen />);
      expect(UNSAFE_root).toBeTruthy();
    });
  });
});