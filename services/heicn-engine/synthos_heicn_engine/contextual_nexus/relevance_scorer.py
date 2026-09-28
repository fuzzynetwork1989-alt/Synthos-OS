"""
Context Relevance Scorer - Automatic ranking of context importance

This module provides relevance scoring for context elements, enabling
the HEICN system to prioritize and focus on the most important information.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import structlog
from datetime import datetime
import uuid
import math

logger = structlog.get_logger(__name__)


@dataclass
class RelevanceFactor:
    """A factor that affects relevance scoring"""
    factor_id: str
    name: str
    description: str
    weight: float = 1.0  # 0.0 to 1.0
    function: str = "linear"  # "linear", "logarithmic", "exponential", "step"
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RelevanceScore:
    """A relevance score for a context element"""
    element_id: str
    element_type: str  # "node", "edge", "frame", "context"
    base_score: float = 0.0
    factor_scores: Dict[str, float] = field(default_factory=dict)
    total_score: float = 0.0
    normalized_score: float = 0.0  # 0.0 to 1.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ScoringModel:
    """A scoring model for relevance calculation"""
    model_id: str
    name: str
    description: str
    factors: List[str] = field(default_factory=list)  # List of factor IDs
    weights: Dict[str, float] = field(default_factory=dict)  # factor_id -> weight
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class ContextRelevanceScorer:
    """
    Context Relevance Scorer - Provides relevance scoring for context elements.
    
    This system:
    - Calculates relevance scores for nodes, edges, and context frames
    - Uses multiple factors to determine importance
    - Adapts scoring models based on feedback
    - Provides normalized scores for comparison
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the context relevance scorer.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._default_config()
        
        # Relevance factors
        self._factors: Dict[str, RelevanceFactor] = {}
        
        # Scoring models
        self._models: Dict[str, ScoringModel] = {}
        
        # Score history
        self._score_history: Dict[str, List[RelevanceScore]] = {}  # element_id -> [scores]
        
        # Current scores
        self._current_scores: Dict[str, RelevanceScore] = {}  # element_id -> current score
        
        # Register default factors
        self._register_default_factors()
        
        # Create default model
        self._create_default_model()
        
        logger.info("ContextRelevanceScorer initialized")
    
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            "max_history": 100,
            "default_model": "comprehensive",
            "normalization_method": "min_max",
            "min_score": 0.0,
            "max_score": 100.0
        }
    
    def _register_default_factors(self):
        """Register default relevance factors"""
        # Recency factor - more recent elements are more relevant
        self.add_factor(
            "recency",
            "Recency",
            "More recent elements are more relevant",
            weight=0.8,
            function="exponential",
            parameters={"decay_rate": 0.1}
        )
        
        # Access frequency factor - more frequently accessed elements are more relevant
        self.add_factor(
            "access_frequency",
            "Access Frequency",
            "Elements accessed more frequently are more relevant",
            weight=0.7,
            function="logarithmic",
            parameters={"base": 2}
        )
        
        # Importance factor - explicitly marked importance
        self.add_factor(
            "importance",
            "Importance",
            "Explicitly marked importance level",
            weight=1.0,
            function="linear"
        )
        
        # Confidence factor - higher confidence elements are more relevant
        self.add_factor(
            "confidence",
            "Confidence",
            "Higher confidence elements are more relevant",
            weight=0.6,
            function="linear"
        )
        
        # Centrality factor - more connected elements are more relevant
        self.add_factor(
            "centrality",
            "Centrality",
            "Elements with more connections are more relevant",
            weight=0.5,
            function="logarithmic",
            parameters={"base": 1.5}
        )
        
        # User interest factor - elements matching user interests are more relevant
        self.add_factor(
            "user_interest",
            "User Interest",
            "Elements matching user interests are more relevant",
            weight=0.9,
            function="linear"
        )
        
        # User understanding factor - elements at appropriate understanding level
        self.add_factor(
            "user_understanding",
            "User Understanding",
            "Elements at appropriate understanding level are more relevant",
            weight=0.7,
            function="inverted_u"  # Custom function for optimal understanding level
        )
        
        # Context match factor - elements matching current context are more relevant
        self.add_factor(
            "context_match",
            "Context Match",
            "Elements matching current context are more relevant",
            weight=1.0,
            function="linear"
        )
    
    def _create_default_model(self):
        """Create the default scoring model"""
        model_id = "comprehensive"
        
        model = ScoringModel(
            model_id=model_id,
            name="Comprehensive Scoring",
            description="Uses all available factors for comprehensive relevance scoring",
            factors=list(self._factors.keys()),
            weights={fid: factor.weight for fid, factor in self._factors.items()},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self._models[model_id] = model
        
        logger.info("Default scoring model created", model_id=model_id)
    
    def add_factor(
        self,
        factor_id: str,
        name: str,
        description: str,
        weight: float = 1.0,
        function: str = "linear",
        parameters: Dict[str, Any] = None
    ) -> str:
        """
        Add a relevance factor.
        
        Args:
            factor_id: Unique factor identifier
            name: Factor name
            description: Factor description
            weight: Factor weight (0.0 to 1.0)
            function: Scoring function type
            parameters: Function parameters
            
        Returns:
            Factor ID
        """
        factor = RelevanceFactor(
            factor_id=factor_id,
            name=name,
            description=description,
            weight=weight,
            function=function,
            parameters=parameters or {}
        )
        
        self._factors[factor_id] = factor
        
        logger.info("Relevance factor added", factor_id=factor_id, name=name)
        return factor_id
    
    def get_factor(self, factor_id: str) -> Optional[RelevanceFactor]:
        """Get a relevance factor by ID"""
        return self._factors.get(factor_id)
    
    def get_all_factors(self) -> Dict[str, RelevanceFactor]:
        """Get all relevance factors"""
        return self._factors.copy()
    
    def add_model(
        self,
        model_id: str,
        name: str,
        description: str,
        factors: List[str],
        weights: Dict[str, float] = None
    ) -> str:
        """
        Add a scoring model.
        
        Args:
            model_id: Unique model identifier
            name: Model name
            description: Model description
            factors: List of factor IDs
            weights: Dictionary of factor weights
            
        Returns:
            Model ID
        """
        model = ScoringModel(
            model_id=model_id,
            name=name,
            description=description,
            factors=factors,
            weights=weights or {fid: 1.0 for fid in factors},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self._models[model_id] = model
        
        logger.info("Scoring model added", model_id=model_id, name=name)
        return model_id
    
    def get_model(self, model_id: str) -> Optional[ScoringModel]:
        """Get a scoring model by ID"""
        return self._models.get(model_id)
    
    def get_all_models(self) -> Dict[str, ScoringModel]:
        """Get all scoring models"""
        return self._models.copy()
    
    def set_model_weights(self, model_id: str, weights: Dict[str, float]) -> bool:
        """
        Set the weights for a scoring model.
        
        Args:
            model_id: Model identifier
            weights: Dictionary of factor weights
            
        Returns:
            True if updated successfully
        """
        if model_id not in self._models:
            return False
        
        model = self._models[model_id]
        model.weights = weights.copy()
        model.updated_at = datetime.now()
        
        logger.info("Model weights updated", model_id=model_id)
        return True
    
    def calculate_relevance(
        self,
        element_id: str,
        element_type: str,
        element_data: Dict[str, Any],
        context: Dict[str, Any] = None,
        model_id: str = None
    ) -> RelevanceScore:
        """
        Calculate the relevance score for a context element.
        
        Args:
            element_id: Element identifier
            element_type: Element type
            element_data: Element data
            context: Optional current context
            model_id: Optional model ID (uses default if None)
            
        Returns:
            Relevance score
        """
        model_id = model_id or self.config.get("default_model", "comprehensive")
        
        if model_id not in self._models:
            raise ValueError(f"Model not found: {model_id}")
        
        model = self._models[model_id]
        
        # Calculate base score
        base_score = 0.0
        
        # Calculate factor scores
        factor_scores = {}
        
        for factor_id in model.factors:
            if factor_id not in self._factors:
                continue
            
            factor = self._factors[factor_id]
            weight = model.weights.get(factor_id, factor.weight)
            
            # Get factor value from element data
            factor_value = self._get_factor_value(factor_id, element_data, context)
            
            # Calculate factor score using the specified function
            score = self._apply_factor_function(factor, factor_value)
            
            # Weight the score
            weighted_score = score * weight
            
            factor_scores[factor_id] = weighted_score
            base_score += weighted_score
        
        # Calculate total score (normalized)
        total_score = base_score
        normalized_score = self._normalize_score(total_score, model_id)
        
        # Create score object
        score = RelevanceScore(
            element_id=element_id,
            element_type=element_type,
            base_score=base_score,
            factor_scores=factor_scores,
            total_score=total_score,
            normalized_score=normalized_score,
            timestamp=datetime.now()
        )
        
        # Store score
        self._current_scores[element_id] = score
        
        if element_id not in self._score_history:
            self._score_history[element_id] = []
        self._score_history[element_id].append(score)
        
        # Keep history limited
        if len(self._score_history[element_id]) > self.config.get("max_history", 100):
            self._score_history[element_id] = self._score_history[element_id][-100:]
        
        logger.info(
            "Relevance calculated",
            element_id=element_id,
            element_type=element_type,
            score=normalized_score
        )
        
        return score
    
    def _get_factor_value(self, factor_id: str, element_data: Dict[str, Any], context: Dict[str, Any] = None) -> float:
        """
        Get the value for a factor from element data.
        
        Args:
            factor_id: Factor identifier
            element_data: Element data
            context: Optional current context
            
        Returns:
            Factor value
        """
        factor = self._factors.get(factor_id)
        if not factor:
            return 0.0
        
        # Map factor ID to element data keys
        key_mapping = {
            "recency": "timestamp",
            "access_frequency": "access_count",
            "importance": "importance",
            "confidence": "confidence",
            "centrality": "connection_count",
            "user_interest": "user_interest",
            "user_understanding": "user_understanding",
            "context_match": "context_match"
        }
        
        key = key_mapping.get(factor_id, factor_id)
        
        # Get value from element data
        if key in element_data:
            return float(element_data[key])
        
        # Get value from context
        if context and key in context:
            return float(context[key])
        
        # Default value
        return 0.0
    
    def _apply_factor_function(self, factor: RelevanceFactor, value: float) -> float:
        """
        Apply a factor's function to a value.
        
        Args:
            factor: Relevance factor
            value: Input value
            
        Returns:
            Transformed value
        """
        if factor.function == "linear":
            return value
        
        elif factor.function == "logarithmic":
            base = factor.parameters.get("base", 2)
            if value > 0:
                return math.log(value, base)
            return 0.0
        
        elif factor.function == "exponential":
            decay_rate = factor.parameters.get("decay_rate", 0.1)
            return math.exp(-decay_rate * value)
        
        elif factor.function == "step":
            threshold = factor.parameters.get("threshold", 0.5)
            return 1.0 if value >= threshold else 0.0
        
        elif factor.function == "inverted_u":
            # Optimal point at 0.7
            optimal = factor.parameters.get("optimal", 0.7)
            width = factor.parameters.get("width", 0.3)
            return math.exp(-((value - optimal) / width) ** 2)
        
        else:
            return value
    
    def _normalize_score(self, score: float, model_id: str) -> float:
        """
        Normalize a score to the 0-1 range.
        
        Args:
            score: Raw score
            model_id: Model identifier
            
        Returns:
            Normalized score (0.0 to 1.0)
        """
        method = self.config.get("normalization_method", "min_max")
        min_score = self.config.get("min_score", 0.0)
        max_score = self.config.get("max_score", 100.0)
        
        if method == "min_max":
            if max_score > min_score:
                return max(0.0, min(1.0, (score - min_score) / (max_score - min_score)))
            return 0.5
        
        elif method == "sigmoid":
            return 1.0 / (1.0 + math.exp(-score))
        
        elif method == "tanh":
            return (math.tanh(score) + 1.0) / 2.0
        
        else:
            return max(0.0, min(1.0, score))
    
    def calculate_frame_relevance(
        self,
        frame: Any,
        nodes: Dict[str, Any],
        edges: Dict[str, Any]
    ) -> float:
        """
        Calculate the relevance score for a context frame.
        
        Args:
            frame: Context frame
            nodes: Dictionary of nodes
            edges: Dictionary of edges
            
        Returns:
            Relevance score (0.0 to 1.0)
        """
        if not frame.node_ids and not frame.edge_ids:
            return 0.0
        
        # Calculate average relevance of nodes and edges
        node_scores = []
        edge_scores = []
        
        for node_id in frame.node_ids:
            if node_id in nodes:
                node_score = self.get_current_score(node_id)
                if node_score:
                    node_scores.append(node_score.normalized_score)
        
        for edge_id in frame.edge_ids:
            if edge_id in edges:
                edge_score = self.get_current_score(edge_id)
                if edge_score:
                    edge_scores.append(edge_score.normalized_score)
        
        # Calculate frame relevance as average of node and edge relevance
        all_scores = node_scores + edge_scores
        
        if all_scores:
            return sum(all_scores) / len(all_scores)
        
        return 0.0
    
    def calculate_response_confidence(
        self,
        query: Any,
        relevant_nodes: List[str],
        relevant_edges: List[str],
        nodes: Dict[str, Any],
        edges: Dict[str, Any]
    ) -> float:
        """
        Calculate the confidence score for a context response.
        
        Args:
            query: Context query
            relevant_nodes: List of relevant node IDs
            relevant_edges: List of relevant edge IDs
            nodes: Dictionary of nodes
            edges: Dictionary of edges
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        if not relevant_nodes and not relevant_edges:
            return 0.0
        
        # Calculate confidence based on relevance scores
        node_confidences = []
        edge_confidences = []
        
        for node_id in relevant_nodes:
            if node_id in nodes:
                node_score = self.get_current_score(node_id)
                if node_score:
                    node_confidences.append(node_score.normalized_score)
        
        for edge_id in relevant_edges:
            if edge_id in edges:
                edge_score = self.get_current_score(edge_id)
                if edge_score:
                    edge_confidences.append(edge_score.normalized_score)
        
        # Calculate confidence as average of node and edge confidence
        all_confidences = node_confidences + edge_confidences
        
        if all_confidences:
            # Add query-specific factors
            query_confidence = 0.5  # Base confidence
            
            # If query has specific intent, increase confidence
            if query.intent:
                query_confidence += 0.1
            
            # If query has entities, increase confidence
            if query.entities:
                query_confidence += 0.1
            
            # Combine
            avg_confidence = sum(all_confidences) / len(all_confidences)
            return min(1.0, (avg_confidence * 0.8) + (query_confidence * 0.2))
        
        return 0.0
    
    def get_current_score(self, element_id: str) -> Optional[RelevanceScore]:
        """Get the current relevance score for an element"""
        return self._current_scores.get(element_id)
    
    def get_score_history(self, element_id: str) -> List[RelevanceScore]:
        """Get the score history for an element"""
        return self._score_history.get(element_id, []).copy()
    
    def update_factor_weights(self, model_id: str, factor_weights: Dict[str, float]) -> bool:
        """
        Update factor weights for a model based on feedback.
        
        Args:
            model_id: Model identifier
            factor_weights: Dictionary of factor weight updates
            
        Returns:
            True if updated successfully
        """
        if model_id not in self._models:
            return False
        
        model = self._models[model_id]
        
        for factor_id, weight in factor_weights.items():
            if factor_id in model.weights:
                # Update with moving average
                current_weight = model.weights[factor_id]
                model.weights[factor_id] = (current_weight * 0.9) + (weight * 0.1)
        
        model.updated_at = datetime.now()
        
        logger.info("Factor weights updated", model_id=model_id)
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the relevance scorer.
        
        Returns:
            Statistics dictionary
        """
        return {
            "factor_count": len(self._factors),
            "model_count": len(self._models),
            "score_count": len(self._current_scores),
            "history_count": sum(len(scores) for scores in self._score_history.values())
        }
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the context relevance scorer"""
        return {
            "system_type": "ContextRelevanceScorer",
            "factor_count": len(self._factors),
            "model_count": len(self._models),
            "score_count": len(self._current_scores)
        }
