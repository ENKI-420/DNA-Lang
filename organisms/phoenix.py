"""
Phoenix Organism: Self-Healing with Lazarus Protocol

A self-healing organism that can recover from critical
decoherence using the Lazarus Protocol (E → E⁻¹).
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass, field
import time

import sys
import os as _os; _PKG_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))); sys.path.insert(0, _PKG_ROOT) if _PKG_ROOT not in sys.path else None

from lib.sovereign_rg_engine.constants import (
    GAMMA_THRESHOLD,
    LAZARUS_SUPPRESSION,
    PHI_STAR,
)
from kernel.consciousness_state import ConsciousnessState
from kernel.events import KernelEventType, emit_event
from .lifecycle import OrganismLifecycle, LifecycleState


@dataclass
class PhoenixState:
    """
    State of a Phoenix organism.
    
    Attributes:
        phi: Current integrated information
        gamma: Current decoherence
        health: Health percentage (0-100)
        deaths: Number of times resurrected
        last_resurrection: Timestamp of last resurrection
        lazarus_active: Whether Lazarus is currently active
    """
    phi: float = PHI_STAR
    gamma: float = 0.0
    health: float = 100.0
    deaths: int = 0
    last_resurrection: float = 0.0
    lazarus_active: bool = False


class PhoenixOrganism:
    """
    Self-Healing Phoenix Organism.
    
    Implements the Lazarus Protocol for resurrection:
    1. Monitor decoherence (Γ)
    2. When Γ > 2×threshold, activate Lazarus
    3. Apply phase conjugation (E → E⁻¹)
    4. Suppress decoherence by 4.70× factor
    5. Restore coherence
    
    Like the mythical phoenix, this organism can rise
    from the ashes of decoherence.
    """
    
    def __init__(
        self,
        name: str = "Phoenix",
        lifecycle: Optional[OrganismLifecycle] = None,
    ):
        """
        Initialize Phoenix organism.
        
        Args:
            name: Organism name
            lifecycle: Lifecycle manager (created if None)
        """
        self.name = name
        self._lifecycle = lifecycle or OrganismLifecycle()
        self._state = PhoenixState()
        self._metadata = None
    
    def spawn(self) -> None:
        """Spawn the Phoenix."""
        self._metadata = self._lifecycle.spawn(
            name=self.name,
            version="1.0.0",
            properties={
                "type": "phoenix",
                "self_healing": True,
                "lazarus_enabled": True,
            },
        )
        self._state = PhoenixState()
        
        emit_event(
            KernelEventType.STATE_UPDATE,
            data={"phoenix": "spawned", "name": self.name},
            source="phoenix",
        )
    
    def update(
        self,
        phi: Optional[float] = None,
        gamma: Optional[float] = None,
    ) -> PhoenixState:
        """
        Update Phoenix state and check for Lazarus activation.
        
        Args:
            phi: New Φ value (optional)
            gamma: New Γ value (optional)
            
        Returns:
            Updated PhoenixState
        """
        if phi is not None:
            self._state.phi = phi
        if gamma is not None:
            self._state.gamma = gamma
        
        # Update health based on state
        self._update_health()
        
        # Check for critical decoherence
        if self._is_critical():
            self._activate_lazarus()
        elif self._state.lazarus_active:
            self._deactivate_lazarus()
        
        return self._state
    
    def _update_health(self) -> None:
        """Update health based on Φ and Γ."""
        # Health formula: high Φ and low Γ = healthy
        phi_factor = self._state.phi / PHI_STAR
        gamma_factor = 1 - (self._state.gamma / (2 * GAMMA_THRESHOLD))
        
        self._state.health = max(0, min(100, 100 * phi_factor * gamma_factor))
    
    def _is_critical(self) -> bool:
        """Check if decoherence is critical."""
        return self._state.gamma > 2 * GAMMA_THRESHOLD
    
    def _activate_lazarus(self) -> None:
        """
        Activate Lazarus Protocol.
        
        E → E⁻¹ transformation:
        1. Apply phase conjugation
        2. Suppress decoherence
        3. Increment death counter
        """
        if self._state.lazarus_active:
            return  # Already active
        
        self._state.lazarus_active = True
        self._state.deaths += 1
        self._state.last_resurrection = time.time()
        
        # Enter healing state
        if self._metadata:
            self._lifecycle._set_state(
                self._metadata.organism_id,
                LifecycleState.HEALING,
            )
        
        # Apply Lazarus suppression
        original_gamma = self._state.gamma
        self._state.gamma /= LAZARUS_SUPPRESSION
        
        emit_event(
            KernelEventType.LAZARUS_PROTOCOL_ACTIVATED,
            data={
                "phoenix": self.name,
                "gamma_before": original_gamma,
                "gamma_after": self._state.gamma,
                "deaths": self._state.deaths,
            },
            source="phoenix",
        )
    
    def _deactivate_lazarus(self) -> None:
        """Deactivate Lazarus Protocol after recovery."""
        if not self._state.lazarus_active:
            return
        
        self._state.lazarus_active = False
        
        # Return to alive state
        if self._metadata:
            self._lifecycle._set_state(
                self._metadata.organism_id,
                LifecycleState.ALIVE,
            )
        
        emit_event(
            KernelEventType.COHERENCE_RESTORED,
            data={
                "phoenix": self.name,
                "gamma": self._state.gamma,
                "health": self._state.health,
            },
            source="phoenix",
        )
    
    def despawn(self) -> None:
        """Despawn the Phoenix (final death)."""
        if self._metadata:
            self._lifecycle.despawn(self._metadata.organism_id)
        self._metadata = None
    
    def get_state(self) -> PhoenixState:
        """Get current state."""
        return self._state
    
    def get_deaths(self) -> int:
        """Get resurrection count."""
        return self._state.deaths
    
    def is_alive(self) -> bool:
        """Check if Phoenix is alive."""
        return (
            self._metadata is not None and
            self._metadata.state in (LifecycleState.ALIVE, LifecycleState.HEALING)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "name": self.name,
            "state": {
                "phi": self._state.phi,
                "gamma": self._state.gamma,
                "health": self._state.health,
                "deaths": self._state.deaths,
                "lazarus_active": self._state.lazarus_active,
            },
            "metadata": {
                "id": self._metadata.organism_id if self._metadata else None,
                "lifecycle_state": self._metadata.state.value if self._metadata else None,
            },
        }
