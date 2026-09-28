"""
Cross-Context Learning - Knowledge transfer between different domains

This module enables the HEICN system to transfer knowledge and learning
across different contexts and domains, improving efficiency and performance.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import structlog
from datetime import datetime
import uuid
import numpy as np

logger = structlog.get_logger(__name__)


@dataclass
class ContextDomain:
    """A domain or context for learning"""
    domain_id: str
    name: str
    description: str
    related_domains: List[str] = field(default_factory=list)
    similarity_scores: Dict[str, float] = field(default_factory=dict)  # domain_id -> similarity
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class TransferableKnowledge:
    """Knowledge that can be transferred between contexts"""
    knowledge_id: str
    source_domain: str
    target_domain: str
    concept: str
    transfer_score: float = 0.5  # 0.0 to 1.0 - how transferable this knowledge is
    adaptation_needed: float = 0.0  # 0.0 to 1.0 - how much adaptation is needed
    success_rate: float = 0.0  # Success rate of transfers
    usage_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None


@dataclass
class TransferMapping:
    """Mapping between concepts in different domains"""
    mapping_id: str
    source_domain: str
    target_domain: str
    source_concept: str
    target_concept: str
    similarity: float = 0.5  # 0.0 to 1.0
    transformation: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.5  # 0.0 to 1.0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class TransferResult:
    """Result of a knowledge transfer"""
    transfer_id: str
    knowledge_id: str
    source_domain: str
    target_domain: str
    success: bool
    adaptation_applied: float = 0.0
    performance: float = 0.0  # 0.0 to 1.0
    timestamp: datetime = field(default_factory=datetime.now)


class CrossContextLearner:
    """
    Cross-Context Learning System.
    
    This system:
    - Transfers knowledge between different domains and contexts
    - Identifies similar contexts for knowledge sharing
    - Adapts transferred knowledge to new contexts
    - Tracks transfer success and improves over time
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the cross-context learner.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._default_config()
        
        # Domains
        self._domains: Dict[str, ContextDomain] = {}
        
        # Transferable knowledge
        self._knowledge: Dict[str, TransferableKnowledge] = {}
        
        # Transfer mappings
        self._mappings: Dict[str, TransferMapping] = {}
        
        # Transfer results
        self._transfer_history: List[TransferResult] = []
        
        # Enabled state
        self.enabled = True
        
        # Learning state
        self._learning_rate = self.config.get("learning_rate", 0.1)
        self._exploration_rate = self.config.get("exploration_rate", 0.2)
        
        logger.info("CrossContextLearner initialized")
    
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            "learning_rate": 0.1,
            "exploration_rate": 0.2,
            "max_domains": 100,
            "max_knowledge": 1000,
            "max_mappings": 5000,
            "max_transfer_history": 1000,
            "similarity_threshold": 0.3,
            "transfer_threshold": 0.5
        }
    
    def add_domain(
        self,
        domain_id: str,
        name: str,
        description: str = ""
    ) -> str:
        """
        Add a domain or context.
        
        Args:
            domain_id: Unique domain identifier
            name: Domain name
            description: Domain description
            
        Returns:
            Domain ID
        """
        domain = ContextDomain(
            domain_id=domain_id,
            name=name,
            description=description,
            created_at=datetime.now()
        )
        
        self._domains[domain_id] = domain
        
        logger.info("Domain added", domain_id=domain_id, name=name)
        return domain_id
    
    def get_domain(self, domain_id: str) -> Optional[ContextDomain]:
        """Get a domain by ID"""
        return self._domains.get(domain_id)
    
    def get_all_domains(self) -> Dict[str, ContextDomain]:
        """Get all domains"""
        return self._domains.copy()
    
    def remove_domain(self, domain_id: str) -> bool:
        """Remove a domain"""
        if domain_id not in self._domains:
            return False
        
        # Remove related knowledge and mappings
        knowledge_to_remove = [
            kid for kid, k in self._knowledge.items() 
            if k.source_domain == domain_id or k.target_domain == domain_id
        ]
        for kid in knowledge_to_remove:
            del self._knowledge[kid]
        
        mappings_to_remove = [
            mid for mid, m in self._mappings.items() 
            if m.source_domain == domain_id or m.target_domain == domain_id
        ]
        for mid in mappings_to_remove:
            del self._mappings[mid]
        
        del self._domains[domain_id]
        
        logger.info("Domain removed", domain_id=domain_id)
        return True
    
    def add_similarity(self, domain_id1: str, domain_id2: str, similarity: float) -> bool:
        """
        Add a similarity score between two domains.
        
        Args:
            domain_id1: First domain ID
            domain_id2: Second domain ID
            similarity: Similarity score (0.0 to 1.0)
            
        Returns:
            True if added successfully
        """
        if domain_id1 not in self._domains or domain_id2 not in self._domains:
            return False
        
        # Add to both domains
        self._domains[domain_id1].similarity_scores[domain_id2] = similarity
        self._domains[domain_id2].similarity_scores[domain_id1] = similarity
        
        # Add to related domains if similarity is high
        if similarity > self.config.get("similarity_threshold", 0.3):
            if domain_id2 not in self._domains[domain_id1].related_domains:
                self._domains[domain_id1].related_domains.append(domain_id2)
            if domain_id1 not in self._domains[domain_id2].related_domains:
                self._domains[domain_id2].related_domains.append(domain_id1)
        
        logger.info("Similarity added", domain1=domain_id1, domain2=domain_id2, similarity=similarity)
        return True
    
    def get_similarity(self, domain_id1: str, domain_id2: str) -> float:
        """
        Get the similarity score between two domains.
        
        Args:
            domain_id1: First domain ID
            domain_id2: Second domain ID
            
        Returns:
            Similarity score (0.0 if not found)
        """
        if domain_id1 in self._domains:
            return self._domains[domain_id1].similarity_scores.get(domain_id2, 0.0)
        return 0.0
    
    def find_similar_domains(self, domain_id: str, threshold: float = 0.3) -> List[Tuple[str, float]]:
        """
        Find domains similar to the specified domain.
        
        Args:
            domain_id: Domain ID
            threshold: Similarity threshold
            
        Returns:
            List of (domain_id, similarity) tuples
        """
        if domain_id not in self._domains:
            return []
        
        domain = self._domains[domain_id]
        results = []
        
        for other_id, similarity in domain.similarity_scores.items():
            if similarity >= threshold:
                results.append((other_id, similarity))
        
        # Sort by similarity
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results
    
    def add_knowledge(
        self,
        source_domain: str,
        target_domain: str,
        concept: str,
        transfer_score: float = 0.5,
        adaptation_needed: float = 0.0
    ) -> str:
        """
        Add transferable knowledge between domains.
        
        Args:
            source_domain: Source domain ID
            target_domain: Target domain ID
            concept: Concept name
            transfer_score: Transferability score (0.0 to 1.0)
            adaptation_needed: Adaptation needed score (0.0 to 1.0)
            
        Returns:
            Knowledge ID
        """
        if source_domain not in self._domains or target_domain not in self._domains:
            raise ValueError("Source or target domain not found")
        
        knowledge_id = str(uuid.uuid4())
        
        knowledge = TransferableKnowledge(
            knowledge_id=knowledge_id,
            source_domain=source_domain,
            target_domain=target_domain,
            concept=concept,
            transfer_score=transfer_score,
            adaptation_needed=adaptation_needed,
            created_at=datetime.now()
        )
        
        self._knowledge[knowledge_id] = knowledge
        
        # Keep within limits
        if len(self._knowledge) > self.config.get("max_knowledge", 1000):
            # Remove least used knowledge
            least_used = min(
                self._knowledge.keys(),
                key=lambda x: self._knowledge[x].usage_count
            )
            del self._knowledge[least_used]
        
        logger.info(
            "Knowledge added",
            knowledge_id=knowledge_id,
            source=source_domain,
            target=target_domain,
            concept=concept
        )
        return knowledge_id
    
    def get_knowledge(self, knowledge_id: str) -> Optional[TransferableKnowledge]:
        """Get knowledge by ID"""
        return self._knowledge.get(knowledge_id)
    
    def get_knowledge_by_domains(
        self,
        source_domain: str,
        target_domain: str
    ) -> List[TransferableKnowledge]:
        """Get knowledge transferable from source to target domain"""
        return [
            k for k in self._knowledge.values()
            if k.source_domain == source_domain and k.target_domain == target_domain
        ]
    
    def update_knowledge(
        self,
        knowledge_id: str,
        updates: Dict[str, Any]
    ) -> bool:
        """
        Update transferable knowledge.
        
        Args:
            knowledge_id: Knowledge identifier
            updates: Dictionary of updates
            
        Returns:
            True if updated successfully
        """
        if knowledge_id not in self._knowledge:
            return False
        
        knowledge = self._knowledge[knowledge_id]
        
        for key, value in updates.items():
            if hasattr(knowledge, key):
                setattr(knowledge, key, value)
        
        knowledge.last_used = datetime.now()
        
        logger.info("Knowledge updated", knowledge_id=knowledge_id)
        return True
    
    def add_mapping(
        self,
        source_domain: str,
        target_domain: str,
        source_concept: str,
        target_concept: str,
        similarity: float = 0.5,
        transformation: Dict[str, Any] = None,
        confidence: float = 0.5
    ) -> str:
        """
        Add a mapping between concepts in different domains.
        
        Args:
            source_domain: Source domain ID
            target_domain: Target domain ID
            source_concept: Source concept
            target_concept: Target concept
            similarity: Similarity score (0.0 to 1.0)
            transformation: Transformation rules
            confidence: Confidence score (0.0 to 1.0)
            
        Returns:
            Mapping ID
        """
        if source_domain not in self._domains or target_domain not in self._domains:
            raise ValueError("Source or target domain not found")
        
        mapping_id = str(uuid.uuid4())
        
        mapping = TransferMapping(
            mapping_id=mapping_id,
            source_domain=source_domain,
            target_domain=target_domain,
            source_concept=source_concept,
            target_concept=target_concept,
            similarity=similarity,
            transformation=transformation or {},
            confidence=confidence,
            created_at=datetime.now()
        )
        
        self._mappings[mapping_id] = mapping
        
        # Keep within limits
        if len(self._mappings) > self.config.get("max_mappings", 5000):
            # Remove least confident mapping
            least_confident = min(
                self._mappings.keys(),
                key=lambda x: self._mappings[x].confidence
            )
            del self._mappings[least_confident]
        
        logger.info(
            "Mapping added",
            mapping_id=mapping_id,
            source_domain=source_domain,
            target_domain=target_domain,
            source_concept=source_concept,
            target_concept=target_concept
        )
        return mapping_id
    
    def get_mapping(self, mapping_id: str) -> Optional[TransferMapping]:
        """Get a mapping by ID"""
        return self._mappings.get(mapping_id)
    
    def find_mapping(
        self,
        source_domain: str,
        source_concept: str,
        target_domain: str
    ) -> List[TransferMapping]:
        """
        Find mappings from a source concept to a target domain.
        
        Args:
            source_domain: Source domain ID
            source_concept: Source concept
            target_domain: Target domain ID
            
        Returns:
            List of matching mappings
        """
        results = []
        
        for mapping in self._mappings.values():
            if (mapping.source_domain == source_domain and 
                mapping.source_concept == source_concept and
                mapping.target_domain == target_domain):
                results.append(mapping)
        
        # Sort by confidence and similarity
        results.sort(
            key=lambda x: x.confidence * 0.7 + x.similarity * 0.3,
            reverse=True
        )
        
        return results
    
    def transfer_knowledge(
        self,
        knowledge_id: str,
        target_domain: str,
        adaptation: float = 0.0
    ) -> TransferResult:
        """
        Transfer knowledge to a new domain.
        
        Args:
            knowledge_id: Knowledge identifier
            target_domain: Target domain ID
            adaptation: Adaptation level to apply
            
        Returns:
            Transfer result
        """
        if not self.enabled:
            return TransferResult(
                transfer_id=str(uuid.uuid4()),
                knowledge_id=knowledge_id,
                source_domain="",
                target_domain=target_domain,
                success=False,
                timestamp=datetime.now()
            )
        
        if knowledge_id not in self._knowledge:
            return TransferResult(
                transfer_id=str(uuid.uuid4()),
                knowledge_id=knowledge_id,
                source_domain="",
                target_domain=target_domain,
                success=False,
                timestamp=datetime.now()
            )
        
        knowledge = self._knowledge[knowledge_id]
        
        # Check if transfer is possible
        if knowledge.transfer_score < self.config.get("transfer_threshold", 0.5):
            return TransferResult(
                transfer_id=str(uuid.uuid4()),
                knowledge_id=knowledge_id,
                source_domain=knowledge.source_domain,
                target_domain=target_domain,
                success=False,
                timestamp=datetime.now()
            )
        
        # Simulate transfer with adaptation
        transfer_id = str(uuid.uuid4())
        
        # Calculate success probability
        base_success = knowledge.success_rate
        similarity = self.get_similarity(knowledge.source_domain, target_domain)
        
        # Adaptation reduces the gap
        gap = 1.0 - similarity
        adapted_gap = max(0.0, gap - adaptation * knowledge.adaptation_needed)
        adapted_similarity = 1.0 - adapted_gap
        
        # Calculate success
        success_probability = base_success * 0.5 + adapted_similarity * 0.5
        success = random.random() < success_probability
        
        # Calculate performance
        performance = 0.0
        if success:
            performance = adapted_similarity * (0.7 + random.random() * 0.3)
            
            # Update knowledge statistics
            knowledge.usage_count += 1
            knowledge.success_rate = (knowledge.success_rate * (knowledge.usage_count - 1) + 1.0) / knowledge.usage_count
            knowledge.last_used = datetime.now()
        else:
            performance = adapted_similarity * (0.3 + random.random() * 0.3)
            
            # Update knowledge statistics
            knowledge.usage_count += 1
            knowledge.success_rate = (knowledge.success_rate * (knowledge.usage_count - 1)) / knowledge.usage_count
        
        result = TransferResult(
            transfer_id=transfer_id,
            knowledge_id=knowledge_id,
            source_domain=knowledge.source_domain,
            target_domain=target_domain,
            success=success,
            adaptation_applied=adaptation,
            performance=performance,
            timestamp=datetime.now()
        )
        
        self._transfer_history.append(result)
        
        # Keep history limited
        if len(self._transfer_history) > self.config.get("max_transfer_history", 1000):
            self._transfer_history = self._transfer_history[-1000:]
        
        logger.info(
            "Knowledge transfer",
            transfer_id=transfer_id,
            knowledge_id=knowledge_id,
            source=knowledge.source_domain,
            target=target_domain,
            success=success,
            performance=performance
        )
        
        return result
    
    def suggest_transfers(
        self,
        source_domain: str,
        target_domain: str
    ) -> List[Dict[str, Any]]:
        """
        Suggest knowledge transfers between domains.
        
        Args:
            source_domain: Source domain ID
            target_domain: Target domain ID
            
        Returns:
            List of suggested transfers
        """
        suggestions = []
        
        # Get similarity between domains
        similarity = self.get_similarity(source_domain, target_domain)
        
        if similarity < self.config.get("similarity_threshold", 0.3):
            return suggestions
        
        # Get knowledge from source domain
        source_knowledge = [
            k for k in self._knowledge.values()
            if k.source_domain == source_domain
        ]
        
        for knowledge in source_knowledge:
            # Calculate potential transfer score
            transfer_score = knowledge.transfer_score * similarity
            
            if transfer_score > self.config.get("transfer_threshold", 0.5):
                suggestions.append({
                    "knowledge_id": knowledge.knowledge_id,
                    "concept": knowledge.concept,
                    "transfer_score": transfer_score,
                    "adaptation_needed": knowledge.adaptation_needed,
                    "expected_success": knowledge.success_rate * similarity,
                    "priority": transfer_score
                })
        
        # Sort by priority
        suggestions.sort(key=lambda x: x["priority"], reverse=True)
        
        return suggestions
    
    def learn_from_transfer(self, result: TransferResult) -> bool:
        """
        Learn from a transfer result to improve future transfers.
        
        Args:
            result: Transfer result
            
        Returns:
            True if learning successful
        """
        if result.knowledge_id not in self._knowledge:
            return False
        
        knowledge = self._knowledge[result.knowledge_id]
        
        # Update transfer score based on success
        if result.success:
            # Increase transfer score
            knowledge.transfer_score = min(
                1.0,
                knowledge.transfer_score + self._learning_rate * (1.0 - knowledge.transfer_score)
            )
        else:
            # Decrease transfer score
            knowledge.transfer_score = max(
                0.0,
                knowledge.transfer_score - self._learning_rate * knowledge.transfer_score
            )
        
        # Update adaptation needed based on adaptation applied
        if result.adaptation_applied > 0:
            if result.success:
                knowledge.adaptation_needed = max(
                    0.0,
                    knowledge.adaptation_needed - self._learning_rate * 0.1
                )
            else:
                knowledge.adaptation_needed = min(
                    1.0,
                    knowledge.adaptation_needed + self._learning_rate * 0.1
                )
        
        # Update domain similarity based on transfer success
        similarity = self.get_similarity(knowledge.source_domain, knowledge.target_domain)
        if result.success:
            new_similarity = min(
                1.0,
                similarity + self._learning_rate * (1.0 - similarity) * result.performance
            )
        else:
            new_similarity = max(
                0.0,
                similarity - self._learning_rate * similarity * (1.0 - result.performance)
            )
        
        self.add_similarity(knowledge.source_domain, knowledge.target_domain, new_similarity)
        
        logger.info("Learned from transfer", transfer_id=result.transfer_id)
        return True
    
    def get_transfer_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about knowledge transfers.
        
        Returns:
            Transfer statistics
        """
        if not self._transfer_history:
            return {
                "total_transfers": 0,
                "success_rate": 0.0,
                "avg_performance": 0.0
            }
        
        total = len(self._transfer_history)
        successful = len([r for r in self._transfer_history if r.success])
        avg_performance = sum(r.performance for r in self._transfer_history) / total
        
        return {
            "total_transfers": total,
            "success_rate": successful / total,
            "avg_performance": avg_performance,
            "recent_success_rate": sum(1 for r in self._transfer_history[-100:] if r.success) / min(100, total)
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall statistics for the cross-context learner.
        
        Returns:
            Statistics dictionary
        """
        return {
            "domain_count": len(self._domains),
            "knowledge_count": len(self._knowledge),
            "mapping_count": len(self._mappings),
            "transfer_history_count": len(self._transfer_history),
            "transfer_statistics": self.get_transfer_statistics(),
            "enabled": self.enabled
        }
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the cross-context learner"""
        return {
            "system_type": "CrossContextLearner",
            "domain_count": len(self._domains),
            "knowledge_count": len(self._knowledge),
            "mapping_count": len(self._mappings),
            "enabled": self.enabled
        }
