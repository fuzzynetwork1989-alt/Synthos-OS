"""Structured logging configuration for API Gateway"""

import structlog
import logging
import sys
from typing import Any
from .config import settings


def configure_logging() -> None:
    """Configure structured logging"""

    # Configure standard logging for libraries
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )

    # Configure structlog
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if settings.log_format == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger"""
    return structlog.get_logger(name)


def log_request(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    request_id: str | None = None,
    user_id: str | None = None,
    **kwargs: Any,
) -> None:
    """Log an HTTP request"""
    logger = get_logger("api.request")
    logger.info(
        "request_processed",
        method=method,
        path=path,
        status_code=status_code,
        duration_ms=duration_ms,
        request_id=request_id,
        user_id=user_id,
        **kwargs,
    )


def log_error(
    error: Exception,
    context: dict[str, Any] | None = None,
    request_id: str | None = None,
    user_id: str | None = None,
) -> None:
    """Log an error"""
    logger = get_logger("api.error")
    logger.error(
        "error_occurred",
        error_type=type(error).__name__,
        error_message=str(error),
        request_id=request_id,
        user_id=user_id,
        **(context or {}),
    )


def log_health_check(
    service: str,
    status: str,
    duration_ms: float,
    **kwargs: Any,
) -> None:
    """Log a health check result"""
    logger = get_logger("health.check")
    logger.info(
        "health_check_completed",
        service=service,
        status=status,
        duration_ms=duration_ms,
        **kwargs,
    )
