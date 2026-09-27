# Synthos-OS Verification Script for Windows
# This script verifies all services are running correctly

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Synthos-OS Verification Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allPassed = $true

# Check Docker
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    Write-Host "✓ Docker: $dockerVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Docker: Not installed or not running" -ForegroundColor Red
    $allPassed = $false
}

# Check Docker Compose
Write-Host "Checking Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version 2>$null
    Write-Host "✓ Docker Compose: $composeVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Docker Compose: Not installed" -ForegroundColor Red
    $allPassed = $false
}

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Python: Not installed" -ForegroundColor Red
    $allPassed = $false
}

# Check Git
Write-Host "Checking Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>$null
    Write-Host "✓ Git: $gitVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Git: Not installed" -ForegroundColor Red
    $allPassed = $false
}

# Check Node.js (optional)
Write-Host "Checking Node.js (optional)..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>$null
    Write-Host "✓ Node.js: $nodeVersion" -ForegroundColor Green
}
catch {
    Write-Host "○ Node.js: Not installed (optional)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Checking Docker Services..." -ForegroundColor Yellow

# Check services
$services = @(
    "synthos-postgres",
    "synthos-redis",
    "synthos-ollama",
    "synthos-api-gateway",
    "synthos-model-gateway",
    "synthos-memory-engine",
    "synthos-rsi-engine",
    "synthos-cognitive-engine",
    "synthos-tool-execution-engine"
)

foreach ($service in $services) {
    $status = docker ps --filter "name=$service" --format "{{.Status}}" 2>$null
    if ($status) {
        Write-Host "✓ $service: $status" -ForegroundColor Green
    } else {
        Write-Host "✗ $service: Not running" -ForegroundColor Red
        $allPassed = $false
    }
}

Write-Host ""
Write-Host "Checking Service Health..." -ForegroundColor Yellow

# Check API Gateway
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ API Gateway: Healthy" -ForegroundColor Green
    } else {
        Write-Host "✗ API Gateway: Unhealthy (Status: $($response.StatusCode))" -ForegroundColor Red
        $allPassed = $false
    }
}
catch {
    Write-Host "✗ API Gateway: Not responding" -ForegroundColor Red
    $allPassed = $false
}

# Check Model Gateway
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8002/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Model Gateway: Healthy" -ForegroundColor Green
    } else {
        Write-Host "✗ Model Gateway: Unhealthy (Status: $($response.StatusCode))" -ForegroundColor Red
        $allPassed = $false
    }
}
catch {
    Write-Host "✗ Model Gateway: Not responding" -ForegroundColor Red
    $allPassed = $false
}

# Check Memory Engine
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8003/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Memory Engine: Healthy" -ForegroundColor Green
    } else {
        Write-Host "✗ Memory Engine: Unhealthy (Status: $($response.StatusCode))" -ForegroundColor Red
        $allPassed = $false
    }
}
catch {
    Write-Host "✗ Memory Engine: Not responding" -ForegroundColor Red
    $allPassed = $false
}

# Check RSI Engine
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8004/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ RSI Engine: Healthy" -ForegroundColor Green
    } else {
        Write-Host "✗ RSI Engine: Unhealthy (Status: $($response.StatusCode))" -ForegroundColor Red
        $allPassed = $false
    }
}
catch {
    Write-Host "✗ RSI Engine: Not responding" -ForegroundColor Red
    $allPassed = $false
}

Write-Host ""
Write-Host "Checking Ollama Models..." -ForegroundColor Yellow

try {
    $models = docker exec synthos-ollama ollama list 2>$null
    if ($models) {
        Write-Host "✓ Ollama models available:" -ForegroundColor Green
        Write-Host $models
    } else {
        Write-Host "✗ No Ollama models found" -ForegroundColor Red
        Write-Host "Run: .\scripts\pull-ollama-models.ps1" -ForegroundColor Yellow
        $allPassed = $false
    }
}
catch {
    Write-Host "✗ Cannot check Ollama models" -ForegroundColor Red
    $allPassed = $false
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($allPassed) {
    Write-Host "  All Checks Passed!" -ForegroundColor Green
} else {
    Write-Host "  Some Checks Failed!" -ForegroundColor Red
}
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not $allPassed) {
    Write-Host "Troubleshooting tips:" -ForegroundColor Yellow
    Write-Host "- Ensure Docker Desktop is running" -ForegroundColor White
    Write-Host "- Run: .\scripts\deploy.bat dev" -ForegroundColor White
    Write-Host "- Run: .\scripts\deploy.bat migrate" -ForegroundColor White
    Write-Host "- Run: .\scripts\pull-ollama-models.ps1" -ForegroundColor White
    Write-Host ""
}

exit (if ($allPassed) { 0 } else { 1 })