#!/bin/bash

# Synthos-OS Monitoring Stack Stop Script

set -e

echo "=========================================="
echo "  Stopping Monitoring Stack"
echo "=========================================="
echo ""

# Stop monitoring stack
echo "Stopping monitoring stack..."
docker-compose -f docker-compose.monitoring.yml down

echo ""
echo "✅ Monitoring stack stopped successfully!"