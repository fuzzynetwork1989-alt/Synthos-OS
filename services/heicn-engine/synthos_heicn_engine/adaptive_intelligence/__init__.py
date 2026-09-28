"""
Adaptive Intelligence Layer for HEICN

The Adaptive Intelligence Layer provides dynamic learning and self-optimization
capabilities for the HEICN architecture, including:

1. Goal-Oriented Reinforcement Learning - Dynamic objective adjustment
2. Self-Optimizing Algorithms - Automatic performance tuning
3. Meta-Learning - Learning how to learn more efficiently
4. Context-Aware Adaptation - Behavior adaptation based on environment
"""

from .goal_oriented_rl import GoalOrientedRL
from .self_optimizing import SelfOptimizingAlgorithm
from .meta_learning import MetaLearningSystem
from .adaptive_engine import AdaptiveIntelligenceEngine

__all__ = [
    "GoalOrientedRL",
    "SelfOptimizingAlgorithm", 
    "MetaLearningSystem",
    "AdaptiveIntelligenceEngine"
]
