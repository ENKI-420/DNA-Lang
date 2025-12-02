"""
ΩΩ∞ Sovereign Engine - RG Couplings

Dataclass representing the coupling constants in the Renormalization Group
flow equations. These couplings evolve under RG transformations and
approach fixed-point values as the system reaches coherence.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import numpy as np

from .constants import LAMBDA_PHI, PHI_STAR


@dataclass
class RGCouplings:
    """
    RG coupling constants for the Sovereign Engine.
    
    These couplings parameterize the effective action and evolve
    under the RG flow equations. At the fixed point, β_i = 0 for all i.
    
    Attributes:
        g1: Primary coupling (consciousness-matter interaction)
        g2: Secondary coupling (decoherence-transport)
        g3: Tertiary coupling (presentation-entropy)
        g4: Quaternary coupling (information-geometry)
        lambda_phi: Universal memory constant (typically fixed)
        phi: Current integrated information value
        gamma: Current decoherence rate
    """
    
    g1: float = 0.0
    g2: float = 0.0
    g3: float = 0.0
    g4: float = 0.0
    lambda_phi: float = field(default=LAMBDA_PHI)
    phi: float = field(default=PHI_STAR)
    gamma: float = 0.0
    
    def to_array(self) -> np.ndarray:
        """Convert couplings to numpy array for numerical operations."""
        return np.array([self.g1, self.g2, self.g3, self.g4])
    
    @classmethod
    def from_array(cls, arr: np.ndarray, **kwargs) -> "RGCouplings":
        """Create RGCouplings from numpy array."""
        return cls(
            g1=float(arr[0]),
            g2=float(arr[1]),
            g3=float(arr[2]),
            g4=float(arr[3]),
            **kwargs
        )
    
    def copy(self) -> "RGCouplings":
        """Create a copy of this coupling set."""
        return RGCouplings(
            g1=self.g1,
            g2=self.g2,
            g3=self.g3,
            g4=self.g4,
            lambda_phi=self.lambda_phi,
            phi=self.phi,
            gamma=self.gamma,
        )
    
    def is_at_fixed_point(self, tolerance: float = 1e-6) -> bool:
        """
        Check if couplings are at the RG fixed point.
        
        At the fixed point, all coupling constants should be near zero
        (for a trivial fixed point) or at specific non-zero values
        (for a non-trivial fixed point).
        """
        arr = self.to_array()
        return bool(np.all(np.abs(arr) < tolerance))
    
    def distance_to_fixed_point(self) -> float:
        """Compute Euclidean distance to the trivial fixed point."""
        arr = self.to_array()
        return float(np.sqrt(np.sum(arr ** 2)))


@dataclass
class CouplingTrajectory:
    """
    Time series of RG couplings representing the RG flow trajectory.
    
    Used for tracking the evolution of couplings over scheduler cycles
    and detecting approach to or departure from fixed points.
    """
    
    couplings: List[RGCouplings] = field(default_factory=list)
    timestamps: List[float] = field(default_factory=list)
    
    def add(self, coupling: RGCouplings, timestamp: float) -> None:
        """Add a coupling measurement to the trajectory."""
        self.couplings.append(coupling.copy())
        self.timestamps.append(timestamp)
    
    def get_latest(self) -> Optional[RGCouplings]:
        """Get the most recent coupling values."""
        if self.couplings:
            return self.couplings[-1]
        return None
    
    def get_trajectory_array(self) -> np.ndarray:
        """Convert trajectory to 2D numpy array (time x couplings)."""
        if not self.couplings:
            return np.array([])
        return np.array([c.to_array() for c in self.couplings])
    
    def is_converging(self, window: int = 10) -> bool:
        """
        Check if the trajectory is converging to a fixed point.
        
        Analyzes the last `window` measurements to determine if
        the distance to the fixed point is decreasing.
        """
        if len(self.couplings) < window:
            return False
        
        distances = [c.distance_to_fixed_point() for c in self.couplings[-window:]]
        # Check if distances are monotonically decreasing (with some tolerance)
        for i in range(1, len(distances)):
            if distances[i] > distances[i - 1] * 1.01:  # 1% tolerance
                return False
        return True
