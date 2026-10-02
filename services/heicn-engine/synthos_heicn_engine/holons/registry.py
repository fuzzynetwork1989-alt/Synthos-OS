"""
Holon Registry - Central registry for all holons in the HEICN system

The Holon Registry maintains a catalog of all available holons, their capabilities,
and provides discovery and routing services for the HEICN architecture.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
import structlog
from datetime import datetime
import asyncio

from .base import BaseHolon, HolonType, HolonStatus

logger = structlog.get_logger(__name__)


@dataclass
class HolonRegistration:
    """Information about a registered holon"""
    holon_id: str
    holon_type: HolonType
    name: str
    description: str
    capabilities: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    status: HolonStatus = HolonStatus.INITIALIZING
    registered_at: datetime = field(default_factory=datetime.now)
    last_heartbeat: Optional[datetime] = None
    health_status: str = "unknown"
    version: str = "1.0"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ServiceDiscoveryResult:
    """Result of a service discovery query"""
    query: str
    results: List[HolonRegistration] = field(default_factory=list)
    total: int = 0
    exact_matches: List[HolonRegistration] = field(default_factory=list)
    partial_matches: List[HolonRegistration] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


class HolonRegistry:
    """
    Central registry for all holons in the HEICN system.
    
    The registry provides:
    - Holon registration and deregistration
    - Capability discovery and lookup
    - Health monitoring
    - Dependency resolution
    - Service routing
    """
    
    def __init__(self):
        """Initialize the holon registry"""
        # Holon storage
        self._holons: Dict[str, HolonRegistration] = {}
        self._holon_by_type: Dict[HolonType, List[str]] = {
            HolonType.COGNITIVE: [],
            HolonType.SERVICE: [],
            HolonType.INTERFACE: [],
            HolonType.INTEGRATION: []
        }
        
        # Capability index
        self._capabilities: Dict[str, List[str]] = {}  # capability -> [holon_ids]
        self._holon_capabilities: Dict[str, List[str]] = {}  # holon_id -> [capabilities]
        
        # Dependency graph
        self._dependencies: Dict[str, List[str]] = {}  # holon_id -> [dependency_ids]
        self._dependents: Dict[str, List[str]] = {}  # holon_id -> [dependent_ids]
        
        # Health tracking
        self._health_status: Dict[str, str] = {}  # holon_id -> health_status
        
        # Lock for thread-safe operations
        self._lock = asyncio.Lock()
        
        logger.info("HolonRegistry initialized")
    
    async def register_holon(
        self,
        holon: BaseHolon,
        version: str = "1.0",
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Register a holon with the registry.
        
        Args:
            holon: The holon instance to register
            version: Version string
            metadata: Additional metadata
            
        Returns:
            Holon ID
        """
        async with self._lock:
            holon_id = holon.holon_id
            
            # Create registration
            registration = HolonRegistration(
                holon_id=holon_id,
                holon_type=holon.holon_type,
                name=holon.name,
                description=holon.description,
                capabilities=list(holon.get_capabilities().keys()),
                dependencies=[dep.holon_id for dep in holon.get_dependencies()],
                status=holon.status,
                registered_at=datetime.now(),
                version=version,
                metadata=metadata or {}
            )
            
            # Store registration
            self._holons[holon_id] = registration
            self._holon_by_type[holon.holon_type].append(holon_id)
            
            # Index capabilities
            for capability in registration.capabilities:
                if capability not in self._capabilities:
                    self._capabilities[capability] = []
                if holon_id not in self._capabilities[capability]:
                    self._capabilities[capability].append(holon_id)
            
            self._holon_capabilities[holon_id] = registration.capabilities
            
            # Build dependency graph
            self._dependencies[holon_id] = registration.dependencies
            for dep_id in registration.dependencies:
                if dep_id not in self._dependents:
                    self._dependents[dep_id] = []
                if holon_id not in self._dependents[dep_id]:
                    self._dependents[dep_id].append(holon_id)
            
            # Track health
            self._health_status[holon_id] = "healthy"
            
            logger.info(
                "Holon registered",
                holon_id=holon_id,
                holon_type=holon.holon_type.value,
                name=holon.name,
                capabilities=len(registration.capabilities)
            )
            
            return holon_id
    
    async def deregister_holon(self, holon_id: str) -> bool:
        """
        Deregister a holon from the registry.
        
        Args:
            holon_id: Holon identifier
            
        Returns:
            True if deregistered successfully
        """
        async with self._lock:
            if holon_id not in self._holons:
                logger.warning("Holon not found for deregistration", holon_id=holon_id)
                return False
            
            registration = self._holons[holon_id]
            
            # Remove from type index
            if holon_id in self._holon_by_type[registration.holon_type]:
                self._holon_by_type[registration.holon_type].remove(holon_id)
            
            # Remove from capability index
            for capability in registration.capabilities:
                if capability in self._capabilities and holon_id in self._capabilities[capability]:
                    self._capabilities[capability].remove(holon_id)
                    if not self._capabilities[capability]:
                        del self._capabilities[capability]
            
            # Remove from capability tracking
            if holon_id in self._holon_capabilities:
                del self._holon_capabilities[holon_id]
            
            # Remove from dependency graph
            if holon_id in self._dependencies:
                for dep_id in self._dependencies[holon_id]:
                    if dep_id in self._dependents and holon_id in self._dependents[dep_id]:
                        self._dependents[dep_id].remove(holon_id)
                        if not self._dependents[dep_id]:
                            del self._dependents[dep_id]
                del self._dependencies[holon_id]
            
            # Remove dependents
            if holon_id in self._dependents:
                del self._dependents[holon_id]
            
            # Remove health tracking
            if holon_id in self._health_status:
                del self._health_status[holon_id]
            
            # Remove registration
            del self._holons[holon_id]
            
            logger.info("Holon deregistered", holon_id=holon_id)
            return True
    
    async def update_holon_status(
        self,
        holon_id: str,
        status: HolonStatus,
        health_status: Optional[str] = None
    ) -> bool:
        """
        Update the status of a registered holon.
        
        Args:
            holon_id: Holon identifier
            status: New status
            health_status: Optional new health status
            
        Returns:
            True if updated successfully
        """
        async with self._lock:
            if holon_id not in self._holons:
                return False
            
            self._holons[holon_id].status = status
            self._holons[holon_id].last_heartbeat = datetime.now()
            
            if health_status:
                self._health_status[holon_id] = health_status
                self._holons[holon_id].health_status = health_status
            
            logger.info(
                "Holon status updated",
                holon_id=holon_id,
                status=status.value,
                health=health_status
            )
            return True
    
    async def get_holon(self, holon_id: str) -> Optional[HolonRegistration]:
        """
        Get information about a registered holon.
        
        Args:
            holon_id: Holon identifier
            
        Returns:
            Holon registration or None if not found
        """
        async with self._lock:
            return self._holons.get(holon_id)
    
    async def list_holons(
        self,
        holon_type: Optional[HolonType] = None,
        status: Optional[HolonStatus] = None
    ) -> List[HolonRegistration]:
        """
        List registered holons with optional filtering.
        
        Args:
            holon_type: Optional type filter
            status: Optional status filter
            
        Returns:
            List of holon registrations
        """
        async with self._lock:
            holons = list(self._holons.values())
            
            if holon_type:
                holons = [h for h in holons if h.holon_type == holon_type]
            
            if status:
                holons = [h for h in holons if h.status == status]
            
            return holons
    
    async def discover_capabilities(
        self,
        capability: str,
        exact_match: bool = False
    ) -> ServiceDiscoveryResult:
        """
        Discover holons that provide a specific capability.
        
        Args:
            capability: Capability to search for
            exact_match: Whether to require exact match
            
        Returns:
            Service discovery result
        """
        async with self._lock:
            results = []
            exact_matches = []
            partial_matches = []
            
            if capability in self._capabilities:
                for holon_id in self._capabilities[capability]:
                    if holon_id in self._holons:
                        exact_matches.append(self._holons[holon_id])
            
            # If no exact matches, try partial matching
            if not exact_matches or not exact_match:
                for cap, holon_ids in self._capabilities.items():
                    if capability.lower() in cap.lower() or cap.lower() in capability.lower():
                        for holon_id in holon_ids:
                            if holon_id in self._holons:
                                partial_match = self._holons[holon_id]
                                if partial_match not in exact_matches:
                                    partial_matches.append(partial_match)
            
            results = exact_matches + partial_matches
            
            return ServiceDiscoveryResult(
                query=capability,
                results=results,
                total=len(results),
                exact_matches=exact_matches,
                partial_matches=partial_matches
            )
    
    async def discover_by_type(self, holon_type: HolonType) -> List[HolonRegistration]:
        """
        Discover holons of a specific type.
        
        Args:
            holon_type: Type of holons to find
            
        Returns:
            List of holon registrations
        """
        async with self._lock:
            holon_ids = self._holon_by_type.get(holon_type, [])
            return [self._holons[hid] for hid in holon_ids if hid in self._holons]
    
    async def get_dependencies(self, holon_id: str, recursive: bool = False) -> List[str]:
        """
        Get dependencies for a holon.
        
        Args:
            holon_id: Holon identifier
            recursive: Whether to get all recursive dependencies
            
        Returns:
            List of dependency IDs
        """
        async with self._lock:
            if holon_id not in self._dependencies:
                return []
            
            if not recursive:
                return self._dependencies[holon_id]
            
            # Get recursive dependencies
            all_deps = set()
            stack = list(self._dependencies[holon_id])
            
            while stack:
                dep_id = stack.pop()
                if dep_id not in all_deps:
                    all_deps.add(dep_id)
                    if dep_id in self._dependencies:
                        stack.extend(self._dependencies[dep_id])
            
            return list(all_deps)
    
    async def get_dependents(self, holon_id: str, recursive: bool = False) -> List[str]:
        """
        Get holons that depend on a specific holon.
        
        Args:
            holon_id: Holon identifier
            recursive: Whether to get all recursive dependents
            
        Returns:
            List of dependent holon IDs
        """
        async with self._lock:
            if holon_id not in self._dependents:
                return []
            
            if not recursive:
                return self._dependents[holon_id]
            
            # Get recursive dependents
            all_dependents = set()
            stack = list(self._dependents[holon_id])
            
            while stack:
                dep_id = stack.pop()
                if dep_id not in all_dependents:
                    all_dependents.add(dep_id)
                    if dep_id in self._dependents:
                        stack.extend(self._dependents[dep_id])
            
            return list(all_dependents)
    
    async def check_dependency_chain(self, holon_id: str) -> Dict[str, Any]:
        """
        Check the dependency chain for a holon.
        
        Args:
            holon_id: Holon identifier
            
        Returns:
            Dictionary with dependency chain information
        """
        async with self._lock:
            dependencies = await self.get_dependencies(holon_id, recursive=True)
            
            # Check status of all dependencies
            missing = []
            failed = []
            degraded = []
            healthy = []
            
            for dep_id in dependencies:
                if dep_id not in self._holons:
                    missing.append(dep_id)
                else:
                    holon = self._holons[dep_id]
                    if holon.status == HolonStatus.FAILED:
                        failed.append(dep_id)
                    elif holon.status == HolonStatus.DEGRADED:
                        degraded.append(dep_id)
                    elif holon.status in [HolonStatus.READY, HolonStatus.ACTIVE]:
                        healthy.append(dep_id)
            
            return {
                "holon_id": holon_id,
                "total_dependencies": len(dependencies),
                "missing": missing,
                "failed": failed,
                "degraded": degraded,
                "healthy": healthy,
                "ready": len(missing) == 0 and len(failed) == 0
            }
    
    async def route_to_capability(
        self,
        capability: str,
        task: Dict,
        context: Optional[Dict] = None
    ) -> Any:
        """
        Route a task to a holon that provides the specified capability.
        
        Args:
            capability: Required capability
            task: Task to execute
            context: Optional context
            
        Returns:
            Result from the holon or error
        """
        # Discover holons with this capability
        result = await self.discover_capabilities(capability)
        
        if not result.results:
            return {"error": f"No holon provides capability: {capability}"}
        
        # For now, just pick the first available holon
        # In a real implementation, this would use load balancing, etc.
        for holon_reg in result.results:
            if holon_reg.status in [HolonStatus.READY, HolonStatus.ACTIVE]:
                # In a real implementation, we would actually call the holon
                # For now, we just return a simulated result
                return {
                    "status": "routed",
                    "holon_id": holon_reg.holon_id,
                    "capability": capability,
                    "task": task,
                    "result": f"Simulated result from {holon_reg.holon_id}"
                }
        
        return {"error": f"No available holon provides capability: {capability}"}
    
    async def get_health_status(self, holon_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get health status for holons.
        
        Args:
            holon_id: Optional specific holon ID
            
        Returns:
            Health status information
        """
        async with self._lock:
            if holon_id:
                if holon_id in self._health_status:
                    return {
                        "holon_id": holon_id,
                        "health": self._health_status[holon_id],
                        "status": self._holons.get(holon_id, {}).get("status", "unknown")
                    }
                else:
                    return {"error": f"Holon not found: {holon_id}"}
            
            # Return all health statuses
            return {
                "all_holons": {
                    hid: {
                        "health": self._health_status.get(hid, "unknown"),
                        "status": self._holons.get(hid, {}).get("status", "unknown").value if hid in self._holons else "unknown"
                    }
                    for hid in self._holons
                }
            }
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get registry statistics.
        
        Returns:
            Statistics about registered holons
        """
        async with self._lock:
            return {
                "total_holons": len(self._holons),
                "by_type": {
                    ht.value: len(ids)
                    for ht, ids in self._holon_by_type.items()
                },
                "total_capabilities": len(self._capabilities),
                "by_status": {
                    status.value: len([h for h in self._holons.values() if h.status == status])
                    for status in HolonStatus
                },
                "health_summary": {
                    "healthy": len([h for h in self._health_status.values() if h == "healthy"]),
                    "unhealthy": len([h for h in self._health_status.values() if h != "healthy"])
                }
            }
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the registry"""
        return {
            "registry_type": "HolonRegistry",
            "total_holons": len(self._holons),
            "total_capabilities": len(self._capabilities),
            "by_type": {ht.value: len(ids) for ht, ids in self._holon_by_type.items()}
        }
