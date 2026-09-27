# Synthos-OS Cleanup Script for Windows
# This script cleans up Docker resources and temporary files

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Synthos-OS Cleanup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "WARNING: This will stop all Synthos-OS services and clean up Docker resources." -ForegroundColor Yellow
Write-Host "This will NOT delete your data volumes unless you choose to." -ForegroundColor Yellow
Write-Host ""

$confirm = Read-Host "Do you want to continue? (y/N)"

if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Cleanup cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Stopping Synthos-OS services..." -ForegroundColor Yellow
docker-compose down

Write-Host ""
Write-Host "Cleaning up Docker resources..." -ForegroundColor Yellow

# Clean up dangling images
Write-Host "Removing dangling Docker images..." -ForegroundColor Gray
docker image prune -f

# Clean up unused containers
Write-Host "Removing unused containers..." -ForegroundColor Gray
docker container prune -f

# Clean up unused networks
Write-Host "Removing unused networks..." -ForegroundColor Gray
docker network prune -f

# Clean up build cache
Write-Host "Cleaning build cache..." -ForegroundColor Gray
docker builder prune -f

Write-Host ""
Write-Host "Cleaning up temporary files..." -ForegroundColor Yellow

# Clean up logs
if (Test-Path "logs") {
    Write-Host "Cleaning log files..." -ForegroundColor Gray
    Remove-Item "logs\*.log" -Force -ErrorAction SilentlyContinue
}

# Clean up cache
if (Test-Path "data\cache") {
    Write-Host "Cleaning cache files..." -ForegroundColor Gray
    Remove-Item "data\cache\*" -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host ""
$deleteVolumes = Read-Host "Do you want to delete data volumes? (WARNING: This will delete all data) (y/N)"

if ($deleteVolumes -eq "y" -or $deleteVolumes -eq "Y") {
    Write-Host ""
    Write-Host "Deleting data volumes..." -ForegroundColor Red
    docker-compose down -v
    Write-Host "Data volumes deleted." -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Cleanup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To restart Synthos-OS:" -ForegroundColor White
Write-Host "Run: .\scripts\deploy.bat dev" -ForegroundColor Gray
Write-Host ""