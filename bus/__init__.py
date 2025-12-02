"""
Bus Package for ΩΩ∞ Sovereign Engine

Provides message bus with W₂-stable ordering for inter-component
communication.
"""

from .manifold_bus import ManifoldBus, BusMessage

__all__ = [
    "ManifoldBus",
    "BusMessage",
]
