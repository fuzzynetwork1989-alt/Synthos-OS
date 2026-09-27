@echo off
REM iOS Build Script for Synthos OS (Windows)
REM This script handles the complete iOS build process for App Store distribution

setlocal enabledelayedexpansion

set APP_NAME=Synthos OS
set BUNDLE_ID=com.synthos.os
set BUILD_TYPE=%1
if "%BUILD_TYPE%"=="" set BUILD_TYPE=production

echo ========================================
echo   iOS Build Script for %APP_NAME%
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "package.json" (
    echo Error: package.json not found. Please run this script from the app root directory.
    exit /b 1
)

REM Check for required tools
echo Checking for required tools...

where eas >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: EAS CLI not found. Install with: npm install -g eas-cli
    exit /b 1
)

where node >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Node.js not found. Please install Node.js 18 or higher.
    exit /b 1
)

echo Required tools found
echo.

REM Install dependencies
echo Installing dependencies...
call npm install
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    exit /b 1
)
echo Dependencies installed
echo.

REM Check environment variables
echo Checking environment variables...

if "%BUILD_TYPE%"=="production" (
    if "%EXPO_IOS_DIST_P12_PASSWORD%"=="" (
        echo Warning: EXPO_IOS_DIST_P12_PASSWORD not set. Production builds may fail.
    )
    
    if "%EXPO_TOKEN%"=="" (
        echo Warning: EXPO_TOKEN not set. You may need to authenticate.
    )
)

echo Environment check complete
echo.

REM Run type checking
echo Running type check...
call npm run typecheck
if %errorlevel% neq 0 (
    echo Error: Type check failed
    exit /b 1
)
echo Type check passed
echo.

REM Run linting
echo Running linter...
call npm run lint
if %errorlevel% neq 0 (
    echo Error: Linting failed
    exit /b 1
)
echo Linting passed
echo.

REM Run tests
echo Running tests...
call npm test
if %errorlevel% neq 0 (
    echo Error: Tests failed
    exit /b 1
)
echo Tests passed
echo.

REM Configure EAS project if needed
if not exist "eas.json" (
    echo Configuring EAS project...
    call eas build:configure
    if %errorlevel% neq 0 (
        echo Error: Failed to configure EAS project
        exit /b 1
    )
    echo EAS project configured
    echo.
)

REM Build the app
echo Building iOS app (%BUILD_TYPE%)...
echo.

if "%BUILD_TYPE%"=="development" (
    call eas build --platform ios --profile development
) else if "%BUILD_TYPE%"=="preview" (
    call eas build --platform ios --profile preview
) else if "%BUILD_TYPE%"=="production" (
    call eas build --platform ios --profile production
) else if "%BUILD_TYPE%"=="simulator" (
    call eas build --platform ios --profile simulator
) else (
    echo Error: Invalid build type. Use: development, preview, production, or simulator
    exit /b 1
)

if %errorlevel% neq 0 (
    echo Error: Build failed
    exit /b 1
)

echo.
echo ========================================
echo   iOS build completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Test the build on iOS devices/simulator
echo 2. For production: Submit to App Store with: npm run submit:ios
echo 3. Monitor build status in EAS dashboard

endlocal
