# App Icon Generation Guide

## Production Icon Requirements

### iOS App Icons
- **App Store Icon**: 1024x1024px (PNG, no transparency)
- **iPhone App Icon**: 60x60pt (@2x: 120x120px, @3x: 180x180px)
- **iPad App Icon**: 76x76pt (@2x: 152x152px)
- **iPad Pro App Icon**: 83.5x83.5pt (@2x: 167x167px)
- **Settings Icon**: 29x29pt (@2x: 58x58px, @3x: 87x87px)
- **Spotlight Icon**: 40x40pt (@2x: 80x80px, @3x: 120x120px)
- **Notification Icon**: 20x20pt (@2x: 40x40px, @3x: 60x60px)

### Android App Icons
- **Play Store Icon**: 512x512px (PNG, no transparency)
- **Adaptive Icon**: 108x108dp (foreground layer)
- **Adaptive Icon Background**: 108x108dp (background layer)
- **Launcher Icon**: 48x48dp (mdpi), 72x72dp (hdpi), 96x96dp (xhdpi), 144x144dp (xxhdpi), 192x192dp (xxxhdpi)
- **Notification Icon**: 24x24dp (mdpi), 36x36dp (hdpi), 48x48dp (xhdpi), 72x72dp (xxhdpi), 96x96dp (xxxhdpi)

## Icon Design Guidelines

### Brand Identity
- **Primary Color**: #007AFF (Blue)
- **Secondary Color**: #4CAF50 (Green for online status)
- **Accent Color**: #FF9800 (Orange for warnings)
- **Style**: Modern, minimalist, tech-focused
- **Elements**: Brain/AI neural network symbol + OS interface elements

### Icon Variations
1. **Main App Icon**: Brain circuit pattern with OS interface elements
2. **Settings Icon**: Gear symbol with neural network background
3. **Notification Icon**: Simplified brain icon
4. **Spotlight Icon**: Square version of main icon

## Generation Tools

### Recommended Tools
- **Figma**: Professional design tool with icon export
- **Sketch**: Mac-based design tool
- **Canva**: Online design tool with icon templates
- **AppIcon.co**: Online icon generator
- **MakeAppIcon.com**: Batch icon generator

### Command Line Tools
```bash
# Using ImageMagick
convert icon-1024.png -resize 180x180 icon-180.png
convert icon-1024.png -resize 152x152 icon-152.png
convert icon-1024.png -resize 120x120 icon-120.png
```

## Implementation Steps

### 1. Create Base Icon
- Design 1024x1024px base icon in Figma
- Use proper color palette
- Ensure no transparency for app store
- Export as PNG

### 2. Generate iOS Icons
- Use AppIcon.co or manual resizing
- Create all required sizes
- Place in `ios/Assets.xcassets/AppIcon.appiconset/`

### 3. Generate Android Icons
- Create adaptive icon layers
- Generate all density variants
- Place in `android/app/src/main/res/mipmap-*/`

### 4. Update Configuration
- Update `app.json` icon references
- Test icon rendering on devices
- Verify icon appears correctly in all contexts

## Current Status
- ✅ Placeholder icons exist
- ❌ Production icons needed
- ❌ Icon generator setup needed
- ❌ Icon optimization needed

## Next Actions
1. Design production app icon (1024x1024px)
2. Generate all iOS icon variants
3. Generate all Android icon variants
4. Update app.json with proper icon paths
5. Test icons on real devices
6. Optimize icon file sizes