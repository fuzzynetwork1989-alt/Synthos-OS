"""
Holonic Architecture for HEICN

Holons are autonomous but interconnected intelligent modules that form
the foundation of the HEICN architecture. Each holon can operate 
independently while cooperating with other holons for complex tasks.

Types of Holons:
- Cognitive Holons: Specialized AI modules for reasoning, planning, memory, etc.
- Service Holons: Infrastructure modules for data, communication, storage
- Interface Holons: User interaction modules for different modalities
- Integration Holons: External system connectors and adapters

Key Capabilities:
- Independent operation when needed
- Cooperation with other holons for complex tasks
- Self-healing and reconfiguration based on conditions
- Independent scaling based on workload
"""

from .base import BaseHolon, HolonType, HolonStatus
from .cognitive_holon import CognitiveHolon
from .service_holon import ServiceHolon
from .interface_holon import InterfaceHolon
from .integration_holon import IntegrationHolon
from .registry import HolonRegistry
from .coordinator import HolonCoordinator

__all__ = [
    "BaseHolon", "HolonType", "HolonStatus",
    "CognitiveHolon", "ServiceHolon", "InterfaceHolon", "IntegrationHolon",
    "HolonRegistry", "HolonCoordinator"
]
