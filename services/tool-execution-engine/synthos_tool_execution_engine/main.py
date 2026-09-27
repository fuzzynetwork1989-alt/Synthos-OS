"""Main application entry point for Tool Execution Engine"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import structlog
from contextlib import asynccontextmanager
import subprocess
import json
import os

from .config import settings

logger = structlog.get_logger(__name__)


class ToolExecutionRequest(BaseModel):
    """Tool execution request"""
    tool_name: str
    parameters: Dict[str, Any]
    timeout: Optional[int] = None
    sandbox: Optional[bool] = None


class ToolExecutionResponse(BaseModel):
    """Tool execution response"""
    success: bool
    result: Any
    error: Optional[str] = None
    execution_time: float
    stdout: Optional[str] = None
    stderr: Optional[str] = None


class ToolInfo(BaseModel):
    """Tool information"""
    name: str
    description: str
    parameters: Dict[str, Any]
    safety_level: str
    requires_sandbox: bool


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info(
        "Tool Execution Engine starting",
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
        sandbox_enabled=settings.enable_sandbox,
    )
    yield
    logger.info("Tool Execution Engine shutting down")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Tool Execution Engine for Synthos-OS - Safe tool execution and sandboxing",
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


# Tool registry (placeholder)
TOOL_REGISTRY = {
    "file_read": {
        "name": "file_read",
        "description": "Read file contents",
        "parameters": {"path": "string"},
        "safety_level": "low",
        "requires_sandbox": False
    },
    "file_write": {
        "name": "file_write",
        "description": "Write content to file",
        "parameters": {"path": "string", "content": "string"},
        "safety_level": "medium",
        "requires_sandbox": True
    },
    "web_search": {
        "name": "web_search",
        "description": "Search the web",
        "parameters": {"query": "string", "num_results": "integer"},
        "safety_level": "low",
        "requires_sandbox": False
    },
    "code_execution": {
        "name": "code_execution",
        "description": "Execute code snippet",
        "parameters": {"code": "string", "language": "string"},
        "safety_level": "high",
        "requires_sandbox": True
    }
}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "sandbox_enabled": settings.enable_sandbox,
        "tool_count": len(TOOL_REGISTRY),
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "sandbox_enabled": settings.enable_sandbox,
        "tool_registry_size": len(TOOL_REGISTRY),
    }


@app.get("/tools", response_model=List[ToolInfo])
async def list_tools():
    """List available tools"""
    return [
        ToolInfo(**tool_info) for tool_info in TOOL_REGISTRY.values()
    ]


@app.get("/tools/{tool_name}", response_model=ToolInfo)
async def get_tool_info(tool_name: str):
    """Get information about a specific tool"""
    if tool_name not in TOOL_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    
    return ToolInfo(**TOOL_REGISTRY[tool_name])


@app.post("/execute", response_model=ToolExecutionResponse)
async def execute_tool(request: ToolExecutionRequest):
    """Execute a tool"""
    import time
    start_time = time.time()
    
    try:
        # Check if tool exists
        if request.tool_name not in TOOL_REGISTRY:
            raise HTTPException(status_code=404, detail=f"Tool '{request.tool_name}' not found")
        
        tool_info = TOOL_REGISTRY[request.tool_name]
        
        # Security check
        if settings.enable_security_checks:
            if _is_blocked_command(request.parameters):
                raise HTTPException(status_code=403, detail="Command blocked by security policy")
        
        # Sandbox check
        use_sandbox = request.sandbox if request.sandbox is not None else settings.enable_sandbox
        if tool_info["requires_sandbox"] and not use_sandbox:
            raise HTTPException(status_code=400, detail="Tool requires sandbox but sandbox is disabled")
        
        # Execute tool
        result = await _execute_tool_impl(request.tool_name, request.parameters, use_sandbox)
        
        execution_time = time.time() - start_time
        
        return ToolExecutionResponse(
            success=True,
            result=result,
            execution_time=execution_time
        )
    
    except HTTPException:
        raise
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error("Tool execution failed", error=str(e), tool=request.tool_name)
        
        return ToolExecutionResponse(
            success=False,
            result=None,
            error=str(e),
            execution_time=execution_time
        )


async def _execute_tool_impl(tool_name: str, parameters: Dict[str, Any], use_sandbox: bool) -> Any:
    """Execute tool implementation"""
    # Placeholder implementations for common tools
    if tool_name == "file_read":
        path = parameters.get("path")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return f.read()
        else:
            raise FileNotFoundError(f"File not found: {path}")
    
    elif tool_name == "file_write":
        path = parameters.get("path")
        content = parameters.get("content")
        with open(path, 'w') as f:
            f.write(content)
        return {"status": "written", "path": path, "bytes": len(content)}
    
    elif tool_name == "web_search":
        query = parameters.get("query")
        # Placeholder - would use actual web search API
        return {
            "query": query,
            "results": [
                {"title": f"Result for {query}", "url": "https://example.com"}
            ]
        }
    
    elif tool_name == "code_execution":
        code = parameters.get("code")
        language = parameters.get("language", "python")
        # Placeholder - would use actual code execution sandbox
        return {
            "language": language,
            "output": f"Executed {len(code)} characters of {language} code"
        }
    
    else:
        raise NotImplementedError(f"Tool '{tool_name}' not implemented")


def _is_blocked_command(parameters: Dict[str, Any]) -> bool:
    """Check if command is blocked by security policy"""
    # Convert parameters to string for checking
    params_str = str(parameters).lower()
    
    for blocked in settings.blocked_commands:
        if blocked.lower() in params_str:
            return True
    
    return False


@app.post("/sandbox/status")
async def sandbox_status():
    """Get sandbox status"""
    return {
        "enabled": settings.enable_sandbox,
        "timeout": settings.sandbox_timeout,
        "max_memory_mb": settings.max_memory_mb,
        "max_cpu_time": settings.max_cpu_time,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "synthos_tool_execution_engine.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=settings.workers if not settings.debug else 1,
    )