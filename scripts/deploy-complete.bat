@echo off
REM Synthos-OS Complete Deployment Script for Windows
REM This script handles the complete deployment of all Synthos-OS services

echo ==========================================
echo   Synthos-OS Complete Deployment
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

if "%COMMAND%"=="dev" (
    echo Starting complete development environment...
    echo This will start all 11 microservices plus infrastructure
    echo.
    
    REM Create necessary directories
    if not exist logs mkdir logs
    if not exist data mkdir data
    
    REM Start infrastructure first
    echo Starting infrastructure services ^(PostgreSQL, Redis, Ollama^)...
    docker-compose up -d postgres redis ollama
    
    REM Wait for infrastructure to be ready
    echo Waiting for infrastructure to be ready...
    timeout /t 10 /nobreak >nul
    
    REM Start core services
    echo Starting core services...
    docker-compose up -d model-gateway memory-engine rsi-engine
    
    REM Wait for core services
    echo Waiting for core services to be ready...
    timeout /t 5 /nobreak >nul
    
    REM Start application services
    echo Starting application services...
    docker-compose up -d cognitive-engine tool-execution-engine workflow-engine policy-engine evaluation-engine device-gateway
    
    REM Start API gateway last
    echo Starting API Gateway...
    docker-compose up -d api-gateway
    
    echo.
    echo Complete development environment started successfully!
    echo.
    echo All Services:
    echo   Infrastructure:
    echo     - PostgreSQL: localhost:5432
    echo     - Redis: localhost:6379
    echo     - Ollama: http://localhost:11434
    echo.
    echo   Core Services:
    echo     - Model Gateway: http://localhost:8002
    echo     - Memory Engine: http://localhost:8003
    echo     - RSI Engine: http://localhost:8004
    echo.
    echo   Application Services:
    echo     - Cognitive Engine: http://localhost:8005
    echo     - Tool Execution Engine: http://localhost:8006
    echo     - Workflow Engine: http://localhost:8007
    echo     - Policy Engine: http://localhost:8008
    echo     - Evaluation Engine: http://localhost:8009
    echo     - Device Gateway: http://localhost:8010
    echo.
    echo   API Gateway:
    echo     - API Gateway: http://localhost:8000
    echo.
    echo Check service status: docker-compose ps
    echo View logs: deploy-complete.bat logs
    echo Stop services: deploy-complete.bat stop
)

if "%COMMAND%"=="stop" (
    echo Stopping all services...
    docker-compose down
    echo All services stopped successfully!
)

if "%COMMAND%"=="restart" (
    echo Restarting all services...
    docker-compose restart
    echo All services restarted successfully!
)

if "%COMMAND%"=="logs" (
    set SERVICE=%2
    if "%SERVICE%"=="" (
        echo Showing logs for all services...
        docker-compose logs -f
    ) else (
        echo Showing logs for %SERVICE%...
        docker-compose logs -f %SERVICE%
    )
)

if "%COMMAND%"=="status" (
    echo Checking service status...
    docker-compose ps
)

if "%COMMAND%"=="health" (
    echo Running health checks on all services...
    echo.
    
    curl -s http://localhost:8000/health >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] API Gateway ^(port 8000^): Healthy
    ) else (
        echo [FAIL] API Gateway ^(port 8000^): Unhealthy
    )
    
    curl -s http://localhost:8002/health >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Model Gateway ^(port 8002^): Healthy
    ) else (
        echo [FAIL] Model Gateway ^(port 8002^): Unhealthy
    )
    
    curl -s http://localhost:8003/health >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Memory Engine ^(port 8003^): Healthy
    ) else (
        echo [FAIL] Memory Engine ^(port 8003^): Unhealthy
    )
    
    curl -s http://localhost:8004/health >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] RSI Engine ^(port 8004^): Healthy
    ) else (
        echo [FAIL] RSI Engine ^(port 8004^): Unhealthy
    )
    
    curl -s http://localhost:8005/health >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Cognitive Engine ^(port 8005^): Healthy
    ) else (
        echo [FAIL] Cognitive Engine ^(port 8005^): Unhealthy
    )
    
    curl -s http://localhost:8006/health >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Tool Execution Engine ^(port 8006^): Healthy
    ) else (
        echo [FAIL] Tool Execution Engine ^(port 8006^): Unhealthy
    )
    
    curl -s http://localhost:8007/health >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Workflow Engine ^(port 8007^): Healthy
    ) else (
        echo [FAIL] Workflow Engine ^(port 8007^): Unhealthy
    )
    
    curl -s http://localhost:8008/health >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Policy Engine ^(port 8008^): Healthy
    ) else (
        echo [FAIL] Policy Engine ^(port 8008^): Unhealthy
    )
    
    curl -s http://localhost:8009/health >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Evaluation Engine ^(port 8009^): Healthy
    ) else (
        echo [FAIL] Evaluation Engine ^(port 8009^): Unhealthy
    )
    
    curl -s http://localhost:8010/health >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Device Gateway ^(port 8010^): Healthy
    ) else (
        echo [FAIL] Device Gateway ^(port 8010^): Unhealthy
    )
)

if "%COMMAND%"=="clean" (
    echo Cleaning up containers and volumes...
    docker-compose down -v
    echo Cleanup completed successfully!
)

if "%COMMAND%"=="help" (
    echo Usage: deploy-complete.bat {dev^|stop^|restart^|logs^|status^|health^|clean}
    echo.
    echo Commands:
    echo   dev     - Start complete development environment ^(default^)
    echo   stop    - Stop all services
    echo   restart - Restart all services
    echo   logs    - View logs ^(optional: specify service name^)
    echo   status  - Check service status
    echo   health  - Run health checks on all services
    echo   clean   - Remove containers and volumes
    echo   help    - Show this help message
)