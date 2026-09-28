"""
Base Holon - Foundation for all holonic modules in HEICN

This module defines the base holon class that all specialized holons inherit from.
It provides core capabilities for autonomous operation, self-healing, and cooperation.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import structlog
from datetime import datetime, timedelta
import asyncio
import uuid
import hashlib

logger = structlog.get_logger(__name__)


class HolonType(Enum):
    """Types of holons in the HEICN architecture"""
    COGNITIVE = "cognitive"           # AI reasoning, planning, memory modules
    SERVICE = "service"               # Infrastructure: data, communication, storage
    INTERFACE = "interface"           # User interaction modules
    INTEGRATION = "integration"       # External system connectors


class HolonStatus(Enum):
    """Operational status of a holon"""
    INITIALIZING = "initializing"
    READY = "ready"
    ACTIVE = "active"
    DEGRADED = "degraded"
    FAILED = "failed"
    RECOVERING = "recovering"
    MAINTENANCE = "maintenance"


class HealthStatus(Enum):
    """Health status for self-healing"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class HolonCapability:
    """A capability that a holon can provide"""
    name: str
    description: str
    version: str = "1.0"
    parameters: Dict[str, Any] = field(default_factory=dict)
    quality_score: float = 1.0  # 0.0 to 1.0
    last_validated: Optional[datetime] = None


@dataclass
class HolonDependency:
    """A dependency on another holon"""
    holon_id: str
    capability: str
    required: bool = True
    priority: int = 1  # 1 = critical, 5 = optional


@dataclass
class HealthCheckResult:
    """Result of a health check"""
    timestamp: datetime
    status: HealthStatus
    checks: Dict[str, bool] = field(default_factory=dict)
    message: Optional[str] = None
    recovery_actions: List[str] = field(default_factory=list)


class BaseHolon(ABC):
    """
    Base class for all holons in HEICN.
    
    Provides core functionality:
    - Lifecycle management
    - Health monitoring and self-healing
    - Capability registration and discovery
    - Cooperation protocols
    - Performance tracking
    """
    
    def __init__(
        self,
        holon_id: Optional[str] = None,
        holon_type: HolonType = HolonType.COGNITIVE,
        name: str = "BaseHolon",
        description: str = "",
        config: Optional[Dict] = None
    ):
        """
        Initialize the base holon.
        
        Args:
            holon_id: Unique identifier for this holon
            holon_type: Type of holon (Cognitive, Service, Interface, Integration)
            name: Human-readable name
            description: Description of holon's purpose
            config: Configuration dictionary
        """
        self.holon_id = holon_id or str(uuid.uuid4())
        self.holon_type = holon_type
        self.name = name
        self.description = description
        self.config = config or {}
        
        # Lifecycle state
        self._status = HolonStatus.INITIALIZING
        self._initialized_at: Optional[datetime] = None
        self._started_at: Optional[datetime] = None
        
        # Capabilities
        self._capabilities: Dict[str, HolonCapability] = {}
        self._provided_capabilities: List[str] = []
        
        # Dependencies
        self._dependencies: List[HolonDependency] = []
        
        # Health monitoring
        self._health_status = HealthStatus.HEALTHY
        self._last_health_check: Optional[datetime] = None
        self._health_check_interval = timedelta(seconds=30)
        
        # Performance tracking
        self._performance_metrics: Dict[str, List[float]] = field(default_factory=dict)
        self._performance_scores: Dict[str, float] = field(default_factory=dict)
        
        # Cooperation
        self._cooperation_partners: Dict[str, Dict] = {}  # holon_id -> cooperation data
        
        # Recovery
        self._recovery_attempts: int = 0
        self._recovery_strategies: List[Callable] = []
        
        # Register default recovery strategies
        self._register_default_recovery_strategies()
        
        logger.info(
            "Holon initialized",
            holon_id=self.holon_id,
            holon_type=self.holon_type.value,
            name=self.name
        )
    
    def _register_default_recovery_strategies(self):
        """Register default recovery strategies"""
        self._recovery_strategies = [
            self._recovery_restart,
            self._recovery_reinitialize,
            self._recovery_degrade_functionality,
        ]
    
    @property
    def status(self) -> HolonStatus:
        """Current status of the holon"""
        return self._status
    
    @property
    def is_healthy(self) -> bool:
        """Check if holon is healthy"""
        return self._health_status == HealthStatus.HEALTHY
    
    @property
    def is_available(self) -> bool:
        """Check if holon is available for tasks"""
        return self._status in [HolonStatus.READY, HolonStatus.ACTIVE]
    
    @abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the holon. Must be implemented by subclasses.
        
        Returns:
            True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def start(self) -> bool:
        """
        Start the holon's main operation. Must be implemented by subclasses.
        
        Returns:
            True if start successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def stop(self) -> bool:
        """
        Stop the holon gracefully. Must be implemented by subclasses.
        
        Returns:
            True if stop successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def execute(self, task: Dict, context: Optional[Dict] = None) -> Any:
        """
        Execute a task. Must be implemented by subclasses.
        
        Args:
            task: Task description dictionary
            context: Optional context dictionary
            
        Returns:
            Result of task execution
        """
        pass
    
    def register_capability(
        self,
        name: str,
        description: str,
        version: str = "1.0",
        parameters: Optional[Dict] = None,
        quality_score: float = 1.0
    ) -> str:
        """
        Register a capability that this holon provides.
        
        Args:
            name: Capability name
            description: Description of capability
            version: Version string
            parameters: Parameter schema
            quality_score: Quality score (0.0 to 1.0)
            
        Returns:
            Capability ID
        """
        capability_id = f"{self.holon_id}:{name}"
        capability = HolonCapability(
            name=name,
            description=description,
            version=version,
            parameters=parameters or {},
            quality_score=quality_score,
            last_validated=datetime.now()
        )
        self._capabilities[capability_id] = capability
        self._provided_capabilities.append(name)
        
        logger.info(
            "Capability registered",
            holon_id=self.holon_id,
            capability=capability_id
        )
        
        return capability_id
    
    def add_dependency(
        self,
        holon_id: str,
        capability: str,
        required: bool = True,
        priority: int = 1
    ):
        """
        Add a dependency on another holon.
        
        Args:
            holon_id: ID of the holon this depends on
            capability: Required capability name
            required: Whether this dependency is required
            priority: Priority level (1-5)
        """
        dependency = HolonDependency(
            holon_id=holon_id,
            capability=capability,
            required=required,
            priority=priority
        )
        self._dependencies.append(dependency)
        
        logger.info(
            "Dependency added",
            holon_id=self.holon_id,
            depends_on=holon_id,
            capability=capability
        )
    
    def get_capabilities(self) -> Dict[str, HolonCapability]:
        """Get all capabilities provided by this holon"""
        return self._capabilities.copy()
    
    def get_dependencies(self) -> List[HolonDependency]:
        """Get all dependencies of this holon"""
        return self._dependencies.copy()
    
    async def check_health(self) -> HealthCheckResult:
        """
        Perform health check on this holon.
        
        Returns:
            HealthCheckResult with status and details
        """
        result = HealthCheckResult(
            timestamp=datetime.now(),
            status=HealthStatus.HEALTHY,
            message="Health check completed"
        )
        
        # Check basic status
        if self._status == HolonStatus.FAILED:
            result.status = HealthStatus.CRITICAL
            result.message = "Holon in failed state"
            result.recovery_actions.append("restart")
            return result
        
        # Check dependencies
        for dep in self._dependencies:
            if dep.required:
                # In a real implementation, we'd check the actual dependency
                result.checks[f"dep:{dep.holon_id}"] = True  # Placeholder
        
        # Check performance metrics
        for metric_name, values in self._performance_metrics.items():
            if values:
                avg = sum(values) / len(values)
                # Simple threshold check
                if avg < 0.3:
                    result.status = HealthStatus.CRITICAL
                    result.checks[f"perf:{metric_name}"] = False
                    result.recovery_actions.append(f"investigate_{metric_name}")
                elif avg < 0.7:
                    result.status = HealthStatus.WARNING
                    result.checks[f"perf:{metric_name}"] = False
        
        self._last_health_check = datetime.now()
        self._health_status = result.status
        
        return result
    
    async def perform_self_healing(self) -> bool:
        """
        Perform self-healing based on current health status.
        
        Returns:
            True if healing successful, False otherwise
        """
        health = await self.check_health()
        
        if health.status == HealthStatus.HEALTHY:
            logger.info("Holon is healthy, no healing needed", holon_id=self.holon_id)
            return True
        
        logger.warning(
            "Performing self-healing",
            holon_id=self.holon_id,
            status=health.status.value
        )
        
        # Try recovery strategies in order
        for strategy in self._recovery_strategies:
            try:
                if await strategy():
                    self._recovery_attempts += 1
                    new_health = await self.check_health()
                    if new_health.status == HealthStatus.HEALTHY:
                        logger.info(
                            "Self-healing successful",
                            holon_id=self.holon_id,
                            strategy=strategy.__name__
                        )
                        return True
            except Exception as e:
                logger.error(
                    "Recovery strategy failed",
                    holon_id=self.holon_id,
                    strategy=strategy.__name__,
                    error=str(e)
                )
        
        # If all strategies failed
        logger.error("All self-healing strategies failed", holon_id=self.holon_id)
        self._status = HolonStatus.FAILED
        return False
    
    async def _recovery_restart(self) -> bool:
        """Recovery strategy: Restart the holon"""
        logger.info("Attempting restart recovery", holon_id=self.holon_id)
        await self.stop()
        await asyncio.sleep(1)
        success = await self.start()
        return success
    
    async def _recovery_reinitialize(self) -> bool:
        """Recovery strategy: Reinitialize the holon"""
        logger.info("Attempting reinitialize recovery", holon_id=self.holon_id)
        await self.stop()
        await asyncio.sleep(1)
        success = await self.initialize()
        if success:
            success = await self.start()
        return success
    
    async def _recovery_degrade_functionality(self) -> bool:
        """Recovery strategy: Degrade to minimal functionality"""
        logger.info("Attempting degrade functionality recovery", holon_id=self.holon_id)
        self._status = HolonStatus.DEGRADED
        # In a real implementation, we'd reduce functionality
        return True
    
    def record_performance(self, metric: str, value: float):
        """
        Record a performance metric.
        
        Args:
            metric: Metric name
            value: Metric value (0.0 to 1.0 recommended)
        """
        if metric not in self._performance_metrics:
            self._performance_metrics[metric] = []
        
        self._performance_metrics[metric].append(value)
        
        # Keep only last 100 values
        if len(self._performance_metrics[metric]) > 100:
            self._performance_metrics[metric] = self._performance_metrics[metric][-100:]
        
        # Update score (simple average)
        if self._performance_metrics[metric]:
            self._performance_scores[metric] = sum(self._performance_metrics[metric]) / len(self._performance_metrics[metric])
    
    def get_performance_score(self, metric: str) -> Optional[float]:
        """Get the current performance score for a metric"""
        return self._performance_scores.get(metric)
    
    async def cooperate(self, holon_id: str, task: Dict) -> Any:
        """
        Cooperate with another holon on a task.
        
        Args:
            holon_id: ID of the holon to cooperate with
            task: Task to perform
            
        Returns:
            Result of cooperation
        """
        # In a real implementation, this would use the holon registry
        # to find and communicate with the other holon
        logger.info(
            "Cooperation requested",
            holon_id=self.holon_id,
            with_holon=holon_id,
            task=task
        )
        
        # For now, return a placeholder
        return {
            "status": "cooperation_initiated",
            "holons": [self.holon_id, holon_id],
            "task": task
        }
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about this holon"""
        return {
            "holon_id": self.holon_id,
            "type": self.holon_type.value,
            "name": self.name,
            "description": self.description,
            "status": self._status.value,
            "health_status": self._health_status.value,
            "capabilities": list(self._capabilities.keys()),
            "dependencies": [
                {"holon_id": d.holon_id, "capability": d.capability, "required": d.required}
                for d in self._dependencies
            ],
            "performance": self._performance_scores,
            "initialized_at": self._initialized_at.isoformat() if self._initialized_at else None,
            "started_at": self._started_at.isoformat() if self._started_at else None,
            "last_health_check": self._last_health_check.isoformat() if self._last_health_check else None,
        }
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.holon_id} type={self.holon_type.value} status={self._status.value}>"
