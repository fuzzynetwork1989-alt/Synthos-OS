#!/bin/bash
# Synthos-OS Restore Script
# This script restores Synthos-OS from a backup

set -e

echo "========================================"
echo "  Synthos-OS Restore"
echo "========================================"
echo ""

# Configuration
BACKUP_DIR="/var/backups/synthos-os"
DATA_DIR="/var/lib/synthos-os"
INSTALL_DIR="/opt/synthos-os"

# List available backups
echo "Available backups:"
ls -lt $BACKUP_DIR/manifest_*.txt 2>/dev/null | head -10 || echo "No backups found"
echo ""

# Get backup timestamp
read -p "Enter backup timestamp (e.g., 20240115_120000): " TIMESTAMP
if [ -z "$TIMESTAMP" ]; then
    echo "Timestamp is required"
    exit 1
fi

# Check if backup exists
if [ ! -f "$BACKUP_DIR/manifest_$TIMESTAMP.txt" ]; then
    echo "Backup not found: $BACKUP_DIR/manifest_$TIMESTAMP.txt"
    exit 1
fi

# Display backup manifest
echo ""
echo "Backup Manifest:"
cat $BACKUP_DIR/manifest_$TIMESTAMP.txt
echo ""

# Confirm restore
read -p "Restore from this backup? This will overwrite current data! (y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Restore cancelled."
    exit 0
fi

echo ""
echo "========================================"
echo "  Step 1: Stop Services"
echo "========================================"
echo "Stopping Synthos-OS services..."
sudo systemctl stop synthos-os
echo "Services stopped"
echo ""

echo "========================================"
echo "  Step 2: Restore PostgreSQL Database"
echo "========================================"
echo "Restoring PostgreSQL database..."
if [ -f "$BACKUP_DIR/postgres_$TIMESTAMP.sql.gz" ]; then
    gunzip -c $BACKUP_DIR/postgres_$TIMESTAMP.sql.gz | docker exec -i synthos-postgres psql -U synthos synthos_os
    echo "PostgreSQL restored"
else
    echo "PostgreSQL backup not found, skipping"
fi
echo ""

echo "========================================"
echo "  Step 3: Restore Redis Data"
echo "========================================"
echo "Restoring Redis data..."
if [ -f "$BACKUP_DIR/redis_$TIMESTAMP.rdb.gz" ]; then
    gunzip -c $BACKUP_DIR/redis_$TIMESTAMP.rdb.gz > $DATA_DIR/redis/dump.rdb
    chown -R synthos:synthos $DATA_DIR/redis
    echo "Redis restored"
else
    echo "Redis backup not found, skipping"
fi
echo ""

echo "========================================"
echo "  Step 4: Restore Ollama Models"
echo "========================================"
echo "Restoring Ollama models..."
if [ -f "$BACKUP_DIR/ollama_models_$TIMESTAMP.tar.gz" ]; then
    rm -rf $DATA_DIR/ollama/*
    tar -xzf $BACKUP_DIR/ollama_models_$TIMESTAMP.tar.gz -C $DATA_DIR/ollama
    chown -R synthos:synthos $DATA_DIR/ollama
    echo "Ollama models restored"
else
    echo "Ollama backup not found, skipping"
fi
echo ""

echo "========================================"
echo "  Step 5: Restore Configuration"
echo "========================================"
echo "Restoring configuration..."
if [ -f "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" ]; then
    tar -xzf $BACKUP_DIR/config_$TIMESTAMP.tar.gz -C $INSTALL_DIR
    echo "Configuration restored"
else
    echo "Configuration backup not found, skipping"
fi
echo ""

echo "========================================"
echo "  Step 6: Start Services"
echo "========================================"
echo "Starting Synthos-OS services..."
sudo systemctl start synthos-os
echo "Services started"
echo ""

echo "========================================"
echo "  Step 7: Wait for Services"
echo "========================================"
echo "Waiting for services to start..."
sleep 30
echo "Services should be ready"
echo ""

echo "========================================"
echo "  Step 8: Health Check"
echo "========================================"
echo "Performing health check..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✓ API Gateway: Healthy"
else
    echo "✗ API Gateway: Unhealthy"
fi

if curl -s http://localhost:8002/health > /dev/null; then
    echo "✓ Model Gateway: Healthy"
else
    echo "✗ Model Gateway: Unhealthy"
fi

if curl -s http://localhost:8003/health > /dev/null; then
    echo "✓ Memory Engine: Healthy"
else
    echo "✗ Memory Engine: Unhealthy"
fi

echo ""

echo "========================================"
echo "  Restore Complete!"
echo "========================================"
echo ""
echo "Summary:"
echo "- Restored from backup: $TIMESTAMP"
echo "- Services started"
echo "- Health check performed"
echo ""
echo "Check logs if services are unhealthy:"
echo "docker-compose logs -f"
echo ""