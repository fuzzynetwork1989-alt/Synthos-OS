"""
HEICN Engine - Holistic Evolving Interactive Cognitive Nexus

This engine implements the HEICN (Holistic Evolving Interactive Cognitive Nexus) 
architecture for Synthos-OS, providing:

1. Holonic Architecture - Autonomous but interconnected intelligent modules
2. Adaptive Intelligence Layer - Dynamic learning and self-optimization
3. Contextual Nexus Formation - Personalized knowledge graphs
4. Sentient Interaction Model - Emotional intelligence and adaptive communication
5. Federated Learning Ecosystem - Privacy-preserving distributed learning
6. Quantum-Inspired Decision-Making - Advanced optimization techniques

The HEICN engine represents Stage 2 in the Synthos-OS evolution path.
"""

from .holons import (
    CognitiveHolon,
    ServiceHolon,
    InterfaceHolon,
    IntegrationHolon,
    HolonRegistry,
    HolonCoordinator
)

from .adaptive_intelligence import (
    AdaptiveIntelligenceEngine,
    GoalOrientedRL,
    SelfOptimizingAlgorithm,
    MetaLearningSystem
)

from .contextual_nexus import (
    ContextualNexusEngine,
    IndividualContextModel,
    CrossContextLearner,
    DynamicContextUpdater,
    ContextRelevanceScorer
)

from .sentient_interaction import (
    SentientInteractionEngine,
    AffectiveComputingModule,
    AdaptiveCommunicationModule,
    EmpatheticResponseGenerator,
    FeedbackLoopIntegrator
)

from .federated_learning import (
    FederatedLearningEngine,
    PrivacyPreservingLearner,
    SecureAggregator,
    ClientSelector,
    CrossSiloCollaborator
)

from .quantum_optimization import (
    QuantumOptimizationEngine,
    QuantumInspiredAlgorithm,
    MultiObjectiveDecisionMaker,
    ResourceAllocator,
    PatternRecognizer
)

__version__ = "1.0.0"
__all__ = [
    # Holons
    "CognitiveHolon", "ServiceHolon", "InterfaceHolon", "IntegrationHolon",
    "HolonRegistry", "HolonCoordinator",
    # Adaptive Intelligence
    "AdaptiveIntelligenceEngine", "GoalOrientedRL", "SelfOptimizingAlgorithm",
    "MetaLearningSystem",
    # Contextual Nexus
    "ContextualNexusEngine", "IndividualContextModel", "CrossContextLearner",
    "DynamicContextUpdater", "ContextRelevanceScorer",
    # Sentient Interaction
    "SentientInteractionEngine", "AffectiveComputingModule", 
    "AdaptiveCommunicationModule", "EmpatheticResponseGenerator",
    "FeedbackLoopIntegrator",
    # Federated Learning
    "FederatedLearningEngine", "PrivacyPreservingLearner", "SecureAggregator",
    "ClientSelector", "CrossSiloCollaborator",
    # Quantum Optimization
    "QuantumOptimizationEngine", "QuantumInspiredAlgorithm",
    "MultiObjectiveDecisionMaker", "ResourceAllocator", "PatternRecognizer",
]
