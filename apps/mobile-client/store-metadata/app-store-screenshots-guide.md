# App Store Screenshots Guide

## Screenshot Requirements

### iOS App Store Screenshots
- **Required Sizes**: 
  - 6.7" Display: 1290x2796px (iPhone 14 Pro Max)
  - 6.5" Display: 1242x2688px (iPhone 14 Plus)
  - 5.5" Display: 1242x2208px (iPhone 8 Plus)
- **Format**: PNG or JPEG
- **Minimum**: 1 screenshot
- **Maximum**: 10 screenshots
- **Content**: Must accurately represent app functionality

### Android Play Store Screenshots
- **Required Sizes**:
  - Phone: 1080x1920px, 1080x2220px
  - Tablet: 1200x1800px
  - Minimum: 2 screenshots (phone)
  - Maximum: 8 screenshots per device type
- **Format**: PNG or JPEG (no transparency)
- **Content**: Must show actual app interface

## Screenshot Strategy

### Screenshot Themes
1. **Hero Shot**: Main interface with key features highlighted
2. **Chat Interface**: AI conversation demonstration
3. **Memory Management**: Memory storage and retrieval
4. **Tool Integration**: Tool execution and results
5. **Settings Interface**: Configuration options
6. **Offline Mode**: Offline functionality demonstration
7. **Security Features**: Privacy and security highlights
8. **Cross-Platform**: Multi-device synchronization

### Design Guidelines
- **Device Frames**: Use realistic device frames for presentation
- **Consistent Branding**: Maintain brand colors and identity
- **Real Content**: Use actual app interface, not mockups
- **Focus on Benefits**: Highlight user benefits, not just features
- **Clear Call-to-Actions**: Include subtle CTAs where appropriate
- **Text Overlays**: Keep text minimal and readable

### Screenshot Descriptions
Each screenshot should have accompanying description:
- **Purpose**: What the screenshot demonstrates
- **Features**: Key features shown
- **Benefits**: User benefits highlighted
- **Use Case**: Typical user scenario

## Creation Tools

### Recommended Tools
- **CleanShot X**: Screen capture with device frames
- **Screenshot Framer**: Add device frames to screenshots
- **Mockup Phone**: Device mockup generator
- **Figma**: Design and prototype screenshots
- **Sketch**: Mac-based design tool

### DIY Approach
```bash
# Using iOS Simulator
xcrun simctl io booted launchScreenshot

# Using Android Emulator
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png
```

## Production Checklist

### Before Upload
- [ ] Screenshots are high resolution (at least 1080p)
- [ ] Screenshots show actual app interface
- [ ] Screenshots are current (not outdated UI)
- [ ] Screenshots follow platform guidelines
- [ ] Screenshots are properly named and organized
- [ ] Screenshots include appropriate device frames
- [ ] Screenshots demonstrate key features
- [ ] Screenshots highlight user benefits
- [ ] Screenshots are consistent with app branding
- [ ] Screenshots comply with content policies

### Quality Assurance
- Test screenshots on different devices
- Verify text readability
- Check color accuracy
- Ensure no distortion or artifacts
- Validate file sizes and formats
- Confirm compliance with store policies

## Current Status
- ✅ Screenshot guidelines created
- ❌ Actual screenshots needed
- ❌ Device frame generation needed
- ❌ Screenshot descriptions needed
- ❌ Store upload process needed

## Next Actions
1. Create app screenshots for iOS (6.7" display)
2. Create app screenshots for Android (phone)
3. Create app screenshots for Android (tablet)
4. Add device frames to screenshots
5. Write screenshot descriptions
6. Test screenshots on actual devices
7. Upload to respective app stores
8. Monitor screenshot performance and iterate