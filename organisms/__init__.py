"""
Organisms Package for ΩΩ∞ Sovereign Engine

Provides organism lifecycle management:
- Lifecycle: Spawn/Despawn/Mutate operations
- Phoenix: Self-healing organism with Lazarus Protocol
- Genome: DNA sequence encoding
"""

from .lifecycle import OrganismLifecycle, LifecycleState
from .phoenix import PhoenixOrganism
from .genome import Genome, Gene

__all__ = [
    "OrganismLifecycle",
    "LifecycleState",
    "PhoenixOrganism",
    "Genome",
    "Gene",
]
