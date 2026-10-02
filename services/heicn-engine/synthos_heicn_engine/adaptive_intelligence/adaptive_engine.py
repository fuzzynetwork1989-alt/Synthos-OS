"""
Adaptive Intelligence Engine - Core adaptive intelligence system for HEICN

This engine integrates all adaptive intelligence components to provide
comprehensive self-optimizing capabilities for the HEICN system.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import structlog
from datetime import datetime
import asyncio
import numpy as np

from .goal_oriented_rl import GoalOrientedRL
from .self_optimizing import SelfOptimizingAlgorithm
from .meta_learning import MetaLearningSystem

logger = structlog.get_logger(__name__)


@dataclass
class AdaptationStrategy:
    """A strategy for adapting system behavior"""
    strategy_id: str
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    success_rate: float = 0.0
    usage_count: int = 0
    last_used: Optional[datetime] = None


@dataclass
class AdaptationResult:
    """Result of an adaptation"""
    adaptation_id: str
    strategy_id: str
    success: bool
    improvement: float
    metrics: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class PerformanceMetric:
    """A performance metric to track"""
    name: str
    description: str
    current_value: float
    target_value: float
    history: List[Tuple[datetime, float]] = field(default_factory=list)
    weight: float = 1.0  # Importance weight


class AdaptiveIntelligenceEngine:
    """
    Adaptive Intelligence Engine - Core adaptive intelligence system.
    
    This engine integrates:
    - Goal-Oriented Reinforcement Learning
    - Self-Optimizing Algorithms
    - Meta-Learning Systems
    
    To provide comprehensive adaptive intelligence for HEICN.
    """
    
    def __init__(
        self,
        config: Optional[Dict] = None
    ):
        """
        Initialize the adaptive intelligence engine.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._default_config()
        
        # Initialize sub-components
        self.goal_rl = GoalOrientedRL(self.config.get("goal_rl_config", {}))
        self.self_optimizing = SelfOptimizingAlgorithm(self.config.get("self_optimizing_config", {}))
        self.meta_learning = MetaLearningSystem(self.config.get("meta_learning_config", {}))
        
        # Adaptation strategies
        self._strategies: Dict[str, AdaptationStrategy] = {}
        self._strategy_history: List[AdaptationResult] = []
        
        # Performance metrics
        self._metrics: Dict[str, PerformanceMetric] = {}
        
        # Adaptation state
        self._adaptation_in_progress: bool = False
        self._last_adaptation: Optional[datetime] = None
        
        # Learning state
        self._learning_rate: float = self.config.get("learning_rate", 0.1)
        self._exploration_rate: float = self.config.get("exploration_rate", 0.2)
        
        logger.info("AdaptiveIntelligenceEngine initialized")
    
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            "learning_rate": 0.1,
            "exploration_rate": 0.2,
            "adaptation_interval": 3600,  # 1 hour
            "max_strategies": 50,
            "metric_history_size": 100,
            "goal_rl_config": {},
            "self_optimizing_config": {},
            "meta_learning_config": {}
        }
    
    def register_metric(
        self,
        name: str,
        description: str = "",
        current_value: float = 0.0,
        target_value: float = 1.0,
        weight: float = 1.0
    ) -> str:
        """
        Register a performance metric to track.
        
        Args:
            name: Metric name
            description: Description
            current_value: Initial value
            target_value: Target value
            weight: Importance weight
            
        Returns:
            Metric name
        """
        metric = PerformanceMetric(
            name=name,
            description=description,
            current_value=current_value,
            target_value=target_value,
            weight=weight
        )
        self._metrics[name] = metric
        
        logger.info("Metric registered", name=name)
        return name
    
    def record_metric(self, name: str, value: float) -> bool:
        """
        Record a value for a performance metric.
        
        Args:
            name: Metric name
            value: Metric value
            
        Returns:
            True if recorded successfully
        """
        if name not in self._metrics:
            return False
        
        metric = self._metrics[name]
        metric.current_value = value
        metric.history.append((datetime.now(), value))
        
        # Keep history size limited
        if len(metric.history) > self.config.get("metric_history_size", 100):
            metric.history = metric.history[-self.config.get("metric_history_size", 100):]
        
        logger.info("Metric recorded", name=name, value=value)
        return True
    
    def get_metric(self, name: str) -> Optional[PerformanceMetric]:
        """Get a performance metric"""
        return self._metrics.get(name)
    
    def get_all_metrics(self) -> Dict[str, PerformanceMetric]:
        """Get all performance metrics"""
        return self._metrics.copy()
    
    def calculate_overall_performance(self) -> float:
        """
        Calculate overall system performance score.
        
        Returns:
            Performance score (0.0 to 1.0)
        """
        if not self._metrics:
            return 0.0
        
        total_score = 0.0
        total_weight = 0.0
        
        for metric in self._metrics.values():
            # Normalize metric to 0-1 range
            if metric.target_value > metric.current_value:
                normalized = metric.current_value / metric.target_value if metric.target_value > 0 else 1.0
            else:
                normalized = metric.target_value / metric.current_value if metric.current_value > 0 else 1.0
            
            total_score += normalized * metric.weight
            total_weight += metric.weight
        
        if total_weight > 0:
            return min(1.0, max(0.0, total_score / total_weight))
        
        return 0.0
    
    def register_strategy(
        self,
        strategy_id: str,
        name: str,
        description: str,
        parameters: Dict[str, Any] = None
    ) -> str:
        """
        Register an adaptation strategy.
        
        Args:
            strategy_id: Unique strategy identifier
            name: Strategy name
            description: Strategy description
            parameters: Strategy parameters
            
        Returns:
            Strategy ID
        """
        strategy = AdaptationStrategy(
            strategy_id=strategy_id,
            name=name,
            description=description,
            parameters=parameters or {}
        )
        self._strategies[strategy_id] = strategy
        
        logger.info("Strategy registered", strategy_id=strategy_id, name=name)
        return strategy_id
    
    def get_strategy(self, strategy_id: str) -> Optional[AdaptationStrategy]:
        """Get an adaptation strategy"""
        return self._strategies.get(strategy_id)
    
    def get_all_strategies(self) -> Dict[str, AdaptationStrategy]:
        """Get all adaptation strategies"""
        return self._strategies.copy()
    
    async def suggest_adaptation(self) -> List[Dict[str, Any]]:
        """
        Suggest adaptations based on current system state.
        
        Returns:
            List of suggested adaptations
        """
        suggestions = []
        
        # Get current performance
        performance = self.calculate_overall_performance()
        
        # Check each metric for improvement opportunities
        for metric_name, metric in self._metrics.items():
            # Calculate gap from target
            if metric.target_value > 0:
                gap = abs(metric.current_value - metric.target_value) / metric.target_value
            else:
                gap = 0.0
            
            # If gap is significant, suggest adaptation
            if gap > 0.1:  # 10% gap
                suggestion = {
                    "type": "metric_improvement",
                    "metric": metric_name,
                    "current_value": metric.current_value,
                    "target_value": metric.target_value,
                    "gap": gap,
                    "priority": gap * metric.weight
                }
                suggestions.append(suggestion)
        
        # Add suggestions from sub-components
        rl_suggestions = self.goal_rl.suggest_actions()
        suggestions.extend([
            {"type": "goal_rl", **s} 
            for s in rl_suggestions
        ])
        
        so_suggestions = self.self_optimizing.suggest_optimizations()
        suggestions.extend([
            {"type": "self_optimizing", **s} 
            for s in so_suggestions
        ])
        
        ml_suggestions = self.meta_learning.suggest_learning_strategies()
        suggestions.extend([
            {"type": "meta_learning", **s} 
            for s in ml_suggestions
        ])
        
        # Sort by priority
        suggestions.sort(key=lambda x: x.get("priority", 0), reverse=True)
        
        return suggestions
    
    async def apply_adaptation(
        self,
        adaptation: Dict[str, Any]
    ) -> AdaptationResult:
        """
        Apply an adaptation to the system.
        
        Args:
            adaptation: Adaptation to apply
            
        Returns:
            Adaptation result
        """
        adaptation_id = str(datetime.now().timestamp())
        strategy_id = adaptation.get("strategy_id", "default")
        
        result = AdaptationResult(
            adaptation_id=adaptation_id,
            strategy_id=strategy_id,
            success=False,
            improvement=0.0
        )
        
        try:
            # Apply the adaptation based on type
            adaptation_type = adaptation.get("type", "unknown")
            
            if adaptation_type == "metric_improvement":
                metric_name = adaptation.get("metric")
                if metric_name in self._metrics:
                    # In a real implementation, this would apply specific improvements
                    # For now, we simulate an improvement
                    metric = self._metrics[metric_name]
                    old_value = metric.current_value
                    
                    # Simulate improvement (5-15% of gap closed)
                    import random
                    improvement_percent = random.uniform(0.05, 0.15)
                    gap = abs(metric.target_value - metric.current_value)
                    improvement = gap * improvement_percent
                    
                    if metric.target_value > metric.current_value:
                        new_value = min(metric.target_value, metric.current_value + improvement)
                    else:
                        new_value = max(metric.target_value, metric.current_value - improvement)
                    
                    metric.current_value = new_value
                    result.improvement = improvement
                    result.success = True
                    
                    # Record the change
                    metric.history.append((datetime.now(), new_value))
            
            elif adaptation_type == "goal_rl":
                # Delegate to goal-oriented RL
                success = self.goal_rl.apply_action(adaptation)
                result.success = success
                result.improvement = 0.1 if success else -0.1
            
            elif adaptation_type == "self_optimizing":
                # Delegate to self-optimizing algorithm
                success = self.self_optimizing.apply_optimization(adaptation)
                result.success = success
                result.improvement = 0.1 if success else -0.1
            
            elif adaptation_type == "meta_learning":
                # Delegate to meta-learning system
                success = self.meta_learning.apply_learning_strategy(adaptation)
                result.success = success
                result.improvement = 0.1 if success else -0.1
            
            # Update strategy history
            if strategy_id in self._strategies:
                strategy = self._strategies[strategy_id]
                strategy.usage_count += 1
                if result.success:
                    strategy.success_rate = (strategy.success_rate * (strategy.usage_count - 1) + 1) / strategy.usage_count
                else:
                    strategy.success_rate = (strategy.success_rate * (strategy.usage_count - 1)) / strategy.usage_count
                strategy.last_used = datetime.now()
            
            # Update adaptation state
            self._last_adaptation = datetime.now()
            self._strategy_history.append(result)
            
            logger.info(
                "Adaptation applied",
                adaptation_id=adaptation_id,
                type=adaptation_type,
                success=result.success,
                improvement=result.improvement
            )
            
        except Exception as e:
            logger.error(
                "Failed to apply adaptation",
                adaptation_id=adaptation_id,
                error=str(e)
            )
            result.error = str(e)
        
        return result
    
    async def auto_adapt(self) -> List[AdaptationResult]:
        """
        Automatically adapt the system based on current state.
        
        Returns:
            List of adaptation results
        """
        if self._adaptation_in_progress:
            logger.info("Adaptation already in progress")
            return []
        
        self._adaptation_in_progress = True
        results = []
        
        try:
            # Get suggestions
            suggestions = await self.suggest_adaptation()
            
            # Apply top suggestions
            for suggestion in suggestions[:5]:  # Apply top 5 suggestions
                result = await self.apply_adaptation(suggestion)
                results.append(result)
                
                # Small delay between adaptations
                await asyncio.sleep(0.1)
            
            logger.info(
                "Auto-adaptation complete",
                adaptations_applied=len(results),
                successful=len([r for r in results if r.success])
            )
            
        except Exception as e:
            logger.error("Error in auto-adaptation", error=str(e))
        
        finally:
            self._adaptation_in_progress = False
        
        return results
    
    async def monitor_and_adapt(self, interval: float = 3600.0):
        """
        Continuously monitor system performance and adapt as needed.
        
        Args:
            interval: Monitoring interval in seconds
        """
        while True:
            try:
                # Calculate performance
                performance = self.calculate_overall_performance()
                
                logger.info(
                    "Performance monitoring",
                    overall_performance=performance,
                    metric_count=len(self._metrics)
                )
                
                # Auto-adapt if performance is below threshold
                if performance < 0.8:  # 80% threshold
                    await self.auto_adapt()
                
                # Wait for next interval
                await asyncio.sleep(interval)
                
            except asyncio.CancelledError:
                logger.info("Monitoring and adaptation stopped")
                break
            except Exception as e:
                logger.error("Error in monitoring loop", error=str(e))
                await asyncio.sleep(60)  # Wait before retrying
    
    def get_performance_report(self) -> Dict[str, Any]:
        """
        Get a comprehensive performance report.
        
        Returns:
            Performance report dictionary
        """
        overall_performance = self.calculate_overall_performance()
        
        # Get metrics summary
        metrics_summary = {}
        for name, metric in self._metrics.items():
            metrics_summary[name] = {
                "current": metric.current_value,
                "target": metric.target_value,
                "gap": abs(metric.current_value - metric.target_value),
                "weight": metric.weight
            }
        
        # Get adaptation history
        recent_adaptations = [
            {
                "adaptation_id": r.adaptation_id,
                "strategy_id": r.strategy_id,
                "success": r.success,
                "improvement": r.improvement,
                "timestamp": r.timestamp.isoformat()
            }
            for r in self._strategy_history[-10:]  # Last 10 adaptations
        ]
        
        return {
            "overall_performance": overall_performance,
            "metrics": metrics_summary,
            "recent_adaptations": recent_adaptations,
            "strategy_count": len(self._strategies),
            "last_adaptation": self._last_adaptation.isoformat() if self._last_adaptation else None
        }
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the adaptive intelligence engine"""
        return {
            "engine_type": "AdaptiveIntelligenceEngine",
            "metric_count": len(self._metrics),
            "strategy_count": len(self._strategies),
            "overall_performance": self.calculate_overall_performance(),
            "adaptation_count": len(self._strategy_history),
            "learning_rate": self._learning_rate,
            "exploration_rate": self._exploration_rate
        }
