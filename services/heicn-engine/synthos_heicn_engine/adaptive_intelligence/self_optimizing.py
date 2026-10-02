"""
Self-Optimizing Algorithm for HEICN

This module implements self-optimizing algorithms that automatically tune
system performance based on feedback and observed behavior.
"""

from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
import structlog
from datetime import datetime
import numpy as np
import random

logger = structlog.get_logger(__name__)


@dataclass
class Parameter:
    """A tunable parameter"""
    name: str
    description: str
    value: float
    min_value: float
    max_value: float
    step_size: float = 0.1
    optimal_value: Optional[float] = None
    history: List[Tuple[datetime, float]] = field(default_factory=list)


@dataclass
class OptimizationTarget:
    """A target for optimization"""
    name: str
    description: str
    current_value: float
    target_value: float
    weight: float = 1.0
    improvement_direction: str = "maximize"  # "maximize" or "minimize"


@dataclass
class OptimizationResult:
    """Result of an optimization"""
    optimization_id: str
    parameter: str
    old_value: float
    new_value: float
    improvement: float
    success: bool
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class TuningStrategy:
    """A strategy for tuning parameters"""
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    success_rate: float = 0.0
    usage_count: int = 0


class SelfOptimizingAlgorithm:
    """
    Self-Optimizing Algorithm System.
    
    This system:
    - Automatically tunes system parameters
    - Optimizes for multiple objectives
    - Learns from optimization results
    - Adapts tuning strategies based on success
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the self-optimizing algorithm.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._default_config()
        
        # Parameters to optimize
        self._parameters: Dict[str, Parameter] = {}
        
        # Optimization targets
        self._targets: Dict[str, OptimizationTarget] = {}
        
        # Tuning strategies
        self._strategies: Dict[str, TuningStrategy] = {}
        
        # Optimization history
        self._optimization_history: List[OptimizationResult] = []
        
        # Current optimization state
        self._optimization_in_progress: bool = False
        self._current_optimization: Optional[str] = None
        
        # Learning state
        self._learning_rate = self.config.get("learning_rate", 0.1)
        self._exploration_rate = self.config.get("exploration_rate", 0.2)
        
        # Register default strategies
        self._register_default_strategies()
        
        logger.info("SelfOptimizingAlgorithm initialized")
    
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            "learning_rate": 0.1,
            "exploration_rate": 0.2,
            "max_history": 1000,
            "optimization_interval": 3600,  # 1 hour
            "tuning_step_size": 0.1,
            "max_iterations": 100
        }
    
    def _register_default_strategies(self):
        """Register default tuning strategies"""
        # Gradient Descent
        self.register_strategy(
            "gradient_descent",
            "Gradient Descent",
            "Adjusts parameters in the direction of improvement"
        )
        
        # Random Search
        self.register_strategy(
            "random_search",
            "Random Search",
            "Randomly samples parameter space"
        )
        
        # Bayesian Optimization
        self.register_strategy(
            "bayesian",
            "Bayesian Optimization",
            "Uses probabilistic models to find optimal parameters"
        )
        
        # Hill Climbing
        self.register_strategy(
            "hill_climbing",
            "Hill Climbing",
            "Iteratively improves parameters in the direction of better performance"
        )
    
    def register_parameter(
        self,
        name: str,
        description: str,
        value: float,
        min_value: float,
        max_value: float,
        step_size: float = 0.1
    ) -> str:
        """
        Register a tunable parameter.
        
        Args:
            name: Parameter name
            description: Parameter description
            value: Initial value
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            step_size: Step size for adjustments
            
        Returns:
            Parameter name
        """
        param = Parameter(
            name=name,
            description=description,
            value=value,
            min_value=min_value,
            max_value=max_value,
            step_size=step_size,
            history=[(datetime.now(), value)]
        )
        self._parameters[name] = param
        
        logger.info("Parameter registered", name=name, value=value)
        return name
    
    def get_parameter(self, name: str) -> Optional[Parameter]:
        """Get a parameter by name"""
        return self._parameters.get(name)
    
    def get_all_parameters(self) -> Dict[str, Parameter]:
        """Get all parameters"""
        return self._parameters.copy()
    
    def set_parameter(self, name: str, value: float) -> bool:
        """
        Set a parameter value.
        
        Args:
            name: Parameter name
            value: New value
            
        Returns:
            True if set successfully
        """
        if name not in self._parameters:
            return False
        
        param = self._parameters[name]
        
        # Clamp value to bounds
        value = max(param.min_value, min(param.max_value, value))
        
        # Update value and history
        param.value = value
        param.history.append((datetime.now(), value))
        
        # Keep history limited
        if len(param.history) > self.config.get("max_history", 1000):
            param.history = param.history[-1000:]
        
        logger.info("Parameter set", name=name, value=value)
        return True
    
    def register_target(
        self,
        name: str,
        description: str,
        current_value: float,
        target_value: float,
        weight: float = 1.0,
        improvement_direction: str = "maximize"
    ) -> str:
        """
        Register an optimization target.
        
        Args:
            name: Target name
            description: Target description
            current_value: Current value
            target_value: Target value
            weight: Importance weight
            improvement_direction: "maximize" or "minimize"
            
        Returns:
            Target name
        """
        target = OptimizationTarget(
            name=name,
            description=description,
            current_value=current_value,
            target_value=target_value,
            weight=weight,
            improvement_direction=improvement_direction
        )
        self._targets[name] = target
        
        logger.info("Target registered", name=name, current=current_value, target=target_value)
        return name
    
    def update_target(self, name: str, current_value: float) -> bool:
        """
        Update the current value of a target.
        
        Args:
            name: Target name
            current_value: New current value
            
        Returns:
            True if updated successfully
        """
        if name not in self._targets:
            return False
        
        self._targets[name].current_value = current_value
        
        logger.info("Target updated", name=name, current=current_value)
        return True
    
    def get_target(self, name: str) -> Optional[OptimizationTarget]:
        """Get a target by name"""
        return self._targets.get(name)
    
    def get_all_targets(self) -> Dict[str, OptimizationTarget]:
        """Get all targets"""
        return self._targets.copy()
    
    def register_strategy(
        self,
        strategy_id: str,
        name: str,
        description: str,
        parameters: Dict[str, Any] = None
    ) -> str:
        """
        Register a tuning strategy.
        
        Args:
            strategy_id: Unique strategy identifier
            name: Strategy name
            description: Strategy description
            parameters: Strategy parameters
            
        Returns:
            Strategy ID
        """
        strategy = TuningStrategy(
            name=name,
            description=description,
            parameters=parameters or {}
        )
        self._strategies[strategy_id] = strategy
        
        logger.info("Strategy registered", strategy_id=strategy_id, name=name)
        return strategy_id
    
    def get_strategy(self, strategy_id: str) -> Optional[TuningStrategy]:
        """Get a strategy by ID"""
        return self._strategies.get(strategy_id)
    
    def get_all_strategies(self) -> Dict[str, TuningStrategy]:
        """Get all strategies"""
        return self._strategies.copy()
    
    def calculate_overall_score(self) -> float:
        """
        Calculate the overall optimization score.
        
        Returns:
            Overall score (0.0 to 1.0)
        """
        if not self._targets:
            return 0.0
        
        total_score = 0.0
        total_weight = 0.0
        
        for target in self._targets.values():
            # Normalize target value
            if target.improvement_direction == "maximize":
                if target.target_value > 0:
                    normalized = min(1.0, target.current_value / target.target_value)
                else:
                    normalized = 1.0
            else:  # minimize
                if target.target_value > 0:
                    normalized = max(0.0, 1.0 - (target.current_value / target.target_value))
                else:
                    normalized = 1.0
            
            total_score += normalized * target.weight
            total_weight += target.weight
        
        if total_weight > 0:
            return min(1.0, max(0.0, total_score / total_weight))
        
        return 0.0
    
    def suggest_optimizations(self) -> List[Dict[str, Any]]:
        """
        Suggest parameter optimizations.
        
        Returns:
            List of suggested optimizations
        """
        suggestions = []
        
        overall_score = self.calculate_overall_score()
        
        # For each parameter, suggest potential improvements
        for param_name, param in self._parameters.items():
            # Check if parameter has been optimized recently
            if len(param.history) < 2:
                continue
            
            # Get recent trend
            recent_values = [v for _, v in param.history[-5:]]
            if len(recent_values) < 2:
                continue
            
            # Calculate trend
            trend = recent_values[-1] - recent_values[0]
            
            # Suggest adjustment based on trend and current score
            if overall_score < 0.8:  # Below target
                # Suggest moving in the direction that improved recent performance
                if trend > 0:
                    # Positive trend, continue in same direction
                    suggested_value = min(param.max_value, param.value + param.step_size)
                else:
                    # Negative or no trend, try opposite direction
                    suggested_value = max(param.min_value, param.value - param.step_size)
                
                improvement = abs(trend) * param.weight if param_name in self._targets else 0.1
                
                suggestions.append({
                    "parameter": param_name,
                    "current_value": param.value,
                    "suggested_value": suggested_value,
                    "improvement": improvement,
                    "priority": improvement,
                    "strategy": "trend_based"
                })
        
        # Sort by priority
        suggestions.sort(key=lambda x: x["priority"], reverse=True)
        
        return suggestions
    
    def apply_optimization(self, optimization: Dict[str, Any]) -> bool:
        """
        Apply a parameter optimization.
        
        Args:
            optimization: Optimization to apply
            
        Returns:
            True if applied successfully
        """
        param_name = optimization.get("parameter")
        suggested_value = optimization.get("suggested_value")
        
        if param_name not in self._parameters:
            return False
        
        param = self._parameters[param_name]
        old_value = param.value
        
        # Apply the optimization
        new_value = max(param.min_value, min(param.max_value, suggested_value))
        self.set_parameter(param_name, new_value)
        
        # Record the optimization
        optimization_id = str(datetime.now().timestamp())
        result = OptimizationResult(
            optimization_id=optimization_id,
            parameter=param_name,
            old_value=old_value,
            new_value=new_value,
            improvement=optimization.get("improvement", 0.0),
            success=True
        )
        self._optimization_history.append(result)
        
        # Keep history limited
        if len(self._optimization_history) > self.config.get("max_history", 1000):
            self._optimization_history = self._optimization_history[-1000:]
        
        logger.info(
            "Optimization applied",
            parameter=param_name,
            old_value=old_value,
            new_value=new_value
        )
        
        return True
    
    async def auto_optimize(self, iterations: int = 10) -> List[OptimizationResult]:
        """
        Automatically optimize parameters.
        
        Args:
            iterations: Number of optimization iterations
            
        Returns:
            List of optimization results
        """
        if self._optimization_in_progress:
            logger.info("Optimization already in progress")
            return []
        
        self._optimization_in_progress = True
        results = []
        
        try:
            for i in range(iterations):
                # Get suggestions
                suggestions = self.suggest_optimizations()
                
                if not suggestions:
                    break
                
                # Apply top suggestion
                suggestion = suggestions[0]
                success = self.apply_optimization(suggestion)
                
                if success:
                    results.append(OptimizationResult(
                        optimization_id=str(datetime.now().timestamp()),
                        parameter=suggestion["parameter"],
                        old_value=suggestion["current_value"],
                        new_value=suggestion["suggested_value"],
                        improvement=suggestion["improvement"],
                        success=True
                    ))
                
                # Small delay between iterations
                import asyncio
                await asyncio.sleep(0.1)
            
            logger.info(
                "Auto-optimization complete",
                iterations=i + 1,
                optimizations_applied=len(results)
            )
            
        except Exception as e:
            logger.error("Error in auto-optimization", error=str(e))
        
        finally:
            self._optimization_in_progress = False
        
        return results
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """
        Get a comprehensive optimization report.
        
        Returns:
            Optimization report dictionary
        """
        overall_score = self.calculate_overall_score()
        
        # Get parameter summary
        parameter_summary = {}
        for name, param in self._parameters.items():
            parameter_summary[name] = {
                "value": param.value,
                "min": param.min_value,
                "max": param.max_value,
                "history_count": len(param.history)
            }
        
        # Get target summary
        target_summary = {}
        for name, target in self._targets.items():
            target_summary[name] = {
                "current": target.current_value,
                "target": target.target_value,
                "direction": target.improvement_direction
            }
        
        # Get recent optimizations
        recent_optimizations = [
            {
                "optimization_id": r.optimization_id,
                "parameter": r.parameter,
                "old_value": r.old_value,
                "new_value": r.new_value,
                "improvement": r.improvement,
                "success": r.success,
                "timestamp": r.timestamp.isoformat()
            }
            for r in self._optimization_history[-10:]  # Last 10 optimizations
        ]
        
        return {
            "overall_score": overall_score,
            "parameters": parameter_summary,
            "targets": target_summary,
            "recent_optimizations": recent_optimizations,
            "strategy_count": len(self._strategies)
        }
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the self-optimizing algorithm"""
        return {
            "system_type": "SelfOptimizingAlgorithm",
            "parameter_count": len(self._parameters),
            "target_count": len(self._targets),
            "strategy_count": len(self._strategies),
            "overall_score": self.calculate_overall_score(),
            "optimization_count": len(self._optimization_history),
            "learning_rate": self._learning_rate,
            "exploration_rate": self._exploration_rate
        }
