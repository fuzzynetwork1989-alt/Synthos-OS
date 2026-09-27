"""Main application entry point for Memory Engine"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import structlog
from contextlib import asynccontextmanager
import redis.asyncio as redis
import asyncpg

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
    # Initialize connections
    app.state.redis = None
    app.state.db_pool = None
    
    try:
        # Connect to Redis
        app.state.redis = redis.from_url(settings.redis_url, decode_responses=True)
        await app.state.redis.ping()
        logger.info("Connected to Redis")
        
        # Connect to PostgreSQL
        app.state.db_pool = await asyncpg.create_pool(settings.database_url)
        logger.info("Connected to PostgreSQL")
        
        logger.info(
            "Memory Engine starting",
            app_name=settings.app_name,
            version=settings.app_version,
            environment=settings.environment,
        )
        yield
        
    finally:
        # Cleanup connections
        if app.state.redis:
            await app.state.redis.close()
        if app.state.db_pool:
            await app.state.db_pool.close()
        logger.info("Memory Engine shutting down")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Memory Engine for Synthos-OS - Persistent memory and knowledge management",
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
    redis_status = "unhealthy"
    db_status = "unhealthy"
    
    try:
        if app.state.redis:
            await app.state.redis.ping()
            redis_status = "healthy"
    except Exception as e:
        logger.error("Redis health check failed", error=str(e))
    
    try:
        if app.state.db_pool:
            async with app.state.db_pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            db_status = "healthy"
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
    
    return {
        "status": "healthy" if redis_status == "healthy" and db_status == "healthy" else "degraded",
        "redis": redis_status,
        "database": db_status,
    }


@app.post("/memory", response_model=MemoryEntry)
async def create_memory(entry: MemoryEntry):
    """Create a new memory entry"""
    try:
        import uuid
        entry_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        # Store in Redis for fast access
        if app.state.redis:
            memory_data = {
                "id": entry_id,
                "content": entry.content,
                "metadata": str(entry.metadata),
                "tags": ",".join(entry.tags),
                "created_at": now.isoformat(),
            }
            await app.state.redis.hset(f"memory:{entry_id}", mapping=memory_data)
            
            if entry.ttl:
                await app.state.redis.expire(f"memory:{entry_id}", entry.ttl)
        
        # Store in PostgreSQL for persistence
        if app.state.db_pool:
            async with app.state.db_pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO memory_entries (id, content, metadata, tags, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    """,
                    entry_id, entry.content, entry.metadata, entry.tags, now, now
                )
        
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
        # Try Redis first
        if app.state.redis:
            memory_data = await app.state.redis.hgetall(f"memory:{memory_id}")
            if memory_data:
                return MemoryEntry(
                    id=memory_id,
                    content=memory_data.get("content", ""),
                    metadata=eval(memory_data.get("metadata", "{}")),
                    tags=memory_data.get("tags", "").split(",") if memory_data.get("tags") else [],
                    created_at=datetime.fromisoformat(memory_data.get("created_at")),
                )
        
        # Fallback to PostgreSQL
        if app.state.db_pool:
            async with app.state.db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT * FROM memory_entries WHERE id = $1", memory_id
                )
                if row:
                    return MemoryEntry(
                        id=row["id"],
                        content=row["content"],
                        metadata=row["metadata"],
                        tags=row["tags"],
                        created_at=row["created_at"],
                        updated_at=row["updated_at"],
                    )
        
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
        
        # Simple text search (in production, use vector search)
        if app.state.db_pool:
            async with app.state.db_pool.acquire() as conn:
                rows = await conn.fetch(
                    """
                    SELECT * FROM memory_entries 
                    WHERE content ILIKE $1 
                    LIMIT $2
                    """,
                    f"%{request.query}%", request.limit
                )
                
                for row in rows:
                    results.append(MemoryEntry(
                        id=row["id"],
                        content=row["content"],
                        metadata=row["metadata"],
                        tags=row["tags"],
                        created_at=row["created_at"],
                        updated_at=row["updated_at"],
                    ))
        
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
        # Delete from Redis
        if app.state.redis:
            await app.state.redis.delete(f"memory:{memory_id}")
        
        # Delete from PostgreSQL
        if app.state.db_pool:
            async with app.state.db_pool.acquire() as conn:
                await conn.execute("DELETE FROM memory_entries WHERE id = $1", memory_id)
        
        return {"status": "deleted", "id": memory_id}
    
    except Exception as e:
        logger.error("Failed to delete memory", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "synthos_memory_engine.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=settings.workers if not settings.debug else 1,
    )