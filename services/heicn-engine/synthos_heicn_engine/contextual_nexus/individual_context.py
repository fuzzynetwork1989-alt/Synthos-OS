"""
Individual Context Model - Evolving representations of each user's knowledge and preferences

This module maintains personalized knowledge graphs and context models for each user,
enabling the HEICN system to provide tailored experiences based on individual interactions.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import structlog
from datetime import datetime
import uuid

logger = structlog.get_logger(__name__)


@dataclass
class UserProfile:
    """Profile information for a user"""
    user_id: str
    name: Optional[str] = None
    preferences: Dict[str, Any] = field(default_factory=dict)
    interests: List[str] = field(default_factory=list)
    expertise: List[str] = field(default_factory=list)
    learning_style: str = "visual"  # visual, auditory, kinesthetic, reading
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class InteractionHistory:
    """History of user interactions"""
    user_id: str
    interactions: List[Dict[str, Any]] = field(default_factory=list)
    patterns: Dict[str, Any] = field(default_factory=dict)  # Detected patterns
    trends: Dict[str, Any] = field(default_factory=dict)  # Identified trends


@dataclass
class PersonalKnowledgeNode:
    """A node in the user's personal knowledge graph"""
    node_id: str
    concept: str
    user_understanding: float = 0.5  # 0.0 to 1.0 - how well user understands
    user_interest: float = 0.5  # 0.0 to 1.0 - user's interest level
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    personal_notes: str = ""
    tags: List[str] = field(default_factory=list)


@dataclass
class ContextPreference:
    """A user's preference for a specific context"""
    context_id: str
    preference_score: float = 0.5  # 0.0 to 1.0
    usage_count: int = 0
    last_used: datetime = field(default_factory=datetime.now)
    feedback: List[Dict[str, Any]] = field(default_factory=list)


class IndividualContextModel:
    """
    Individual Context Model - Maintains personalized knowledge graphs
    and context models for each user.
    
    This model:
    - Tracks each user's knowledge and preferences
    - Builds personal knowledge graphs
    - Identifies patterns in user behavior
    - Adapts responses based on individual context
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the individual context model.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._default_config()
        
        # User profiles
        self._profiles: Dict[str, UserProfile] = {}
        
        # Interaction histories
        self._histories: Dict[str, InteractionHistory] = {}
        
        # Personal knowledge graphs
        self._knowledge_graphs: Dict[str, Dict[str, PersonalKnowledgeNode]] = {}
        
        # Context preferences
        self._context_preferences: Dict[str, Dict[str, ContextPreference]] = {}
        
        # User statistics
        self._user_stats: Dict[str, Dict[str, Any]] = {}
        
        logger.info("IndividualContextModel initialized")
    
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            "max_interaction_history": 1000,
            "max_knowledge_nodes_per_user": 5000,
            "learning_forgetting_rate": 0.01,
            "interest_decay_rate": 0.005
        }
    
    def create_user_profile(
        self,
        user_id: str,
        name: Optional[str] = None
    ) -> UserProfile:
        """
        Create a user profile.
        
        Args:
            user_id: User identifier
            name: Optional user name
            
        Returns:
            User profile
        """
        profile = UserProfile(
            user_id=user_id,
            name=name,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self._profiles[user_id] = profile
        self._histories[user_id] = InteractionHistory(user_id=user_id)
        self._knowledge_graphs[user_id] = {}
        self._context_preferences[user_id] = {}
        self._user_stats[user_id] = {
            "total_interactions": 0,
            "first_interaction": datetime.now(),
            "last_interaction": datetime.now(),
            "knowledge_nodes": 0,
            "context_preferences": 0
        }
        
        logger.info("User profile created", user_id=user_id)
        return profile
    
    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get a user profile"""
        return self._profiles.get(user_id)
    
    def update_user_profile(
        self,
        user_id: str,
        updates: Dict[str, Any]
    ) -> bool:
        """
        Update a user profile.
        
        Args:
            user_id: User identifier
            updates: Dictionary of updates
            
        Returns:
            True if updated successfully
        """
        if user_id not in self._profiles:
            return False
        
        profile = self._profiles[user_id]
        
        for key, value in updates.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        profile.updated_at = datetime.now()
        
        logger.info("User profile updated", user_id=user_id)
        return True
    
    def record_interaction(
        self,
        user_id: str,
        interaction: Dict[str, Any]
    ) -> str:
        """
        Record a user interaction.
        
        Args:
            user_id: User identifier
            interaction: Interaction data
            
        Returns:
            Interaction ID
        """
        if user_id not in self._histories:
            self.create_user_profile(user_id)
        
        interaction_id = str(uuid.uuid4())
        interaction["interaction_id"] = interaction_id
        interaction["timestamp"] = datetime.now()
        
        history = self._histories[user_id]
        history.interactions.append(interaction)
        
        # Keep history limited
        if len(history.interactions) > self.config.get("max_interaction_history", 1000):
            history.interactions = history.interactions[-1000:]
        
        # Update statistics
        self._user_stats[user_id]["total_interactions"] += 1
        self._user_stats[user_id]["last_interaction"] = datetime.now()
        
        # Update patterns and trends
        self._update_patterns(user_id, interaction)
        
        logger.info("Interaction recorded", user_id=user_id, interaction_id=interaction_id)
        return interaction_id
    
    def _update_patterns(self, user_id: str, interaction: Dict[str, Any]):
        """Update detected patterns based on new interaction"""
        history = self._histories[user_id]
        
        # Simple pattern detection - in a real implementation this would be more sophisticated
        
        # Track interaction types
        interaction_type = interaction.get("type", "unknown")
        if "interaction_types" not in history.patterns:
            history.patterns["interaction_types"] = {}
        if interaction_type not in history.patterns["interaction_types"]:
            history.patterns["interaction_types"][interaction_type] = 0
        history.patterns["interaction_types"][interaction_type] += 1
        
        # Track topics
        topics = interaction.get("topics", [])
        if "topics" not in history.patterns:
            history.patterns["topics"] = {}
        for topic in topics:
            if topic not in history.patterns["topics"]:
                history.patterns["topics"][topic] = 0
            history.patterns["topics"][topic] += 1
        
        # Track time patterns
        timestamp = interaction.get("timestamp", datetime.now())
        hour = timestamp.hour
        if "hours" not in history.patterns:
            history.patterns["hours"] = {}
        if hour not in history.patterns["hours"]:
            history.patterns["hours"][hour] = 0
        history.patterns["hours"][hour] += 1
        
        # Update trends (moving averages)
        self._update_trends(user_id)
    
    def _update_trends(self, user_id: str):
        """Update trend analysis based on interaction history"""
        history = self._histories[user_id]
        interactions = history.interactions
        
        if len(interactions) < 2:
            return
        
        # Calculate recent interaction frequency
        recent_count = len([i for i in interactions if (datetime.now() - i.get("timestamp", datetime.now())).days < 7])
        history.trends["recent_frequency"] = recent_count / 7  # Per day
        
        # Calculate topic trends
        all_topics = []
        for interaction in interactions[-100:]:  # Last 100 interactions
            all_topics.extend(interaction.get("topics", []))
        
        if all_topics:
            topic_counts = {}
            for topic in all_topics:
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
            
            # Get trending topics (most frequent in recent interactions)
            trending_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            history.trends["trending_topics"] = [topic for topic, count in trending_topics]
    
    def get_interaction_history(self, user_id: str) -> Optional[InteractionHistory]:
        """Get the interaction history for a user"""
        return self._histories.get(user_id)
    
    def get_patterns(self, user_id: str) -> Dict[str, Any]:
        """Get detected patterns for a user"""
        if user_id not in self._histories:
            return {}
        return self._histories[user_id].patterns.copy()
    
    def get_trends(self, user_id: str) -> Dict[str, Any]:
        """Get identified trends for a user"""
        if user_id not in self._histories:
            return {}
        return self._histories[user_id].trends.copy()
    
    def add_knowledge_node(
        self,
        user_id: str,
        concept: str,
        understanding: float = 0.5,
        interest: float = 0.5,
        personal_notes: str = "",
        tags: List[str] = None
    ) -> str:
        """
        Add a knowledge node to a user's personal knowledge graph.
        
        Args:
            user_id: User identifier
            concept: Concept name
            understanding: User's understanding level (0.0 to 1.0)
            interest: User's interest level (0.0 to 1.0)
            personal_notes: User's personal notes
            tags: List of tags
            
        Returns:
            Node ID
        """
        if user_id not in self._knowledge_graphs:
            self.create_user_profile(user_id)
        
        node_id = str(uuid.uuid4())
        
        node = PersonalKnowledgeNode(
            node_id=node_id,
            concept=concept,
            user_understanding=understanding,
            user_interest=interest,
            last_accessed=datetime.now(),
            access_count=0,
            personal_notes=personal_notes,
            tags=tags or []
        )
        
        self._knowledge_graphs[user_id][node_id] = node
        self._user_stats[user_id]["knowledge_nodes"] += 1
        
        # Keep within limits
        if len(self._knowledge_graphs[user_id]) > self.config.get("max_knowledge_nodes_per_user", 5000):
            # Remove least accessed node
            least_accessed = min(
                self._knowledge_graphs[user_id].keys(),
                key=lambda x: self._knowledge_graphs[user_id][x].access_count
            )
            del self._knowledge_graphs[user_id][least_accessed]
            self._user_stats[user_id]["knowledge_nodes"] -= 1
        
        logger.info("Knowledge node added", user_id=user_id, node_id=node_id, concept=concept)
        return node_id
    
    def get_knowledge_node(self, user_id: str, node_id: str) -> Optional[PersonalKnowledgeNode]:
        """Get a knowledge node for a user"""
        if user_id not in self._knowledge_graphs:
            return None
        return self._knowledge_graphs[user_id].get(node_id)
    
    def update_knowledge_node(
        self,
        user_id: str,
        node_id: str,
        updates: Dict[str, Any]
    ) -> bool:
        """
        Update a knowledge node for a user.
        
        Args:
            user_id: User identifier
            node_id: Node identifier
            updates: Dictionary of updates
            
        Returns:
            True if updated successfully
        """
        if user_id not in self._knowledge_graphs or node_id not in self._knowledge_graphs[user_id]:
            return False
        
        node = self._knowledge_graphs[user_id][node_id]
        
        for key, value in updates.items():
            if hasattr(node, key):
                setattr(node, key, value)
        
        # If accessed, update access count and last accessed
        if "accessed" in updates:
            node.access_count += 1
            node.last_accessed = datetime.now()
        
        # Apply forgetting curve to understanding
        if "user_understanding" in updates:
            # In a real implementation, we would apply a more sophisticated forgetting curve
            node.user_understanding = max(0.0, node.user_understanding * (1 - self.config.get("learning_forgetting_rate", 0.01)))
            node.user_understanding = min(1.0, node.user_understanding + updates["user_understanding"] * 0.1)
        
        # Apply decay to interest
        time_since_access = (datetime.now() - node.last_accessed).days
        interest_decay = self.config.get("interest_decay_rate", 0.005) * time_since_access
        node.user_interest = max(0.0, node.user_interest - interest_decay)
        
        logger.info("Knowledge node updated", user_id=user_id, node_id=node_id)
        return True
    
    def access_knowledge_node(self, user_id: str, node_id: str) -> bool:
        """
        Mark a knowledge node as accessed.
        
        Args:
            user_id: User identifier
            node_id: Node identifier
            
        Returns:
            True if accessed successfully
        """
        if user_id not in self._knowledge_graphs or node_id not in self._knowledge_graphs[user_id]:
            return False
        
        node = self._knowledge_graphs[user_id][node_id]
        node.access_count += 1
        node.last_accessed = datetime.now()
        
        logger.info("Knowledge node accessed", user_id=user_id, node_id=node_id)
        return True
    
    def search_knowledge(
        self,
        user_id: str,
        query: str,
        limit: int = 10
    ) -> List[PersonalKnowledgeNode]:
        """
        Search a user's knowledge graph.
        
        Args:
            user_id: User identifier
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching knowledge nodes
        """
        if user_id not in self._knowledge_graphs:
            return []
        
        results = []
        query_lower = query.lower()
        
        for node_id, node in self._knowledge_graphs[user_id].items():
            if (query_lower in node.concept.lower() or 
                query_lower in node.personal_notes.lower() or
                any(query_lower in tag.lower() for tag in node.tags)):
                results.append(node)
        
        # Sort by relevance (access count + interest + understanding)
        results.sort(
            key=lambda x: x.access_count * 0.4 + x.user_interest * 0.3 + x.user_understanding * 0.3,
            reverse=True
        )
        
        return results[:limit]
    
    def add_context_preference(
        self,
        user_id: str,
        context_id: str,
        preference_score: float = 0.5
    ) -> ContextPreference:
        """
        Add or update a context preference for a user.
        
        Args:
            user_id: User identifier
            context_id: Context identifier
            preference_score: Preference score (0.0 to 1.0)
            
        Returns:
            Context preference
        """
        if user_id not in self._context_preferences:
            self.create_user_profile(user_id)
        
        if context_id not in self._context_preferences[user_id]:
            preference = ContextPreference(
                context_id=context_id,
                preference_score=preference_score,
                usage_count=0,
                last_used=datetime.now()
            )
            self._context_preferences[user_id][context_id] = preference
            self._user_stats[user_id]["context_preferences"] += 1
        else:
            preference = self._context_preferences[user_id][context_id]
            # Update with moving average
            preference.preference_score = (preference.preference_score + preference_score) / 2
        
        logger.info("Context preference added/updated", user_id=user_id, context_id=context_id)
        return preference
    
    def get_context_preference(self, user_id: str, context_id: str) -> Optional[ContextPreference]:
        """Get a context preference for a user"""
        if user_id not in self._context_preferences:
            return None
        return self._context_preferences[user_id].get(context_id)
    
    def record_context_usage(self, user_id: str, context_id: str, feedback: Dict[str, Any] = None) -> bool:
        """
        Record usage of a context.
        
        Args:
            user_id: User identifier
            context_id: Context identifier
            feedback: Optional feedback
            
        Returns:
            True if recorded successfully
        """
        if user_id not in self._context_preferences or context_id not in self._context_preferences[user_id]:
            return False
        
        preference = self._context_preferences[user_id][context_id]
        preference.usage_count += 1
        preference.last_used = datetime.now()
        
        if feedback:
            preference.feedback.append(feedback)
        
        # Adjust preference score based on feedback
        if feedback and "rating" in feedback:
            rating = feedback["rating"]
            # Update with moving average
            preference.preference_score = (preference.preference_score * (preference.usage_count - 1) + rating) / preference.usage_count
        
        logger.info("Context usage recorded", user_id=user_id, context_id=context_id)
        return True
    
    def get_recommended_contexts(self, user_id: str, limit: int = 5) -> List[ContextPreference]:
        """
        Get recommended contexts for a user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of results
            
        Returns:
            List of recommended context preferences
        """
        if user_id not in self._context_preferences:
            return []
        
        preferences = list(self._context_preferences[user_id].values())
        
        # Sort by preference score and recency
        preferences.sort(
            key=lambda x: x.preference_score * 0.7 + (1.0 / (1.0 + (datetime.now() - x.last_used).days)) * 0.3,
            reverse=True
        )
        
        return preferences[:limit]
    
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
        # Record the interaction
        self.record_interaction(user_id, interaction_data)
        
        # Extract knowledge from interaction
        concepts = interaction_data.get("concepts", [])
        for concept in concepts:
            # Add or update knowledge node
            existing_nodes = self.search_knowledge(user_id, concept)
            if existing_nodes:
                # Update existing node
                node_id = existing_nodes[0].node_id
                self.update_knowledge_node(user_id, node_id, {
                    "accessed": True,
                    "user_understanding": min(1.0, existing_nodes[0].user_understanding + 0.05)
                })
            else:
                # Add new node
                self.add_knowledge_node(
                    user_id=user_id,
                    concept=concept,
                    understanding=0.3,
                    interest=interaction_data.get("interest", 0.5)
                )
        
        # Update profile based on interaction
        if "preferences" in interaction_data:
            self.update_user_profile(user_id, {
                "preferences": interaction_data["preferences"]
            })
        
        if "interests" in interaction_data:
            profile = self.get_user_profile(user_id)
            if profile:
                for interest in interaction_data["interests"]:
                    if interest not in profile.interests:
                        profile.interests.append(interest)
        
        logger.info("User context updated", user_id=user_id)
        return True
    
    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        Get statistics for a specific user.
        
        Args:
            user_id: User identifier
            
        Returns:
            User statistics
        """
        if user_id not in self._user_stats:
            return {}
        return self._user_stats[user_id].copy()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall statistics for the individual context model.
        
        Returns:
            Statistics dictionary
        """
        return {
            "user_count": len(self._profiles),
            "total_interactions": sum(stats.get("total_interactions", 0) for stats in self._user_stats.values()),
            "total_knowledge_nodes": sum(stats.get("knowledge_nodes", 0) for stats in self._user_stats.values()),
            "total_context_preferences": sum(stats.get("context_preferences", 0) for stats in self._user_stats.values())
        }
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the individual context model"""
        return {
            "model_type": "IndividualContextModel",
            "user_count": len(self._profiles),
            "total_interactions": sum(stats.get("total_interactions", 0) for stats in self._user_stats.values()),
            "total_knowledge_nodes": sum(stats.get("knowledge_nodes", 0) for stats in self._user_stats.values())
        }
