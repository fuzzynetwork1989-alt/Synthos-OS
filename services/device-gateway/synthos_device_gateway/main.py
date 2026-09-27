"""Main FastAPI application for Device Gateway"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import structlog

from .config import Settings

logger = structlog.get_logger(__name__)

# Initialize settings
settings = Settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Device communication and management gateway for Synthos-OS"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DeviceRegistration(BaseModel):
    """Device registration schema"""
    device_id: str
    device_type: str  # sensor, actuator, controller, interface
    name: str
    capabilities: List[str]
    protocol: str  # websocket, mqtt, http
    metadata: Optional[Dict[str, Any]] = None


class DeviceMessage(BaseModel):
    """Device message schema"""
    device_id: str
    message_type: str
    payload: Dict[str, Any]
    timestamp: Optional[str] = None


class DeviceCommand(BaseModel):
    """Device command schema"""
    device_id: str
    command: str
    parameters: Dict[str, Any]


class ConnectionManager:
    """WebSocket connection manager"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        
    async def connect(self, device_id: str, websocket: WebSocket):
        """Connect a device"""
        await websocket.accept()
        self.active_connections[device_id] = websocket
        logger.info("Device connected", device_id=device_id)
        
    def disconnect(self, device_id: str):
        """Disconnect a device"""
        if device_id in self.active_connections:
            del self.active_connections[device_id]
            logger.info("Device disconnected", device_id=device_id)
            
    async def send_message(self, device_id: str, message: Dict):
        """Send message to a device"""
        if device_id in self.active_connections:
            await self.active_connections[device_id].send_json(message)
            
    async def broadcast(self, message: Dict):
        """Broadcast message to all connected devices"""
        for connection in self.active_connections.values():
            await connection.send_json(message)


manager = ConnectionManager()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "connected_devices": len(manager.active_connections),
        "max_devices": settings.max_connected_devices
    }


@app.post("/devices")
async def register_device(device: DeviceRegistration):
    """Register a new device"""
    try:
        logger.info(
            "Device registered",
            device_id=device.device_id,
            device_type=device.device_type,
            name=device.name
        )
        
        return {
            "device_id": device.device_id,
            "status": "registered",
            "name": device.name,
            "protocol": device.protocol
        }
    except Exception as e:
        logger.error("Failed to register device", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/devices/{device_id}")
async def get_device(device_id: str):
    """Get device information"""
    # Placeholder for device retrieval
    return {
        "device_id": device_id,
        "status": "connected" if device_id in manager.active_connections else "offline",
        "name": "Example Device",
        "capabilities": []
    }


@app.get("/devices")
async def list_devices():
    """List all registered devices"""
    # Placeholder for device listing
    return {
        "devices": [],
        "total": 0,
        "connected": len(manager.active_connections)
    }


@app.delete("/devices/{device_id}")
async def unregister_device(device_id: str):
    """Unregister a device"""
    try:
        manager.disconnect(device_id)
        logger.info("Device unregistered", device_id=device_id)
        
        return {
            "device_id": device_id,
            "status": "unregistered"
        }
    except Exception as e:
        logger.error("Failed to unregister device", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/command")
async def send_device_command(command: DeviceCommand):
    """Send command to a device"""
    try:
        logger.info(
            "Command sent to device",
            device_id=command.device_id,
            command=command.command
        )
        
        # Send via WebSocket if connected
        await manager.send_message(command.device_id, {
            "type": "command",
            "command": command.command,
            "parameters": command.parameters
        })
        
        return {
            "device_id": command.device_id,
            "command": command.command,
            "status": "sent"
        }
    except Exception as e:
        logger.error("Failed to send command", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/message")
async def receive_device_message(message: DeviceMessage):
    """Receive message from a device"""
    try:
        logger.info(
            "Message received from device",
            device_id=message.device_id,
            message_type=message.message_type
        )
        
        return {
            "device_id": message.device_id,
            "message_type": message.message_type,
            "status": "received"
        }
    except Exception as e:
        logger.error("Failed to process message", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    """WebSocket endpoint for device communication"""
    await manager.connect(device_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logger.info("WebSocket message received", device_id=device_id, data=data)
            
            # Process device message
            # Placeholder for message processing logic
            
    except WebSocketDisconnect:
        manager.disconnect(device_id)


@app.get("/devices/connected")
async def get_connected_devices():
    """Get currently connected devices"""
    return {
        "connected_devices": list(manager.active_connections.keys()),
        "total": len(manager.active_connections)
    }


@app.get("/metrics")
async def get_metrics():
    """Get device gateway metrics"""
    return {
        "total_devices": 0,
        "connected_devices": len(manager.active_connections),
        "messages_today": 0,
        "commands_sent": 0,
        "average_message_latency": 0.0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "synthos_device_gateway.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.device_debug
    )