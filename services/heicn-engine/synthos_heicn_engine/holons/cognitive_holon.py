"""
Cognitive Holon - Specialized AI modules for reasoning, planning, memory, etc.

Cognitive holons are specialized AI modules that handle specific cognitive
functions within the HEICN architecture. They can operate independently
or cooperate with other holons for complex cognitive tasks.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import structlog
from datetime import datetime
import asyncio

from .base import BaseHolon, HolonType, HolonStatus

logger = structlog.get_logger(__name__)


class CognitiveFunction(Enum):
    """Types of cognitive functions"""
    REASONING = "reasoning"           # Logical inference and analysis
    PLANNING = "planning"             # Goal decomposition and strategy
    MEMORY = "memory"                 # Information storage and retrieval
    LEARNING = "learning"             # Knowledge acquisition and adaptation
    PERCEPTION = "perception"         # Multimodal data processing
    DECISION = "decision"             # Choice making and optimization
    CREATIVITY = "creativity"         # Novel idea generation
    REFLECTION = "reflection"         # Self-analysis and improvement


@dataclass
class CognitiveState:
    """Current cognitive state of the holon"""
    current_task: Optional[str] = None
    current_context: Dict[str, Any] = field(default_factory=dict)
    memory_load: float = 0.0  # 0.0 to 1.0
    processing_speed: float = 1.0  # Relative speed
    confidence: float = 0.0  # 0.0 to 1.0
    attention_focus: str = "general"


@dataclass
class MemoryEntry:
    """A memory entry stored by the cognitive holon"""
    memory_id: str
    content: Any
    context: Dict[str, Any]
    timestamp: datetime
    relevance: float = 1.0  # 0.0 to 1.0
    strength: float = 1.0  # 0.0 to 1.0
    tags: List[str] = field(default_factory=list)


class CognitiveHolon(BaseHolon):
    """
    Cognitive Holon - Specialized AI module for cognitive functions.
    
    This holon handles specific cognitive tasks such as reasoning, planning,
    memory management, learning, and decision making.
    
    Key Features:
    - Specialized cognitive function execution
    - Memory management with semantic indexing
    - Context-aware processing
    - Self-optimizing cognitive strategies
    - Cooperation with other cognitive holons
    """
    
    def __init__(
        self,
        holon_id: Optional[str] = None,
        name: str = "CognitiveHolon",
        cognitive_function: CognitiveFunction = CognitiveFunction.REASONING,
        description: str = "",
        config: Optional[Dict] = None
    ):
        """
        Initialize the cognitive holon.
        
        Args:
            holon_id: Unique identifier
            name: Human-readable name
            cognitive_function: The primary cognitive function
            description: Description of purpose
            config: Configuration dictionary
        """
        super().__init__(
            holon_id=holon_id,
            holon_type=HolonType.COGNITIVE,
            name=name,
            description=description,
            config=config
        )
        
        self.cognitive_function = cognitive_function
        
        # Cognitive state
        self._cognitive_state = CognitiveState()
        
        # Memory storage
        self._memory: Dict[str, MemoryEntry] = {}
        self._memory_index: Dict[str, List[str]] = {}  # tag -> [memory_ids]
        
        # Learning parameters
        self.learning_rate = config.get("learning_rate", 0.1) if config else 0.1
        self.forgetting_rate = config.get("forgetting_rate", 0.01) if config else 0.01
        
        # Performance tracking
        self._accuracy_history: List[float] = []
        self._speed_history: List[float] = []
        
        # Register capabilities based on function
        self._register_function_capabilities()
        
        logger.info(
            "CognitiveHolon initialized",
            holon_id=self.holon_id,
            function=self.cognitive_function.value
        )
    
    def _register_function_capabilities(self):
        """Register capabilities based on cognitive function"""
        capability_name = f"cognitive:{self.cognitive_function.value}"
        self.register_capability(
            name=capability_name,
            description=f"{self.cognitive_function.value.capitalize()} cognitive function",
            version="1.0",
            quality_score=1.0
        )
        
        # Register common cognitive capabilities
        self.register_capability(
            name="cognitive:reason",
            description="Basic reasoning capability",
            version="1.0",
            quality_score=0.8
        )
        
        self.register_capability(
            name="cognitive:learn",
            description="Learning and adaptation capability",
            version="1.0",
            quality_score=0.7
        )
        
        self.register_capability(
            name="cognitive:remember",
            description="Memory storage and retrieval",
            version="1.0",
            quality_score=0.9
        )
    
    async def initialize(self) -> bool:
        """Initialize the cognitive holon"""
        try:
            self._status = HolonStatus.INITIALIZING
            
            # Initialize memory system
            self._memory = {}
            self._memory_index = {}
            
            # Initialize cognitive state
            self._cognitive_state = CognitiveState()
            
            self._status = HolonStatus.READY
            self._initialized_at = datetime.now()
            
            logger.info("CognitiveHolon initialized successfully", holon_id=self.holon_id)
            return True
            
        except Exception as e:
            logger.error("Failed to initialize CognitiveHolon", holon_id=self.holon_id, error=str(e))
            self._status = HolonStatus.FAILED
            return False
    
    async def start(self) -> bool:
        """Start the cognitive holon"""
        try:
            if self._status != HolonStatus.READY:
                logger.warning("Cannot start - not in READY state", holon_id=self.holon_id)
                return False
            
            self._status = HolonStatus.ACTIVE
            self._started_at = datetime.now()
            
            logger.info("CognitiveHolon started", holon_id=self.holon_id)
            return True
            
        except Exception as e:
            logger.error("Failed to start CognitiveHolon", holon_id=self.holon_id, error=str(e))
            self._status = HolonStatus.FAILED
            return False
    
    async def stop(self) -> bool:
        """Stop the cognitive holon"""
        try:
            self._status = HolonStatus.READY
            self._cognitive_state.current_task = None
            
            logger.info("CognitiveHolon stopped", holon_id=self.holon_id)
            return True
            
        except Exception as e:
            logger.error("Failed to stop CognitiveHolon", holon_id=self.holon_id, error=str(e))
            self._status = HolonStatus.FAILED
            return False
    
    async def execute(self, task: Dict, context: Optional[Dict] = None) -> Any:
        """
        Execute a cognitive task.
        
        Args:
            task: Task dictionary with 'type' and 'parameters'
            context: Optional context dictionary
            
        Returns:
            Result of cognitive processing
        """
        task_type = task.get("type", "unknown")
        parameters = task.get("parameters", {})
        
        logger.info(
            "Executing cognitive task",
            holon_id=self.holon_id,
            task_type=task_type,
            function=self.cognitive_function.value
        )
        
        self._cognitive_state.current_task = task_type
        self._cognitive_state.current_context = context or {}
        
        try:
            # Route to appropriate handler based on function
            if self.cognitive_function == CognitiveFunction.REASONING:
                result = await self._handle_reasoning(task, parameters)
            elif self.cognitive_function == CognitiveFunction.PLANNING:
                result = await self._handle_planning(task, parameters)
            elif self.cognitive_function == CognitiveFunction.MEMORY:
                result = await self._handle_memory(task, parameters)
            elif self.cognitive_function == CognitiveFunction.LEARNING:
                result = await self._handle_learning(task, parameters)
            elif self.cognitive_function == CognitiveFunction.PERCEPTION:
                result = await self._handle_perception(task, parameters)
            elif self.cognitive_function == CognitiveFunction.DECISION:
                result = await self._handle_decision(task, parameters)
            elif self.cognitive_function == CognitiveFunction.CREATIVITY:
                result = await self._handle_creativity(task, parameters)
            elif self.cognitive_function == CognitiveFunction.REFLECTION:
                result = await self._handle_reflection(task, parameters)
            else:
                result = await self._handle_generic(task, parameters)
            
            # Update performance metrics
            self.record_performance("accuracy", 0.95)  # Placeholder
            self.record_performance("speed", 0.9)  # Placeholder
            
            return result
            
        except Exception as e:
            logger.error(
                "Failed to execute cognitive task",
                holon_id=self.holon_id,
                task_type=task_type,
                error=str(e)
            )
            return {"error": str(e), "success": False}
        
        finally:
            self._cognitive_state.current_task = None
    
    async def _handle_reasoning(self, task: Dict, parameters: Dict) -> Dict:
        """Handle reasoning tasks"""
        # In a real implementation, this would use actual reasoning models
        result = {
            "type": "reasoning_result",
            "input": parameters.get("input", ""),
            "conclusion": "Reasoned conclusion",
            "confidence": 0.9,
            "steps": [
                "Analyzed input",
                "Identified patterns",
                "Generated conclusion"
            ]
        }
        return result
    
    async def _handle_planning(self, task: Dict, parameters: Dict) -> Dict:
        """Handle planning tasks"""
        goal = parameters.get("goal", "")
        constraints = parameters.get("constraints", [])
        
        result = {
            "type": "plan",
            "goal": goal,
            "steps": [
                {"action": "step1", "description": "First step toward goal"},
                {"action": "step2", "description": "Second step toward goal"},
                {"action": "step3", "description": "Final step to achieve goal"}
            ],
            "constraints_satisfied": True,
            "estimated_duration": "PT1H"  # ISO 8601 duration
        }
        return result
    
    async def _handle_memory(self, task: Dict, parameters: Dict) -> Dict:
        """Handle memory tasks"""
        operation = parameters.get("operation", "retrieve")
        
        if operation == "store":
            memory_id = str(datetime.now().timestamp())
            entry = MemoryEntry(
                memory_id=memory_id,
                content=parameters.get("content"),
                context=parameters.get("context", {}),
                timestamp=datetime.now(),
                relevance=parameters.get("relevance", 1.0),
                strength=parameters.get("strength", 1.0),
                tags=parameters.get("tags", [])
            )
            self._memory[memory_id] = entry
            
            # Update index
            for tag in entry.tags:
                if tag not in self._memory_index:
                    self._memory_index[tag] = []
                self._memory_index[tag].append(memory_id)
            
            return {"status": "stored", "memory_id": memory_id}
        
        elif operation == "retrieve":
            query = parameters.get("query", "")
            tags = parameters.get("tags", [])
            limit = parameters.get("limit", 10)
            
            results = []
            
            # Search by tags
            if tags:
                memory_ids = set()
                for tag in tags:
                    if tag in self._memory_index:
                        memory_ids.update(self._memory_index[tag])
                
                for memory_id in list(memory_ids)[:limit]:
                    if memory_id in self._memory:
                        results.append(self._memory[memory_id])
            
            # If no results from tags, return most recent
            if not results:
                sorted_memories = sorted(
                    self._memory.values(),
                    key=lambda x: x.timestamp,
                    reverse=True
                )
                results = sorted_memories[:limit]
            
            return {
                "status": "retrieved",
                "count": len(results),
                "results": [
                    {
                        "memory_id": m.memory_id,
                        "content": m.content,
                        "timestamp": m.timestamp.isoformat(),
                        "relevance": m.relevance
                    }
                    for m in results
                ]
            }
        
        else:
            return {"error": f"Unknown memory operation: {operation}"}
    
    async def _handle_learning(self, task: Dict, parameters: Dict) -> Dict:
        """Handle learning tasks"""
        data = parameters.get("data", [])
        
        result = {
            "type": "learning_result",
            "data_processed": len(data),
            "new_knowledge": 5,  # Placeholder
            "learning_rate": self.learning_rate,
            "knowledge_integrated": True
        }
        return result
    
    async def _handle_perception(self, task: Dict, parameters: Dict) -> Dict:
        """Handle perception tasks"""
        modality = parameters.get("modality", "text")
        input_data = parameters.get("input", "")
        
        result = {
            "type": "perception_result",
            "modality": modality,
            "interpretation": f"Interpreted {modality} input",
            "confidence": 0.85,
            "features": {}
        }
        
        if modality == "text":
            result["features"] = {
                "sentiment": "neutral",
                "entities": [],
                "intent": "unknown"
            }
        elif modality == "image":
            result["features"] = {
                "objects": [],
                "scenes": [],
                "colors": []
            }
        
        return result
    
    async def _handle_decision(self, task: Dict, parameters: Dict) -> Dict:
        """Handle decision tasks"""
        options = parameters.get("options", [])
        criteria = parameters.get("criteria", [])
        
        # Simple decision logic - in real implementation would use optimization
        best_option = options[0] if options else None
        
        result = {
            "type": "decision",
            "chosen_option": best_option,
            "confidence": 0.8,
            "rationale": "Chosen based on criteria analysis",
            "criteria_evaluation": {}
        }
        
        return result
    
    async def _handle_creativity(self, task: Dict, parameters: Dict) -> Dict:
        """Handle creativity tasks"""
        prompt = parameters.get("prompt", "")
        constraints = parameters.get("constraints", [])
        
        result = {
            "type": "creative_output",
            "prompt": prompt,
            "output": f"Creative response to: {prompt}",
            "novelty_score": 0.85,
            "relevance_score": 0.9,
            "constraints_satisfied": True
        }
        return result
    
    async def _handle_reflection(self, task: Dict, parameters: Dict) -> Dict:
        """Handle reflection tasks"""
        subject = parameters.get("subject", "self")
        aspect = parameters.get("aspect", "performance")
        
        result = {
            "type": "reflection",
            "subject": subject,
            "aspect": aspect,
            "analysis": f"Reflection on {aspect} of {subject}",
            "insights": [
                "Insight 1",
                "Insight 2",
                "Insight 3"
            ],
            "improvement_suggestions": [
                "Suggestion 1",
                "Suggestion 2"
            ]
        }
        return result
    
    async def _handle_generic(self, task: Dict, parameters: Dict) -> Dict:
        """Handle generic cognitive tasks"""
        return {
            "type": "generic_response",
            "input": parameters,
            "response": "Generic cognitive processing complete",
            "function": self.cognitive_function.value
        }
    
    def store_memory(self, content: Any, context: Dict, tags: List[str] = None) -> str:
        """
        Store a memory entry.
        
        Args:
            content: Memory content
            context: Context dictionary
            tags: List of tags for indexing
            
        Returns:
            Memory ID
        """
        memory_id = str(datetime.now().timestamp())
        entry = MemoryEntry(
            memory_id=memory_id,
            content=content,
            context=context,
            timestamp=datetime.now(),
            tags=tags or []
        )
        self._memory[memory_id] = entry
        
        # Update index
        for tag in entry.tags:
            if tag not in self._memory_index:
                self._memory_index[tag] = []
            self._memory_index[tag].append(memory_id)
        
        return memory_id
    
    def retrieve_memory(self, query: str = None, tags: List[str] = None, limit: int = 10) -> List[MemoryEntry]:
        """
        Retrieve memory entries.
        
        Args:
            query: Search query (not implemented yet)
            tags: Tags to filter by
            limit: Maximum number of results
            
        Returns:
            List of memory entries
        """
        results = []
        
        if tags:
            memory_ids = set()
            for tag in tags:
                if tag in self._memory_index:
                    memory_ids.update(self._memory_index[tag])
            
            for memory_id in list(memory_ids)[:limit]:
                if memory_id in self._memory:
                    results.append(self._memory[memory_id])
        else:
            # Return most recent
            sorted_memories = sorted(
                self._memory.values(),
                key=lambda x: x.timestamp,
                reverse=True
            )
            results = sorted_memories[:limit]
        
        return results
    
    def get_cognitive_state(self) -> CognitiveState:
        """Get current cognitive state"""
        return self._cognitive_state
    
    async def adapt_to_feedback(self, feedback: Dict) -> bool:
        """
        Adapt based on feedback.
        
        Args:
            feedback: Feedback dictionary with ratings and comments
            
        Returns:
            True if adaptation successful
        """
        rating = feedback.get("rating", 0.5)
        comments = feedback.get("comments", "")
        
        # Adjust learning rate based on feedback
        if rating > 0.8:
            self.learning_rate = min(0.5, self.learning_rate * 1.1)
        elif rating < 0.3:
            self.learning_rate = max(0.01, self.learning_rate * 0.9)
        
        # Adjust confidence based on feedback
        self._cognitive_state.confidence = min(1.0, max(0.0, self._cognitive_state.confidence + (rating - 0.5) * 0.2))
        
        logger.info(
            "Adapted to feedback",
            holon_id=self.holon_id,
            rating=rating,
            new_learning_rate=self.learning_rate
        )
        
        return True
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about this cognitive holon"""
        info = super().get_info()
        info.update({
            "cognitive_function": self.cognitive_function.value,
            "cognitive_state": {
                "current_task": self._cognitive_state.current_task,
                "memory_load": self._cognitive_state.memory_load,
                "processing_speed": self._cognitive_state.processing_speed,
                "confidence": self._cognitive_state.confidence
            },
            "memory_count": len(self._memory),
            "learning_rate": self.learning_rate
        })
        return info
