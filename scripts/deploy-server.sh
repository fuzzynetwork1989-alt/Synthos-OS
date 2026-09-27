#!/bin/bash
# Synthos-OS Production Deployment Script
# This script deploys Synthos-OS to production server

set -e

echo "========================================"
echo "  Synthos-OS Production Deployment"
echo "========================================"
echo ""

# Check if running as synthos user or with sudo
if [ "$EUID" -eq 0 ]; then
    echo "Running as root. Switching to synthos user..."
    sudo -u synthos $0 "$@"
    exit $?
fi

# Configuration
INSTALL_DIR="/opt/synthos-os"
DATA_DIR="/var/lib/synthos-os"
LOG_DIR="/var/log/synthos-os"
DOMAIN=${DOMAIN:-"localhost"}
ENVIRONMENT=${ENVIRONMENT:-"production"}

echo "Configuration:"
echo "Install Directory: $INSTALL_DIR"
echo "Data Directory: $DATA_DIR"
echo "Log Directory: $LOG_DIR"
echo "Domain: $DOMAIN"
echo "Environment: $ENVIRONMENT"
echo ""

# Confirm deployment
read -p "Proceed with deployment? (y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Deployment cancelled."
    exit 0
fi

echo ""
echo "========================================"
echo "  Step 1: Clone/Update Repository"
echo "========================================"
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "Updating existing repository..."
    cd $INSTALL_DIR
    git fetch origin
    git pull origin main
else
    echo "Cloning repository..."
    sudo rm -rf $INSTALL_DIR
    git clone https://github.com/fuzzynetwork1989-alt/Synthos-OS.git $INSTALL_DIR
    cd $INSTALL_DIR
fi
echo "Repository ready"
echo ""

echo "========================================"
echo "  Step 2: Install Python Dependencies"
echo "========================================"
echo "Installing Python dependencies..."
cd $INSTALL_DIR
python3 -m pip install --upgrade pip
pip3 install -e .
echo "Python dependencies installed"
echo ""

echo "========================================"
echo "  Step 3: Configure Environment"
echo "========================================"
echo "Configuring environment..."
if [ ! -f "$INSTALL_DIR/.env" ]; then
    cp $INSTALL_DIR/.env.example $INSTALL_DIR/.env
fi

# Update production environment variables
sed -i "s/ENVIRONMENT=development/ENVIRONMENT=$ENVIRONMENT/g" $INSTALL_DIR/.env
sed -i "s/DEBUG=true/DEBUG=false/g" $INSTALL_DIR/.env
sed -i "s/POSTGRES_PASSWORD=synthos_dev_password/POSTGRES_PASSWORD=$(openssl rand -base64 32)/g" $INSTALL_DIR/.env

echo "Environment configured"
echo ""

echo "========================================"
echo "  Step 4: Setup Data Directories"
echo "========================================"
echo "Setting up data directories..."
mkdir -p $DATA_DIR/postgres
mkdir -p $DATA_DIR/redis
mkdir -p $DATA_DIR/ollama
mkdir -p $LOG_DIR
chown -R synthos:synthos $DATA_DIR
chown -R synthos:synthos $LOG_DIR
echo "Data directories ready"
echo ""

echo "========================================"
echo "  Step 5: Build Docker Images"
echo "========================================"
echo "Building Docker images..."
cd $INSTALL_DIR
docker-compose build
echo "Docker images built"
echo ""

echo "========================================"
echo "  Step 6: Stop Existing Services"
echo "========================================"
echo "Stopping existing services..."
cd $INSTALL_DIR
docker-compose down 2>/dev/null || true
echo "Services stopped"
echo ""

echo "========================================"
echo "  Step 7: Start Services"
echo "========================================"
echo "Starting production services..."
cd $INSTALL_DIR
docker-compose -f docker-compose.yml up -d
echo "Services started"
echo ""

echo "========================================"
echo "  Step 8: Wait for Services to Start"
echo "========================================"
echo "Waiting for services to be healthy..."
sleep 30
echo "Services should be ready"
echo ""

echo "========================================"
echo "  Step 9: Run Database Migrations"
echo "========================================"
echo "Running database migrations..."
cd $INSTALL_DIR
docker-compose exec -T postgres psql -U synthos -d synthos_os -f /docker-entrypoint-initdb.d/001_create_memory_tables.sql
echo "Migrations applied"
echo ""

echo "========================================"
echo "  Step 10: Pull Ollama Models"
echo "========================================"
echo "Pulling Ollama models..."
cd $INSTALL_DIR
docker exec synthos-ollama ollama pull llama2
docker exec synthos-ollama ollama pull mistral
docker exec synthos-ollama ollama pull neural-chat
echo "Models pulled"
echo ""

echo "========================================"
echo "  Step 11: Configure Nginx"
echo "========================================"
echo "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/synthos-os > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN;

    # API Gateway
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Model Gateway
    location /models/ {
        proxy_pass http://localhost:8002/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Memory Engine
    location /memory/ {
        proxy_pass http://localhost:8003/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # RSI Engine
    location /rsi/ {
        proxy_pass http://localhost:8004/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Cognitive Engine
    location /cognitive/ {
        proxy_pass http://localhost:8005/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Tool Execution Engine
    location /tools/ {
        proxy_pass http://localhost:8006/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Web UI
    location / {
        proxy_pass http://localhost:3000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/synthos-os /etc/nginx/sites-enabled/synthos-os
sudo nginx -t
sudo systemctl reload nginx
echo "Nginx configured"
echo ""

echo "========================================"
echo "  Step 12: Setup Systemd Services"
echo "========================================"
echo "Setting up systemd services..."
sudo tee /etc/systemd/system/synthos-os.service > /dev/null <<EOF
[Unit]
Description=Synthos-OS Services
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
ExecReload=/usr/bin/docker-compose restart
User=synthos
Group=synthos

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable synthos-os
echo "Systemd services configured"
echo ""

echo "========================================"
echo "  Step 13: Setup Log Rotation"
echo "========================================"
echo "Configuring log rotation..."
sudo tee /etc/logrotate.d/synthos-os > /dev/null <<EOF
$LOG_DIR/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 synthos synthos
    sharedscripts
    postrotate
        docker-compose logs -t --tail="0" > /dev/null 2>&1 || true
    endscript
}
EOF
echo "Log rotation configured"
echo ""

echo "========================================"
echo "  Step 14: Health Check"
echo "========================================"
echo "Performing health check..."
sleep 10

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

if curl -s http://localhost:8004/health > /dev/null; then
    echo "✓ RSI Engine: Healthy"
else
    echo "✗ RSI Engine: Unhealthy"
fi

echo ""

echo "========================================"
echo "  Deployment Complete!"
echo "========================================"
echo ""
echo "Summary:"
echo "- Synthos-OS deployed to: $INSTALL_DIR"
echo "- Data directory: $DATA_DIR"
echo "- Log directory: $LOG_DIR"
echo "- Domain: $DOMAIN"
echo "- Environment: $ENVIRONMENT"
echo ""
echo "Services running:"
echo "- API Gateway: http://localhost:8000"
echo "- Model Gateway: http://localhost:8002"
echo "- Memory Engine: http://localhost:8003"
echo "- RSI Engine: http://localhost:8004"
echo "- Cognitive Engine: http://localhost:8005"
echo "- Tool Execution Engine: http://localhost:8006"
echo "- Web UI: http://localhost:3000"
echo "- Nginx: http://$DOMAIN"
echo ""
echo "Next steps:"
echo "1. Configure SSL: sudo certbot --nginx -d $DOMAIN"
echo "2. Check status: sudo systemctl status synthos-os"
echo "3. View logs: docker-compose logs -f"
echo "4. Monitor: cd $INSTALL_DIR && ./scripts/monitor.sh"
echo ""
echo "Useful commands:"
echo "- Restart services: sudo systemctl restart synthos-os"
echo "- Stop services: sudo systemctl stop synthos-os"
echo "- Start services: sudo systemctl start synthos-os"
echo "- View logs: docker-compose logs -f"
echo "- Update: cd $INSTALL_DIR && git pull && sudo systemctl restart synthos-os"
echo ""