import React from 'react';
import { render, screen } from '@testing-library/react-native';
import { Text, View } from 'react-native';

// Basic component tests - expand as components are added
describe('Basic Components', () => {
  it('renders a Text component', () => {
    render(<Text>Test Text</Text>);
    expect(screen.getByText('Test Text')).toBeTruthy();
  });

  it('renders a View component', () => {
    const { getByTestId } = render(
      <View testID="test-view">
        <Text>Content</Text>
      </View>
    );
    expect(getByTestId('test-view')).toBeTruthy();
  });
});