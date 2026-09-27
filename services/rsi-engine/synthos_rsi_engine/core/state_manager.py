"""State Manager - System state and versioning for RSI"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import structlog

logger = structlog.get_logger(__name__)


class SystemState(Enum):
    """System states for RSI"""
    IDLE = "idle"
    IMPROVING = "improving"
    TESTING = "testing"
    VALIDATING = "validating"
    APPROVING = "approving"
    APPLYING = "applying"
    ERROR = "error"


@dataclass
class SystemVersion:
    """System version information"""
    version: str
    timestamp: str
    git_commit: str
    changes: List[str]
    performance_metrics: Dict


class StateManager:
    """
    Manage system state and versioning for RSI
    
    Tracks system state, versions, and ensures rollback capability
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize state manager
        
        Args:
            config: Configuration for state manager
        """
        self.config = config or self._default_config()
        
        self.current_state = SystemState.IDLE
        self.current_version = SystemVersion(
            version="0.1.0",
            timestamp=self._get_timestamp(),
            git_commit="initial",
            changes=[],
            performance_metrics={}
        )
        
        self.version_history: List[SystemVersion] = [self.current_version]
        
        logger.info("State Manager initialized", initial_version=self.current_version.version)
    
    def _default_config(self) -> Dict:
        """Default configuration for state manager"""
        return {
            "max_history_size": 100,
            "auto_backup": True,
        }
    
    def set_state(self, new_state: SystemState):
        """
        Set system state
        
        Args:
            new_state: New system state
        """
        logger.info("State changed", from_state=self.current_state.value, to_state=new_state.value)
        self.current_state = new_state
    
    def get_state(self) -> SystemState:
        """Get current system state"""
        return self.current_state
    
    def create_version(
        self,
        changes: List[str],
        performance_metrics: Dict
    ) -> SystemVersion:
        """
        Create a new system version
        
        Args:
            changes: List of changes in this version
            performance_metrics: Performance metrics for this version
            
        Returns:
            New SystemVersion object
        """
        # Increment version
        version_parts = self.current_version.version.split(".")
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        new_version = ".".join(version_parts)
        
        # Create new version
        new_system_version = SystemVersion(
            version=new_version,
            timestamp=self._get_timestamp(),
            git_commit=self._get_git_commit(),
            changes=changes,
            performance_metrics=performance_metrics
        )
        
        # Update current version
        self.current_version = new_system_version
        self.version_history.append(new_system_version)
        
        # Trim history if needed
        if len(self.version_history) > self.config["max_history_size"]:
            self.version_history = self.version_history[-self.config["max_history_size"]:]
        
        logger.info(
            "New version created",
            version=new_version,
            changes_count=len(changes)
        )
        
        return new_system_version
    
    def rollback_to_version(self, version: str) -> bool:
        """
        Rollback to a previous version
        
        Args:
            version: Version to rollback to
            
        Returns:
            True if rollback successful
        """
        # Find version in history
        target_version = None
        for v in self.version_history:
            if v.version == version:
                target_version = v
                break
        
        if not target_version:
            logger.error("Version not found in history", version=version)
            return False
        
        # Perform rollback
        logger.info("Rolling back to version", version=version)
        
        # In production, this would:
        # - Checkout git commit
        # - Restore state
        # - Reapply configuration
        
        self.current_version = target_version
        
        return True
    
    def get_version_history(self) -> List[SystemVersion]:
        """Get version history"""
        return self.version_history
    
    def get_current_version(self) -> SystemVersion:
        """Get current version"""
        return self.current_version
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat()
    
    def _get_git_commit(self) -> str:
        """Get current git commit"""
        # Placeholder for git commit retrieval
        # In production, this would use gitpython
        return "unknown"
