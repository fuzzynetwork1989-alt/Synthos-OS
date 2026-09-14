"""Main application entry point for API Gateway"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import uuid

from .config import settings
from .logging import configure_logging, log_request, log_error, get_logger
from .health import router as health_router


# Configure logging on startup
configure_logging()
logger = get_logger("api.gateway")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Validate configuration on startup
    warnings = settings.validate_configuration()
    for warning in warnings:
        logger.warning("configuration_warning", warning=warning)

    logger.info(
        "application_startup",
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )

    yield

    logger.info("application_shutdown")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API Gateway for Synthos-OS",
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


# Include routers
app.include_router(health_router, prefix="/api/v1", tags=["health"])


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    """Middleware to log all HTTP requests"""
    request_id = str(uuid.uuid4())
    start_time = time.time()

    # Add request_id to request state
    request.state.request_id = request_id

    try:
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000

        log_request(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            request_id=request_id,
        )

        # Add request_id to response headers
        response.headers["X-Request-ID"] = request_id
        return response

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        log_error(
            error=e,
            context={"method": request.method, "path": request.url.path},
            request_id=request_id,
        )
        raise


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    request_id = getattr(request.state, "request_id", None)

    logger.error(
        "unhandled_exception",
        error_type=type(exc).__name__,
        error_message=str(exc),
        path=request.url.path,
        method=request.method,
        request_id=request_id,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred",
                "request_id": request_id,
            }
        },
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


@app.get("/api/v1")
async def api_root():
    """API root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "endpoints": {
            "health": "/api/v1/health",
            "readiness": "/api/v1/health/ready",
            "liveness": "/api/v1/health/live",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "synthos_api_gateway.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=settings.workers if not settings.debug else 1,
    )
