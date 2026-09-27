# Synthos-OS Deployment Guide

## Overview

This guide covers the complete deployment of Synthos-OS, including local development, production deployment, and Kubernetes cluster setup.

## Prerequisites

### Required Software
- Docker 20.10+
- Docker Compose 2.0+
- Python 3.10+ (for local development)
- kubectl (for Kubernetes deployment)
- Helm 3.x (optional, for Helm charts)

### Hardware Requirements

#### Minimum (Development)
- CPU: 4 cores
- RAM: 8GB
- Storage: 50GB

#### Recommended (Production)
- CPU: 8+ cores
- RAM: 16GB+
- Storage: 200GB+
- GPU: Optional, for model acceleration

## Quick Start

### Development Environment

1. **Clone the repository**
```bash
git clone https://github.com/fuzzynetwork1989-alt/Synthos-OS.git
cd Synthos-OS
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start all services**
```bash
# On Linux/Mac
./scripts/deploy.sh dev

# On Windows
scripts\deploy.bat dev
```

4. **Run database migrations**
```bash
# On Linux/Mac
./scripts/deploy.sh migrate

# On Windows
scripts\deploy.bat migrate
```

5. **Verify deployment**
```bash
# Check service status
./scripts/deploy.sh status

# Or check individual services
curl http://localhost:8000/health  # API Gateway
curl http://localhost:8002/health  # Model Gateway
curl http://localhost:8003/health  # Memory Engine
curl http://localhost:8004/health  # RSI Engine
```

## Service Architecture

### Core Services

| Service | Port | Description |
|---------|------|-------------|
| API Gateway | 8000 | Main API entry point and routing |
| Model Gateway | 8002 | Model provider routing and management |
| Memory Engine | 8003 | Persistent memory and knowledge storage |
| RSI Engine | 8004 | Recursive self-improvement system |
| Ollama | 11434 | Local LLM inference |
| PostgreSQL | 5432 | Primary database |
| Redis | 6379 | Cache and message broker |

### Application Interfaces

| Application | Port | Description |
|-------------|------|-------------|
| Operator Console | 3000 | Web-based management interface |
| Desktop Shell | 3001 | Desktop application |
| Mobile Client | 19000-19001 | Expo development server |
| Quest 3 App | 8081 | VR/AR application |

## Production Deployment

### Docker Compose Production

1. **Create production configuration**
```bash
cp docker-compose.yml docker-compose.prod.yml
# Edit docker-compose.prod.yml for production settings
```

2. **Configure production environment**
```bash
# Set strong passwords
export POSTGRES_PASSWORD=$(openssl rand -base64 32)
export REDIS_PASSWORD=$(openssl rand -base32 16)

# Configure domain names
export DOMAIN=your-domain.com
```

3. **Deploy production services**
```bash
./scripts/deploy.sh prod
```

### Kubernetes Deployment

1. **Create namespace**
```bash
kubectl apply -f infra/kubernetes/synthos-namespace.yaml
```

2. **Deploy Ollama cluster**
```bash
kubectl apply -f infra/ollama-cluster/kubernetes/namespace.yaml
kubectl apply -f infra/ollama-cluster/kubernetes/ollama-deployment.yaml
kubectl apply -f infra/ollama-cluster/kubernetes/ollama-hpa.yaml
```

3. **Deploy monitoring**
```bash
kubectl apply -f infra/monitoring/prometheus-config.yaml
kubectl apply -f infra/monitoring/grafana-dashboard.yaml
```

4. **Deploy Synthos services**
```bash
# Apply service deployments (create these files)
kubectl apply -f infra/kubernetes/services/
```

### Cloud Deployment

#### AWS Deployment

1. **Create EKS cluster**
```bash
eksctl create cluster --name synthos --region us-west-2
```

2. **Configure storage**
```bash
# Create EBS storage class
kubectl apply -f infra/aws/storage-class.yaml
```

3. **Deploy with Helm**
```bash
helm install synthos ./charts/synthos --namespace synthos
```

#### Railway Deployment

1. **Connect GitHub repository**
2. **Configure environment variables**
3. **Deploy services**

## Ollama Model Setup

### Initial Model Download

```bash
# Connect to Ollama container
docker exec -it synthos-ollama bash

# Download models
ollama pull llama2
ollama pull mistral
ollama pull neural-chat
ollama pull codellama
```

### Model Configuration

Edit `services/model-gateway/synthos_model_gateway/config.py`:
```python
default_model = "llama2"  # Change to preferred model
fallback_models = ["llama2", "mistral", "neural-chat"]
```

## Monitoring and Observability

### Prometheus Metrics

All services expose metrics at `/metrics` endpoint:

```bash
# Access metrics
curl http://localhost:8000/metrics
curl http://localhost:8002/metrics
curl http://localhost:8003/metrics
curl http://localhost:8004/metrics
```

### Grafana Dashboards

Access Grafana at `http://localhost:3000` (default credentials: admin/admin)

Pre-configured dashboards:
- Synthos-OS Overview
- Service Health
- RSI Performance
- Memory Usage
- Request Rates

### Log Aggregation

View logs for all services:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api-gateway
docker-compose logs -f model-gateway
```

## Scaling

### Horizontal Scaling

#### Docker Compose
```yaml
# In docker-compose.yml
services:
  api-gateway:
    deploy:
      replicas: 3
```

#### Kubernetes
```bash
# Scale deployment
kubectl scale deployment api-gateway --replicas=3 -n synthos
```

### Auto-scaling

The Ollama cluster includes Horizontal Pod Autoscaler:
- Min replicas: 2
- Max replicas: 10
- Target CPU: 70%
- Target memory: 80%

## Backup and Recovery

### Database Backup

```bash
# Backup PostgreSQL
docker exec synthos-postgres pg_dump -U synthos synthos_os > backup.sql

# Restore PostgreSQL
docker exec -i synthos-postgres psql -U synthos synthos_os < backup.sql
```

### Redis Backup

```bash
# Backup Redis
docker exec synthos-redis redis-cli BGSAVE

# Copy RDB file
docker cp synthos-redis:/data/dump.rdb ./redis-backup.rdb
```

### Ollama Model Backup

```bash
# Backup model storage
docker cp synthos-ollama:/root/.ollama ./ollama-backup
```

## Security Configuration

### SSL/TLS Setup

1. **Generate SSL certificates**
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl.key -out ssl.crt
```

2. **Configure Nginx reverse proxy**
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/ssl.crt;
    ssl_certificate_key /path/to/ssl.key;
    
    location / {
        proxy_pass http://localhost:8000;
    }
}
```

### Firewall Configuration

```bash
# Allow only necessary ports
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

## Troubleshooting

### Service Not Starting

```bash
# Check logs
docker-compose logs [service-name]

# Check resource usage
docker stats

# Restart specific service
docker-compose restart [service-name]
```

### Database Connection Issues

```bash
# Check PostgreSQL status
docker-compose exec postgres pg_isready -U synthos

# Check Redis status
docker-compose exec redis redis-cli ping
```

### Ollama Model Issues

```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Re-download models
docker exec -it synthos-ollama ollama pull llama2
```

### Performance Issues

```bash
# Check resource usage
docker stats

# Enable detailed logging
export DEBUG=true
docker-compose restart
```

## Maintenance

### Regular Tasks

1. **Daily**
   - Check service health
   - Review error logs
   - Monitor resource usage

2. **Weekly**
   - Database backups
   - Security updates
   - Performance review

3. **Monthly**
   - Model updates
   - Storage cleanup
   - Security audit

### Updates and Upgrades

```bash
# Pull latest images
docker-compose pull

# Restart services
docker-compose up -d

# Run migrations
./scripts/deploy.sh migrate
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/fuzzynetwork1989-alt/Synthos-OS/issues
- Documentation: https://github.com/fuzzynetwork1989-alt/Synthos-OS/tree/main/docs
- Architecture Guide: See `docs/architecture/`