# Asset Requirements for Quest 3

## Required Assets

### Icons
- `icon-72.png` - 72x72 pixels
- `icon-96.png` - 96x96 pixels
- `icon-144.png` - 144x144 pixels
- `icon-192.png` - 192x192 pixels
- `icon-512.png` - 512x512 pixels (primary icon)

### Images
- `banner-1200x630.png` - Store banner (1200x630 pixels)
- `hero-1024x500.png` - Hero image (1024x500 pixels)

### Screenshots (Required for Store)
- `screenshot1.png` - 1920x1080 pixels
- `screenshot2.png` - 1920x1080 pixels
- `screenshot3.png` - 1920x1080 pixels
- `screenshot4.png` - 1920x1080 pixels
- `screenshot5.png` - 1920x1080 pixels

### Audio Assets
- `ui-click.wav` - UI interaction sound
- `ui-hover.wav` - UI hover sound
- `notification.wav` - Notification sound
- `voice-start.wav` - Voice activation sound
- `voice-end.wav` - Voice deactivation sound

### 3D Assets
- `panel-gltf/` - Holographic panel 3D models
- `cursor-gltf/` - 3D cursor models
- `avatar-gltf/` - AI avatar models

## Asset Guidelines

### Icons
- Use PNG format with transparency
- Maintain visual consistency across sizes
- Follow Meta Quest design guidelines
- Ensure high contrast for visibility

### Screenshots
- 1920x1080 resolution minimum
- Show core features in action
- Include UI elements clearly visible
- Demonstrate spatial interactions
- Show AI assistance features

### Audio
- WAV or OGG format
- 48kHz sample rate
- 16-bit or 24-bit depth
- Short duration (< 3 seconds for UI sounds)
- Spatial audio format for 3D positioning

### 3D Models
- glTF 2.0 format
- Optimized polygon count (< 50k per model)
- Compressed textures (ASTC)
- Proper UV mapping
- Include normal maps for detail

## Asset Creation Workflow

1. Create high-resolution source assets
2. Optimize for Quest 3 performance
3. Test on actual hardware
4. Verify file sizes and formats
5. Update asset references in code

## Asset Optimization

### Image Optimization
- Use PNG-8 for simple graphics
- Use PNG-24 for complex images
- Consider WebP for better compression
- Remove unnecessary metadata

### Audio Optimization
- Use appropriate bitrates
- Remove silence from beginning/end
- Normalize audio levels
- Use mono for UI sounds

### 3D Model Optimization
- Reduce polygon count
- Combine similar materials
- Use texture atlases
- Optimize UV layouts
- Remove hidden faces

## Asset Storage Structure
```
assets/
├── icons/
│   ├── icon-72.png
│   ├── icon-96.png
│   ├── icon-144.png
│   ├── icon-192.png
│   └── icon-512.png
├── images/
│   ├── banner-1200x630.png
│   ├── hero-1024x500.png
│   └── screenshots/
│       ├── screenshot1.png
│       ├── screenshot2.png
│       ├── screenshot3.png
│       ├── screenshot4.png
│       └── screenshot5.png
├── audio/
│   ├── ui-click.wav
│   ├── ui-hover.wav
│   ├── notification.wav
│   ├── voice-start.wav
│   └── voice-end.wav
└── 3d/
    ├── panel-gltf/
    ├── cursor-gltf/
    └── avatar-gltf/
```

## Current Status
Currently using placeholder assets. Production assets need to be created following the guidelines above.