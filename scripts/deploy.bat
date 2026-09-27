@echo off
REM Synthos-OS Deployment Script for Windows
REM This script handles the complete deployment of Synthos-OS

setlocal enabledelayedexpansion

echo ==========================================
echo   Synthos-OS Deployment Script
echo ==========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

REM Parse command line arguments
set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=dev
set ENVIRONMENT=%2
if "%ENVIRONMENT%"=="" set ENVIRONMENT=development

if "%COMMAND%"=="dev" (
    echo Starting development environment...
    docker-compose up -d
    echo Development environment started successfully!
    echo.
    echo Services:
    echo   - API Gateway: http://localhost:8000
    echo   - Model Gateway: http://localhost:8002
    echo   - Memory Engine: http://localhost:8003
    echo   - RSI Engine: http://localhost:8004
    echo   - Ollama: http://localhost:11434
    echo   - PostgreSQL: localhost:5432
    echo   - Redis: localhost:6379
) else if "%COMMAND%"=="prod" (
    echo Starting production environment...
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
    echo Production environment started successfully!
) else if "%COMMAND%"=="stop" (
    echo Stopping all services...
    docker-compose down
    echo All services stopped successfully!
) else if "%COMMAND%"=="restart" (
    echo Restarting all services...
    docker-compose restart
    echo All services restarted successfully!
) else if "%COMMAND%"=="logs" (
    set SERVICE=%2
    if "%SERVICE%"=="" (
        docker-compose logs -f
    ) else (
        docker-compose logs -f %SERVICE%
    )
) else if "%COMMAND%"=="status" (
    echo Checking service status...
    docker-compose ps
) else if "%COMMAND%"=="migrate" (
    echo Running database migrations...
    docker-compose exec postgres psql -U synthos -d synthos_os -f /docker-entrypoint-initdb.d/001_create_memory_tables.sql
    echo Migrations completed successfully!
) else if "%COMMAND%"=="clean" (
    echo Cleaning up containers and volumes...
    docker-compose down -v
    echo Cleanup completed successfully!
) else (
    echo Usage: %0 {dev^|prod^|stop^|restart^|logs^|status^|migrate^|clean} [environment]
    echo.
    echo Commands:
    echo   dev     - Start development environment (default)
    echo   prod    - Start production environment
    echo   stop    - Stop all services
    echo   restart - Restart all services
    echo   logs    - View logs (optional: specify service name)
    echo   status  - Check service status
    echo   migrate - Run database migrations
    echo   clean   - Remove containers and volumes
    exit /b 1
)

endlocal