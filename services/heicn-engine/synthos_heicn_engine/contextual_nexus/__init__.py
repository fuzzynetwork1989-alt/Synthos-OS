"""
Contextual Nexus Formation for HEICN

The Contextual Nexus Formation system builds and maintains personalized
knowledge graphs that evolve from user interactions, providing context-aware
intelligence for the HEICN architecture.

Components:
1. Individual Context Models - Evolving representations of user knowledge
2. Cross-Context Learning - Knowledge transfer between domains
3. Dynamic Context Updates - Real-time context adaptation
4. Context Relevance Scoring - Automatic ranking of context importance
"""

from .individual_context import IndividualContextModel
from .cross_context import CrossContextLearner
from .dynamic_updater import DynamicContextUpdater
from .relevance_scorer import ContextRelevanceScorer
from .nexus_engine import ContextualNexusEngine

__all__ = [
    "IndividualContextModel",
    "CrossContextLearner",
    "DynamicContextUpdater",
    "ContextRelevanceScorer",
    "ContextualNexusEngine"
]
