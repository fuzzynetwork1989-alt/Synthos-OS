# Synthos-OS Ollama Model Pull Script for Windows
# This script pulls required Ollama models for Synthos-OS

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Ollama Model Pull Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker status..." -ForegroundColor Yellow
try {
    $dockerStatus = docker ps 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Docker is running" -ForegroundColor Green
    } else {
        Write-Host "Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if Ollama container is running
Write-Host "Checking Ollama container..." -ForegroundColor Yellow
$ollamaRunning = docker ps --filter "name=synthos-ollama" --format "{{.Names}}" 2>$null
if ($ollamaRunning -eq "synthos-ollama") {
    Write-Host "Ollama container is running" -ForegroundColor Green
} else {
    Write-Host "Ollama container is not running. Starting it..." -ForegroundColor Yellow
    docker-compose up -d ollama
    Start-Sleep -Seconds 10
}

# Models to pull
$models = @(
    "llama2",
    "mistral",
    "neural-chat",
    "codellama",
    "phi"
)

Write-Host ""
Write-Host "Pulling Ollama models..." -ForegroundColor Yellow
Write-Host "This may take several minutes depending on your internet connection." -ForegroundColor Gray
Write-Host ""

foreach ($model in $models) {
    Write-Host "Pulling $model..." -ForegroundColor Cyan
    try {
        docker exec synthos-ollama ollama pull $model
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Successfully pulled $model" -ForegroundColor Green
        } else {
            Write-Host "Failed to pull $model" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "Error pulling $model: $_" -ForegroundColor Red
    }
    Write-Host ""
}

# List available models
Write-Host "Available models in Ollama:" -ForegroundColor Yellow
try {
    docker exec synthos-ollama ollama list
}
catch {
    Write-Host "Failed to list models" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Model Pull Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now use the models through the Model Gateway at:" -ForegroundColor Green
Write-Host "http://localhost:8002/models" -ForegroundColor White
Write-Host ""