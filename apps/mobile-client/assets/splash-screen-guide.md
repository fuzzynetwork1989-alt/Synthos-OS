# Splash Screen Design Guide

## Splash Screen Requirements

### iOS Splash Screens
- **iPhone XS Max and later**: 896x414pt (@3x: 2688x1242px)
- **iPhone 8 and earlier**: 667x375pt (@2x: 1334x750px)
- **iPad Pro 12.9": 1366x1024pt (@2x: 2732x2048px)
- **iPad Pro 11": 1194x834pt (@2x: 2388x1668px)
- **iPad Mini and Air**: 1024x768pt (@2x: 2048x1536px)

### Android Splash Screens
- **Portrait**: 1080x1920px (mdpi), 1620x2880px (hdpi), 2160x3840px (xhdpi), 3240x5760px (xxhdpi), 4320x7680px (xxxhdpi)
- **Landscape**: 1920x1080px (mdpi), 2880x1620px (hdpi), 3840x2160px (xhdpi), 5760x3240px (xxhdpi), 7680x4320px (xxxhdpi)

## Design Guidelines

### Visual Elements
- **Background**: Gradient from #007AFF to #0056b3
- **Logo**: Centered Synthos OS logo (white)
- **Tagline**: "Next-Generation AI Operating System" (small, white)
- **Loading Indicator**: Subtle animation (optional)
- **Version Number**: Bottom corner, small text

### Animation Considerations
- Keep animations minimal and smooth
- Avoid heavy animations that might cause lag
- Consider system-wide animation settings
- Provide static fallback for users who disable animations

### Content Guidelines
- **No promotional content**: Splash screens should not contain ads or promotional material
- **Brand consistency**: Maintain brand identity throughout
- **Fast transition**: Keep splash screen duration short (2-3 seconds max)
- **Purpose**: Serve as loading screen, not promotional space

## Technical Implementation

### Expo Splash Screen Configuration
```json
{
  "splash": {
    "image": "./assets/splash.png",
    "resizeMode": "contain",
    "backgroundColor": "#007AFF"
  }
}
```

### Custom Splash Screen Components
- Create custom splash screen component
- Implement smooth transitions
- Handle loading states
- Provide fallback for offline scenarios

## Current Status
- ✅ Placeholder splash screen exists
- ❌ Production splash screens needed
- ❌ Multiple device variants needed
- ❌ Animation implementation needed
- ❌ Loading state handling needed

## Next Actions
1. Design production splash screen (1080x1920px base)
2. Generate all device-specific variants
3. Implement smooth loading transitions
4. Add loading state indicators
5. Test on different devices and orientations
6. Optimize splash screen performance
7. Ensure splash screen follows platform guidelines