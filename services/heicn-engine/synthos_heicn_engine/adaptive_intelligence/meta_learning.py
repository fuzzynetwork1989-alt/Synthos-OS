"""
Meta-Learning System for HEICN

This module implements meta-learning capabilities that learn how to learn
more efficiently, enabling the system to adapt its learning strategies
based on past experience and current context.
"""

from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
import structlog
from datetime import datetime
import numpy as np
import random
from collections import defaultdict

logger = structlog.get_logger(__name__)


@dataclass
class LearningExperience:
    """A record of a learning experience"""
    experience_id: str
    task_type: str
    strategy: str
    success: bool
    performance: float  # 0.0 to 1.0
    duration: float  # seconds
    parameters: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class LearningStrategy:
    """A learning strategy"""
    strategy_id: str
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    success_rate: float = 0.0
    avg_performance: float = 0.0
    usage_count: int = 0
    best_for: List[str] = field(default_factory=list)  # task types this strategy works best for
    last_used: Optional[datetime] = None


@dataclass
class MetaKnowledge:
    """Meta-knowledge about learning"""
    knowledge_id: str
    concept: str
    description: str
    examples: List[Dict] = field(default_factory=list)
    confidence: float = 0.0  # 0.0 to 1.0
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class AdaptationRule:
    """A rule for adapting learning strategies"""
    rule_id: str
    condition: Dict[str, Any]
    action: Dict[str, Any]
    priority: int = 1
    success_rate: float = 0.0


class MetaLearningSystem:
    """
    Meta-Learning System for HEICN.
    
    This system:
    - Learns from past learning experiences
    - Adapts learning strategies based on context
    - Develops meta-knowledge about effective learning
    - Optimizes the learning process itself
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the meta-learning system.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._default_config()
        
        # Learning experiences
        self._experiences: Dict[str, LearningExperience] = {}
        self._experiences_by_task: Dict[str, List[str]] = defaultdict(list)  # task_type -> [experience_ids]
        self._experiences_by_strategy: Dict[str, List[str]] = defaultdict(list)  # strategy -> [experience_ids]
        
        # Learning strategies
        self._strategies: Dict[str, LearningStrategy] = {}
        
        # Meta-knowledge
        self._meta_knowledge: Dict[str, MetaKnowledge] = {}
        
        # Adaptation rules
        self._adaptation_rules: Dict[str, AdaptationRule] = {}
        
        # Current context
        self._current_context: Dict[str, Any] = {}
        
        # Learning state
        self._learning_rate = self.config.get("learning_rate", 0.1)
        self._exploration_rate = self.config.get("exploration_rate", 0.2)
        
        # Register default strategies
        self._register_default_strategies()
        
        logger.info("MetaLearningSystem initialized")
    
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            "learning_rate": 0.1,
            "exploration_rate": 0.2,
            "max_experiences": 1000,
            "max_strategies": 50,
            "max_meta_knowledge": 100,
            "context_window": 10  # Number of recent experiences to consider
        }
    
    def _register_default_strategies(self):
        """Register default learning strategies"""
        # Supervised Learning
        self.register_strategy(
            "supervised",
            "Supervised Learning",
            "Learning from labeled examples"
        )
        
        # Reinforcement Learning
        self.register_strategy(
            "reinforcement",
            "Reinforcement Learning",
            "Learning from rewards and punishments"
        )
        
        # Unsupervised Learning
        self.register_strategy(
            "unsupervised",
            "Unsupervised Learning",
            "Learning from unlabeled data by finding patterns"
        )
        
        # Transfer Learning
        self.register_strategy(
            "transfer",
            "Transfer Learning",
            "Applying knowledge from one domain to another"
        )
        
        # Active Learning
        self.register_strategy(
            "active",
            "Active Learning",
            "Selectively sampling the most informative examples"
        )
        
        # Incremental Learning
        self.register_strategy(
            "incremental",
            "Incremental Learning",
            "Continuously updating models with new data"
        )
    
    def set_context(self, context: Dict[str, Any]) -> bool:
        """
        Set the current learning context.
        
        Args:
            context: Context dictionary
            
        Returns:
            True if set successfully
        """
        self._current_context = context.copy()
        
        logger.info("Context set", context_keys=list(context.keys()))
        return True
    
    def get_context(self) -> Dict[str, Any]:
        """Get the current learning context"""
        return self._current_context.copy()
    
    def record_experience(
        self,
        task_type: str,
        strategy: str,
        success: bool,
        performance: float,
        duration: float,
        parameters: Dict[str, Any] = None,
        context: Dict[str, Any] = None
    ) -> str:
        """
        Record a learning experience.
        
        Args:
            task_type: Type of task
            strategy: Learning strategy used
            success: Whether the learning was successful
            performance: Performance score (0.0 to 1.0)
            duration: Duration in seconds
            parameters: Strategy parameters
            context: Learning context
            
        Returns:
            Experience ID
        """
        experience_id = str(datetime.now().timestamp())
        
        experience = LearningExperience(
            experience_id=experience_id,
            task_type=task_type,
            strategy=strategy,
            success=success,
            performance=performance,
            duration=duration,
            parameters=parameters or {},
            context=context or self._current_context.copy()
        )
        
        self._experiences[experience_id] = experience
        self._experiences_by_task[task_type].append(experience_id)
        self._experiences_by_strategy[strategy].append(experience_id)
        
        # Update strategy statistics
        if strategy in self._strategies:
            strat = self._strategies[strategy]
            strat.usage_count += 1
            
            # Update success rate (moving average)
            strat.success_rate = (strat.success_rate * (strat.usage_count - 1) + (1.0 if success else 0.0)) / strat.usage_count
            
            # Update average performance (moving average)
            strat.avg_performance = (strat.avg_performance * (strat.usage_count - 1) + performance) / strat.usage_count
            
            strat.last_used = datetime.now()
            
            # Update best_for list
            if task_type not in strat.best_for:
                strat.best_for.append(task_type)
        
        # Keep experiences limited
        if len(self._experiences) > self.config.get("max_experiences", 1000):
            # Remove oldest experience
            oldest_id = min(self._experiences.keys(), key=lambda x: self._experiences[x].timestamp)
            oldest = self._experiences[oldest_id]
            
            # Remove from indexes
            if oldest.task_type in self._experiences_by_task:
                if oldest_id in self._experiences_by_task[oldest.task_type]:
                    self._experiences_by_task[oldest.task_type].remove(oldest_id)
            
            if oldest.strategy in self._experiences_by_strategy:
                if oldest_id in self._experiences_by_strategy[oldest.strategy]:
                    self._experiences_by_strategy[oldest.strategy].remove(oldest_id)
            
            del self._experiences[oldest_id]
        
        logger.info(
            "Experience recorded",
            experience_id=experience_id,
            task_type=task_type,
            strategy=strategy,
            success=success,
            performance=performance
        )
        
        return experience_id
    
    def get_experience(self, experience_id: str) -> Optional[LearningExperience]:
        """Get a learning experience by ID"""
        return self._experiences.get(experience_id)
    
    def get_experiences_by_task(self, task_type: str) -> List[LearningExperience]:
        """Get experiences for a specific task type"""
        experience_ids = self._experiences_by_task.get(task_type, [])
        return [self._experiences[eid] for eid in experience_ids if eid in self._experiences]
    
    def get_experiences_by_strategy(self, strategy: str) -> List[LearningExperience]:
        """Get experiences for a specific strategy"""
        experience_ids = self._experiences_by_strategy.get(strategy, [])
        return [self._experiences[eid] for eid in experience_ids if eid in self._experiences]
    
    def register_strategy(
        self,
        strategy_id: str,
        name: str,
        description: str,
        parameters: Dict[str, Any] = None
    ) -> str:
        """
        Register a learning strategy.
        
        Args:
            strategy_id: Unique strategy identifier
            name: Strategy name
            description: Strategy description
            parameters: Strategy parameters
            
        Returns:
            Strategy ID
        """
        strategy = LearningStrategy(
            strategy_id=strategy_id,
            name=name,
            description=description,
            parameters=parameters or {}
        )
        self._strategies[strategy_id] = strategy
        
        logger.info("Strategy registered", strategy_id=strategy_id, name=name)
        return strategy_id
    
    def get_strategy(self, strategy_id: str) -> Optional[LearningStrategy]:
        """Get a strategy by ID"""
        return self._strategies.get(strategy_id)
    
    def get_all_strategies(self) -> Dict[str, LearningStrategy]:
        """Get all strategies"""
        return self._strategies.copy()
    
    def get_best_strategy(self, task_type: str = None) -> Optional[str]:
        """
        Get the best strategy for a given task type.
        
        Args:
            task_type: Optional task type to find best strategy for
            
        Returns:
            Best strategy ID or None
        """
        if not self._strategies:
            return None
        
        if task_type:
            # Find strategy with best success rate for this task type
            best_strategy = None
            best_score = -1.0
            
            for strat_id, strategy in self._strategies.items():
                # Check if this strategy has experience with this task type
                experiences = self.get_experiences_by_strategy(strat_id)
                task_experiences = [e for e in experiences if e.task_type == task_type]
                
                if task_experiences:
                    # Calculate average performance for this task type
                    avg_performance = sum(e.performance for e in task_experiences) / len(task_experiences)
                    success_rate = sum(1 for e in task_experiences if e.success) / len(task_experiences)
                    score = (avg_performance * 0.7) + (success_rate * 0.3)
                    
                    if score > best_score:
                        best_score = score
                        best_strategy = strat_id
            
            if best_strategy:
                return best_strategy
        
        # If no specific task type or no experience, return strategy with highest overall success rate
        return max(
            self._strategies.items(),
            key=lambda x: x[1].success_rate
        )[0]
    
    def suggest_learning_strategies(self) -> List[Dict[str, Any]]:
        """
        Suggest learning strategies based on current context.
        
        Returns:
            List of suggested strategies with priorities
        """
        suggestions = []
        
        # Get current context
        context = self._current_context
        task_type = context.get("task_type", "unknown")
        
        # For each strategy, calculate a priority score
        for strat_id, strategy in self._strategies.items():
            score = 0.0
            
            # Base score on success rate
            score += strategy.success_rate * 0.5
            
            # Bonus if this strategy works well for the current task type
            if task_type in strategy.best_for:
                score += 0.3
            
            # Bonus if this strategy has been used recently
            if strategy.last_used:
                time_since_use = (datetime.now() - strategy.last_used).total_seconds()
                if time_since_use < 3600:  # Used in last hour
                    score += 0.2
            
            # Malus if this strategy has low usage (exploration)
            if strategy.usage_count < 5:
                score += 0.1  # Exploration bonus
            
            suggestions.append({
                "strategy_id": strat_id,
                "name": strategy.name,
                "score": score,
                "priority": score,
                "success_rate": strategy.success_rate,
                "usage_count": strategy.usage_count
            })
        
        # Sort by score
        suggestions.sort(key=lambda x: x["score"], reverse=True)
        
        return suggestions
    
    def apply_learning_strategy(self, strategy: Dict[str, Any]) -> bool:
        """
        Apply a learning strategy.
        
        Args:
            strategy: Strategy to apply
            
        Returns:
            True if applied successfully
        """
        strategy_id = strategy.get("strategy_id")
        
        if strategy_id not in self._strategies:
            return False
        
        # In a real implementation, this would actually apply the strategy
        # For now, we just simulate it
        
        # Simulate learning with this strategy
        task_type = self._current_context.get("task_type", "unknown")
        
        # Simulate performance based on strategy success rate
        strat = self._strategies[strategy_id]
        success = random.random() < strat.success_rate
        performance = strat.avg_performance * (0.9 + random.random() * 0.2)  # Add some noise
        duration = random.uniform(0.1, 2.0)  # Random duration
        
        # Record the experience
        self.record_experience(
            task_type=task_type,
            strategy=strategy_id,
            success=success,
            performance=performance,
            duration=duration,
            parameters=strategy.get("parameters", {})
        )
        
        logger.info(
            "Learning strategy applied",
            strategy_id=strategy_id,
            success=success,
            performance=performance
        )
        
        return success
    
    def add_meta_knowledge(
        self,
        knowledge_id: str,
        concept: str,
        description: str,
        examples: List[Dict] = None,
        confidence: float = 0.5
    ) -> str:
        """
        Add meta-knowledge about learning.
        
        Args:
            knowledge_id: Unique knowledge identifier
            concept: Concept name
            description: Knowledge description
            examples: Example experiences
            confidence: Confidence level (0.0 to 1.0)
            
        Returns:
            Knowledge ID
        """
        knowledge = MetaKnowledge(
            knowledge_id=knowledge_id,
            concept=concept,
            description=description,
            examples=examples or [],
            confidence=confidence
        )
        self._meta_knowledge[knowledge_id] = knowledge
        
        logger.info("Meta-knowledge added", concept=concept, confidence=confidence)
        return knowledge_id
    
    def get_meta_knowledge(self, knowledge_id: str) -> Optional[MetaKnowledge]:
        """Get meta-knowledge by ID"""
        return self._meta_knowledge.get(knowledge_id)
    
    def get_all_meta_knowledge(self) -> Dict[str, MetaKnowledge]:
        """Get all meta-knowledge"""
        return self._meta_knowledge.copy()
    
    def add_adaptation_rule(
        self,
        rule_id: str,
        condition: Dict[str, Any],
        action: Dict[str, Any],
        priority: int = 1
    ) -> str:
        """
        Add an adaptation rule.
        
        Args:
            rule_id: Unique rule identifier
            condition: Condition for applying the rule
            action: Action to take when condition is met
            priority: Rule priority
            
        Returns:
            Rule ID
        """
        rule = AdaptationRule(
            rule_id=rule_id,
            condition=condition,
            action=action,
            priority=priority
        )
        self._adaptation_rules[rule_id] = rule
        
        logger.info("Adaptation rule added", rule_id=rule_id, priority=priority)
        return rule_id
    
    def get_adaptation_rule(self, rule_id: str) -> Optional[AdaptationRule]:
        """Get an adaptation rule by ID"""
        return self._adaptation_rules.get(rule_id)
    
    def get_all_adaptation_rules(self) -> Dict[str, AdaptationRule]:
        """Get all adaptation rules"""
        return self._adaptation_rules.copy()
    
    def apply_adaptation_rules(self) -> List[Dict[str, Any]]:
        """
        Apply adaptation rules based on current context.
        
        Returns:
            List of applied adaptations
        """
        applied = []
        
        for rule_id, rule in self._adaptation_rules.items():
            # Check if condition is met
            condition_met = True
            
            for key, value in rule.condition.items():
                if key not in self._current_context:
                    condition_met = False
                    break
                
                if self._current_context[key] != value:
                    condition_met = False
                    break
            
            if condition_met:
                # Apply the action
                applied.append({
                    "rule_id": rule_id,
                    "action": rule.action
                })
                
                # In a real implementation, we would execute the action
                # For now, we just record it
                logger.info("Adaptation rule applied", rule_id=rule_id)
        
        return applied
    
    def get_learning_report(self) -> Dict[str, Any]:
        """
        Get a comprehensive learning report.
        
        Returns:
            Learning report dictionary
        """
        # Get strategy summary
        strategy_summary = {}
        for strat_id, strategy in self._strategies.items():
            strategy_summary[strat_id] = {
                "name": strategy.name,
                "success_rate": strategy.success_rate,
                "avg_performance": strategy.avg_performance,
                "usage_count": strategy.usage_count,
                "best_for": strategy.best_for
            }
        
        # Get experience statistics
        experience_stats = {
            "total": len(self._experiences),
            "by_task": {
                task: len(ids)
                for task, ids in self._experiences_by_task.items()
            },
            "by_strategy": {
                strat: len(ids)
                for strat, ids in self._experiences_by_strategy.items()
            }
        }
        
        # Get meta-knowledge summary
        meta_knowledge_summary = {
            "total": len(self._meta_knowledge),
            "concepts": [k.concept for k in self._meta_knowledge.values()]
        }
        
        return {
            "strategies": strategy_summary,
            "experiences": experience_stats,
            "meta_knowledge": meta_knowledge_summary,
            "adaptation_rules": len(self._adaptation_rules),
            "current_context": self._current_context
        }
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the meta-learning system"""
        return {
            "system_type": "MetaLearningSystem",
            "strategy_count": len(self._strategies),
            "experience_count": len(self._experiences),
            "meta_knowledge_count": len(self._meta_knowledge),
            "adaptation_rule_count": len(self._adaptation_rules),
            "learning_rate": self._learning_rate,
            "exploration_rate": self._exploration_rate
        }
