#!/bin/bash
# Synthos-OS Backup Script
# This script creates backups of database, configuration, and data

set -e

echo "========================================"
echo "  Synthos-OS Backup"
echo "========================================"
echo ""

# Configuration
BACKUP_DIR="/var/backups/synthos-os"
DATA_DIR="/var/lib/synthos-os"
INSTALL_DIR="/opt/synthos-os"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p $BACKUP_DIR

echo "Backup Configuration:"
echo "Backup Directory: $BACKUP_DIR"
echo "Data Directory: $DATA_DIR"
echo "Install Directory: $INSTALL_DIR"
echo "Timestamp: $TIMESTAMP"
echo "Retention: $RETENTION_DAYS days"
echo ""

# Confirm backup
read -p "Proceed with backup? (y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Backup cancelled."
    exit 0
fi

echo ""
echo "========================================"
echo "  Step 1: Backup PostgreSQL Database"
echo "========================================"
echo "Backing up PostgreSQL database..."
docker exec synthos-postgres pg_dump -U synthos synthos_os | gzip > $BACKUP_DIR/postgres_$TIMESTAMP.sql.gz
echo "PostgreSQL backup complete: postgres_$TIMESTAMP.sql.gz"
echo ""

echo "========================================"
echo "  Step 2: Backup Redis Data"
echo "========================================"
echo "Backing up Redis data..."
docker exec synthos-redis redis-cli BGSAVE
sleep 5
docker cp synthos-redis:/data/dump.rdb $BACKUP_DIR/redis_$TIMESTAMP.rdb
gzip $BACKUP_DIR/redis_$TIMESTAMP.rdb
echo "Redis backup complete: redis_$TIMESTAMP.rdb.gz"
echo ""

echo "========================================"
echo "  Step 3: Backup Ollama Models"
echo "========================================"
echo "Backing up Ollama models..."
docker exec synthos-ollama ollama list > $BACKUP_DIR/ollama_models_$TIMESTAMP.txt
tar -czf $BACKUP_DIR/ollama_models_$TIMESTAMP.tar.gz -C $DATA_DIR/ollama .
echo "Ollama backup complete: ollama_models_$TIMESTAMP.tar.gz"
echo ""

echo "========================================"
echo "  Step 4: Backup Configuration"
echo "========================================"
echo "Backing up configuration..."
tar -czf $BACKUP_DIR/config_$TIMESTAMP.tar.gz -C $INSTALL_DIR .env docker-compose.yml
echo "Configuration backup complete: config_$TIMESTAMP.tar.gz"
echo ""

echo "========================================"
echo "  Step 5: Backup Logs"
echo "========================================"
echo "Backing up recent logs..."
mkdir -p $BACKUP_DIR/logs_$TIMESTAMP
cp /var/log/synthos-os/*.log $BACKUP_DIR/logs_$TIMESTAMP/ 2>/dev/null || true
tar -czf $BACKUP_DIR/logs_$TIMESTAMP.tar.gz -C $BACKUP_DIR logs_$TIMESTAMP
rm -rf $BACKUP_DIR/logs_$TIMESTAMP
echo "Logs backup complete: logs_$TIMESTAMP.tar.gz"
echo ""

echo "========================================"
echo "  Step 6: Create Backup Manifest"
echo "========================================"
echo "Creating backup manifest..."
cat > $BACKUP_DIR/manifest_$TIMESTAMP.txt <<EOF
Synthos-OS Backup Manifest
Generated: $(date)
Timestamp: $TIMESTAMP

Files:
- postgres_$TIMESTAMP.sql.gz (PostgreSQL database)
- redis_$TIMESTAMP.rdb.gz (Redis data)
- ollama_models_$TIMESTAMP.tar.gz (Ollama models)
- config_$TIMESTAMP.tar.gz (Configuration files)
- logs_$TIMESTAMP.tar.gz (Log files)

System Information:
OS: $(lsb_release -d | cut -f2)
Kernel: $(uname -r)
Docker: $(docker --version)
Docker Compose: $(docker-compose --version)

Synthos-OS Version:
$(cd $INSTALL_DIR && git log -1 --oneline 2>/dev/null || echo "Not a git repository")
EOF
echo "Manifest created: manifest_$TIMESTAMP.txt"
echo ""

echo "========================================"
echo "  Step 7: Clean Old Backups"
echo "========================================"
echo "Cleaning backups older than $RETENTION_DAYS days..."
find $BACKUP_DIR -name "*.gz" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "*.txt" -mtime +$RETENTION_DAYS -delete
echo "Old backups cleaned"
echo ""

echo "========================================"
echo "  Step 8: Calculate Backup Size"
echo "========================================"
BACKUP_SIZE=$(du -sh $BACKUP_DIR | cut -f1)
echo "Total backup size: $BACKUP_SIZE"
echo ""

echo "========================================"
echo "  Backup Complete!"
echo "========================================"
echo ""
echo "Summary:"
echo "- Backup location: $BACKUP_DIR"
echo "- Backup timestamp: $TIMESTAMP"
echo "- Total size: $BACKUP_SIZE"
echo "- Retention: $RETENTION_DAYS days"
echo ""
echo "Backup files:"
ls -lh $BACKUP_DIR/*_$TIMESTAMP.*
echo ""
echo "To restore from backup:"
echo "1. Stop services: sudo systemctl stop synthos-os"
echo "2. Restore database: gunzip -c $BACKUP_DIR/postgres_$TIMESTAMP.sql.gz | docker exec -i synthos-postgres psql -U synthos synthos_os"
echo "3. Restore Redis: gunzip -c $BACKUP_DIR/redis_$TIMESTAMP.rdb.gz > $DATA_DIR/redis/dump.rdb"
echo "4. Restore Ollama: tar -xzf $BACKUP_DIR/ollama_models_$TIMESTAMP.tar.gz -C $DATA_DIR/ollama"
echo "5. Restore config: tar -xzf $BACKUP_DIR/config_$TIMESTAMP.tar.gz -C $INSTALL_DIR"
echo "6. Start services: sudo systemctl start synthos-os"
echo ""