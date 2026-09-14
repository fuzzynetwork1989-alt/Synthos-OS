"""Health check endpoints and monitoring"""

from fastapi import APIRouter
from pydantic import BaseModel
import time
import asyncio
from .logging import log_health_check, get_logger

router = APIRouter()
logger = get_logger("health")


class HealthCheckResponse(BaseModel):
    """Health check response model"""

    status: str
    version: str
    checks: dict[str, dict[str, str | float]]


class CheckStatus(BaseModel):
    """Individual check status"""

    status: str
    message: str
    duration_ms: float


async def check_database() -> CheckStatus:
    """Check database connectivity"""
    start_time = time.time()
    try:
        # TODO: Implement actual database check
        # For now, return simulated check
        await asyncio.sleep(0.01)
        duration_ms = (time.time() - start_time) * 1000
        log_health_check("database", "healthy", duration_ms)
        return CheckStatus(status="healthy", message="Database accessible", duration_ms=duration_ms)
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        log_health_check("database", "unhealthy", duration_ms, error=str(e))
        return CheckStatus(status="unhealthy", message=str(e), duration_ms=duration_ms)


async def check_redis() -> CheckStatus:
    """Check Redis connectivity"""
    start_time = time.time()
    try:
        # TODO: Implement actual Redis check
        # For now, return simulated check
        await asyncio.sleep(0.01)
        duration_ms = (time.time() - start_time) * 1000
        log_health_check("redis", "healthy", duration_ms)
        return CheckStatus(status="healthy", message="Redis accessible", duration_ms=duration_ms)
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        log_health_check("redis", "unhealthy", duration_ms, error=str(e))
        return CheckStatus(status="unhealthy", message=str(e), duration_ms=duration_ms)


async def check_ollama() -> CheckStatus:
    """Check Ollama service connectivity"""
    start_time = time.time()
    try:
        # TODO: Implement actual Ollama check
        # For now, return simulated check
        await asyncio.sleep(0.01)
        duration_ms = (time.time() - start_time) * 1000
        log_health_check("ollama", "healthy", duration_ms)
        return CheckStatus(status="healthy", message="Ollama accessible", duration_ms=duration_ms)
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        log_health_check("ollama", "unhealthy", duration_ms, error=str(e))
        return CheckStatus(status="unhealthy", message=str(e), duration_ms=duration_ms)


@router.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """Comprehensive health check endpoint"""
    from .config import settings

    checks: dict[str, dict[str, str | float]] = {}

    # Run all checks in parallel
    results = await asyncio.gather(
        check_database(),
        check_redis(),
        check_ollama(),
        return_exceptions=True,
    )

    db_status, redis_status, ollama_status = results

    # Handle exceptions from gather
    if isinstance(db_status, Exception):
        db_status = CheckStatus(status="unhealthy", message=str(db_status), duration_ms=0)
    if isinstance(redis_status, Exception):
        redis_status = CheckStatus(status="unhealthy", message=str(redis_status), duration_ms=0)
    if isinstance(ollama_status, Exception):
        ollama_status = CheckStatus(status="unhealthy", message=str(ollama_status), duration_ms=0)

    checks["database"] = {
        "status": db_status.status,
        "message": db_status.message,
        "duration_ms": db_status.duration_ms,
    }
    checks["redis"] = {
        "status": redis_status.status,
        "message": redis_status.message,
        "duration_ms": redis_status.duration_ms,
    }
    checks["ollama"] = {
        "status": ollama_status.status,
        "message": ollama_status.message,
        "duration_ms": ollama_status.duration_ms,
    }

    # Determine overall status
    all_healthy = all(
        check["status"] == "healthy" for check in checks.values()
    )
    overall_status = "healthy" if all_healthy else "degraded"

    logger.info(
        "health_check_completed",
        status=overall_status,
        checks=checks,
    )

    return HealthCheckResponse(
        status=overall_status,
        version=settings.app_version,
        checks=checks,
    )


@router.get("/health/ready")
async def readiness_check() -> dict[str, str]:
    """Readiness check - returns 200 if service is ready to accept traffic"""
    # For now, always return ready
    # TODO: Add actual readiness logic (e.g., dependencies ready)
    return {"status": "ready"}


@router.get("/health/live")
async def liveness_check() -> dict[str, str]:
    """Liveness check - returns 200 if service is running"""
    return {"status": "alive"}
