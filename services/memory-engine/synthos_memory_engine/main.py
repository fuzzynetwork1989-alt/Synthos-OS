"""Main application entry point for Memory Engine"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import structlog
from contextlib import asynccontextmanager

from .config import settings

logger = structlog.get_logger(__name__)


class MemoryEntry(BaseModel):
    """Memory entry model"""
    id: Optional[str] = None
    content: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = {}
    tags: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    ttl: Optional[int] = None


class SearchRequest(BaseModel):
    """Memory search request"""
    query: str
    query_embedding: Optional[List[float]] = None
    limit: int = 10
    filters: Dict[str, Any] = {}


class SearchResponse(BaseModel):
    """Memory search response"""
    results: List[MemoryEntry]
    total_count: int
    search_time_ms: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Initialize in-memory storage
    app.state.memory_store = {}
    
    logger.info(
        "Memory Engine starting",
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )
    yield
    
    logger.info("Memory Engine shutting down")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Memory Engine for Synthos-OS - Persistent memory and knowledge management",
    lifespan=lifespan,
    debug=settings.memory_debug,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "memory_enabled": settings.enable_persistence,
        "vector_search_enabled": settings.enable_vector_search,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "storage": "in-memory",
        "memory_entries": len(app.state.memory_store),
    }


@app.post("/memory", response_model=MemoryEntry)
async def create_memory(entry: MemoryEntry):
    """Create a new memory entry"""
    try:
        import uuid
        entry_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        # Store in memory
        app.state.memory_store[entry_id] = {
            "id": entry_id,
            "content": entry.content,
            "metadata": entry.metadata,
            "tags": entry.tags,
            "created_at": now,
            "updated_at": now,
            "ttl": entry.ttl
        }
        
        return MemoryEntry(
            id=entry_id,
            content=entry.content,
            metadata=entry.metadata,
            tags=entry.tags,
            created_at=now,
            updated_at=now,
            ttl=entry.ttl
        )
    
    except Exception as e:
        logger.error("Failed to create memory", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory/{memory_id}", response_model=MemoryEntry)
async def get_memory(memory_id: str):
    """Get a specific memory entry"""
    try:
        memory_data = app.state.memory_store.get(memory_id)
        if memory_data:
            return MemoryEntry(**memory_data)
        
        raise HTTPException(status_code=404, detail="Memory not found")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get memory", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/memory/search", response_model=SearchResponse)
async def search_memory(request: SearchRequest):
    """Search memory entries"""
    import time
    start_time = time.time()
    
    try:
        results = []
        
        # Simple text search
        query_lower = request.query.lower()
        for memory_id, memory_data in app.state.memory_store.items():
            if query_lower in memory_data["content"].lower():
                results.append(MemoryEntry(**memory_data))
                if len(results) >= request.limit:
                    break
        
        search_time = (time.time() - start_time) * 1000
        
        return SearchResponse(
            results=results,
            total_count=len(results),
            search_time_ms=search_time
        )
    
    except Exception as e:
        logger.error("Failed to search memory", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/memory/{memory_id}")
async def delete_memory(memory_id: str):
    """Delete a memory entry"""
    try:
        if memory_id in app.state.memory_store:
            del app.state.memory_store[memory_id]
            return {"status": "deleted", "id": memory_id}
        
        raise HTTPException(status_code=404, detail="Memory not found")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete memory", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "synthos_memory_engine.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.memory_debug,
        workers=settings.workers if not settings.memory_debug else 1,
    )