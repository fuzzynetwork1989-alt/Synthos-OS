# Code Signing and Certificate Configuration

This directory contains documentation and configuration for code signing certificates required for app store deployment.

## Overview

Code signing is required for both iOS and Android apps to be distributed through app stores. This ensures app authenticity and security.

## iOS Code Signing

### Prerequisites

1. **Apple Developer Account** ($99/year)
   - Enroll at https://developer.apple.com/programs/
   - Individual or Organization membership
   - Complete enrollment process

2. **Xcode** (macOS required)
   - Install Xcode from Mac App Store
   - Install command line tools: `xcode-select --install`

### Certificate Types

#### Development Certificate
- Used for development and testing
- Valid for 1 year
- Requires registered test devices

#### Distribution Certificate
- Used for App Store distribution
- Valid for 1 year
- Can be used for all users

### Setup Steps

#### 1. Create Certificate Signing Request (CSR)
```bash
# In Keychain Access:
# Keychain Access > Certificate Assistant > Request a Certificate from a Certificate Authority
# Save as: SynthosOS.certSigningRequest
```

#### 2. Create Development Certificate
- Go to Apple Developer Portal
- Certificates, Identifiers & Profiles > Certificates
- Create a new certificate > iOS App Development
- Upload CSR
- Download and install the certificate

#### 3. Create Distribution Certificate
- Go to Apple Developer Portal
- Certificates, Identifiers & Profiles > Certificates
- Create a new certificate > iOS Distribution (App Store and Ad Hoc)
- Upload CSR
- Download and install the certificate

#### 4. Register App ID
- Go to Identifiers > App IDs
- Register new App ID: `com.synthos.os`
- Configure capabilities (Camera, Microphone, Location, etc.)

#### 5. Create Provisioning Profiles
- Development Profile
  - For development builds
  - Include test devices
- App Store Profile
  - For App Store distribution
  - No device limitations

#### 6. Configure in Xcode
- Open project in Xcode
- Select target > Signing & Capabilities
- Select your team
- Choose correct provisioning profile

### Expo/EAS Build Configuration

For EAS builds, configure certificates in `eas.json`:

```json
{
  "build": {
    "production": {
      "ios": {
        "autoIncrement": true
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your-apple-id@example.com",
        "ascAppId": "YOUR_APP_STORE_CONNECT_APP_ID",
        "appleTeamId": "YOUR_APPLE_TEAM_ID"
      }
    }
  }
}
```

### Managing Certificates

#### Renew Certificates
- Certificates expire after 1 year
- Create new CSR before expiration
- Generate new certificate
- Update provisioning profiles

#### Backup Certificates
```bash
# Export from Keychain Access:
# Keychain Access > My Certificates
# Right-click certificate > Export
# Save as .p12 file (set password)
```

#### Share with Team
- Export certificates as .p12 files
- Share password securely
- Import on team machines

## Android Code Signing

### Prerequisites

1. **Google Play Developer Account** ($25 one-time)
   - Register at https://play.google.com/console
   - Complete registration and pay fee
   - Verify identity

2. **Java Development Kit (JDK)**
   - Install JDK 8 or higher
   - Set JAVA_HOME environment variable

### Keystore Management

#### 1. Generate Keystore
```bash
keytool -genkey -v -keystore synthos-os-release.keystore \
  -alias synthos-os-key-alias \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -storepass YOUR_STORE_PASSWORD \
  -keypass YOUR_KEY_PASSWORD \
  -dname "CN=Synthos OS, OU=Development, O=Synthos OS, L=City, ST=State, C=US"
```

#### 2. Secure Keystore
- **NEVER commit keystore to version control**
- Store in secure location (password manager, encrypted drive)
- Keep backup in secure location
- Share only with trusted team members

#### 3. Configure Signing in EAS
```json
{
  "build": {
    "production": {
      "android": {
        "autoIncrement": true
      }
    }
  }
}
```

#### 4. Environment Variables
Set these in your environment or CI/CD:
```bash
EXPO_ANDROID_KEYSTORE_PASSWORD=YOUR_STORE_PASSWORD
EXPO_ANDROID_KEY_PASSWORD=YOUR_KEY_PASSWORD
```

### Google Play App Signing

Google Play manages app signing for you:

#### 1. Upload App Bundle
- Use `eas build --platform android`
- Upload .aab file to Play Console

#### 2. Play App Signing
- Google generates signing key
- You keep upload key
- Google manages app signing key

#### 3. Upload Key
- Upload your keystore to Play Console
- Set up upload key credentials
- Configure release tracks

### Managing Android Keys

#### Key Rotation
- If keystore is compromised, rotate immediately
- Use Play Console key rotation feature
- Update upload key in console

#### Backup Strategy
- Keep multiple secure backups
- Document keystore location and passwords
- Use secure sharing for team access

## Environment Configuration

### Local Development
```bash
# iOS
export EXPO_IOS_DIST_P12_PASSWORD=your_p12_password
export EXPO_IOS_PROVISIONING_PROFILE_SPECIFIER=your_profile_id

# Android
export EXPO_ANDROID_KEYSTORE_PASSWORD=your_keystore_password
export EXPO_ANDROID_KEY_PASSWORD=your_key_password
```

### CI/CD (GitHub Actions)
```yaml
- name: Set up environment
  run: |
    echo "EXPO_IOS_DIST_P12_PASSWORD=${{ secrets.IOS_P12_PASSWORD }}" >> $GITHUB_ENV
    echo "EXPO_ANDROID_KEYSTORE_PASSWORD=${{ secrets.ANDROID_KEYSTORE_PASSWORD }}" >> $GITHUB_ENV
```

## Security Best Practices

### General
- Never commit credentials to version control
- Use environment variables for secrets
- Rotate credentials periodically
- Limit access to signing certificates
- Monitor certificate expiration dates

### iOS Specific
- Use separate certificates for dev/prod
- Keep provisioning profiles up to date
- Manage test devices carefully
- Use App Store Connect 2FA

### Android Specific
- Use strong keystore passwords
- Never share keystore files publicly
- Use Google Play App Signing when possible
- Keep backup of keystore in secure location
- Document keystore recovery process

## Troubleshooting

### iOS Issues

#### Certificate Expired
- Generate new CSR
- Create new certificate
- Update provisioning profiles
- Rebuild app

#### Provisioning Profile Mismatch
- Check bundle identifier matches
- Verify correct profile selected
- Update profile in Xcode
- Clean build folder

#### Team ID Issues
- Verify team membership
- Check Apple Developer account status
- Update team ID in configuration

### Android Issues

#### Keystore Password Wrong
- Verify password in environment variables
- Check for typos in configuration
- Reset keystore password if needed

#### Key Alias Mismatch
- Verify alias matches keystore
- Check build configuration
- Update alias in build scripts

#### Signature Version
- Ensure using APK Signature Scheme v2
- Check target SDK version
- Update build configuration

## Resources

### Apple Resources
- [Apple Developer Documentation](https://developer.apple.com/documentation/)
- [App Distribution Guide](https://help.apple.com/xcode/mac/current/#/dev154b28f09)
- [Expo iOS Builds](https://docs.expo.dev/build/introduction/)

### Android Resources
- [Google Play Console Help](https://support.google.com/googleplay/android-developer)
- [Android App Signing](https://developer.android.com/studio/publish/app-signing)
- [Expo Android Builds](https://docs.expo.dev/build/introduction/)

## Next Steps

1. Set up Apple Developer account
2. Set up Google Play Developer account
3. Generate iOS certificates
4. Generate Android keystore
5. Configure environment variables
6. Test build process
7. Deploy to app stores
