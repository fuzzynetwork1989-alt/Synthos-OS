"""
Contextual Nexus Engine - Core system for building and maintaining personalized knowledge graphs

This engine integrates all contextual nexus components to provide comprehensive
context-aware intelligence for the HEICN architecture.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import structlog
from datetime import datetime
import asyncio
import uuid

from .individual_context import IndividualContextModel
from .cross_context import CrossContextLearner
from .dynamic_updater import DynamicContextUpdater
from .relevance_scorer import ContextRelevanceScorer

logger = structlog.get_logger(__name__)


@dataclass
class KnowledgeNode:
    """A node in the knowledge graph"""
    node_id: str
    concept: str
    description: str
    type: str  # "concept", "entity", "relationship", "event", "fact"
    properties: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.5  # 0.0 to 1.0
    importance: float = 0.5  # 0.0 to 1.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    related_nodes: List[str] = field(default_factory=list)  # List of node IDs


@dataclass
class KnowledgeEdge:
    """An edge between nodes in the knowledge graph"""
    edge_id: str
    source: str  # Node ID
    target: str  # Node ID
    relationship: str
    strength: float = 0.5  # 0.0 to 1.0
    confidence: float = 0.5  # 0.0 to 1.0
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ContextFrame:
    """A frame of context for a specific situation"""
    frame_id: str
    name: str
    description: str
    node_ids: List[str] = field(default_factory=list)
    edge_ids: List[str] = field(default_factory=list)
    relevance_score: float = 0.0  # 0.0 to 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    user_id: Optional[str] = None


@dataclass
class ContextQuery:
    """A query for context information"""
    query_id: str
    user_id: Optional[str] = None
    intent: Optional[str] = None
    entities: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ContextResponse:
    """Response to a context query"""
    response_id: str
    query_id: str
    relevant_nodes: List[str] = field(default_factory=list)
    relevant_edges: List[str] = field(default_factory=list)
    context_frame: Optional[ContextFrame] = None
    confidence: float = 0.0
    explanation: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


class ContextualNexusEngine:
    """
    Contextual Nexus Engine - Core system for building and maintaining
    personalized knowledge graphs in HEICN.
    
    This engine:
    - Maintains individual context models for each user
    - Enables cross-context learning between domains
    - Dynamically updates context based on new interactions
    - Scores and ranks context relevance
    - Provides context-aware query responses
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the contextual nexus engine.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._default_config()
        
        # Initialize sub-components
        self.individual_context = IndividualContextModel(self.config.get("individual_context_config", {}))
        self.cross_context = CrossContextLearner(self.config.get("cross_context_config", {}))
        self.dynamic_updater = DynamicContextUpdater(self.config.get("dynamic_updater_config", {}))
        self.relevance_scorer = ContextRelevanceScorer(self.config.get("relevance_scorer_config", {}))
        
        # Knowledge graph storage
        self._nodes: Dict[str, KnowledgeNode] = {}
        self._edges: Dict[str, KnowledgeEdge] = {}
        
        # Context frames
        self._frames: Dict[str, ContextFrame] = {}
        
        # User contexts
        self._user_contexts: Dict[str, Dict] = {}  # user_id -> context data
        
        # Query tracking
        self._query_history: List[ContextQuery] = []
        self._response_history: List[ContextResponse] = []
        
        # Performance metrics
        self._query_count: int = 0
        self._successful_queries: int = 0
        
        logger.info("ContextualNexusEngine initialized")
    
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            "max_nodes": 10000,
            "max_edges": 50000,
            "max_frames": 1000,
            "query_history_size": 1000,
            "response_history_size": 1000,
            "individual_context_config": {},
            "cross_context_config": {},
            "dynamic_updater_config": {},
            "relevance_scorer_config": {}
        }
    
    def add_node(
        self,
        concept: str,
        description: str = "",
        node_type: str = "concept",
        properties: Dict[str, Any] = None,
        confidence: float = 0.5,
        importance: float = 0.5
    ) -> str:
        """
        Add a node to the knowledge graph.
        
        Args:
            concept: Concept name
            description: Node description
            node_type: Node type
            properties: Node properties
            confidence: Confidence level (0.0 to 1.0)
            importance: Importance level (0.0 to 1.0)
            
        Returns:
            Node ID
        """
        node_id = str(uuid.uuid4())
        
        node = KnowledgeNode(
            node_id=node_id,
            concept=concept,
            description=description,
            type=node_type,
            properties=properties or {},
            confidence=confidence,
            importance=importance,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self._nodes[node_id] = node
        
        # Keep within limits
        if len(self._nodes) > self.config.get("max_nodes", 10000):
            # Remove least important node
            least_important = min(self._nodes.keys(), key=lambda x: self._nodes[x].importance)
            del self._nodes[least_important]
        
        logger.info("Node added", node_id=node_id, concept=concept, type=node_type)
        return node_id
    
    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        """Get a node by ID"""
        return self._nodes.get(node_id)
    
    def update_node(
        self,
        node_id: str,
        updates: Dict[str, Any]
    ) -> bool:
        """
        Update a node in the knowledge graph.
        
        Args:
            node_id: Node identifier
            updates: Dictionary of updates
            
        Returns:
            True if updated successfully
        """
        if node_id not in self._nodes:
            return False
        
        node = self._nodes[node_id]
        
        for key, value in updates.items():
            if hasattr(node, key):
                setattr(node, key, value)
        
        node.updated_at = datetime.now()
        
        logger.info("Node updated", node_id=node_id)
        return True
    
    def add_edge(
        self,
        source: str,
        target: str,
        relationship: str,
        strength: float = 0.5,
        confidence: float = 0.5,
        properties: Dict[str, Any] = None
    ) -> str:
        """
        Add an edge between nodes in the knowledge graph.
        
        Args:
            source: Source node ID
            target: Target node ID
            relationship: Relationship type
            strength: Edge strength (0.0 to 1.0)
            confidence: Edge confidence (0.0 to 1.0)
            properties: Edge properties
            
        Returns:
            Edge ID
        """
        edge_id = str(uuid.uuid4())
        
        edge = KnowledgeEdge(
            edge_id=edge_id,
            source=source,
            target=target,
            relationship=relationship,
            strength=strength,
            confidence=confidence,
            properties=properties or {},
            created_at=datetime.now()
        )
        
        self._edges[edge_id] = edge
        
        # Update node relationships
        if source in self._nodes:
            if edge_id not in self._nodes[source].related_nodes:
                self._nodes[source].related_nodes.append(edge_id)
        if target in self._nodes:
            if edge_id not in self._nodes[target].related_nodes:
                self._nodes[target].related_nodes.append(edge_id)
        
        # Keep within limits
        if len(self._edges) > self.config.get("max_edges", 50000):
            # Remove weakest edge
            weakest = min(self._edges.keys(), key=lambda x: self._edges[x].strength)
            del self._edges[weakest]
        
        logger.info("Edge added", edge_id=edge_id, source=source, target=target, relationship=relationship)
        return edge_id
    
    def get_edge(self, edge_id: str) -> Optional[KnowledgeEdge]:
        """Get an edge by ID"""
        return self._edges.get(edge_id)
    
    def remove_edge(self, edge_id: str) -> bool:
        """
        Remove an edge from the knowledge graph.
        
        Args:
            edge_id: Edge identifier
            
        Returns:
            True if removed successfully
        """
        if edge_id not in self._edges:
            return False
        
        edge = self._edges[edge_id]
        
        # Remove from node relationships
        if edge.source in self._nodes:
            if edge_id in self._nodes[edge.source].related_nodes:
                self._nodes[edge.source].related_nodes.remove(edge_id)
        if edge.target in self._nodes:
            if edge_id in self._nodes[edge.target].related_nodes:
                self._nodes[edge.target].related_nodes.remove(edge_id)
        
        del self._edges[edge_id]
        
        logger.info("Edge removed", edge_id=edge_id)
        return True
    
    def create_context_frame(
        self,
        name: str,
        description: str = "",
        node_ids: List[str] = None,
        edge_ids: List[str] = None,
        user_id: Optional[str] = None
    ) -> str:
        """
        Create a context frame from nodes and edges.
        
        Args:
            name: Frame name
            description: Frame description
            node_ids: List of node IDs
            edge_ids: List of edge IDs
            user_id: Optional user ID
            
        Returns:
            Frame ID
        """
        frame_id = str(uuid.uuid4())
        
        frame = ContextFrame(
            frame_id=frame_id,
            name=name,
            description=description,
            node_ids=node_ids or [],
            edge_ids=edge_ids or [],
            timestamp=datetime.now(),
            user_id=user_id
        )
        
        # Calculate relevance score
        frame.relevance_score = self.relevance_scorer.calculate_frame_relevance(
            frame, self._nodes, self._edges
        )
        
        self._frames[frame_id] = frame
        
        # Keep within limits
        if len(self._frames) > self.config.get("max_frames", 1000):
            # Remove least relevant frame
            least_relevant = min(self._frames.keys(), key=lambda x: self._frames[x].relevance_score)
            del self._frames[least_relevant]
        
        logger.info("Context frame created", frame_id=frame_id, name=name)
        return frame_id
    
    def get_frame(self, frame_id: str) -> Optional[ContextFrame]:
        """Get a context frame by ID"""
        return self._frames.get(frame_id)
    
    def get_frames_by_user(self, user_id: str) -> List[ContextFrame]:
        """Get all context frames for a specific user"""
        return [frame for frame in self._frames.values() if frame.user_id == user_id]
    
    def query_context(
        self,
        query: str = None,
        user_id: Optional[str] = None,
        intent: Optional[str] = None,
        entities: List[str] = None,
        constraints: Dict[str, Any] = None
    ) -> ContextResponse:
        """
        Query the knowledge graph for context information.
        
        Args:
            query: Natural language query
            user_id: Optional user ID for personalization
            intent: Optional intent
            entities: List of entities to focus on
            constraints: Query constraints
            
        Returns:
            Context response
        """
        query_id = str(uuid.uuid4())
        
        # Create query object
        context_query = ContextQuery(
            query_id=query_id,
            user_id=user_id,
            intent=intent,
            entities=entities or [],
            constraints=constraints or {},
            timestamp=datetime.now()
        )
        
        self._query_count += 1
        self._query_history.append(context_query)
        
        # Keep history limited
        if len(self._query_history) > self.config.get("query_history_size", 1000):
            self._query_history = self._query_history[-1000:]
        
        # Process query
        response = self._process_query(context_query)
        response.query_id = query_id
        
        self._response_history.append(response)
        self._successful_queries += 1
        
        # Keep history limited
        if len(self._response_history) > self.config.get("response_history_size", 1000):
            self._response_history = self._response_history[-1000:]
        
        logger.info(
            "Context query processed",
            query_id=query_id,
            user_id=user_id,
            node_count=len(response.relevant_nodes),
            edge_count=len(response.relevant_edges)
        )
        
        return response
    
    def _process_query(self, query: ContextQuery) -> ContextResponse:
        """
        Process a context query and generate a response.
        
        Args:
            query: Context query
            
        Returns:
            Context response
        """
        # Find relevant nodes
        relevant_nodes = []
        relevant_edges = []
        
        # Search by entities
        for entity in query.entities:
            # Find nodes matching the entity
            for node_id, node in self._nodes.items():
                if (entity.lower() in node.concept.lower() or 
                    entity.lower() in node.description.lower()):
                    relevant_nodes.append(node_id)
        
        # If no entities, search by intent
        if not relevant_nodes and query.intent:
            for node_id, node in self._nodes.items():
                if query.intent.lower() in node.concept.lower():
                    relevant_nodes.append(node_id)
        
        # If still no nodes, return most important nodes
        if not relevant_nodes:
            relevant_nodes = sorted(
                self._nodes.keys(),
                key=lambda x: self._nodes[x].importance,
                reverse=True
            )[:10]
        
        # Find relevant edges between nodes
        node_set = set(relevant_nodes)
        for edge_id, edge in self._edges.items():
            if edge.source in node_set and edge.target in node_set:
                relevant_edges.append(edge_id)
        
        # Create a context frame
        frame_id = self.create_context_frame(
            name=f"Query Response: {query.query_id}",
            description=f"Context for query: {query.intent or query.query or 'unknown'}",
            node_ids=relevant_nodes,
            edge_ids=relevant_edges,
            user_id=query.user_id
        )
        
        # Get the frame
        frame = self._frames.get(frame_id)
        
        # Calculate confidence
        confidence = self.relevance_scorer.calculate_response_confidence(
            query, relevant_nodes, relevant_edges, self._nodes, self._edges
        )
        
        # Generate explanation
        explanation = self._generate_explanation(query, relevant_nodes, relevant_edges)
        
        return ContextResponse(
            response_id=str(uuid.uuid4()),
            query_id=query.query_id,
            relevant_nodes=relevant_nodes,
            relevant_edges=relevant_edges,
            context_frame=frame,
            confidence=confidence,
            explanation=explanation,
            timestamp=datetime.now()
        )
    
    def _generate_explanation(
        self,
        query: ContextQuery,
        relevant_nodes: List[str],
        relevant_edges: List[str]
    ) -> str:
        """Generate a natural language explanation of the context response"""
        parts = []
        
        # Explain nodes
        if relevant_nodes:
            node_concepts = [self._nodes[nid].concept for nid in relevant_nodes[:5]]
            parts.append(f"Found relevant concepts: {', '.join(node_concepts)}")
        
        # Explain edges
        if relevant_edges:
            edge_relationships = [self._edges[eid].relationship for eid in relevant_edges[:5]]
            parts.append(f"Found relationships: {', '.join(edge_relationships)}")
        
        # Add confidence note
        parts.append("Context confidence is based on knowledge graph relevance and recency.")
        
        return " ".join(parts)
    
    def update_user_context(
        self,
        user_id: str,
        interaction_data: Dict[str, Any]
    ) -> bool:
        """
        Update the context for a specific user based on new interaction.
        
        Args:
            user_id: User identifier
            interaction_data: Interaction data
            
        Returns:
            True if updated successfully
        """
        # Update individual context model
        success = self.individual_context.update_user_context(user_id, interaction_data)
        
        # Update dynamic context
        self.dynamic_updater.update_from_interaction(user_id, interaction_data)
        
        # Update knowledge graph based on new information
        self._update_knowledge_graph_from_interaction(user_id, interaction_data)
        
        logger.info("User context updated", user_id=user_id)
        return success
    
    def _update_knowledge_graph_from_interaction(
        self,
        user_id: str,
        interaction_data: Dict[str, Any]
    ):
        """Update the knowledge graph based on user interaction"""
        # Extract concepts from interaction
        concepts = interaction_data.get("concepts", [])
        entities = interaction_data.get("entities", [])
        relationships = interaction_data.get("relationships", [])
        
        # Add new nodes for concepts and entities
        for concept in concepts:
            if not any(concept.lower() in node.concept.lower() for node in self._nodes.values()):
                self.add_node(
                    concept=concept,
                    description=interaction_data.get("description", ""),
                    node_type="concept",
                    confidence=interaction_data.get("confidence", 0.5)
                )
        
        for entity in entities:
            if not any(entity.lower() in node.concept.lower() for node in self._nodes.values()):
                self.add_node(
                    concept=entity,
                    node_type="entity",
                    confidence=interaction_data.get("confidence", 0.5)
                )
        
        # Add edges for relationships
        for rel in relationships:
            source = rel.get("source")
            target = rel.get("target")
            relationship = rel.get("type", "related")
            
            # Find or create source node
            source_node_id = None
            for node_id, node in self._nodes.items():
                if source.lower() in node.concept.lower():
                    source_node_id = node_id
                    break
            if not source_node_id:
                source_node_id = self.add_node(concept=source, node_type="entity")
            
            # Find or create target node
            target_node_id = None
            for node_id, node in self._nodes.items():
                if target.lower() in node.concept.lower():
                    target_node_id = node_id
                    break
            if not target_node_id:
                target_node_id = self.add_node(concept=target, node_type="entity")
            
            # Add edge
            self.add_edge(
                source=source_node_id,
                target=target_node_id,
                relationship=relationship,
                confidence=rel.get("confidence", 0.5)
            )
    
    def enable_cross_context_learning(self, enable: bool = True) -> bool:
        """
        Enable or disable cross-context learning.
        
        Args:
            enable: Whether to enable
            
        Returns:
            Previous state
        """
        previous = self.cross_context.enabled
        self.cross_context.enabled = enable
        return previous
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the contextual nexus engine.
        
        Returns:
            Statistics dictionary
        """
        return {
            "node_count": len(self._nodes),
            "edge_count": len(self._edges),
            "frame_count": len(self._frames),
            "user_context_count": len(self._user_contexts),
            "query_count": self._query_count,
            "successful_queries": self._successful_queries,
            "individual_context_stats": self.individual_context.get_statistics(),
            "cross_context_stats": self.cross_context.get_statistics(),
            "relevance_scorer_stats": self.relevance_scorer.get_statistics()
        }
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the contextual nexus engine"""
        return {
            "engine_type": "ContextualNexusEngine",
            "node_count": len(self._nodes),
            "edge_count": len(self._edges),
            "frame_count": len(self._frames),
            "query_count": self._query_count,
            "user_context_count": len(self._user_contexts)
        }
