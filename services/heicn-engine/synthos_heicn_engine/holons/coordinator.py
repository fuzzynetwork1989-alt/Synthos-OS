"""
Holon Coordinator - Coordinates holon interactions and task delegation

The Holon Coordinator is responsible for:
- Managing holon lifecycle
- Coordinating task delegation
- Handling inter-holon communication
- Monitoring system health
- Optimizing resource allocation
"""

from typing import Dict, List, Optional, Any, Callable, Coroutine
from dataclasses import dataclass, field
from enum import Enum
import structlog
from datetime import datetime
import asyncio

from .base import BaseHolon, HolonType, HolonStatus
from .registry import HolonRegistry

logger = structlog.get_logger(__name__)


class TaskPriority(Enum):
    """Priority levels for tasks"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    BACKGROUND = 1


class TaskStatus(Enum):
    """Status of a task"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """A task to be executed by holons"""
    task_id: str
    capability: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    retries: int = 0
    max_retries: int = 3


@dataclass
class Workflow:
    """A workflow consisting of multiple tasks"""
    workflow_id: str
    name: str
    description: str = ""
    tasks: List[Task] = field(default_factory=list)
    dependencies: Dict[str, List[str]] = field(default_factory=dict)  # task_id -> [dependency_ids]
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: float = 0.0  # 0.0 to 1.0


@dataclass
class OptimizationStrategy:
    """Strategy for optimizing holon operations"""
    name: str
    description: str
    weight: float = 1.0  # 0.0 to 1.0
    enabled: bool = True


class HolonCoordinator:
    """
    Holon Coordinator - Manages holon interactions and task delegation.
    
    The coordinator is the central manager for the HEICN holonic architecture,
    responsible for:
    - Registering and tracking holons
    - Delegating tasks to appropriate holons
    - Managing workflows
    - Optimizing system performance
    - Handling failures and retries
    """
    
    def __init__(self, registry: Optional[HolonRegistry] = None):
        """
        Initialize the holon coordinator.
        
        Args:
            registry: Optional holon registry (creates new if not provided)
        """
        self.registry = registry or HolonRegistry()
        
        # Task management
        self._tasks: Dict[str, Task] = {}
        self._task_queue: Dict[str, List[Task]] = {}  # priority -> [tasks]
        self._pending_tasks: List[Task] = []
        self._in_progress_tasks: Dict[str, Task] = {}  # task_id -> task
        
        # Workflow management
        self._workflows: Dict[str, Workflow] = {}
        
        # Holon instances
        self._holons: Dict[str, BaseHolon] = {}
        
        # Performance tracking
        self._task_count: int = 0
        self._completed_count: int = 0
        self._failed_count: int = 0
        self._average_latency: float = 0.0
        
        # Optimization strategies
        self._optimization_strategies: Dict[str, OptimizationStrategy] = {}
        
        # Lock for thread-safe operations
        self._lock = asyncio.Lock()
        
        # Event callbacks
        self._event_callbacks: Dict[str, List[Callable]] = {
            "task_completed": [],
            "task_failed": [],
            "workflow_completed": [],
            "holon_registered": [],
            "holon_deregistered": []
        }
        
        logger.info("HolonCoordinator initialized")
    
    async def register_holon(self, holon: BaseHolon) -> str:
        """
        Register a holon with the coordinator.
        
        Args:
            holon: Holon instance to register
            
        Returns:
            Holon ID
        """
        async with self._lock:
            holon_id = await self.registry.register_holon(holon)
            self._holons[holon_id] = holon
            
            # Initialize the holon
            await holon.initialize()
            await holon.start()
            
            # Update registry with new status
            await self.registry.update_holon_status(
                holon_id,
                holon.status,
                "healthy"
            )
            
            # Trigger event callbacks
            for callback in self._event_callbacks.get("holon_registered", []):
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(holon_id, holon)
                    else:
                        callback(holon_id, holon)
                except Exception as e:
                    logger.error("Error in holon_registered callback", error=str(e))
            
            logger.info(
                "Holon registered with coordinator",
                holon_id=holon_id,
                type=holon.holon_type.value
            )
            
            return holon_id
    
    async def deregister_holon(self, holon_id: str) -> bool:
        """
        Deregister a holon from the coordinator.
        
        Args:
            holon_id: Holon identifier
            
        Returns:
            True if deregistered successfully
        """
        async with self._lock:
            if holon_id not in self._holons:
                return False
            
            holon = self._holons[holon_id]
            
            # Stop the holon
            await holon.stop()
            
            # Deregister from registry
            await self.registry.deregister_holon(holon_id)
            
            # Remove from local tracking
            del self._holons[holon_id]
            
            # Trigger event callbacks
            for callback in self._event_callbacks.get("holon_deregistered", []):
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(holon_id)
                    else:
                        callback(holon_id)
                except Exception as e:
                    logger.error("Error in holon_deregistered callback", error=str(e))
            
            logger.info("Holon deregistered from coordinator", holon_id=holon_id)
            return True
    
    async def submit_task(
        self,
        capability: str,
        parameters: Dict[str, Any] = None,
        context: Dict[str, Any] = None,
        priority: TaskPriority = TaskPriority.MEDIUM
    ) -> str:
        """
        Submit a task to be executed by a holon with the specified capability.
        
        Args:
            capability: Required capability
            parameters: Task parameters
            context: Optional context
            priority: Task priority
            
        Returns:
            Task ID
        """
        async with self._lock:
            task_id = str(datetime.now().timestamp())
            
            task = Task(
                task_id=task_id,
                capability=capability,
                parameters=parameters or {},
                context=context or {},
                priority=priority
            )
            
            self._tasks[task_id] = task
            self._pending_tasks.append(task)
            self._task_count += 1
            
            logger.info(
                "Task submitted",
                task_id=task_id,
                capability=capability,
                priority=priority.value
            )
            
            # Try to assign immediately
            await self._assign_tasks()
            
            return task_id
    
    async def submit_workflow(self, workflow: Workflow) -> str:
        """
        Submit a workflow to be executed.
        
        Args:
            workflow: Workflow to execute
            
        Returns:
            Workflow ID
        """
        async with self._lock:
            workflow_id = workflow.workflow_id
            self._workflows[workflow_id] = workflow
            
            # Submit all tasks in the workflow
            for task in workflow.tasks:
                task.workflow_id = workflow_id
                self._tasks[task.task_id] = task
                self._pending_tasks.append(task)
            
            self._task_count += len(workflow.tasks)
            
            logger.info(
                "Workflow submitted",
                workflow_id=workflow_id,
                name=workflow.name,
                task_count=len(workflow.tasks)
            )
            
            # Try to assign tasks
            await self._assign_tasks()
            
            return workflow_id
    
    async def _assign_tasks(self):
        """Assign pending tasks to available holons"""
        async with self._lock:
            # Sort pending tasks by priority (descending)
            self._pending_tasks.sort(
                key=lambda t: t.priority.value,
                reverse=True
            )
            
            # Process tasks in priority order
            for task in list(self._pending_tasks):
                # Find holons with the required capability
                result = await self.registry.discover_capabilities(task.capability)
                
                if not result.results:
                    logger.warning(
                        "No holon available for capability",
                        capability=task.capability
                    )
                    continue
                
                # Find the best available holon
                assigned_holon_id = None
                for holon_reg in result.results:
                    if holon_reg.status in [HolonStatus.READY, HolonStatus.ACTIVE]:
                        assigned_holon_id = holon_reg.holon_id
                        break
                
                if not assigned_holon_id:
                    logger.warning(
                        "No available holon for capability",
                        capability=task.capability
                    )
                    continue
                
                # Assign the task
                task.assigned_to = assigned_holon_id
                task.status = TaskStatus.ASSIGNED
                task.started_at = datetime.now()
                
                self._pending_tasks.remove(task)
                self._in_progress_tasks[task.task_id] = task
                
                # Execute the task in the background
                asyncio.create_task(self._execute_task(task))
                
                logger.info(
                    "Task assigned",
                    task_id=task.task_id,
                    holon_id=assigned_holon_id,
                    capability=task.capability
                )
    
    async def _execute_task(self, task: Task):
        """Execute a task on the assigned holon"""
        try:
            # Update status
            task.status = TaskStatus.PROCESSING
            
            # Get the holon instance
            if task.assigned_to not in self._holons:
                raise Exception(f"Holon not found: {task.assigned_to}")
            
            holon = self._holons[task.assigned_to]
            
            # Build task dictionary for execution
            execution_task = {
                "type": task.capability,
                "parameters": task.parameters,
                "context": task.context
            }
            
            # Execute on the holon
            result = await holon.execute(execution_task, task.context)
            
            # Update task
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.result = result
            
            # Update statistics
            self._completed_count += 1
            
            # Trigger completion callbacks
            for callback in self._event_callbacks.get("task_completed", []):
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(task)
                    else:
                        callback(task)
                except Exception as e:
                    logger.error("Error in task_completed callback", error=str(e))
            
            logger.info(
                "Task completed",
                task_id=task.task_id,
                holon_id=task.assigned_to
            )
            
        except Exception as e:
            # Handle task failure
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now()
            task.error = str(e)
            task.retries += 1
            
            # Update statistics
            self._failed_count += 1
            
            # Check if we should retry
            if task.retries < task.max_retries:
                task.status = TaskStatus.PENDING
                self._pending_tasks.append(task)
                
                logger.warning(
                    "Task failed, retrying",
                    task_id=task.task_id,
                    retry_count=task.retries,
                    error=str(e)
                )
                
                # Try to reassign
                await self._assign_tasks()
            else:
                # Trigger failure callbacks
                for callback in self._event_callbacks.get("task_failed", []):
                    try:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(task)
                        else:
                            callback(task)
                    except Exception as cb_error:
                        logger.error("Error in task_failed callback", error=str(cb_error))
                
                logger.error(
                    "Task failed permanently",
                    task_id=task.task_id,
                    error=str(e)
                )
        
        finally:
            # Clean up in-progress tracking
            if task.task_id in self._in_progress_tasks:
                del self._in_progress_tasks[task.task_id]
    
    async def get_task_status(self, task_id: str) -> Optional[Task]:
        """
        Get the status of a task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Task or None if not found
        """
        async with self._lock:
            return self._tasks.get(task_id)
    
    async def get_workflow_status(self, workflow_id: str) -> Optional[Workflow]:
        """
        Get the status of a workflow.
        
        Args:
            workflow_id: Workflow identifier
            
        Returns:
            Workflow or None if not found
        """
        async with self._lock:
            return self._workflows.get(workflow_id)
    
    async def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            True if cancelled successfully
        """
        async with self._lock:
            if task_id not in self._tasks:
                return False
            
            task = self._tasks[task_id]
            
            if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                return False
            
            task.status = TaskStatus.CANCELLED
            task.completed_at = datetime.now()
            
            # Remove from queues
            if task in self._pending_tasks:
                self._pending_tasks.remove(task)
            if task_id in self._in_progress_tasks:
                del self._in_progress_tasks[task_id]
            
            logger.info("Task cancelled", task_id=task_id)
            return True
    
    async def optimize_system(self) -> Dict[str, Any]:
        """
        Optimize the holon system based on current workload and performance.
        
        Returns:
            Optimization results
        """
        async with self._lock:
            # Get current system state
            stats = await self.registry.get_statistics()
            
            # Simple optimization: balance load across holons
            # In a real implementation, this would be more sophisticated
            optimization_actions = []
            
            # Check for overloaded holons
            for holon_id, holon in self._holons.items():
                # Check if holon is overloaded
                # This would use performance metrics in a real implementation
                pass
            
            # Check for underutilized holons
            # This would use performance metrics in a real implementation
            
            return {
                "optimization_actions": optimization_actions,
                "system_stats": stats,
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_system_health(self) -> Dict[str, Any]:
        """
        Get overall system health.
        
        Returns:
            System health information
        """
        async with self._lock:
            registry_stats = await self.registry.get_statistics()
            
            return {
                "registry": registry_stats,
                "tasks": {
                    "total": self._task_count,
                    "pending": len(self._pending_tasks),
                    "in_progress": len(self._in_progress_tasks),
                    "completed": self._completed_count,
                    "failed": self._failed_count
                },
                "workflows": {
                    "total": len(self._workflows),
                    "active": len([w for w in self._workflows.values() if w.status == "pending" or w.status == "running"])
                },
                "holons": {
                    "total": len(self._holons),
                    "by_type": {
                        ht.value: len([h for h in self._holons.values() if h.holon_type == ht])
                        for ht in HolonType
                    }
                }
            }
    
    def on(self, event: str, callback: Callable):
        """
        Register a callback for an event.
        
        Args:
            event: Event name
            callback: Callback function
        """
        if event not in self._event_callbacks:
            self._event_callbacks[event] = []
        self._event_callbacks[event].append(callback)
        
        return callback
    
    def off(self, event: str, callback: Callable) -> bool:
        """
        Unregister a callback for an event.
        
        Args:
            event: Event name
            callback: Callback function to remove
            
        Returns:
            True if removed successfully
        """
        if event in self._event_callbacks:
            try:
                self._event_callbacks[event].remove(callback)
                return True
            except ValueError:
                pass
        return False
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the coordinator"""
        return {
            "coordinator_type": "HolonCoordinator",
            "holon_count": len(self._holons),
            "task_count": self._task_count,
            "pending_tasks": len(self._pending_tasks),
            "in_progress_tasks": len(self._in_progress_tasks),
            "completed_tasks": self._completed_count,
            "failed_tasks": self._failed_count,
            "workflow_count": len(self._workflows)
        }
