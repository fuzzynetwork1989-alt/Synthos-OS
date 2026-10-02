#!/bin/bash

# Synthos-OS Monitoring Stack Startup Script

set -e

echo "=========================================="
echo "  Synthos-OS Monitoring Stack"
echo "=========================================="
echo ""

# Create monitoring network if it doesn't exist
if ! docker network inspect synthos-network &> /dev/null; then
    echo "Creating synthos-network..."
    docker network create synthos-network
fi

# Start monitoring stack
echo "Starting monitoring stack..."
docker-compose -f docker-compose.monitoring.yml up -d

echo ""
echo "✅ Monitoring stack started successfully!"
echo ""
echo "Monitoring Services:"
echo "  - Prometheus: http://localhost:9090"
echo "  - Grafana: http://localhost:3001 (admin/admin)"
echo "  - Node Exporter: http://localhost:9100"
echo ""
echo "📊 View metrics in Grafana dashboards"
echo "🛑 Stop monitoring: ./scripts/monitoring-stop.sh"