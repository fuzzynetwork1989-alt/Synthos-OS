"""Common type definitions for Synthos-OS"""

from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum


class LayerId(str, Enum):
    """21 AI OS Architecture Layers"""

    PERCEPTION = "perception"
    IDENTITY = "identity"
    MEMORY = "memory"
    RETRIEVAL = "retrieval"
    CONTEXT_ASSEMBLY = "context_assembly"
    WORLD_MODELING = "world_modeling"
    REASONING = "reasoning"
    PLANNING = "planning"
    TOOL_ROUTING = "tool_routing"
    TASK_EXECUTION = "task_execution"
    ORCHESTRATION = "orchestration"
    PERMISSIONS = "permissions"
    GOVERNANCE = "governance"
    SAFETY = "safety"
    OBSERVABILITY = "observability"
    EVALUATION = "evaluation"
    PERSISTENCE = "persistence"
    SYNCHRONIZATION = "synchronization"
    USER_INTERFACE = "user_interface"
    DEPLOYMENT = "deployment"
    ONGOING_LEARNING = "ongoing_learning"


class UserId(str):
    """User identifier"""


class TaskId(str):
    """Task identifier"""


class MemoryId(str):
    """Memory identifier"""


class DocumentId(str):
    """Document identifier"""


class ToolId(str):
    """Tool identifier"""


class WorkflowId(str):
    """Workflow identifier"""


class RiskTier(int, Enum):
    """Tool risk classification"""

    READ_ONLY = 0
    REVERSIBLE_WRITE = 1
    IRREVERSIBLE_WRITE = 2
    HIGH_IMPACT = 3


class ApprovalState(str, Enum):
    """Approval workflow states"""

    NONE = "none"
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"


class MemoryType(str, Enum):
    """Memory type classification"""

    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"


class TaskState(str, Enum):
    """Workflow task states"""

    DRAFT = "draft"
    AWAITING_CLARIFICATION = "awaiting_clarification"
    AWAITING_APPROVAL = "awaiting_approval"
    QUEUED = "queued"
    RUNNING = "running"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ROLLED_BACK = "rolled_back"
