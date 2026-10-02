"""
Service Holon - Infrastructure modules for data, communication, storage

Service holons provide the infrastructure backbone for the HEICN system,
handling data storage, communication between holons, and system services.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import structlog
from datetime import datetime
import asyncio
import json

from .base import BaseHolon, HolonType, HolonStatus

logger = structlog.get_logger(__name__)


class ServiceType(Enum):
    """Types of service holons"""
    DATA = "data"                 # Data storage and retrieval
    COMMUNICATION = "communication" # Message passing and coordination
    STORAGE = "storage"             # Persistent storage
    CACHE = "cache"                 # Temporary data caching
    INDEX = "index"                 # Search and indexing
    QUEUE = "queue"                 # Task and message queuing
    MONITORING = "monitoring"       # System monitoring
    SECURITY = "security"           # Authentication and authorization


@dataclass
class DataRecord:
    """A data record stored by a service holon"""
    record_id: str
    content: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    ttl: Optional[datetime] = None  # Time-to-live


@dataclass
class Message:
    """A message for communication between holons"""
    message_id: str
    sender: str
    recipient: str
    content: Any
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 1  # 1-5, 5 being highest
    retry_count: int = 0
    max_retries: int = 3


class ServiceHolon(BaseHolon):
    """
    Service Holon - Infrastructure module for HEICN.
    
    Service holons provide the infrastructure backbone, handling:
    - Data storage and retrieval
    - Communication between holons
    - System services like caching, indexing, queuing
    
    Key Features:
    - Efficient data handling
    - Reliable message delivery
    - Scalable infrastructure services
    - Self-optimizing performance
    """
    
    def __init__(
        self,
        holon_id: Optional[str] = None,
        name: str = "ServiceHolon",
        service_type: ServiceType = ServiceType.DATA,
        description: str = "",
        config: Optional[Dict] = None
    ):
        """
        Initialize the service holon.
        
        Args:
            holon_id: Unique identifier
            name: Human-readable name
            service_type: Type of service provided
            description: Description of purpose
            config: Configuration dictionary
        """
        super().__init__(
            holon_id=holon_id,
            holon_type=HolonType.SERVICE,
            name=name,
            description=description,
            config=config
        )
        
        self.service_type = service_type
        
        # Data storage
        self._data: Dict[str, DataRecord] = {}
        self._data_index: Dict[str, List[str]] = {}  # key -> [record_ids]
        
        # Message queue
        self._message_queue: Dict[str, List[Message]] = {}  # recipient -> [messages]
        self._pending_messages: Dict[str, Message] = {}  # message_id -> message
        
        # Performance metrics
        self._request_count: int = 0
        self._success_count: int = 0
        self._error_count: int = 0
        
        # Register capabilities based on service type
        self._register_service_capabilities()
        
        logger.info(
            "ServiceHolon initialized",
            holon_id=self.holon_id,
            service_type=self.service_type.value
        )
    
    def _register_service_capabilities(self):
        """Register capabilities based on service type"""
        capability_name = f"service:{self.service_type.value}"
        self.register_capability(
            name=capability_name,
            description=f"{self.service_type.value.capitalize()} service",
            version="1.0",
            quality_score=1.0
        )
        
        # Register common service capabilities
        if self.service_type == ServiceType.DATA:
            self.register_capability(
                name="service:store",
                description="Data storage capability",
                version="1.0",
                quality_score=0.9
            )
            self.register_capability(
                name="service:retrieve",
                description="Data retrieval capability",
                version="1.0",
                quality_score=0.9
            )
        
        elif self.service_type == ServiceType.COMMUNICATION:
            self.register_capability(
                name="service:send_message",
                description="Message sending capability",
                version="1.0",
                quality_score=0.9
            )
            self.register_capability(
                name="service:receive_message",
                description="Message receiving capability",
                version="1.0",
                quality_score=0.9
            )
        
        elif self.service_type == ServiceType.CACHE:
            self.register_capability(
                name="service:cache_set",
                description="Cache storage capability",
                version="1.0",
                quality_score=0.95
            )
            self.register_capability(
                name="service:cache_get",
                description="Cache retrieval capability",
                version="1.0",
                quality_score=0.95
            )
        
        elif self.service_type == ServiceType.INDEX:
            self.register_capability(
                name="service:index",
                description="Data indexing capability",
                version="1.0",
                quality_score=0.85
            )
            self.register_capability(
                name="service:search",
                description="Search capability",
                version="1.0",
                quality_score=0.85
            )
    
    async def initialize(self) -> bool:
        """Initialize the service holon"""
        try:
            self._status = HolonStatus.INITIALIZING
            
            # Initialize data structures
            self._data = {}
            self._data_index = {}
            self._message_queue = {}
            self._pending_messages = {}
            
            self._request_count = 0
            self._success_count = 0
            self._error_count = 0
            
            self._status = HolonStatus.READY
            self._initialized_at = datetime.now()
            
            logger.info("ServiceHolon initialized successfully", holon_id=self.holon_id)
            return True
            
        except Exception as e:
            logger.error("Failed to initialize ServiceHolon", holon_id=self.holon_id, error=str(e))
            self._status = HolonStatus.FAILED
            return False
    
    async def start(self) -> bool:
        """Start the service holon"""
        try:
            if self._status != HolonStatus.READY:
                logger.warning("Cannot start - not in READY state", holon_id=self.holon_id)
                return False
            
            self._status = HolonStatus.ACTIVE
            self._started_at = datetime.now()
            
            logger.info("ServiceHolon started", holon_id=self.holon_id)
            return True
            
        except Exception as e:
            logger.error("Failed to start ServiceHolon", holon_id=self.holon_id, error=str(e))
            self._status = HolonStatus.FAILED
            return False
    
    async def stop(self) -> bool:
        """Stop the service holon"""
        try:
            self._status = HolonStatus.READY
            
            # Clean up pending messages
            self._pending_messages.clear()
            
            logger.info("ServiceHolon stopped", holon_id=self.holon_id)
            return True
            
        except Exception as e:
            logger.error("Failed to stop ServiceHolon", holon_id=self.holon_id, error=str(e))
            self._status = HolonStatus.FAILED
            return False
    
    async def execute(self, task: Dict, context: Optional[Dict] = None) -> Any:
        """
        Execute a service task.
        
        Args:
            task: Task dictionary with 'type' and 'parameters'
            context: Optional context dictionary
            
        Returns:
            Result of service operation
        """
        task_type = task.get("type", "unknown")
        parameters = task.get("parameters", {})
        
        self._request_count += 1
        
        logger.info(
            "Executing service task",
            holon_id=self.holon_id,
            task_type=task_type,
            service_type=self.service_type.value
        )
        
        try:
            # Route to appropriate handler based on service type
            if self.service_type == ServiceType.DATA:
                result = await self._handle_data(task, parameters)
            elif self.service_type == ServiceType.COMMUNICATION:
                result = await self._handle_communication(task, parameters)
            elif self.service_type == ServiceType.CACHE:
                result = await self._handle_cache(task, parameters)
            elif self.service_type == ServiceType.INDEX:
                result = await self._handle_index(task, parameters)
            elif self.service_type == ServiceType.QUEUE:
                result = await self._handle_queue(task, parameters)
            elif self.service_type == ServiceType.MONITORING:
                result = await self._handle_monitoring(task, parameters)
            else:
                result = await self._handle_generic(task, parameters)
            
            self._success_count += 1
            return result
            
        except Exception as e:
            self._error_count += 1
            logger.error(
                "Failed to execute service task",
                holon_id=self.holon_id,
                task_type=task_type,
                error=str(e)
            )
            return {"error": str(e), "success": False}
    
    async def _handle_data(self, task: Dict, parameters: Dict) -> Dict:
        """Handle data service tasks"""
        operation = parameters.get("operation", "retrieve")
        
        if operation == "store":
            record_id = str(datetime.now().timestamp())
            record = DataRecord(
                record_id=record_id,
                content=parameters.get("content"),
                metadata=parameters.get("metadata", {}),
                timestamp=datetime.now()
            )
            self._data[record_id] = record
            
            # Update index
            for key, value in record.metadata.items():
                if key not in self._data_index:
                    self._data_index[key] = []
                self._data_index[key].append(record_id)
            
            return {"status": "stored", "record_id": record_id}
        
        elif operation == "retrieve":
            record_id = parameters.get("record_id")
            if record_id in self._data:
                record = self._data[record_id]
                return {
                    "status": "retrieved",
                    "record": {
                        "record_id": record.record_id,
                        "content": record.content,
                        "metadata": record.metadata,
                        "timestamp": record.timestamp.isoformat()
                    }
                }
            else:
                return {"status": "not_found", "record_id": record_id}
        
        elif operation == "search":
            query = parameters.get("query", {})
            results = []
            
            for key, value in query.items():
                if key in self._data_index:
                    for record_id in self._data_index[key]:
                        if record_id in self._data:
                            results.append(self._data[record_id])
            
            return {
                "status": "search_complete",
                "count": len(results),
                "results": [
                    {
                        "record_id": r.record_id,
                        "content": r.content,
                        "metadata": r.metadata
                    }
                    for r in results[:10]  # Limit to 10 results
                ]
            }
        
        else:
            return {"error": f"Unknown data operation: {operation}"}
    
    async def _handle_communication(self, task: Dict, parameters: Dict) -> Dict:
        """Handle communication service tasks"""
        operation = parameters.get("operation", "send")
        
        if operation == "send":
            message = Message(
                message_id=str(datetime.now().timestamp()),
                sender=parameters.get("sender", self.holon_id),
                recipient=parameters.get("recipient"),
                content=parameters.get("content"),
                priority=parameters.get("priority", 1)
            )
            
            # Store in recipient's queue
            if message.recipient not in self._message_queue:
                self._message_queue[message.recipient] = []
            self._message_queue[message.recipient].append(message)
            
            # Also store in pending
            self._pending_messages[message.message_id] = message
            
            return {"status": "sent", "message_id": message.message_id}
        
        elif operation == "receive":
            recipient = parameters.get("recipient", self.holon_id)
            
            if recipient in self._message_queue and self._message_queue[recipient]:
                message = self._message_queue[recipient].pop(0)
                # Remove from pending
                if message.message_id in self._pending_messages:
                    del self._pending_messages[message.message_id]
                
                return {
                    "status": "received",
                    "message": {
                        "message_id": message.message_id,
                        "sender": message.sender,
                        "content": message.content,
                        "timestamp": message.timestamp.isoformat()
                    }
                }
            else:
                return {"status": "no_messages", "recipient": recipient}
        
        elif operation == "peek":
            recipient = parameters.get("recipient", self.holon_id)
            
            if recipient in self._message_queue:
                count = len(self._message_queue[recipient])
                return {"status": "queue_status", "recipient": recipient, "count": count}
            else:
                return {"status": "queue_status", "recipient": recipient, "count": 0}
        
        else:
            return {"error": f"Unknown communication operation: {operation}"}
    
    async def _handle_cache(self, task: Dict, parameters: Dict) -> Dict:
        """Handle cache service tasks"""
        operation = parameters.get("operation", "get")
        
        if operation == "set":
            key = parameters.get("key")
            value = parameters.get("value")
            ttl = parameters.get("ttl")  # seconds
            
            record = DataRecord(
                record_id=key,
                content=value,
                metadata={"type": "cache"},
                timestamp=datetime.now()
            )
            
            if ttl:
                record.ttl = datetime.now() + timedelta(seconds=ttl)
            
            self._data[key] = record
            
            # Update index
            if "cache" not in self._data_index:
                self._data_index["cache"] = []
            if key not in self._data_index["cache"]:
                self._data_index["cache"].append(key)
            
            return {"status": "cached", "key": key}
        
        elif operation == "get":
            key = parameters.get("key")
            
            if key in self._data:
                record = self._data[key]
                
                # Check TTL
                if record.ttl and record.ttl < datetime.now():
                    del self._data[key]
                    return {"status": "expired", "key": key}
                
                return {"status": "hit", "key": key, "value": record.content}
            else:
                return {"status": "miss", "key": key}
        
        elif operation == "delete":
            key = parameters.get("key")
            
            if key in self._data:
                del self._data[key]
                
                # Remove from index
                if "cache" in self._data_index and key in self._data_index["cache"]:
                    self._data_index["cache"].remove(key)
                
                return {"status": "deleted", "key": key}
            else:
                return {"status": "not_found", "key": key}
        
        else:
            return {"error": f"Unknown cache operation: {operation}"}
    
    async def _handle_index(self, task: Dict, parameters: Dict) -> Dict:
        """Handle index service tasks"""
        operation = parameters.get("operation", "index")
        
        if operation == "index":
            record_id = parameters.get("record_id")
            keys = parameters.get("keys", [])
            
            if record_id in self._data:
                for key in keys:
                    if key not in self._data_index:
                        self._data_index[key] = []
                    if record_id not in self._data_index[key]:
                        self._data_index[key].append(record_id)
                
                return {"status": "indexed", "record_id": record_id, "keys": keys}
            else:
                return {"status": "not_found", "record_id": record_id}
        
        elif operation == "search":
            query = parameters.get("query", "")
            keys = parameters.get("keys", [])
            
            results = []
            for key in keys:
                if key in self._data_index:
                    results.extend(self._data_index[key])
            
            return {
                "status": "search_complete",
                "query": query,
                "count": len(results),
                "record_ids": results[:10]  # Limit to 10
            }
        
        else:
            return {"error": f"Unknown index operation: {operation}"}
    
    async def _handle_queue(self, task: Dict, parameters: Dict) -> Dict:
        """Handle queue service tasks"""
        operation = parameters.get("operation", "enqueue")
        
        if operation == "enqueue":
            queue_name = parameters.get("queue", "default")
            item = parameters.get("item")
            
            if queue_name not in self._message_queue:
                self._message_queue[queue_name] = []
            
            # Use message structure for queue items
            message = Message(
                message_id=str(datetime.now().timestamp()),
                sender=parameters.get("sender", self.holon_id),
                recipient=queue_name,
                content=item
            )
            self._message_queue[queue_name].append(message)
            
            return {"status": "enqueued", "queue": queue_name, "item_id": message.message_id}
        
        elif operation == "dequeue":
            queue_name = parameters.get("queue", "default")
            
            if queue_name in self._message_queue and self._message_queue[queue_name]:
                message = self._message_queue[queue_name].pop(0)
                return {
                    "status": "dequeued",
                    "queue": queue_name,
                    "item": message.content,
                    "item_id": message.message_id
                }
            else:
                return {"status": "empty", "queue": queue_name}
        
        elif operation == "peek":
            queue_name = parameters.get("queue", "default")
            
            if queue_name in self._message_queue:
                count = len(self._message_queue[queue_name])
                return {"status": "queue_status", "queue": queue_name, "count": count}
            else:
                return {"status": "queue_status", "queue": queue_name, "count": 0}
        
        else:
            return {"error": f"Unknown queue operation: {operation}"}
    
    async def _handle_monitoring(self, task: Dict, parameters: Dict) -> Dict:
        """Handle monitoring service tasks"""
        operation = parameters.get("operation", "status")
        
        if operation == "status":
            return {
                "status": "monitoring",
                "requests": self._request_count,
                "successes": self._success_count,
                "errors": self._error_count,
                "success_rate": self._success_count / max(1, self._request_count)
            }
        
        elif operation == "reset_stats":
            self._request_count = 0
            self._success_count = 0
            self._error_count = 0
            return {"status": "reset"}
        
        else:
            return {"error": f"Unknown monitoring operation: {operation}"}
    
    async def _handle_generic(self, task: Dict, parameters: Dict) -> Dict:
        """Handle generic service tasks"""
        return {
            "type": "generic_response",
            "input": parameters,
            "response": f"Generic service processing: {self.service_type.value}",
            "service_type": self.service_type.value
        }
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about this service holon"""
        info = super().get_info()
        info.update({
            "service_type": self.service_type.value,
            "data_count": len(self._data),
            "message_count": len(self._pending_messages),
            "queue_count": len(self._message_queue),
            "requests": self._request_count,
            "successes": self._success_count,
            "errors": self._error_count
        })
        return info
