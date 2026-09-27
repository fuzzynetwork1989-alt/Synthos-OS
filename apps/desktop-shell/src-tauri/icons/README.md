# Desktop App Icons

This directory contains icon files for the Synthos OS desktop application.

## Required Icons

The following icon files are required for Tauri desktop builds:

- `32x32.png` - 32x32 pixel PNG icon
- `128x128.png` - 128x128 pixel PNG icon  
- `128x128@2x.png` - 256x256 pixel PNG icon (retina)
- `icon.icns` - macOS icon file
- `icon.ico` - Windows icon file

## Icon Generation

These are placeholder files. For production, you need to:

1. Create a high-quality app icon design
2. Generate multiple sizes for different platforms
3. Use tools like:
   - [Tauri Icon Maker](https://tauri.app/v1/guides/features/icons/)
   - [ImageMagick](https://imagemagick.org/)
   - Professional design tools (Figma, Sketch, Adobe Illustrator)

## Icon Requirements

### Windows
- ICO format with multiple sizes embedded
- Required sizes: 16x16, 32x32, 48x48, 256x256
- Should follow Windows design guidelines

### macOS
- ICNS format with multiple sizes
- Required sizes: 16x16, 32x32, 128x128, 256x256, 512x512, 1024x1024
- Should follow Apple Human Interface Guidelines

### Linux
- PNG format at 128x128 and 512x512
- Should follow freedesktop.org icon theme specification

## Current Status

Placeholders are provided for development. Replace with production icons before distribution.
