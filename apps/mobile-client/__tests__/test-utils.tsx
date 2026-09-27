import React from 'react';
import { render, RenderOptions } from '@testing-library/react-native';

// Custom render function that wraps components with necessary providers
const AllTheProviders = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};

const customRender = (ui: React.ReactElement, options?: Omit<RenderOptions, 'wrapper'>) =>
  render(ui, { wrapper: AllTheProviders, ...options });

// Re-export everything from testing-library
export * from '@testing-library/react-native';
export { customRender as render };