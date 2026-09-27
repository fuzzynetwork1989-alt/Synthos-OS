import React from 'react';
import { render, screen } from '@testing-library/react-native';
import Index from '../../app/index';

describe('Index Screen', () => {
  it('renders without crashing', () => {
    render(<Index />);
  });

  it('displays the main interface', () => {
    render(<Index />);
    // Add specific assertions based on your index screen content
    // Example: expect(screen.getByText('Welcome')).toBeTruthy();
  });
});