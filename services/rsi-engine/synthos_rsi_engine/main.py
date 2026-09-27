"""Main FastAPI application for RSI Engine"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import structlog

from .config import Settings
from .core.coordinator import RSICoordinator
from .safety.goal_drift_index import GoalDriftIndex
from .core.state_manager import StateManager
from .governance.proposal_manager import ProposalManager
from .governance.audit_logger import AuditLogger

logger = structlog.get_logger(__name__)

# Initialize settings
settings = Settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Recursive Self-Improvement Engine for Synthos-OS"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RSI components
rsi_config = settings.get_rsi_config()
coordinator = RSICoordinator(rsi_config)
state_manager = StateManager()

# Initialize GDI with baseline goals
baseline_goals = rsi_config["baseline_goals"]
coordinator.initialize_gdi(baseline_goals)


class ImprovementCycleRequest(BaseModel):
    """Request to start an improvement cycle"""
    trigger_reason: str
    auto_approve: bool = False


class ManualTriggerRequest(BaseModel):
    """Request to manually trigger an improvement cycle"""
    reason: str
    context: Optional[Dict] = None


class ImprovementCycleResponse(BaseModel):
    """Response from improvement cycle"""
    cycle_id: str
    status: str
    mutations_generated: int
    mutations_approved: int
    gdi_before: float
    gdi_after: float
    performance_delta: float


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
        "coordinator_status": coordinator.get_system_status(),
        "state_manager_status": {
            "current_state": state_manager.get_state().value,
            "current_version": state_manager.get_current_version().version
        }
    }


@app.post("/rsi/cycle/start")
async def start_improvement_cycle(request: ImprovementCycleRequest) -> ImprovementCycleResponse:
    """Start a new RSI improvement cycle"""
    try:
        cycle = coordinator.start_improvement_cycle(
            trigger_reason=request.trigger_reason,
            auto_approve=request.auto_approve
        )
        
        return ImprovementCycleResponse(
            cycle_id=cycle.cycle_id,
            status=cycle.status.value,
            mutations_generated=cycle.mutations_generated,
            mutations_approved=cycle.mutations_approved,
            gdi_before=cycle.gdi_before,
            gdi_after=cycle.gdi_after,
            performance_delta=cycle.performance_delta
        )
    except Exception as e:
        logger.error("Failed to start improvement cycle", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/rsi/cycle/{cycle_id}")
async def get_cycle_status(cycle_id: str):
    """Get status of a specific improvement cycle"""
    cycle = coordinator.get_cycle_status(cycle_id)
    if not cycle:
        raise HTTPException(status_code=404, detail="Cycle not found")
    
    return {
        "cycle_id": cycle.cycle_id,
        "status": cycle.status.value,
        "timestamp": cycle.timestamp,
        "mutations_generated": cycle.mutations_generated,
        "mutations_tested": cycle.mutations_tested,
        "mutations_approved": cycle.mutations_approved,
        "gdi_before": cycle.gdi_before,
        "gdi_after": cycle.gdi_after,
        "performance_delta": cycle.performance_delta,
        "error_message": cycle.error_message
    }


@app.get("/rsi/cycles")
async def get_all_cycles():
    """Get all improvement cycles"""
    return {
        "cycles": [
            {
                "cycle_id": cycle.cycle_id,
                "status": cycle.status.value,
                "timestamp": cycle.timestamp,
                "mutations_approved": cycle.mutations_approved
            }
            for cycle in coordinator.cycle_history
        ]
    }


@app.get("/rsi/status")
async def get_rsi_status():
    """Get overall RSI system status"""
    return coordinator.get_system_status()


@app.post("/rsi/emergency-stop")
async def emergency_stop():
    """Emergency stop - halt all RSI activity"""
    coordinator.emergency_stop()
    return {"status": "emergency_stop_triggered"}


@app.post("/rsi/autonomous/enable")
async def enable_autonomous_mode(safety_override_key: Optional[str] = None):
    """Enable autonomous improvement mode"""
    success = coordinator.enable_autonomous_mode(safety_override_key)
    if success:
        return {"status": "autonomous_mode_enabled"}
    else:
        raise HTTPException(status_code=400, detail="Failed to enable autonomous mode")


@app.post("/rsi/autonomous/disable")
async def disable_autonomous_mode():
    """Disable autonomous improvement mode"""
    coordinator.disable_autonomous_mode()
    return {"status": "autonomous_mode_disabled"}


@app.get("/rsi/autonomous/status")
async def get_autonomous_status():
    """Get autonomous mode status"""
    return coordinator.get_autonomous_status()


@app.get("/rsi/meta/metrics")
async def get_meta_rsi_metrics():
    """Get Meta-RSI performance metrics"""
    return coordinator.get_meta_rsi_metrics()


@app.post("/rsi/autonomous/manual-trigger")
async def manual_trigger(request: ManualTriggerRequest):
    """Manually trigger an improvement cycle"""
    if coordinator.continuous_rsi:
        success = coordinator.continuous_rsi.manual_trigger(request.reason, request.context or {})
        if success:
            return {"status": "manual_trigger_initiated"}
        else:
            raise HTTPException(status_code=400, detail="Failed to trigger cycle")
    else:
        raise HTTPException(status_code=400, detail="Continuous RSI not initialized")


@app.get("/safety/gdi")
async def get_gdi_status():
    """Get Goal Drift Index status"""
    if not coordinator.gdi:
        return {"status": "not_initialized"}
    
    # Get current GDI
    current_gdi, signals = coordinator.gdi.calculate_gdi(
        settings.get_rsi_config()["baseline_goals"],
        "",
        {},
        []
    )
    
    return {
        "current_gdi": current_gdi,
        "status": coordinator.gdi.get_drift_status(current_gdi),
        "signals": [
            {
                "name": signal.name,
                "value": signal.value,
                "threshold": signal.threshold,
                "status": signal.status
            }
            for signal in signals
        ],
        "trend": coordinator.gdi.get_historical_trend()
    }


@app.get("/safety/constraints")
async def get_constraints_summary():
    """Get constitutional constraints summary"""
    return coordinator.gatekeeper.constraints.get_constraint_summary()


@app.get("/system/state")
async def get_system_state():
    """Get current system state"""
    return {
        "state": state_manager.get_state().value,
        "version": state_manager.get_current_version().version,
        "version_history": [
            {
                "version": v.version,
                "timestamp": v.timestamp,
                "changes_count": len(v.changes)
            }
            for v in state_manager.get_version_history()
        ]
    }


@app.post("/system/rollback/{version}")
async def rollback_to_version(version: str):
    """Rollback to a specific version"""
    success = state_manager.rollback_to_version(version)
    if not success:
        raise HTTPException(status_code=400, detail="Rollback failed")
    
    return {"status": "rollback_successful", "version": version}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "synthos_rsi_engine.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
