# GitHub Secrets Configuration for Mobile CI/CD

This document outlines all required GitHub secrets for the mobile build workflows in Synthos-OS.

## Required GitHub Secrets

### EAS Authentication

#### `EXPO_TOKEN`
- **Description**: Expo/EAS authentication token for build and submission
- **How to obtain**: 
  1. Login to Expo: `eas login`
  2. Get token: `eas whoami` or from Expo account settings
  3. Or generate from Expo dashboard: https://expo.dev/accounts/[your-account]/settings/access-tokens
- **Required for**: All builds and submissions
- **Workflows**: `mobile-ios-build.yml`, `mobile-android-build.yml`

### iOS Secrets

#### `EXPO_APPLE_ID`
- **Description**: Apple ID email for App Store Connect
- **Format**: Email address (e.g., `your-apple-id@example.com`)
- **How to obtain**: Your Apple Developer account email
- **Required for**: iOS App Store submission
- **Workflows**: `mobile-ios-build.yml` (ios-submit job)

#### `EXPO_APPLE_ASC_APP_ID`
- **Description**: App Store Connect App ID (not bundle identifier)
- **Format**: Numeric string (e.g., `1234567890`)
- **How to obtain**: 
  1. Go to App Store Connect
  2. Select your app
  3. Find App ID in URL or App Information section
- **Required for**: iOS App Store submission
- **Workflows**: `mobile-ios-build.yml` (ios-submit job)

#### `EXPO_APPLE_TEAM_ID`
- **Description**: Apple Developer Team ID
- **Format**: 10-character alphanumeric string (e.g., `ABCD123456`)
- **How to obtain**: 
  1. Go to Apple Developer Portal
  2. Account > Membership
  3. Find Team ID
- **Required for**: iOS App Store submission
- **Workflows**: `mobile-ios-build.yml` (ios-submit job)

#### `EXPO_IOS_DIST_P12_PASSWORD` (Optional)
- **Description**: Password for iOS distribution certificate (.p12 file)
- **Format**: String password
- **How to obtain**: Set when exporting certificate from Keychain Access
- **Required for**: Manual iOS builds (if not using EAS managed certificates)
- **Workflows**: Local build scripts

### Android Secrets

#### `EXPO_ANDROID_KEYSTORE_PASSWORD`
- **Description**: Password for Android keystore file
- **Format**: String password
- **How to obtain**: Set when generating keystore with keytool
- **Required for**: Android production builds
- **Workflows**: `mobile-android-build.yml` (android-build job)

#### `EXPO_ANDROID_KEY_PASSWORD`
- **Description**: Password for specific key within keystore
- **Format**: String password
- **How to obtain**: Set when generating keystore with keytool
- **Required for**: Android production builds
- **Workflows**: `mobile-android-build.yml` (android-build job)

#### `EXPO_ANDROID_SERVICE_ACCOUNT_KEY`
- **Description**: Google Play Service Account JSON key for API access
- **Format**: JSON string (must be properly escaped for GitHub Actions)
- **How to obtain**: 
  1. Go to Google Play Console
  2. Setup > API access
  3. Create service account or use existing
  4. Download JSON key
  5. Grant permissions in Play Console
- **Required for**: Android Play Store submission
- **Workflows**: `mobile-android-build.yml` (android-submit job)

## Setting Up GitHub Secrets

### Via GitHub Web Interface

1. Go to your repository: `https://github.com/fuzzynetwork1989-alt/Synthos-OS`
2. Navigate to **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Add each secret with its name and value
5. Click **Add secret**

### Via GitHub CLI

```bash
# Set each secret
gh secret set EXPO_TOKEN
gh secret set EXPO_APPLE_ID
gh secret set EXPO_APPLE_ASC_APP_ID
gh secret set EXPO_APPLE_TEAM_ID
gh secret set EXPO_ANDROID_KEYSTORE_PASSWORD
gh secret set EXPO_ANDROID_KEY_PASSWORD
gh secret set EXPO_ANDROID_SERVICE_ACCOUNT_KEY
```

### Environment-Specific Secrets (Optional)

For different environments (development, staging, production), you can use GitHub Environments:

1. Go to **Settings** > **Environments**
2. Create environments: `development`, `preview`, `production`
3. Add environment-specific secrets to each environment
4. Update workflows to use environment-specific secrets

## Secret Management Best Practices

### Security
- Never commit secrets to version control
- Use strong, unique passwords for each secret
- Rotate secrets periodically (recommended: every 90 days)
- Limit secret access to necessary team members
- Use GitHub's secret scanning to detect accidental commits

### Access Control
- Only give repository admin access to manage secrets
- Use separate service accounts for automated submissions
- Implement approval workflows for production deployments
- Monitor secret usage in GitHub Actions logs

### Backup and Recovery
- Document secret values in secure password manager
- Store keystore files and certificates in secure location
- Have process for secret rotation and recovery
- Test secret validity before production deployments

## Troubleshooting

### Secret Not Found
- **Error**: `Error: Input required and not supplied: secrets.EXPO_TOKEN`
- **Solution**: Verify secret name matches exactly (case-sensitive)
- **Check**: Repository Settings > Secrets to confirm secret exists

### Invalid Credentials
- **Error**: `Authentication failed` or `401 Unauthorized`
- **Solution**: Verify secret value is correct and not expired
- **Check**: Expo token validity, Apple Developer account status, Google Play Console access

### Malformed JSON
- **Error**: `Invalid JSON in service account key`
- **Solution**: Ensure JSON is properly escaped for GitHub Actions
- **Check**: Use `echo 'JSON' | base64` for safe encoding

### Permission Issues
- **Error**: `Permission denied` or `403 Forbidden`
- **Solution**: Verify service account has correct permissions
- **Check**: App Store Connect roles, Google Play Console API access

## Workflow-Specific Secret Requirements

### iOS Build Workflow
- **Always required**: `EXPO_TOKEN`
- **Production builds**: `EXPO_APPLE_ID`, `EXPO_APPLE_ASC_APP_ID`, `EXPO_APPLE_TEAM_ID`
- **Optional**: `EXPO_IOS_DIST_P12_PASSWORD` (for manual certificate management)

### Android Build Workflow
- **Always required**: `EXPO_TOKEN`
- **Production builds**: `EXPO_ANDROID_KEYSTORE_PASSWORD`, `EXPO_ANDROID_KEY_PASSWORD`
- **Store submission**: `EXPO_ANDROID_SERVICE_ACCOUNT_KEY`

## Testing Secret Configuration

### Test EAS Token
```bash
# Locally test your Expo token
eas whoami
# Should show your account information
```

### Test Apple Credentials
```bash
# Verify Apple Developer account access
# Check App Store Connect for your app
```

### Test Android Credentials
```bash
# Verify keystore access
keytool -list -v -keystore your-keystore.keystore
# Enter password when prompted
```

### Test GitHub Actions
1. Push a small change to trigger workflow
2. Monitor Actions tab for workflow execution
3. Check logs for secret-related errors
4. Verify build completes successfully

## Next Steps

1. Set up Apple Developer account ($99/year)
2. Set up Google Play Developer account ($25 one-time)
3. Generate Expo token and add to GitHub secrets
4. Configure Apple Developer App ID and provisioning profiles
5. Generate Android keystore and add passwords to GitHub secrets
6. Set up Google Play Service Account for API access
7. Test workflows with a sample build
8. Monitor first production deployment carefully

## Additional Resources

- [GitHub Actions Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Expo EAS Build Documentation](https://docs.expo.dev/build/introduction/)
- [Apple Developer Documentation](https://developer.apple.com/documentation/)
- [Google Play Console API Access](https://support.google.com/googleplay/android-developer/answer/9844756)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)