"""Main application entry point for Cognitive Engine"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import httpx
import structlog
from contextlib import asynccontextmanager

from .config import settings

logger = structlog.get_logger(__name__)


class ReasoningRequest(BaseModel):
    """Reasoning request"""
    query: str
    context: Optional[str] = None
    reasoning_method: str = "chain_of_thought"
    max_steps: int = 5


class ReasoningResponse(BaseModel):
    """Reasoning response"""
    reasoning: str
    steps: List[str]
    confidence: float
    method: str


class PlanningRequest(BaseModel):
    """Planning request"""
    goal: str
    current_state: Dict[str, Any]
    constraints: Optional[List[str]] = None
    max_depth: int = 5


class PlanningResponse(BaseModel):
    """Planning response"""
    plan: List[Dict[str, Any]]
    estimated_time: str
    resource_requirements: Dict[str, Any]
    confidence: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info(
        "Cognitive Engine starting",
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )
    yield
    logger.info("Cognitive Engine shutting down")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Cognitive Engine for Synthos-OS - Reasoning and planning capabilities",
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
        "capabilities": ["reasoning", "planning", "context_management"],
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check connectivity to dependent services
        async with httpx.AsyncClient() as client:
            model_gateway = await client.get(f"{settings.model_gateway_url}/health", timeout=5.0)
            memory_engine = await client.get(f"{settings.memory_engine_url}/health", timeout=5.0)
            
            return {
                "status": "healthy",
                "dependencies": {
                    "model_gateway": "healthy" if model_gateway.status_code == 200 else "unhealthy",
                    "memory_engine": "healthy" if memory_engine.status_code == 200 else "unhealthy",
                },
            }
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return {
            "status": "degraded",
            "error": str(e),
        }


@app.post("/reasoning", response_model=ReasoningResponse)
async def reasoning(request: ReasoningRequest):
    """Process reasoning request"""
    try:
        if request.reasoning_method == "chain_of_thought":
            return await _chain_of_thought(request)
        elif request.reasoning_method == "tree_of_thoughts":
            return await _tree_of_thoughts(request)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown reasoning method: {request.reasoning_method}")
    
    except Exception as e:
        logger.error("Reasoning failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


async def _chain_of_thought(request: ReasoningRequest) -> ReasoningResponse:
    """Chain of thought reasoning"""
    # Placeholder implementation
    steps = [
        f"Analyze query: {request.query}",
        "Identify key components",
        "Apply reasoning rules",
        "Synthesize conclusion",
        "Validate result"
    ]
    
    reasoning = f"Using chain-of-thought reasoning to address: {request.query}"
    
    return ReasoningResponse(
        reasoning=reasoning,
        steps=steps,
        confidence=0.85,
        method="chain_of_thought"
    )


async def _tree_of_thoughts(request: ReasoningRequest) -> ReasoningResponse:
    """Tree of thoughts reasoning"""
    # Placeholder implementation
    steps = [
        f"Generate multiple reasoning paths for: {request.query}",
        "Evaluate each path",
        "Select best path",
        "Refine conclusion",
        "Final validation"
    ]
    
    reasoning = f"Using tree-of-thoughts reasoning to address: {request.query}"
    
    return ReasoningResponse(
        reasoning=reasoning,
        steps=steps,
        confidence=0.82,
        method="tree_of_thoughts"
    )


@app.post("/planning", response_model=PlanningResponse)
async def planning(request: PlanningRequest):
    """Process planning request"""
    try:
        return await _generate_plan(request)
    
    except Exception as e:
        logger.error("Planning failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


async def _generate_plan(request: PlanningRequest) -> PlanningResponse:
    """Generate execution plan"""
    # Placeholder implementation
    plan = [
        {
            "step": 1,
            "action": "analyze_goal",
            "description": f"Analyze goal: {request.goal}",
            "estimated_time": "5 minutes"
        },
        {
            "step": 2,
            "action": "assess_current_state",
            "description": "Assess current state and resources",
            "estimated_time": "3 minutes"
        },
        {
            "step": 3,
            "action": "identify_dependencies",
            "description": "Identify dependencies and constraints",
            "estimated_time": "5 minutes"
        },
        {
            "step": 4,
            "action": "create_execution_plan",
            "description": "Create detailed execution plan",
            "estimated_time": "10 minutes"
        },
        {
            "step": 5,
            "action": "execute_plan",
            "description": "Execute the plan with monitoring",
            "estimated_time": "Variable"
        }
    ]
    
    return PlanningResponse(
        plan=plan,
        estimated_time="30-60 minutes",
        resource_requirements={
            "cpu": "2 cores",
            "memory": "4GB",
            "storage": "10GB"
        },
        confidence=0.78
    )


@app.get("/capabilities")
async def get_capabilities():
    """Get available cognitive capabilities"""
    return {
        "reasoning_methods": ["chain_of_thought", "tree_of_thoughts"],
        "planning_algorithms": ["forward_chaining", "backward_chaining", "hierarchical"],
        "context_management": {
            "max_context_length": settings.max_context_length,
            "context_window": settings.context_window,
        },
        "features": {
            "multi_step_reasoning": True,
            "backtracking": settings.enable_backtracking,
            "constraint_handling": True,
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "synthos_cognitive_engine.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=settings.workers if not settings.debug else 1,
    )