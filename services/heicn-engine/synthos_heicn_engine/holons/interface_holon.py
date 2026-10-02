"""
Interface Holon - User interaction modules for different modalities

Interface holons handle user interactions across various modalities,
providing natural and adaptive interfaces for users to interact with the HEICN system.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import structlog
from datetime import datetime
import asyncio

from .base import BaseHolon, HolonType, HolonStatus

logger = structlog.get_logger(__name__)


class InterfaceModality(Enum):
    """Types of interface modalities"""
    TEXT = "text"                 # Text-based interaction
    VOICE = "voice"               # Voice/speech interaction
    VISUAL = "visual"             # Visual/graphical interaction
    GESTURE = "gesture"           # Gesture-based interaction
    TOUCH = "touch"               # Touch-based interaction
    MULTIMODAL = "multimodal"     # Combined modalities
    AR = "ar"                     # Augmented reality
    VR = "vr"                     # Virtual reality
    HOLOGRAPHIC = "holographic"   # Holographic display


@dataclass
class UserContext:
    """Context about the current user interaction"""
    user_id: str
    session_id: str
    interaction_history: List[Dict] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)
    current_goal: Optional[str] = None
    emotional_state: Dict[str, float] = field(default_factory=dict)
    engagement_level: float = 0.5  # 0.0 to 1.0


@dataclass
class Interaction:
    """A user interaction record"""
    interaction_id: str
    user_id: str
    modality: str
    input: Any
    output: Any
    timestamp: datetime = field(default_factory=datetime.now)
    intent: Optional[str] = None
    confidence: float = 0.0
    sentiment: float = 0.0  # -1.0 to 1.0


class InterfaceHolon(BaseHolon):
    """
    Interface Holon - User interaction module for HEICN.
    
    Interface holons handle user interactions across various modalities,
    providing natural and adaptive interfaces.
    
    Key Features:
    - Multi-modality support
    - Context-aware interactions
    - Adaptive communication
    - User preference learning
    - Emotional state tracking
    """
    
    def __init__(
        self,
        holon_id: Optional[str] = None,
        name: str = "InterfaceHolon",
        modality: InterfaceModality = InterfaceModality.TEXT,
        description: str = "",
        config: Optional[Dict] = None
    ):
        """
        Initialize the interface holon.
        
        Args:
            holon_id: Unique identifier
            name: Human-readable name
            modality: Primary interface modality
            description: Description of purpose
            config: Configuration dictionary
        """
        super().__init__(
            holon_id=holon_id,
            holon_type=HolonType.INTERFACE,
            name=name,
            description=description,
            config=config
        )
        
        self.modality = modality
        
        # User contexts
        self._user_contexts: Dict[str, UserContext] = {}
        
        # Interaction history
        self._interactions: Dict[str, Interaction] = {}
        
        # Adaptive preferences
        self._adaptive_preferences: Dict[str, Dict] = {}  # user_id -> preferences
        
        # Performance metrics
        self._interaction_count: int = 0
        self._successful_interactions: int = 0
        
        # Register capabilities based on modality
        self._register_modality_capabilities()
        
        logger.info(
            "InterfaceHolon initialized",
            holon_id=self.holon_id,
            modality=self.modality.value
        )
    
    def _register_modality_capabilities(self):
        """Register capabilities based on interface modality"""
        capability_name = f"interface:{self.modality.value}"
        self.register_capability(
            name=capability_name,
            description=f"{self.modality.value.capitalize()} interface",
            version="1.0",
            quality_score=1.0
        )
        
        # Register common interface capabilities
        self.register_capability(
            name="interface:input",
            description="User input processing",
            version="1.0",
            quality_score=0.9
        )
        
        self.register_capability(
            name="interface:output",
            description="User output generation",
            version="1.0",
            quality_score=0.9
        )
        
        self.register_capability(
            name="interface:context",
            description="Context management",
            version="1.0",
            quality_score=0.8
        )
        
        # Modality-specific capabilities
        if self.modality == InterfaceModality.TEXT:
            self.register_capability(
                name="interface:text_process",
                description="Text processing",
                version="1.0",
                quality_score=0.95
            )
        elif self.modality == InterfaceModality.VOICE:
            self.register_capability(
                name="interface:speech_recognize",
                description="Speech recognition",
                version="1.0",
                quality_score=0.85
            )
            self.register_capability(
                name="interface:speech_synthesize",
                description="Speech synthesis",
                version="1.0",
                quality_score=0.85
            )
        elif self.modality == InterfaceModality.VISUAL:
            self.register_capability(
                name="interface:render",
                description="Visual rendering",
                version="1.0",
                quality_score=0.9
            )
        elif self.modality == InterfaceModality.GESTURE:
            self.register_capability(
                name="interface:gesture_recognize",
                description="Gesture recognition",
                version="1.0",
                quality_score=0.8
            )
        elif self.modality == InterfaceModality.HOLOGRAPHIC:
            self.register_capability(
                name="interface:hologram_render",
                description="Holographic rendering",
                version="1.0",
                quality_score=0.75
            )
    
    async def initialize(self) -> bool:
        """Initialize the interface holon"""
        try:
            self._status = HolonStatus.INITIALIZING
            
            # Initialize data structures
            self._user_contexts = {}
            self._interactions = {}
            self._adaptive_preferences = {}
            
            self._interaction_count = 0
            self._successful_interactions = 0
            
            self._status = HolonStatus.READY
            self._initialized_at = datetime.now()
            
            logger.info("InterfaceHolon initialized successfully", holon_id=self.holon_id)
            return True
            
        except Exception as e:
            logger.error("Failed to initialize InterfaceHolon", holon_id=self.holon_id, error=str(e))
            self._status = HolonStatus.FAILED
            return False
    
    async def start(self) -> bool:
        """Start the interface holon"""
        try:
            if self._status != HolonStatus.READY:
                logger.warning("Cannot start - not in READY state", holon_id=self.holon_id)
                return False
            
            self._status = HolonStatus.ACTIVE
            self._started_at = datetime.now()
            
            logger.info("InterfaceHolon started", holon_id=self.holon_id)
            return True
            
        except Exception as e:
            logger.error("Failed to start InterfaceHolon", holon_id=self.holon_id, error=str(e))
            self._status = HolonStatus.FAILED
            return False
    
    async def stop(self) -> bool:
        """Stop the interface holon"""
        try:
            self._status = HolonStatus.READY
            
            logger.info("InterfaceHolon stopped", holon_id=self.holon_id)
            return True
            
        except Exception as e:
            logger.error("Failed to stop InterfaceHolon", holon_id=self.holon_id, error=str(e))
            self._status = HolonStatus.FAILED
            return False
    
    async def execute(self, task: Dict, context: Optional[Dict] = None) -> Any:
        """
        Execute an interface task.
        
        Args:
            task: Task dictionary with 'type' and 'parameters'
            context: Optional context dictionary
            
        Returns:
            Result of interface operation
        """
        task_type = task.get("type", "unknown")
        parameters = task.get("parameters", {})
        
        self._interaction_count += 1
        
        logger.info(
            "Executing interface task",
            holon_id=self.holon_id,
            task_type=task_type,
            modality=self.modality.value
        )
        
        try:
            # Route to appropriate handler based on modality
            if self.modality == InterfaceModality.TEXT:
                result = await self._handle_text(task, parameters)
            elif self.modality == InterfaceModality.VOICE:
                result = await self._handle_voice(task, parameters)
            elif self.modality == InterfaceModality.VISUAL:
                result = await self._handle_visual(task, parameters)
            elif self.modality == InterfaceModality.GESTURE:
                result = await self._handle_gesture(task, parameters)
            elif self.modality == InterfaceModality.TOUCH:
                result = await self._handle_touch(task, parameters)
            elif self.modality == InterfaceModality.HOLOGRAPHIC:
                result = await self._handle_holographic(task, parameters)
            else:
                result = await self._handle_generic(task, parameters)
            
            self._successful_interactions += 1
            return result
            
        except Exception as e:
            logger.error(
                "Failed to execute interface task",
                holon_id=self.holon_id,
                task_type=task_type,
                error=str(e)
            )
            return {"error": str(e), "success": False}
    
    async def _handle_text(self, task: Dict, parameters: Dict) -> Dict:
        """Handle text interface tasks"""
        operation = parameters.get("operation", "process")
        
        if operation == "process":
            text = parameters.get("text", "")
            user_id = parameters.get("user_id", "unknown")
            
            # In a real implementation, this would use NLP models
            result = {
                "type": "text_processed",
                "input": text,
                "intent": "unknown",
                "entities": [],
                "sentiment": 0.0,
                "confidence": 0.8
            }
            
            # Record interaction
            self._record_interaction(user_id, "text", text, result)
            
            return result
        
        elif operation == "generate":
            prompt = parameters.get("prompt", "")
            user_id = parameters.get("user_id", "unknown")
            
            # In a real implementation, this would use text generation models
            result = {
                "type": "text_generated",
                "prompt": prompt,
                "output": f"Response to: {prompt}",
                "confidence": 0.85
            }
            
            # Record interaction
            self._record_interaction(user_id, "text", prompt, result)
            
            return result
        
        else:
            return {"error": f"Unknown text operation: {operation}"}
    
    async def _handle_voice(self, task: Dict, parameters: Dict) -> Dict:
        """Handle voice interface tasks"""
        operation = parameters.get("operation", "recognize")
        
        if operation == "recognize":
            audio_data = parameters.get("audio", b"")
            user_id = parameters.get("user_id", "unknown")
            
            # In a real implementation, this would use speech recognition
            result = {
                "type": "speech_recognized",
                "input": "<audio data>",
                "transcript": "Recognized speech text",
                "confidence": 0.85,
                "language": "en"
            }
            
            # Record interaction
            self._record_interaction(user_id, "voice", "<audio>", result)
            
            return result
        
        elif operation == "synthesize":
            text = parameters.get("text", "")
            user_id = parameters.get("user_id", "unknown")
            
            # In a real implementation, this would use text-to-speech
            result = {
                "type": "speech_synthesized",
                "input": text,
                "audio": "<synthesized audio>",
                "confidence": 0.9
            }
            
            # Record interaction
            self._record_interaction(user_id, "voice", text, result)
            
            return result
        
        else:
            return {"error": f"Unknown voice operation: {operation}"}
    
    async def _handle_visual(self, task: Dict, parameters: Dict) -> Dict:
        """Handle visual interface tasks"""
        operation = parameters.get("operation", "render")
        
        if operation == "render":
            data = parameters.get("data", {})
            user_id = parameters.get("user_id", "unknown")
            
            # In a real implementation, this would use rendering engines
            result = {
                "type": "visual_rendered",
                "input": data,
                "output": "<rendered visual>",
                "format": "3d" if self.modality == InterfaceModality.HOLOGRAPHIC else "2d"
            }
            
            # Record interaction
            self._record_interaction(user_id, "visual", data, result)
            
            return result
        
        elif operation == "recognize":
            image_data = parameters.get("image", b"")
            user_id = parameters.get("user_id", "unknown")
            
            # In a real implementation, this would use computer vision
            result = {
                "type": "visual_recognized",
                "input": "<image data>",
                "objects": [],
                "scenes": [],
                "confidence": 0.75
            }
            
            # Record interaction
            self._record_interaction(user_id, "visual", "<image>", result)
            
            return result
        
        else:
            return {"error": f"Unknown visual operation: {operation}"}
    
    async def _handle_gesture(self, task: Dict, parameters: Dict) -> Dict:
        """Handle gesture interface tasks"""
        operation = parameters.get("operation", "recognize")
        
        if operation == "recognize":
            gesture_data = parameters.get("gesture", {})
            user_id = parameters.get("user_id", "unknown")
            
            # In a real implementation, this would use gesture recognition
            result = {
                "type": "gesture_recognized",
                "input": gesture_data,
                "gesture": "wave",
                "confidence": 0.8,
                "intent": "greeting"
            }
            
            # Record interaction
            self._record_interaction(user_id, "gesture", gesture_data, result)
            
            return result
        
        else:
            return {"error": f"Unknown gesture operation: {operation}"}
    
    async def _handle_touch(self, task: Dict, parameters: Dict) -> Dict:
        """Handle touch interface tasks"""
        operation = parameters.get("operation", "process")
        
        if operation == "process":
            touch_data = parameters.get("touch", {})
            user_id = parameters.get("user_id", "unknown")
            
            # In a real implementation, this would process touch input
            result = {
                "type": "touch_processed",
                "input": touch_data,
                "action": "tap",
                "coordinates": [0, 0],
                "intent": "select"
            }
            
            # Record interaction
            self._record_interaction(user_id, "touch", touch_data, result)
            
            return result
        
        else:
            return {"error": f"Unknown touch operation: {operation}"}
    
    async def _handle_holographic(self, task: Dict, parameters: Dict) -> Dict:
        """Handle holographic interface tasks"""
        operation = parameters.get("operation", "render")
        
        if operation == "render":
            scene_data = parameters.get("scene", {})
            user_id = parameters.get("user_id", "unknown")
            
            # In a real implementation, this would use holographic rendering
            result = {
                "type": "hologram_rendered",
                "input": scene_data,
                "output": "<holographic data>",
                "format": "volumetric",
                "quality": "high"
            }
            
            # Record interaction
            self._record_interaction(user_id, "holographic", scene_data, result)
            
            return result
        
        elif operation == "interact":
            interaction_data = parameters.get("interaction", {})
            user_id = parameters.get("user_id", "unknown")
            
            # In a real implementation, this would handle holographic interaction
            result = {
                "type": "hologram_interaction",
                "input": interaction_data,
                "action": "manipulate",
                "target": "hologram_1",
                "success": True
            }
            
            # Record interaction
            self._record_interaction(user_id, "holographic", interaction_data, result)
            
            return result
        
        else:
            return {"error": f"Unknown holographic operation: {operation}"}
    
    async def _handle_generic(self, task: Dict, parameters: Dict) -> Dict:
        """Handle generic interface tasks"""
        return {
            "type": "generic_response",
            "input": parameters,
            "response": f"Generic interface processing: {self.modality.value}",
            "modality": self.modality.value
        }
    
    def _record_interaction(self, user_id: str, modality: str, input_data: Any, output: Any):
        """Record a user interaction"""
        interaction_id = str(datetime.now().timestamp())
        
        interaction = Interaction(
            interaction_id=interaction_id,
            user_id=user_id,
            modality=modality,
            input=input_data,
            output=output,
            timestamp=datetime.now()
        )
        
        self._interactions[interaction_id] = interaction
        
        # Update user context
        if user_id not in self._user_contexts:
            self._user_contexts[user_id] = UserContext(
                user_id=user_id,
                session_id=str(datetime.now().timestamp())
            )
        
        user_context = self._user_contexts[user_id]
        user_context.interaction_history.append({
            "interaction_id": interaction_id,
            "modality": modality,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update adaptive preferences
        if user_id not in self._adaptive_preferences:
            self._adaptive_preferences[user_id] = {
                "preferred_modality": modality,
                "interaction_count": 0
            }
        
        self._adaptive_preferences[user_id]["interaction_count"] += 1
        self._adaptive_preferences[user_id]["preferred_modality"] = modality
    
    def get_user_context(self, user_id: str) -> Optional[UserContext]:
        """Get the context for a specific user"""
        return self._user_contexts.get(user_id)
    
    def update_user_context(self, user_id: str, updates: Dict) -> bool:
        """Update context for a specific user"""
        if user_id not in self._user_contexts:
            self._user_contexts[user_id] = UserContext(user_id=user_id, session_id=str(datetime.now().timestamp()))
        
        for key, value in updates.items():
            if hasattr(self._user_contexts[user_id], key):
                setattr(self._user_contexts[user_id], key, value)
        
        return True
    
    async def adapt_to_user(self, user_id: str) -> Dict:
        """
        Adapt the interface to a specific user's preferences.
        
        Args:
            user_id: User identifier
            
        Returns:
            Adaptation result
        """
        if user_id not in self._adaptive_preferences:
            return {"status": "no_preferences", "user_id": user_id}
        
        preferences = self._adaptive_preferences[user_id]
        
        # In a real implementation, this would adjust interface behavior
        adaptation = {
            "status": "adapted",
            "user_id": user_id,
            "preferred_modality": preferences.get("preferred_modality", "text"),
            "interaction_count": preferences.get("interaction_count", 0)
        }
        
        return adaptation
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about this interface holon"""
        info = super().get_info()
        info.update({
            "modality": self.modality.value,
            "user_count": len(self._user_contexts),
            "interaction_count": self._interaction_count,
            "successful_interactions": self._successful_interactions
        })
        return info
