"""Synthos RSI Engine - Recursive Self-Improvement Engine"""

__version__ = "0.1.0"

from .core.coordinator import RSICoordinator
from .core.state_manager import StateManager
from .safety.gatekeeper import Gatekeeper
from .safety.goal_drift_index import GoalDriftIndex
from .mutation.generator import MutationGenerator
from .evaluation.benchmark_runner import BenchmarkRunner
from .governance.proposal_manager import ProposalManager
from .governance.audit_logger import AuditLogger

__all__ = [
    "RSICoordinator",
    "StateManager",
    "Gatekeeper",
    "GoalDriftIndex",
    "MutationGenerator",
    "BenchmarkRunner",
    "ProposalManager",
    "AuditLogger",
]
