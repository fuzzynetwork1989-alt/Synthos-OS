#!/bin/bash

# Synthos-OS Deployment Script
# This script handles the complete deployment of Synthos-OS

set -e

echo "=========================================="
echo "  Synthos-OS Deployment Script"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Parse command line arguments
COMMAND=${1:-"dev"}
ENVIRONMENT=${2:-"development"}

case $COMMAND in
    dev)
        echo "Starting development environment..."
        docker-compose up -d
        echo "Development environment started successfully!"
        echo ""
        echo "Services:"
        echo "  - API Gateway: http://localhost:8000"
        echo "  - Model Gateway: http://localhost:8002"
        echo "  - Memory Engine: http://localhost:8003"
        echo "  - RSI Engine: http://localhost:8004"
        echo "  - Ollama: http://localhost:11434"
        echo "  - PostgreSQL: localhost:5432"
        echo "  - Redis: localhost:6379"
        ;;
    
    prod)
        echo "Starting production environment..."
        docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
        echo "Production environment started successfully!"
        ;;
    
    stop)
        echo "Stopping all services..."
        docker-compose down
        echo "All services stopped successfully!"
        ;;
    
    restart)
        echo "Restarting all services..."
        docker-compose restart
        echo "All services restarted successfully!"
        ;;
    
    logs)
        SERVICE=${2:-""}
        if [ -z "$SERVICE" ]; then
            docker-compose logs -f
        else
            docker-compose logs -f "$SERVICE"
        fi
        ;;
    
    status)
        echo "Checking service status..."
        docker-compose ps
        ;;
    
    migrate)
        echo "Running database migrations..."
        docker-compose exec postgres psql -U synthos -d synthos_os -f /docker-entrypoint-initdb.d/001_create_memory_tables.sql
        echo "Migrations completed successfully!"
        ;;
    
    clean)
        echo "Cleaning up containers and volumes..."
        docker-compose down -v
        echo "Cleanup completed successfully!"
        ;;
    
    *)
        echo "Usage: $0 {dev|prod|stop|restart|logs|status|migrate|clean} [environment]"
        echo ""
        echo "Commands:"
        echo "  dev     - Start development environment (default)"
        echo "  prod    - Start production environment"
        echo "  stop    - Stop all services"
        echo "  restart - Restart all services"
        echo "  logs    - View logs (optional: specify service name)"
        echo "  status  - Check service status"
        echo "  migrate - Run database migrations"
        echo "  clean   - Remove containers and volumes"
        exit 1
        ;;
esac