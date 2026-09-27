#!/bin/bash
# Synthos-OS SSL/HTTPS Setup Script
# This script configures SSL certificates using Let's Encrypt

set -e

echo "========================================"
echo "  Synthos-OS SSL/HTTPS Setup"
echo "========================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Get domain
read -p "Enter your domain (e.g., synthos.example.com): " DOMAIN
if [ -z "$DOMAIN" ]; then
    echo "Domain is required"
    exit 1
fi

# Get email for SSL
read -p "Enter your email for SSL notifications: " EMAIL
if [ -z "$EMAIL" ]; then
    echo "Email is required"
    exit 1
fi

echo ""
echo "Configuration:"
echo "Domain: $DOMAIN"
echo "Email: $EMAIL"
echo ""

# Confirm
read -p "Proceed with SSL setup? (y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "SSL setup cancelled."
    exit 0
fi

echo ""
echo "========================================"
echo "  Step 1: Check Certbot Installation"
echo "========================================"
if ! command -v certbot &> /dev/null; then
    echo "Certbot not found. Installing..."
    apt-get update
    apt-get install -y certbot python3-certbot-nginx
else
    echo "Certbot is installed: $(certbot --version)"
fi
echo ""

echo "========================================"
echo "  Step 2: Update Nginx Configuration"
echo "========================================"
echo "Updating Nginx for domain $DOMAIN..."
tee /etc/nginx/sites-available/synthos-os > /dev/null <<EOF
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

nginx -t
systemctl reload nginx
echo "Nginx updated"
echo ""

echo "========================================"
echo "  Step 3: Obtain SSL Certificate"
echo "========================================"
echo "Obtaining SSL certificate for $DOMAIN..."
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email $EMAIL

if [ $? -eq 0 ]; then
    echo "SSL certificate obtained successfully"
else
    echo "Failed to obtain SSL certificate"
    echo "Make sure:"
    echo "- Domain $DOMAIN points to this server"
    echo "- Port 80 is accessible from internet"
    echo "- DNS has propagated"
    exit 1
fi
echo ""

echo "========================================"
echo "  Step 4: Setup Auto-Renewal"
echo "========================================"
echo "Setting up SSL auto-renewal..."
systemctl enable certbot.timer
systemctl start certbot.timer
echo "Auto-renewal configured"
echo ""

echo "========================================"
echo "  Step 5: Update Firewall"
echo "========================================"
echo "Updating firewall for HTTPS..."
ufw allow 443/tcp comment 'HTTPS'
echo "Firewall updated"
echo ""

echo "========================================"
echo "  Step 6: Test SSL Configuration"
echo "========================================"
echo "Testing SSL configuration..."
nginx -t
systemctl reload nginx
echo "SSL configuration tested"
echo ""

echo "========================================"
echo "  SSL Setup Complete!"
echo "========================================"
echo ""
echo "Summary:"
echo "- Domain: $DOMAIN"
echo "- SSL Certificate: Obtained"
echo "- Auto-renewal: Enabled"
echo "- Firewall: Updated for HTTPS"
echo ""
echo "Your Synthos-OS is now accessible via HTTPS:"
echo "https://$DOMAIN"
echo ""
echo "Certificate details:"
certbot certificates
echo ""
echo "Test auto-renewal:"
echo "sudo certbot renew --dry-run"
echo ""
echo "View certificate:"
echo "sudo certbot certificates"
echo ""
echo "Renew certificate manually:"
echo "sudo certbot renew"
echo ""