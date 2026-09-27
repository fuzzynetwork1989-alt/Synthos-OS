"""Main FastAPI application for Policy Engine"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import structlog

from .config import Settings

logger = structlog.get_logger(__name__)

# Initialize settings
settings = Settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Policy enforcement and governance engine for Synthos-OS"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PolicyDefinition(BaseModel):
    """Policy definition schema"""
    name: str
    description: str
    scope: str  # system, user, workflow, tool
    rules: List[Dict[str, Any]]
    conditions: Optional[Dict[str, Any]] = None
    severity: str = "medium"  # low, medium, high, critical


class PolicyEvaluation(BaseModel):
    """Policy evaluation request"""
    policy_id: str
    action: str
    context: Dict[str, Any]
    subject: Optional[str] = None
    resource: Optional[str] = None


class PolicyResult(BaseModel):
    """Policy evaluation result"""
    allowed: bool
    policy_id: str
    reason: str
    violations: List[str]
    metadata: Dict[str, Any]


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "enforcement_mode": settings.policy_enforcement_mode,
        "policy_cache_ttl": settings.policy_cache_ttl
    }


@app.post("/policies")
async def create_policy(policy: PolicyDefinition):
    """Create a new policy"""
    try:
        policy_id = f"policy_{hash(policy.name)}"
        
        logger.info(
            "Policy created",
            policy_id=policy_id,
            name=policy.name,
            scope=policy.scope,
            rules_count=len(policy.rules)
        )
        
        return {
            "policy_id": policy_id,
            "status": "created",
            "name": policy.name,
            "scope": policy.scope
        }
    except Exception as e:
        logger.error("Failed to create policy", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/policies/{policy_id}")
async def get_policy(policy_id: str):
    """Get policy by ID"""
    # Placeholder for policy retrieval
    return {
        "policy_id": policy_id,
        "status": "active",
        "name": "Example Policy",
        "scope": "system",
        "rules": []
    }


@app.get("/policies")
async def list_policies():
    """List all policies"""
    # Placeholder for policy listing
    return {
        "policies": [],
        "total": 0
    }


@app.post("/policies/evaluate")
async def evaluate_policy(evaluation: PolicyEvaluation) -> PolicyResult:
    """Evaluate a policy against an action"""
    try:
        logger.info(
            "Policy evaluation",
            policy_id=evaluation.policy_id,
            action=evaluation.action
        )
        
        # Placeholder for policy evaluation logic
        result = PolicyResult(
            allowed=True,
            policy_id=evaluation.policy_id,
            reason="Action complies with policy",
            violations=[],
            metadata={"evaluated_at": "2024-01-01T00:00:00"}
        )
        
        return result
    except Exception as e:
        logger.error("Failed to evaluate policy", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/policies/batch-evaluate")
async def batch_evaluate_policies(evaluations: List[PolicyEvaluation]):
    """Evaluate multiple policies"""
    try:
        results = []
        for evaluation in evaluations:
            result = await evaluate_policy(evaluation)
            results.append(result)
        
        return {
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        logger.error("Failed to batch evaluate policies", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/policies/{policy_id}")
async def update_policy(policy_id: str, policy: PolicyDefinition):
    """Update an existing policy"""
    try:
        logger.info("Policy updated", policy_id=policy_id, name=policy.name)
        
        return {
            "policy_id": policy_id,
            "status": "updated",
            "name": policy.name
        }
    except Exception as e:
        logger.error("Failed to update policy", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/policies/{policy_id}")
async def delete_policy(policy_id: str):
    """Delete a policy"""
    try:
        logger.info("Policy deleted", policy_id=policy_id)
        
        return {
            "policy_id": policy_id,
            "status": "deleted"
        }
    except Exception as e:
        logger.error("Failed to delete policy", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/policies/active")
async def get_active_policies():
    """Get currently active policies"""
    # Placeholder for active policies listing
    return {
        "active_policies": [],
        "total": 0
    }


@app.get("/metrics")
async def get_metrics():
    """Get policy engine metrics"""
    return {
        "total_policies": 0,
        "active_policies": 0,
        "evaluations_today": 0,
        "violations_detected": 0,
        "average_evaluation_time": 0.0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "synthos_policy_engine.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.policy_debug
    )