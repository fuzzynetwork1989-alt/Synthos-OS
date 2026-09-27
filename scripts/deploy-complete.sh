#!/bin/bash

# Synthos-OS Complete Deployment Script
# This script handles the complete deployment of all Synthos-OS services

set -e

echo "=========================================="
echo "  Synthos-OS Complete Deployment"
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

case $COMMAND in
    dev)
        echo "Starting complete development environment..."
        echo "This will start all 11 microservices plus infrastructure"
        echo ""
        
        # Create necessary directories
        mkdir -p logs data
        
        # Start infrastructure first
        echo "Starting infrastructure services (PostgreSQL, Redis, Ollama)..."
        docker-compose up -d postgres redis ollama
        
        # Wait for infrastructure to be ready
        echo "Waiting for infrastructure to be ready..."
        sleep 10
        
        # Start core services
        echo "Starting core services..."
        docker-compose up -d model-gateway memory-engine rsi-engine
        
        # Wait for core services
        echo "Waiting for core services to be ready..."
        sleep 5
        
        # Start application services
        echo "Starting application services..."
        docker-compose up -d cognitive-engine tool-execution-engine workflow-engine policy-engine evaluation-engine device-gateway
        
        # Start API gateway last
        echo "Starting API Gateway..."
        docker-compose up -d api-gateway
        
        echo ""
        echo "✅ Complete development environment started successfully!"
        echo ""
        echo "🚀 All Services:"
        echo "  Infrastructure:"
        echo "    - PostgreSQL: localhost:5432"
        echo "    - Redis: localhost:6379"
        echo "    - Ollama: http://localhost:11434"
        echo ""
        echo "  Core Services:"
        echo "    - Model Gateway: http://localhost:8002"
        echo "    - Memory Engine: http://localhost:8003"
        echo "    - RSI Engine: http://localhost:8004"
        echo ""
        echo "  Application Services:"
        echo "    - Cognitive Engine: http://localhost:8005"
        echo "    - Tool Execution Engine: http://localhost:8006"
        echo "    - Workflow Engine: http://localhost:8007"
        echo "    - Policy Engine: http://localhost:8008"
        echo "    - Evaluation Engine: http://localhost:8009"
        echo "    - Device Gateway: http://localhost:8010"
        echo ""
        echo "  API Gateway:"
        echo "    - API Gateway: http://localhost:8000"
        echo ""
        echo "📊 Check service status: docker-compose ps"
        echo "📋 View logs: ./scripts/deploy-complete.sh logs"
        echo "🛑 Stop services: ./scripts/deploy-complete.sh stop"
        ;;
    
    prod)
        echo "Starting production environment..."
        docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
        echo "✅ Production environment started successfully!"
        ;;
    
    stop)
        echo "Stopping all services..."
        docker-compose down
        echo "✅ All services stopped successfully!"
        ;;
    
    restart)
        echo "Restarting all services..."
        docker-compose restart
        echo "✅ All services restarted successfully!"
        ;;
    
    logs)
        SERVICE=${2:-""}
        if [ -z "$SERVICE" ]; then
            echo "Showing logs for all services..."
            docker-compose logs -f
        else
            echo "Showing logs for $SERVICE..."
            docker-compose logs -f "$SERVICE"
        fi
        ;;
    
    status)
        echo "Checking service status..."
        docker-compose ps
        echo ""
        echo "Health Checks:"
        echo "  API Gateway: curl http://localhost:8000/health"
        echo "  Model Gateway: curl http://localhost:8002/health"
        echo "  Memory Engine: curl http://localhost:8003/health"
        echo "  RSI Engine: curl http://localhost:8004/health"
        echo "  Cognitive Engine: curl http://localhost:8005/health"
        echo "  Tool Execution: curl http://localhost:8006/health"
        echo "  Workflow Engine: curl http://localhost:8007/health"
        echo "  Policy Engine: curl http://localhost:8008/health"
        echo "  Evaluation Engine: curl http://localhost:8009/health"
        echo "  Device Gateway: curl http://localhost:8010/health"
        ;;
    
    health)
        echo "Running health checks on all services..."
        echo ""
        
        services=(
            "API Gateway:8000"
            "Model Gateway:8002"
            "Memory Engine:8003"
            "RSI Engine:8004"
            "Cognitive Engine:8005"
            "Tool Execution:8006"
            "Workflow Engine:8007"
            "Policy Engine:8008"
            "Evaluation Engine:8009"
            "Device Gateway:8010"
        )
        
        for service in "${services[@]}"; do
            name="${service%%:*}"
            port="${service##*:}"
            
            if curl -s "http://localhost:$port/health" > /dev/null; then
                echo "✅ $name (port $port): Healthy"
            else
                echo "❌ $name (port $port): Unhealthy or not responding"
            fi
        done
        ;;
    
    migrate)
        echo "Running database migrations..."
        docker-compose exec postgres psql -U synthos -d synthos_os -f /docker-entrypoint-initdb.d/001_create_memory_tables.sql
        echo "✅ Migrations completed successfully!"
        ;;
    
    clean)
        echo "Cleaning up containers and volumes..."
        docker-compose down -v
        echo "✅ Cleanup completed successfully!"
        ;;
    
    *)
        echo "Usage: $0 {dev|prod|stop|restart|logs|status|health|migrate|clean}"
        echo ""
        echo "Commands:"
        echo "  dev     - Start complete development environment (default)"
        echo "  prod    - Start production environment"
        echo "  stop    - Stop all services"
        echo "  restart - Restart all services"
        echo "  logs    - View logs (optional: specify service name)"
        echo "  status  - Check service status"
        echo "  health  - Run health checks on all services"
        echo "  migrate - Run database migrations"
        echo "  clean   - Remove containers and volumes"
        exit 1
        ;;
esac