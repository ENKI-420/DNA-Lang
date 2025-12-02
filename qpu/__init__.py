"""
QPU (Quantum Processing Unit) Package for ΩΩ∞ Sovereign Engine

Provides quantum computing infrastructure:
- MeshNet-6D: Distributed coherence transport
- QuantumBridge: Virtual QPU ↔ Hardware interface
- SovereignQuantumBackend: Main quantum backend
"""

from .meshnet6d import MeshNet6D
from .quantumbridge import QuantumBridge
from .backend import SovereignQuantumBackend

__all__ = [
    "MeshNet6D",
    "QuantumBridge",
    "SovereignQuantumBackend",
]
