#!/bin/bash
# Synthos-OS Verification Script for Linux/Mac
# This script verifies all services are running correctly

set -e

echo "========================================"
echo "  Synthos-OS Verification Script"
echo "========================================"
echo ""

all_passed=true

# Check Docker
echo "Checking Docker..."
if command -v docker &> /dev/null; then
    echo "✓ Docker: $(docker --version)"
else
    echo "✗ Docker: Not installed or not running"
    all_passed=false
fi

# Check Docker Compose
echo "Checking Docker Compose..."
if command -v docker-compose &> /dev/null; then
    echo "✓ Docker Compose: $(docker-compose --version)"
else
    echo "✗ Docker Compose: Not installed"
    all_passed=false
fi

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    echo "✓ Python: $(python3 --version)"
else
    echo "✗ Python: Not installed"
    all_passed=false
fi

# Check Git
echo "Checking Git..."
if command -v git &> /dev/null; then
    echo "✓ Git: $(git --version)"
else
    echo "✗ Git: Not installed"
    all_passed=false
fi

# Check Node.js (optional)
echo "Checking Node.js (optional)..."
if command -v node &> /dev/null; then
    echo "✓ Node.js: $(node --version)"
else
    echo "○ Node.js: Not installed (optional)"
fi

echo ""
echo "Checking Docker Services..."

# Check services
services=(
    "synthos-postgres"
    "synthos-redis"
    "synthos-ollama"
    "synthos-api-gateway"
    "synthos-model-gateway"
    "synthos-memory-engine"
    "synthos-rsi-engine"
    "synthos-cognitive-engine"
    "synthos-tool-execution-engine"
)

for service in "${services[@]}"; do
    status=$(docker ps --filter "name=$service" --format "{{.Status}}" 2>/dev/null)
    if [ -n "$status" ]; then
        echo "✓ $service: $status"
    else
        echo "✗ $service: Not running"
        all_passed=false
    fi
done

echo ""
echo "Checking Service Health..."

# Check API Gateway
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✓ API Gateway: Healthy"
else
    echo "✗ API Gateway: Not responding"
    all_passed=false
fi

# Check Model Gateway
if curl -s http://localhost:8002/health > /dev/null 2>&1; then
    echo "✓ Model Gateway: Healthy"
else
    echo "✗ Model Gateway: Not responding"
    all_passed=false
fi

# Check Memory Engine
if curl -s http://localhost:8003/health > /dev/null 2>&1; then
    echo "✓ Memory Engine: Healthy"
else
    echo "✗ Memory Engine: Not responding"
    all_passed=false
fi

# Check RSI Engine
if curl -s http://localhost:8004/health > /dev/null 2>&1; then
    echo "✓ RSI Engine: Healthy"
else
    echo "✗ RSI Engine: Not responding"
    all_passed=false
fi

echo ""
echo "Checking Ollama Models..."

if docker exec synthos-ollama ollama list > /dev/null 2>&1; then
    echo "✓ Ollama models available:"
    docker exec synthos-ollama ollama list
else
    echo "✗ No Ollama models found"
    echo "Run: docker exec -it synthos-ollama bash"
    echo "     ollama pull llama2 mistral neural-chat"
    echo "     exit"
    all_passed=false
fi

echo ""
echo "========================================"
if [ "$all_passed" = true ]; then
    echo "  All Checks Passed!"
else
    echo "  Some Checks Failed!"
fi
echo "========================================"
echo ""

if [ "$all_passed" = false ]; then
    echo "Troubleshooting tips:"
    echo "- Ensure Docker is running"
    echo "- Run: ./scripts/deploy.sh dev"
    echo "- Run: ./scripts/deploy.sh migrate"
    echo "- Run: docker exec -it synthos-ollama bash && ollama pull llama2 mistral neural-chat"
    echo ""
fi

if [ "$all_passed" = true ]; then
    exit 0
else
    exit 1
fi