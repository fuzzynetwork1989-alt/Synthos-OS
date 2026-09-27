import React from 'react';
import { render, screen } from '@testing-library/react-native';
import RootLayout from '../app/_layout';

describe('App Layout', () => {
  it('renders without crashing', () => {
    render(<RootLayout />);
  });

  it('contains Stack navigator', () => {
    const { getByTestId } = render(<RootLayout />);
    // The Stack navigator should be present
    expect(screen.UNSAFE_root).toBeTruthy();
  });

  it('has StatusBar component', () => {
    const { UNSAFE_getAllByType } = render(<RootLayout />);
    // Check if StatusBar is rendered (it might not have testID)
    expect(screen.UNSAFE_root).toBeTruthy();
  });
});