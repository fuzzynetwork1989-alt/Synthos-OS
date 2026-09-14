"""Domain models for Synthos-OS"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal
from synthos_contracts.types import (
    UserId,
    TaskId,
    MemoryId,
    DocumentId,
    ToolId,
    WorkflowId,
    MemoryType,
    TaskState,
    RiskTier,
    ApprovalState,
)


class MemoryRecord(BaseModel):
    """Base memory record"""

    id: MemoryId
    owner_id: UserId
    memory_type: MemoryType
    content: str
    source: str | None = None
    confidence: float | None = Field(None, ge=0.0, le=1.0)
    metadata: dict = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
    access_classification: str = "private"
    retention_policy: str = "default"


class DocumentRecord(BaseModel):
    """Document record for ingestion and retrieval"""

    id: DocumentId
    owner_id: UserId
    title: str
    content: str
    content_hash: str
    mime_type: str
    metadata: dict = Field(default_factory=dict)
    source_uri: str | None = None
    created_at: datetime
    updated_at: datetime
    access_classification: str = "private"


class ToolDefinition(BaseModel):
    """Tool definition for the tool registry"""

    id: ToolId
    name: str
    version: str
    description: str
    input_schema: dict
    output_schema: dict
    required_permissions: list[str] = Field(default_factory=list)
    risk_tier: RiskTier
    timeout: int = Field(gt=0)
    retry_policy: dict = Field(default_factory=dict)
    network_requirements: list[str] = Field(default_factory=list)
    audit_fields: list[str] = Field(default_factory=list)
    rollback_capability: bool = False
    owner_service: str
    enabled: bool = True


class TaskStep(BaseModel):
    """Individual step in a workflow"""

    step_id: str
    description: str
    layer: str
    requires_tool: bool = False
    requires_approval: bool = False
    risk_tier: RiskTier = RiskTier.READ_ONLY
    status: TaskState = TaskState.DRAFT
    result: dict | None = None
    error: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class Workflow(BaseModel):
    """Workflow definition and state"""

    id: WorkflowId
    user_id: UserId
    goal: str
    steps: list[TaskStep] = Field(default_factory=list)
    state: TaskState = TaskState.DRAFT
    approval_state: ApprovalState = ApprovalState.NONE
    created_at: datetime
    updated_at: datetime
    context: dict = Field(default_factory=dict)
    metadata: dict = Field(default_factory=dict)
