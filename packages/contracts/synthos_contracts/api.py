"""API response and error contract definitions"""

from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field
from enum import Enum


class ErrorCode(str, Enum):
    """Standard error codes for the Synthos-OS platform"""

    # General errors
    INTERNAL_ERROR = "INTERNAL_ERROR"
    INVALID_REQUEST = "INVALID_REQUEST"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"
    RATE_LIMITED = "RATE_LIMITED"

    # AI/Model errors
    MODEL_UNAVAILABLE = "MODEL_UNAVAILABLE"
    MODEL_TIMEOUT = "MODEL_TIMEOUT"
    MODEL_VALIDATION_FAILED = "MODEL_VALIDATION_FAILED"
    MODEL_RATE_LIMITED = "MODEL_RATE_LIMITED"

    # Memory/Retrieval errors
    MEMORY_NOT_FOUND = "MEMORY_NOT_FOUND"
    RETRIEVAL_FAILED = "RETRIEVAL_FAILED"
    CONTEXT_EXCEEDED = "CONTEXT_EXCEEDED"

    # Workflow/Tool errors
    TOOL_NOT_FOUND = "TOOL_NOT_FOUND"
    TOOL_EXECUTION_FAILED = "TOOL_EXECUTION_FAILED"
    TOOL_PERMISSION_DENIED = "TOOL_PERMISSION_DENIED"
    WORKFLOW_INVALID_STATE = "WORKFLOW_INVALID_STATE"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    APPROVAL_DENIED = "APPROVAL_DENIED"

    # Security errors
    PERMISSION_DENIED = "PERMISSION_DENIED"
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    POLICY_VIOLATION = "POLICY_VIOLATION"
    INPUT_VALIDATION_FAILED = "INPUT_VALIDATION_FAILED"


class ErrorDetail(BaseModel):
    """Detailed error information"""

    code: ErrorCode
    message: str
    field: str | None = None
    context: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    """Standard error response format"""

    error: ErrorDetail
    request_id: str | None = None
    timestamp: str


T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper"""

    success: bool
    data: T | None = None
    error: ErrorDetail | None = None
    request_id: str | None = None
    timestamp: str


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper"""

    items: list[T]
    total: int
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)
    total_pages: int
    has_next: bool
    has_previous: bool
