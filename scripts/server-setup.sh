#!/bin/bash
# Synthos-OS Server Setup Script for Ubuntu/Debian
# This script prepares a fresh Ubuntu/Debian server for Synthos-OS production deployment

set -e

echo "========================================"
echo "  Synthos-OS Server Setup"
echo "  Ubuntu/Debian Production Server"
echo "========================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Get server information
echo "Server Information:"
echo "OS: $(lsb_release -d | cut -f2)"
echo "Kernel: $(uname -r)"
echo "Architecture: $(uname -m)"
echo "CPU Cores: $(nproc)"
echo "Memory: $(free -h | grep Mem | awk '{print $2}')"
echo "Disk: $(df -h / | tail -1 | awk '{print $2}')"
echo ""

# Confirm setup
read -p "Proceed with server setup? (y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Setup cancelled."
    exit 0
fi

echo ""
echo "========================================"
echo "  Step 1: System Update"
echo "========================================"
echo "Updating system packages..."
apt-get update
apt-get upgrade -y
echo "System updated successfully"
echo ""

echo "========================================"
echo "  Step 2: Install Essential Packages"
echo "========================================"
echo "Installing essential packages..."
apt-get install -y \
    curl \
    wget \
    git \
    unzip \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    ufw \
    fail2ban \
    htop \
    tmux \
    vim \
    net-tools \
    dnsutils
echo "Essential packages installed"
echo ""

echo "========================================"
echo "  Step 3: Install Docker"
echo "========================================"
echo "Installing Docker..."
# Remove old versions
apt-get remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true

# Add Docker's official GPG key
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd docker-buildx-plugin docker-compose-plugin

# Enable and start Docker
systemctl enable docker
systemctl start docker

# Add current user to docker group
if [ -n "$SUDO_USER" ]; then
    usermod -aG docker $SUDO_USER
    echo "Added user $SUDO_USER to docker group"
fi

echo "Docker installed: $(docker --version)"
echo ""

echo "========================================"
echo "  Step 4: Install Python 3.10"
echo "========================================"
echo "Installing Python 3.10..."
apt-get install -y python3.10 python3.10-venv python3-pip python3-dev
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
echo "Python installed: $(python3 --version)"
echo ""

echo "========================================"
echo "  Step 5: Install Node.js"
echo "========================================"
echo "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs
echo "Node.js installed: $(node --version)"
echo "Npm installed: $(npm --version)"
echo ""

echo "========================================"
echo "  Step 6: Install Nginx"
echo "========================================"
echo "Installing Nginx..."
apt-get install -y nginx
systemctl enable nginx
systemctl start nginx
echo "Nginx installed and started"
echo ""

echo "========================================"
echo "  Step 7: Configure Firewall"
echo "========================================"
echo "Configuring UFW firewall..."
# Reset UFW
ufw --force reset

# Allow SSH
ufw allow 22/tcp

# Allow HTTP
ufw allow 80/tcp

# Allow HTTPS
ufw allow 443/tcp

# Allow Docker services (adjust ports as needed)
ufw allow 8000/tcp  # API Gateway
ufw allow 8002/tcp  # Model Gateway
ufw allow 8003/tcp  # Memory Engine
ufw allow 8004/tcp  # RSI Engine
ufw allow 8005/tcp  # Cognitive Engine
ufw allow 8006/tcp  # Tool Execution Engine

# Enable firewall
ufw --force enable

echo "Firewall configured and enabled"
echo ""

echo "========================================"
echo "  Step 8: Configure Fail2Ban"
echo "========================================"
echo "Configuring Fail2Ban..."
cat > /etc/fail2ban/jail.local <<'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-noscript]
enabled = true
port = http,https
filter = nginx-noscript
logpath = /var/log/nginx/access.log
maxretry = 6
EOF

systemctl enable fail2ban
systemctl restart fail2ban
echo "Fail2Ban configured"
echo ""

echo "========================================"
echo "  Step 9: Install Certbot for SSL"
echo "========================================"
echo "Installing Certbot..."
apt-get install -y certbot python3-certbot-nginx
echo "Certbot installed"
echo ""

echo "========================================"
echo "  Step 10: Create Synthos-OS User"
echo "========================================"
echo "Creating synthos user..."
if ! id -u synthos &>/dev/null; then
    useradd -m -s /bin/bash synthos
    echo "User 'synthos' created"
else
    echo "User 'synthos' already exists"
fi

# Create directories
mkdir -p /opt/synthos-os
mkdir -p /var/log/synthos-os
mkdir -p /var/lib/synthos-os
chown -R synthos:synthos /opt/synthos-os
chown -R synthos:synthos /var/log/synthos-os
chown -R synthos:synthos /var/lib/synthos-os
echo "Directories created"
echo ""

echo "========================================"
echo "  Step 11: Configure System Limits"
echo "========================================"
echo "Configuring system limits..."
cat >> /etc/sysctl.conf <<'EOF'
# Synthos-OS System Limits
fs.file-max = 100000
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.ipv4.tcp_tw_reuse = 1
net.ipv4.ip_local_port_range = 1024 65535
EOF

sysctl -p
echo "System limits configured"
echo ""

echo "========================================"
echo "  Step 12: Configure Docker Daemon"
echo "========================================"
echo "Configuring Docker daemon..."
mkdir -p /etc/docker
cat > /etc/docker/daemon.json <<'EOF'
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "live-restore": true,
  "max-concurrent-downloads": 10,
  "max-concurrent-uploads": 5
}
EOF

systemctl restart docker
echo "Docker daemon configured"
echo ""

echo "========================================"
echo "  Step 13: Create Swap (if needed)"
echo "========================================"
SWAP_SIZE=4096
if [ $(free -m | grep Swap | awk '{print $2}') -eq 0 ]; then
    echo "Creating $SWAP_SIZE MB swap file..."
    fallocate -l ${SWAP_SIZE}M /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    echo "Swap file created"
else
    echo "Swap already exists"
fi
echo ""

echo "========================================"
echo "  Step 14: Install Monitoring Tools"
echo "========================================"
echo "Installing monitoring tools..."
apt-get install -y prometheus-node-exporter
systemctl enable prometheus-node-exporter
systemctl start prometheus-node-exporter
echo "Node Exporter installed"
echo ""

echo "========================================"
echo "  Server Setup Complete!"
echo "========================================"
echo ""
echo "Summary:"
echo "- System updated"
echo "- Docker installed: $(docker --version)"
echo "- Python installed: $(python3 --version)"
echo "- Node.js installed: $(node --version)"
echo "- Nginx installed and running"
echo "- Firewall configured (UFW)"
echo "- Fail2Ban configured"
echo "- Certbot installed for SSL"
echo "- User 'synthos' created"
echo "- System limits configured"
echo "- Docker daemon optimized"
echo "- Swap configured"
echo "- Node Exporter installed"
echo ""
echo "Next steps:"
echo "1. Log out and log back in (for docker group)"
echo "2. Clone Synthos-OS repository: sudo -u synthos git clone https://github.com/fuzzynetwork1989-alt/Synthos-OS.git /opt/synthos-os"
echo "3. Run: sudo -u synthos ./scripts/deploy-server.sh"
echo "4. Configure SSL: sudo certbot --nginx -d your-domain.com"
echo ""
echo "Important:"
echo "- Synthos-OS installed in: /opt/synthos-os"
echo "- Logs in: /var/log/synthos-os"
echo "- Data in: /var/lib/synthos-os"
echo "- Docker group added to user: $SUDO_USER"
echo ""