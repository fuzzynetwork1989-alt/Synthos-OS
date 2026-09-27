#!/bin/bash

# iOS Build Script for Synthos OS
# This script handles the complete iOS build process for App Store distribution

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="Synthos OS"
BUNDLE_ID="com.synthos.os"
BUILD_TYPE=${1:-production}  # Default to production build

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  iOS Build Script for $APP_NAME${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo -e "${RED}Error: package.json not found. Please run this script from the app root directory.${NC}"
    exit 1
fi

# Check for required tools
echo -e "${YELLOW}Checking for required tools...${NC}"

if ! command -v eas &> /dev/null; then
    echo -e "${RED}Error: EAS CLI not found. Install with: npm install -g eas-cli${NC}"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js not found. Please install Node.js 18 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Required tools found${NC}"
echo ""

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
npm install
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Check environment variables
echo -e "${YELLOW}Checking environment variables...${NC}"

if [ "$BUILD_TYPE" = "production" ]; then
    if [ -z "$EXPO_IOS_DIST_P12_PASSWORD" ]; then
        echo -e "${YELLOW}Warning: EXPO_IOS_DIST_P12_PASSWORD not set. Production builds may fail.${NC}"
    fi
    
    if [ -z "$EXPO_TOKEN" ]; then
        echo -e "${YELLOW}Warning: EXPO_TOKEN not set. You may need to authenticate.${NC}"
    fi
fi

echo -e "${GREEN}✓ Environment check complete${NC}"
echo ""

# Run type checking
echo -e "${YELLOW}Running type check...${NC}"
npm run typecheck
echo -e "${GREEN}✓ Type check passed${NC}"
echo ""

# Run linting
echo -e "${YELLOW}Running linter...${NC}"
npm run lint
echo -e "${GREEN}✓ Linting passed${NC}"
echo ""

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
npm test
echo -e "${GREEN}✓ Tests passed${NC}"
echo ""

# Configure EAS project if needed
if [ ! -f "eas.json" ]; then
    echo -e "${YELLOW}Configuring EAS project...${NC}"
    eas build:configure
    echo -e "${GREEN}✓ EAS project configured${NC}"
    echo ""
fi

# Build the app
echo -e "${YELLOW}Building iOS app ($BUILD_TYPE)...${NC}"
echo ""

case $BUILD_TYPE in
    "development")
        eas build --platform ios --profile development
        ;;
    "preview")
        eas build --platform ios --profile preview
        ;;
    "production")
        eas build --platform ios --profile production
        ;;
    "simulator")
        eas build --platform ios --profile simulator
        ;;
    *)
        echo -e "${RED}Error: Invalid build type. Use: development, preview, production, or simulator${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  iOS build completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Test the build on iOS devices/simulator"
echo "2. For production: Submit to App Store with: npm run submit:ios"
echo "3. Monitor build status in EAS dashboard"
