"""Main application entry point for Model Gateway"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import httpx
import structlog
from contextlib import asynccontextmanager

from .config import settings

logger = structlog.get_logger(__name__)


class ChatRequest(BaseModel):
    """Chat completion request"""
    messages: List[Dict[str, str]]
    model: Optional[str] = None
    provider: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    stream: bool = False


class ChatResponse(BaseModel):
    """Chat completion response"""
    content: str
    model: str
    provider: str
    tokens_used: int
    finish_reason: str


class ModelInfo(BaseModel):
    """Model information"""
    name: str
    provider: str
    capabilities: List[str]
    context_length: int
    parameters: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info(
        "Model Gateway starting",
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )
    yield
    logger.info("Model Gateway shutting down")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Model Gateway for Synthos-OS - Routes requests to multiple model providers",
    lifespan=lifespan,
    debug=settings.debug,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# Provider clients
ollama_client = httpx.AsyncClient(base_url=settings.ollama_base_url, timeout=settings.request_timeout)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "default_provider": settings.default_provider,
        "default_model": settings.default_model,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check Ollama connection
        response = await ollama_client.get("/api/tags")
        ollama_status = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception as e:
        ollama_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy",
        "providers": {
            "ollama": ollama_status,
        },
        "default_provider": settings.default_provider,
    }


@app.get("/models")
async def list_models():
    """List available models from all providers"""
    models = []
    
    try:
        # Get Ollama models
        response = await ollama_client.get("/api/tags")
        if response.status_code == 200:
            ollama_models = response.json().get("models", [])
            for model in ollama_models:
                models.append(ModelInfo(
                    name=model["name"],
                    provider="ollama",
                    capabilities=["chat", "completion"],
                    context_length=4096,
                    parameters="unknown"
                ))
    except Exception as e:
        logger.error("Failed to fetch Ollama models", error=str(e))
    
    return {"models": models}


@app.post("/chat/completions", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    """Process chat completion request"""
    provider = request.provider or settings.default_provider
    model = request.model or settings.default_model
    
    try:
        if provider == "ollama":
            return await _ollama_chat(request, model)
        else:
            raise HTTPException(status_code=400, detail=f"Provider {provider} not yet implemented")
    
    except Exception as e:
        logger.error("Chat completion failed", error=str(e), provider=provider, model=model)
        raise HTTPException(status_code=500, detail=str(e))


async def _ollama_chat(request: ChatRequest, model: str) -> ChatResponse:
    """Handle Ollama chat completion"""
    payload = {
        "model": model,
        "messages": request.messages,
        "stream": request.stream,
        "options": {
            "temperature": request.temperature or settings.temperature,
            "num_predict": request.max_tokens or settings.max_tokens,
        }
    }
    
    response = await ollama_client.post("/api/chat", json=payload)
    response.raise_for_status()
    
    result = response.json()
    
    return ChatResponse(
        content=result.get("message", {}).get("content", ""),
        model=model,
        provider="ollama",
        tokens_used=result.get("eval_count", 0),
        finish_reason=result.get("done_reason", "stop")
    )


@app.get("/providers")
async def list_providers():
    """List available model providers"""
    return {
        "providers": [
            {
                "name": "ollama",
                "status": "available",
                "base_url": settings.ollama_base_url,
                "models": settings.fallback_models
            },
            {
                "name": "lm_studio",
                "status": "configured",
                "base_url": settings.lm_studio_base_url,
                "models": []
            },
            {
                "name": "openai",
                "status": "configured" if settings.openai_api_key else "not_configured",
                "base_url": "https://api.openai.com/v1",
                "models": []
            },
            {
                "name": "anthropic",
                "status": "configured" if settings.anthropic_api_key else "not_configured",
                "base_url": "https://api.anthropic.com",
                "models": []
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "synthos_model_gateway.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=settings.workers if not settings.debug else 1,
    )