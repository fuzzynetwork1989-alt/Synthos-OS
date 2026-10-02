"""
Integration Holon - External system connectors and adapters

Integration holons provide connectivity to external systems, APIs, and services,
allowing the HEICN system to interact with the broader digital ecosystem.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import structlog
from datetime import datetime
import asyncio
import aiohttp
import json

from .base import BaseHolon, HolonType, HolonStatus

logger = structlog.get_logger(__name__)


class IntegrationType(Enum):
    """Types of integration holons"""
    API = "api"                     # REST/GraphQL API connectors
    DATABASE = "database"           # Database connectors
    STORAGE = "storage"             # Cloud storage connectors
    MESSAGE_QUEUE = "message_queue" # Message queue connectors (Kafka, RabbitMQ)
    STREAMING = "streaming"         # Streaming data connectors
    WEBHOOK = "webhook"             # Webhook receivers
    PLUGIN = "plugin"               # Plugin system connectors
    CUSTOM = "custom"               # Custom integration


class AuthenticationMethod(Enum):
    """Authentication methods for external systems"""
    NONE = "none"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    JWT = "jwt"
    BASIC_AUTH = "basic_auth"
    CUSTOM = "custom"


@dataclass
class ConnectionConfig:
    """Configuration for an external connection"""
    connection_id: str
    name: str
    integration_type: IntegrationType
    base_url: Optional[str] = None
    authentication: AuthenticationMethod = AuthenticationMethod.NONE
    auth_config: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    timeout: int = 30
    retry_attempts: int = 3
    rate_limit: Optional[float] = None  # requests per second


@dataclass
class APIResponse:
    """Response from an external API call"""
    request_id: str
    status_code: int
    data: Any
    headers: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    latency: float = 0.0  # milliseconds
    success: bool = True
    error: Optional[str] = None


@dataclass
class DataMapping:
    """Mapping between external and internal data formats"""
    mapping_id: str
    source_format: str
    target_format: str
    field_mappings: Dict[str, str] = field(default_factory=dict)
    transforms: List[Dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


class IntegrationHolon(BaseHolon):
    """
    Integration Holon - External system connector for HEICN.
    
    Integration holons provide connectivity to external systems, allowing
    the HEICN system to interact with APIs, databases, and other services.
    
    Key Features:
    - Multi-protocol support (REST, GraphQL, WebSocket, etc.)
    - Authentication management
    - Data transformation and mapping
    - Rate limiting and throttling
    - Error handling and retry logic
    - Connection pooling
    """
    
    def __init__(
        self,
        holon_id: Optional[str] = None,
        name: str = "IntegrationHolon",
        integration_type: IntegrationType = IntegrationType.API,
        description: str = "",
        config: Optional[Dict] = None
    ):
        """
        Initialize the integration holon.
        
        Args:
            holon_id: Unique identifier
            name: Human-readable name
            integration_type: Type of integration
            description: Description of purpose
            config: Configuration dictionary
        """
        super().__init__(
            holon_id=holon_id,
            holon_type=HolonType.INTEGRATION,
            name=name,
            description=description,
            config=config
        )
        
        self.integration_type = integration_type
        
        # Connection management
        self._connections: Dict[str, ConnectionConfig] = {}
        self._active_connections: Dict[str, Any] = {}  # connection_id -> connection object
        
        # Data mappings
        self._mappings: Dict[str, DataMapping] = {}
        
        # Request tracking
        self._request_history: List[APIResponse] = []
        self._request_count: int = 0
        self._success_count: int = 0
        self._error_count: int = 0
        
        # Rate limiting
        self._rate_limiters: Dict[str, Dict] = {}  # connection_id -> rate limiter state
        
        # Register capabilities based on integration type
        self._register_integration_capabilities()
        
        logger.info(
            "IntegrationHolon initialized",
            holon_id=self.holon_id,
            integration_type=self.integration_type.value
        )
    
    def _register_integration_capabilities(self):
        """Register capabilities based on integration type"""
        capability_name = f"integration:{self.integration_type.value}"
        self.register_capability(
            name=capability_name,
            description=f"{self.integration_type.value.replace('_', ' ').title()} integration",
            version="1.0",
            quality_score=1.0
        )
        
        # Register common integration capabilities
        self.register_capability(
            name="integration:connect",
            description="Connection management",
            version="1.0",
            quality_score=0.9
        )
        
        self.register_capability(
            name="integration:request",
            description="Request execution",
            version="1.0",
            quality_score=0.9
        )
        
        self.register_capability(
            name="integration:transform",
            description="Data transformation",
            version="1.0",
            quality_score=0.85
        )
        
        # Type-specific capabilities
        if self.integration_type == IntegrationType.API:
            self.register_capability(
                name="integration:rest_call",
                description="REST API calls",
                version="1.0",
                quality_score=0.95
            )
            self.register_capability(
                name="integration:graphql_query",
                description="GraphQL queries",
                version="1.0",
                quality_score=0.9
            )
        
        elif self.integration_type == IntegrationType.DATABASE:
            self.register_capability(
                name="integration:sql_query",
                description="SQL query execution",
                version="1.0",
                quality_score=0.9
            )
        
        elif self.integration_type == IntegrationType.MESSAGE_QUEUE:
            self.register_capability(
                name="integration:publish",
                description="Message publishing",
                version="1.0",
                quality_score=0.9
            )
            self.register_capability(
                name="integration:subscribe",
                description="Message subscription",
                version="1.0",
                quality_score=0.9
            )
    
    async def initialize(self) -> bool:
        """Initialize the integration holon"""
        try:
            self._status = HolonStatus.INITIALIZING
            
            # Initialize data structures
            self._connections = {}
            self._active_connections = {}
            self._mappings = {}
            self._request_history = []
            
            self._request_count = 0
            self._success_count = 0
            self._error_count = 0
            
            self._rate_limiters = {}
            
            self._status = HolonStatus.READY
            self._initialized_at = datetime.now()
            
            logger.info("IntegrationHolon initialized successfully", holon_id=self.holon_id)
            return True
            
        except Exception as e:
            logger.error("Failed to initialize IntegrationHolon", holon_id=self.holon_id, error=str(e))
            self._status = HolonStatus.FAILED
            return False
    
    async def start(self) -> bool:
        """Start the integration holon"""
        try:
            if self._status != HolonStatus.READY:
                logger.warning("Cannot start - not in READY state", holon_id=self.holon_id)
                return False
            
            self._status = HolonStatus.ACTIVE
            self._started_at = datetime.now()
            
            # Initialize rate limiters for all connections
            for conn_id, config in self._connections.items():
                if config.rate_limit:
                    self._rate_limiters[conn_id] = {
                        "last_request": datetime.min,
                        "request_count": 0
                    }
            
            logger.info("IntegrationHolon started", holon_id=self.holon_id)
            return True
            
        except Exception as e:
            logger.error("Failed to start IntegrationHolon", holon_id=self.holon_id, error=str(e))
            self._status = HolonStatus.FAILED
            return False
    
    async def stop(self) -> bool:
        """Stop the integration holon"""
        try:
            # Close all active connections
            for conn_id, connection in self._active_connections.items():
                try:
                    if hasattr(connection, 'close'):
                        await connection.close()
                except Exception as e:
                    logger.warning("Error closing connection", connection_id=conn_id, error=str(e))
            
            self._active_connections.clear()
            self._status = HolonStatus.READY
            
            logger.info("IntegrationHolon stopped", holon_id=self.holon_id)
            return True
            
        except Exception as e:
            logger.error("Failed to stop IntegrationHolon", holon_id=self.holon_id, error=str(e))
            self._status = HolonStatus.FAILED
            return False
    
    async def execute(self, task: Dict, context: Optional[Dict] = None) -> Any:
        """
        Execute an integration task.
        
        Args:
            task: Task dictionary with 'type' and 'parameters'
            context: Optional context dictionary
            
        Returns:
            Result of integration operation
        """
        task_type = task.get("type", "unknown")
        parameters = task.get("parameters", {})
        
        self._request_count += 1
        
        logger.info(
            "Executing integration task",
            holon_id=self.holon_id,
            task_type=task_type,
            integration_type=self.integration_type.value
        )
        
        try:
            # Route to appropriate handler based on integration type
            if self.integration_type == IntegrationType.API:
                result = await self._handle_api(task, parameters)
            elif self.integration_type == IntegrationType.DATABASE:
                result = await self._handle_database(task, parameters)
            elif self.integration_type == IntegrationType.MESSAGE_QUEUE:
                result = await self._handle_message_queue(task, parameters)
            elif self.integration_type == IntegrationType.STREAMING:
                result = await self._handle_streaming(task, parameters)
            elif self.integration_type == IntegrationType.WEBHOOK:
                result = await self._handle_webhook(task, parameters)
            else:
                result = await self._handle_generic(task, parameters)
            
            self._success_count += 1
            return result
            
        except Exception as e:
            self._error_count += 1
            logger.error(
                "Failed to execute integration task",
                holon_id=self.holon_id,
                task_type=task_type,
                error=str(e)
            )
            return {"error": str(e), "success": False}
    
    async def add_connection(self, config: ConnectionConfig) -> str:
        """
        Add a new external connection.
        
        Args:
            config: Connection configuration
            
        Returns:
            Connection ID
        """
        config.connection_id = config.connection_id or str(datetime.now().timestamp())
        self._connections[config.connection_id] = config
        
        logger.info(
            "Connection added",
            holon_id=self.holon_id,
            connection_id=config.connection_id,
            name=config.name,
            type=config.integration_type.value
        )
        
        return config.connection_id
    
    async def remove_connection(self, connection_id: str) -> bool:
        """
        Remove an external connection.
        
        Args:
            connection_id: Connection identifier
            
        Returns:
            True if removed successfully
        """
        if connection_id in self._connections:
            del self._connections[connection_id]
            
            # Close active connection if exists
            if connection_id in self._active_connections:
                try:
                    if hasattr(self._active_connections[connection_id], 'close'):
                        await self._active_connections[connection_id].close()
                except Exception:
                    pass
                del self._active_connections[connection_id]
            
            # Remove rate limiter
            if connection_id in self._rate_limiters:
                del self._rate_limiters[connection_id]
            
            logger.info("Connection removed", holon_id=self.holon_id, connection_id=connection_id)
            return True
        
        return False
    
    async def get_connection(self, connection_id: str) -> Optional[ConnectionConfig]:
        """Get connection configuration"""
        return self._connections.get(connection_id)
    
    async def list_connections(self) -> List[Dict]:
        """List all connections"""
        return [
            {
                "connection_id": conn_id,
                "name": config.name,
                "type": config.integration_type.value,
                "base_url": config.base_url,
                "authentication": config.authentication.value,
                "active": connection_id in self._active_connections
            }
            for connection_id, config in self._connections.items()
        ]
    
    async def add_mapping(self, mapping: DataMapping) -> str:
        """
        Add a data mapping.
        
        Args:
            mapping: Data mapping configuration
            
        Returns:
            Mapping ID
        """
        mapping.mapping_id = mapping.mapping_id or str(datetime.now().timestamp())
        self._mappings[mapping.mapping_id] = mapping
        
        logger.info(
            "Mapping added",
            holon_id=self.holon_id,
            mapping_id=mapping.mapping_id,
            source=mapping.source_format,
            target=mapping.target_format
        )
        
        return mapping.mapping_id
    
    async def apply_mapping(self, data: Any, mapping_id: str) -> Any:
        """
        Apply a data mapping to transform data.
        
        Args:
            data: Data to transform
            mapping_id: Mapping identifier
            
        Returns:
            Transformed data
        """
        if mapping_id not in self._mappings:
            raise ValueError(f"Mapping not found: {mapping_id}")
        
        mapping = self._mappings[mapping_id]
        
        # Apply field mappings
        if isinstance(data, dict):
            transformed = {}
            for source_field, target_field in mapping.field_mappings.items():
                if source_field in data:
                    transformed[target_field] = data[source_field]
                else:
                    transformed[target_field] = None
            
            # Apply transforms (simplified - real implementation would be more complex)
            for transform in mapping.transforms:
                transform_type = transform.get("type", "copy")
                if transform_type == "copy":
                    pass  # Already handled by field mappings
                elif transform_type == "convert":
                    # Simple type conversion
                    pass
            
            return transformed
        
        return data
    
    async def _handle_api(self, task: Dict, parameters: Dict) -> Dict:
        """Handle API integration tasks"""
        operation = parameters.get("operation", "request")
        
        if operation == "request":
            connection_id = parameters.get("connection_id")
            method = parameters.get("method", "GET").upper()
            endpoint = parameters.get("endpoint", "/")
            data = parameters.get("data", None)
            headers = parameters.get("headers", {})
            
            if connection_id not in self._connections:
                return {"error": f"Connection not found: {connection_id}"}
            
            config = self._connections[connection_id]
            
            # Check rate limiting
            if config.rate_limit:
                if not await self._check_rate_limit(connection_id, config.rate_limit):
                    return {"error": "Rate limit exceeded", "retry_after": 1.0}
            
            # Build full URL
            base_url = config.base_url.rstrip('/') if config.base_url else ""
            full_url = f"{base_url}{endpoint}"
            
            # Add authentication headers
            auth_headers = self._get_auth_headers(config)
            all_headers = {**config.headers, **auth_headers, **headers}
            
            # In a real implementation, this would make the actual HTTP request
            # For now, we simulate it
            request_id = str(datetime.now().timestamp())
            
            try:
                # Simulate API call
                latency = 0.1  # 100ms
                
                # Simulate response based on method
                if method == "GET":
                    response_data = {"status": "success", "data": {"endpoint": endpoint}}
                elif method == "POST":
                    response_data = {"status": "created", "data": data, "id": request_id}
                elif method == "PUT":
                    response_data = {"status": "updated", "data": data}
                elif method == "DELETE":
                    response_data = {"status": "deleted", "id": endpoint.split('/')[-1]}
                else:
                    response_data = {"status": "unknown_method", "method": method}
                
                response = APIResponse(
                    request_id=request_id,
                    status_code=200,
                    data=response_data,
                    headers={"content-type": "application/json"},
                    latency=latency * 1000
                )
                
                self._request_history.append(response)
                
                # Apply data mapping if specified
                mapping_id = parameters.get("mapping_id")
                if mapping_id:
                    response_data = await self.apply_mapping(response_data, mapping_id)
                
                return {
                    "status": "success",
                    "request_id": request_id,
                    "data": response_data,
                    "latency": latency
                }
                
            except Exception as e:
                error_response = APIResponse(
                    request_id=request_id,
                    status_code=500,
                    data=None,
                    error=str(e),
                    success=False
                )
                self._request_history.append(error_response)
                return {"error": str(e), "request_id": request_id}
        
        elif operation == "connect":
            connection_id = parameters.get("connection_id")
            if connection_id not in self._connections:
                return {"error": f"Connection not found: {connection_id}"}
            
            # In a real implementation, this would establish the connection
            # For now, we just mark it as active
            config = self._connections[connection_id]
            
            # Create a mock connection object
            connection = {
                "config": config,
                "connected_at": datetime.now(),
                "status": "connected"
            }
            self._active_connections[connection_id] = connection
            
            return {"status": "connected", "connection_id": connection_id}
        
        elif operation == "disconnect":
            connection_id = parameters.get("connection_id")
            if connection_id in self._active_connections:
                del self._active_connections[connection_id]
                return {"status": "disconnected", "connection_id": connection_id}
            else:
                return {"error": f"Connection not active: {connection_id}"}
        
        else:
            return {"error": f"Unknown API operation: {operation}"}
    
    async def _handle_database(self, task: Dict, parameters: Dict) -> Dict:
        """Handle database integration tasks"""
        operation = parameters.get("operation", "query")
        
        if operation == "query":
            connection_id = parameters.get("connection_id")
            sql = parameters.get("sql", "")
            params = parameters.get("params", {})
            
            if connection_id not in self._connections:
                return {"error": f"Connection not found: {connection_id}"}
            
            # In a real implementation, this would execute the SQL query
            # For now, we simulate it
            result = {
                "status": "success",
                "query": sql,
                "results": [{"row": 1, "data": "sample"}],
                "affected_rows": 1
            }
            
            return result
        
        elif operation == "execute":
            connection_id = parameters.get("connection_id")
            sql = parameters.get("sql", "")
            
            if connection_id not in self._connections:
                return {"error": f"Connection not found: {connection_id}"}
            
            # Simulate execution
            result = {
                "status": "success",
                "query": sql,
                "affected_rows": 1
            }
            
            return result
        
        else:
            return {"error": f"Unknown database operation: {operation}"}
    
    async def _handle_message_queue(self, task: Dict, parameters: Dict) -> Dict:
        """Handle message queue integration tasks"""
        operation = parameters.get("operation", "publish")
        
        if operation == "publish":
            connection_id = parameters.get("connection_id")
            topic = parameters.get("topic", "default")
            message = parameters.get("message", {})
            
            if connection_id not in self._connections:
                return {"error": f"Connection not found: {connection_id}"}
            
            # In a real implementation, this would publish to the message queue
            # For now, we simulate it
            message_id = str(datetime.now().timestamp())
            
            return {
                "status": "published",
                "message_id": message_id,
                "topic": topic
            }
        
        elif operation == "subscribe":
            connection_id = parameters.get("connection_id")
            topic = parameters.get("topic", "default")
            callback_url = parameters.get("callback_url", "")
            
            if connection_id not in self._connections:
                return {"error": f"Connection not found: {connection_id}"}
            
            # In a real implementation, this would subscribe to the topic
            subscription_id = str(datetime.now().timestamp())
            
            return {
                "status": "subscribed",
                "subscription_id": subscription_id,
                "topic": topic
            }
        
        else:
            return {"error": f"Unknown message queue operation: {operation}"}
    
    async def _handle_streaming(self, task: Dict, parameters: Dict) -> Dict:
        """Handle streaming integration tasks"""
        operation = parameters.get("operation", "start")
        
        if operation == "start":
            connection_id = parameters.get("connection_id")
            stream_name = parameters.get("stream_name", "default")
            
            if connection_id not in self._connections:
                return {"error": f"Connection not found: {connection_id}"}
            
            # In a real implementation, this would start a streaming connection
            stream_id = str(datetime.now().timestamp())
            
            return {
                "status": "streaming",
                "stream_id": stream_id,
                "stream_name": stream_name
            }
        
        elif operation == "stop":
            stream_id = parameters.get("stream_id")
            
            return {
                "status": "stopped",
                "stream_id": stream_id
            }
        
        else:
            return {"error": f"Unknown streaming operation: {operation}"}
    
    async def _handle_webhook(self, task: Dict, parameters: Dict) -> Dict:
        """Handle webhook integration tasks"""
        operation = parameters.get("operation", "register")
        
        if operation == "register":
            connection_id = parameters.get("connection_id")
            endpoint = parameters.get("endpoint", "/webhook")
            events = parameters.get("events", [])
            
            if connection_id not in self._connections:
                return {"error": f"Connection not found: {connection_id}"}
            
            # In a real implementation, this would register the webhook
            webhook_id = str(datetime.now().timestamp())
            
            return {
                "status": "registered",
                "webhook_id": webhook_id,
                "endpoint": endpoint,
                "events": events
            }
        
        elif operation == "unregister":
            webhook_id = parameters.get("webhook_id")
            
            return {
                "status": "unregistered",
                "webhook_id": webhook_id
            }
        
        else:
            return {"error": f"Unknown webhook operation: {operation}"}
    
    async def _handle_generic(self, task: Dict, parameters: Dict) -> Dict:
        """Handle generic integration tasks"""
        return {
            "type": "generic_response",
            "input": parameters,
            "response": f"Generic integration processing: {self.integration_type.value}",
            "integration_type": self.integration_type.value
        }
    
    async def _check_rate_limit(self, connection_id: str, rate_limit: float) -> bool:
        """
        Check if rate limit allows another request.
        
        Args:
            connection_id: Connection identifier
            rate_limit: Requests per second limit
            
        Returns:
            True if request is allowed
        """
        if connection_id not in self._rate_limiters:
            self._rate_limiters[connection_id] = {
                "last_request": datetime.min,
                "request_count": 0
            }
        
        limiter = self._rate_limiters[connection_id]
        now = datetime.now()
        
        # Calculate time since last request
        time_since_last = (now - limiter["last_request"]).total_seconds()
        
        # Reset if enough time has passed
        if time_since_last > 1.0:  # 1 second window
            limiter["last_request"] = now
            limiter["request_count"] = 0
            return True
        
        # Check if we're under the limit
        if limiter["request_count"] < rate_limit:
            limiter["request_count"] += 1
            limiter["last_request"] = now
            return True
        
        return False
    
    def _get_auth_headers(self, config: ConnectionConfig) -> Dict[str, str]:
        """
        Get authentication headers for a connection.
        
        Args:
            config: Connection configuration
            
        Returns:
            Dictionary of authentication headers
        """
        headers = {}
        
        if config.authentication == AuthenticationMethod.API_KEY:
            api_key = config.auth_config.get("api_key", "")
            header_name = config.auth_config.get("header_name", "Authorization")
            headers[header_name] = f"Bearer {api_key}"
        
        elif config.authentication == AuthenticationMethod.BASIC_AUTH:
            username = config.auth_config.get("username", "")
            password = config.auth_config.get("password", "")
            # In a real implementation, this would be base64 encoded
            headers["Authorization"] = f"Basic {username}:{password}"
        
        elif config.authentication == AuthenticationMethod.JWT:
            token = config.auth_config.get("token", "")
            headers["Authorization"] = f"Bearer {token}"
        
        return headers
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about this integration holon"""
        info = super().get_info()
        info.update({
            "integration_type": self.integration_type.value,
            "connection_count": len(self._connections),
            "active_connections": len(self._active_connections),
            "mapping_count": len(self._mappings),
            "requests": self._request_count,
            "successes": self._success_count,
            "errors": self._error_count
        })
        return info
