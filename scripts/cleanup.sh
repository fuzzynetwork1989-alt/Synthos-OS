#!/bin/bash
# Synthos-OS Cleanup Script for Linux/Mac
# This script cleans up Docker resources and temporary files

set -e

echo "========================================"
echo "  Synthos-OS Cleanup Script"
echo "========================================"
echo ""
echo "WARNING: This will stop all Synthos-OS services and clean up Docker resources."
echo "This will NOT delete your data volumes unless you choose to."
echo ""

read -p "Do you want to continue? (y/N): " confirm

if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "Stopping Synthos-OS services..."
docker-compose down

echo ""
echo "Cleaning up Docker resources..."

# Clean up dangling images
echo "Removing dangling Docker images..."
docker image prune -f

# Clean up unused containers
echo "Removing unused containers..."
docker container prune -f

# Clean up unused networks
echo "Removing unused networks..."
docker network prune -f

# Clean up build cache
echo "Cleaning build cache..."
docker builder prune -f

echo ""
echo "Cleaning up temporary files..."

# Clean up logs
if [ -d "logs" ]; then
    echo "Cleaning log files..."
    rm -f logs/*.log
fi

# Clean up cache
if [ -d "data/cache" ]; then
    echo "Cleaning cache files..."
    rm -rf data/cache/*
fi

echo ""
read -p "Do you want to delete data volumes? (WARNING: This will delete all data) (y/N): " delete_volumes

if [[ "$delete_volumes" == "y" || "$delete_volumes" == "Y" ]]; then
    echo ""
    echo "Deleting data volumes..."
    docker-compose down -v
    echo "Data volumes deleted."
fi

echo ""
echo "========================================"
echo "  Cleanup Complete!"
echo "========================================"
echo ""
echo "To restart Synthos-OS:"
echo "Run: ./scripts/deploy.sh dev"
echo ""