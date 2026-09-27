#!/bin/bash
# Synthos-OS Monitoring Script
# This script monitors Synthos-OS services and system health

echo "========================================"
echo "  Synthos-OS System Monitor"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check service
check_service() {
    local name=$1
    local url=$2
    
    if curl -s --max-time 5 "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $name: Healthy"
        return 0
    else
        echo -e "${RED}✗${NC} $name: Unhealthy"
        return 1
    fi
}

# Function to check docker container
check_container() {
    local name=$1
    
    if docker ps --filter "name=$name" --format "{{.Status}}" 2>/dev/null | grep -q "Up"; then
        echo -e "${GREEN}✓${NC} $name: Running"
        return 0
    else
        echo -e "${RED}✗${NC} $name: Not running"
        return 1
    fi
}

echo "========================================"
echo "  System Information"
echo "========================================"
echo "Hostname: $(hostname)"
echo "Uptime: $(uptime -p)"
echo "Load Average: $(uptime | awk -F'load average:' '{print $2}')"
echo "Memory Usage: $(free -h | grep Mem | awk '{print $3 "/" $2}')"
echo "Disk Usage: $(df -h / | tail -1 | awk '{print $3 "/" $2 " (" $5 ")"}')"
echo "Docker Version: $(docker --version)"
echo ""

echo "========================================"
echo "  Docker Containers"
echo "========================================"
check_container "synthos-postgres"
check_container "synthos-redis"
check_container "synthos-ollama"
check_container "synthos-api-gateway"
check_container "synthos-model-gateway"
check_container "synthos-memory-engine"
check_container "synthos-rsi-engine"
check_container "synthos-cognitive-engine"
check_container "synthos-tool-execution-engine"
echo ""

echo "========================================"
echo "  Service Health"
echo "========================================"
check_service "API Gateway" "http://localhost:8000/health"
check_service "Model Gateway" "http://localhost:8002/health"
check_service "Memory Engine" "http://localhost:8003/health"
check_service "RSI Engine" "http://localhost:8004/health"
check_service "Cognitive Engine" "http://localhost:8005/health"
check_service "Tool Execution Engine" "http://localhost:8006/health"
echo ""

echo "========================================"
echo "  Resource Usage"
echo "========================================"
echo "CPU Usage:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}" 2>/dev/null | grep synthos || echo "No containers running"
echo ""
echo "Memory Usage:"
docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}" 2>/dev/null | grep synthos || echo "No containers running"
echo ""

echo "========================================"
echo "  Disk Usage"
echo "========================================"
df -h | grep -E "(Filesystem|/dev/)"
echo ""
echo "Docker Disk Usage:"
docker system df
echo ""

echo "========================================"
echo "  Network Status"
echo "========================================"
echo "Active Connections:"
netstat -an | grep ESTABLISHED | wc -l
echo ""
echo "Listening Ports:"
netstat -tlnp 2>/dev/null | grep -E "(8000|8002|8003|8004|8005|8006|3000|5432|6379|11434)" || echo "No relevant ports listening"
echo ""

echo "========================================"
echo "  Recent Errors"
echo "========================================"
echo "Recent Docker errors (last 10 lines):"
docker-compose logs --tail=10 2>/dev/null | grep -i error || echo "No recent errors"
echo ""

echo "========================================"
echo "  Ollama Models"
echo "========================================"
docker exec synthos-ollama ollama list 2>/dev/null || echo "Cannot list models"
echo ""

echo "========================================"
echo "  Database Status"
echo "========================================"
echo "PostgreSQL Connections:"
docker exec synthos-postgres psql -U synthos -d synthos_os -c "SELECT count(*) FROM pg_stat_activity;" 2>/dev/null || echo "Cannot check connections"
echo ""
echo "Database Size:"
docker exec synthos-postgres psql -U synthos -d synthos_os -c "SELECT pg_size_pretty(pg_database_size('synthos_os'));" 2>/dev/null || echo "Cannot check size"
echo ""

echo "========================================"
echo "  SSL Certificate Status"
echo "========================================"
if command -v certbot &> /dev/null; then
    certbot certificates 2>/dev/null || echo "No SSL certificates found"
else
    echo "Certbot not installed"
fi
echo ""

echo "========================================"
echo "  Backup Status"
echo "========================================"
BACKUP_DIR="/var/backups/synthos-os"
if [ -d "$BACKUP_DIR" ]; then
    echo "Latest backup:"
    ls -lt $BACKUP_DIR/manifest_*.txt 2>/dev/null | head -1 || echo "No backups found"
    echo ""
    echo "Backup directory size:"
    du -sh $BACKUP_DIR 2>/dev/null || echo "Cannot check size"
else
    echo "Backup directory not found"
fi
echo ""

echo "========================================"
echo "  Systemd Service Status"
echo "========================================"
systemctl status synthos-os --no-pager -l 2>/dev/null || echo "Service not found"
echo ""

echo "========================================"
echo "  Monitor Complete!"
echo "========================================"
echo ""
echo "Quick Actions:"
echo "- View logs: docker-compose logs -f"
echo "- Restart services: sudo systemctl restart synthos-os"
echo "- Check status: sudo systemctl status synthos-os"
echo "- Create backup: ./scripts/backup.sh"
echo ""