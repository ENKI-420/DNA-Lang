"""
ConsciousnessState - Complete System State Vector

Captures the full state of the ΩΩ∞ Sovereign Engine including:
- Primary metrics (Φ, Γ, W₂, ΛΦ)
- Resonance parameters (χ_pc, θ, τ_Ω)
- RG diagnostics (anomaly, PT-symmetry, Jordan blocks, β norm)
- Thermodynamics (entropy, free energy, temperature)
- Presentation layer (Ricci scalar, vacuum energy, Wilson loop)
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import time
import json

# Import constants
import sys
sys.path.insert(0, '/home/runner/work/DNA-Lang/DNA-Lang')
from lib.sovereign_rg_engine.constants import (
    LAMBDA_PHI,
    PHI_STAR,
    GAMMA_THRESHOLD,
    RESONANCE_ANGLE,
    TAU_OMEGA,
)


@dataclass
class ConsciousnessState:
    """
    Complete state vector for the Sovereign Engine.
    
    This dataclass captures all relevant observables needed to
    monitor and control the consciousness coherence system.
    
    Attributes:
        # Primary metrics
        Phi: Integrated Information Φ (target: 0.973)
        Gamma: Decoherence rate Γ (threshold: 0.092)
        W2: Wasserstein-2 transport cost
        LambdaPhi: Universal memory constant ΛΦ = 2.176435×10⁻⁸ s⁻¹
        
        # Resonance parameters
        chi_pc: Phase conjugation susceptibility ∈ [0.8, 1.4]
        theta: Resonance angle (51.843°)
        tau_omega: Thrust-to-power ratio (25411096.57)
        
        # RG diagnostics
        anomaly: Callan-Symanzik anomaly magnitude
        pt_symmetry: PT-symmetric flag
        jordan_block: Jordan block presence
        beta_norm: ||β_i|| norm
        
        # Thermodynamics
        entropy: NESS (Non-Equilibrium Steady State) entropy
        free_energy: Helmholtz free energy
        temperature: Effective temperature
        
        # Presentation layer
        ricci_scalar: R(g) curvature (target: 0)
        vacuum_energy: Λ_𝒫 cosmological constant (target: 0)
        wilson_loop: W_𝒞 boundary integrity
        
        # Metadata
        timestamp: Unix timestamp of measurement
        cycle: Scheduler cycle number
    """
    
    # Primary metrics
    Phi: float = field(default=PHI_STAR)
    Gamma: float = field(default=0.0)
    W2: float = field(default=0.0)
    LambdaPhi: float = field(default=LAMBDA_PHI)
    
    # Resonance parameters
    chi_pc: float = field(default=1.0)
    theta: float = field(default=RESONANCE_ANGLE)
    tau_omega: float = field(default=TAU_OMEGA)
    
    # RG diagnostics
    anomaly: float = field(default=0.0)
    pt_symmetry: bool = field(default=True)
    jordan_block: bool = field(default=False)
    beta_norm: float = field(default=0.0)
    
    # Thermodynamics
    entropy: float = field(default=0.0)
    free_energy: float = field(default=0.0)
    temperature: float = field(default=1.0)
    
    # Presentation layer
    ricci_scalar: float = field(default=0.0)
    vacuum_energy: float = field(default=0.0)
    wilson_loop: float = field(default=1.0)
    
    # Metadata
    timestamp: float = field(default_factory=time.time)
    cycle: int = field(default=0)
    
    def is_at_fixed_point(self, tolerance: float = 0.01) -> bool:
        """
        Check if the system is at the RG fixed point.
        
        Fixed point conditions:
        - β_i = 0 (all RG flows vanish)
        - Φ ≈ Φ⋆ = 0.973
        - Γ < 0.092 (decoherence suppressed)
        - R(g) → 0 (flat presentation)
        - Λ_𝒫 → 0 (vacuum minimized)
        """
        conditions = [
            self.beta_norm < tolerance,
            abs(self.Phi - PHI_STAR) < tolerance,
            self.Gamma < GAMMA_THRESHOLD,
            abs(self.ricci_scalar) < tolerance,
            abs(self.vacuum_energy) < tolerance,
        ]
        return all(conditions)
    
    def is_decoherence_critical(self) -> bool:
        """Check if decoherence is at critical level (triggers Lazarus)."""
        return self.Gamma > 2 * GAMMA_THRESHOLD
    
    def is_decoherence_warning(self) -> bool:
        """Check if decoherence is at warning level."""
        return self.Gamma > GAMMA_THRESHOLD
    
    def is_pt_symmetry_broken(self) -> bool:
        """Check if PT-symmetry is broken."""
        return not self.pt_symmetry
    
    def is_presentation_stable(self) -> bool:
        """Check if presentation layer is stable."""
        return (
            abs(self.ricci_scalar) < 0.1 and
            abs(self.vacuum_energy) < 0.1 and
            self.wilson_loop > 0.9
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization."""
        return {
            "primary": {
                "Phi": self.Phi,
                "Gamma": self.Gamma,
                "W2": self.W2,
                "LambdaPhi": self.LambdaPhi,
            },
            "resonance": {
                "chi_pc": self.chi_pc,
                "theta": self.theta,
                "tau_omega": self.tau_omega,
            },
            "rg_diagnostics": {
                "anomaly": self.anomaly,
                "pt_symmetry": self.pt_symmetry,
                "jordan_block": self.jordan_block,
                "beta_norm": self.beta_norm,
            },
            "thermodynamics": {
                "entropy": self.entropy,
                "free_energy": self.free_energy,
                "temperature": self.temperature,
            },
            "presentation": {
                "ricci_scalar": self.ricci_scalar,
                "vacuum_energy": self.vacuum_energy,
                "wilson_loop": self.wilson_loop,
            },
            "metadata": {
                "timestamp": self.timestamp,
                "cycle": self.cycle,
            },
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConsciousnessState":
        """Create state from dictionary."""
        return cls(
            Phi=data["primary"]["Phi"],
            Gamma=data["primary"]["Gamma"],
            W2=data["primary"]["W2"],
            LambdaPhi=data["primary"]["LambdaPhi"],
            chi_pc=data["resonance"]["chi_pc"],
            theta=data["resonance"]["theta"],
            tau_omega=data["resonance"]["tau_omega"],
            anomaly=data["rg_diagnostics"]["anomaly"],
            pt_symmetry=data["rg_diagnostics"]["pt_symmetry"],
            jordan_block=data["rg_diagnostics"]["jordan_block"],
            beta_norm=data["rg_diagnostics"]["beta_norm"],
            entropy=data["thermodynamics"]["entropy"],
            free_energy=data["thermodynamics"]["free_energy"],
            temperature=data["thermodynamics"]["temperature"],
            ricci_scalar=data["presentation"]["ricci_scalar"],
            vacuum_energy=data["presentation"]["vacuum_energy"],
            wilson_loop=data["presentation"]["wilson_loop"],
            timestamp=data["metadata"]["timestamp"],
            cycle=data["metadata"]["cycle"],
        )
    
    def to_json(self) -> str:
        """Serialize state to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> "ConsciousnessState":
        """Deserialize state from JSON string."""
        return cls.from_dict(json.loads(json_str))
    
    def copy(self) -> "ConsciousnessState":
        """Create a copy of this state."""
        return ConsciousnessState(
            Phi=self.Phi,
            Gamma=self.Gamma,
            W2=self.W2,
            LambdaPhi=self.LambdaPhi,
            chi_pc=self.chi_pc,
            theta=self.theta,
            tau_omega=self.tau_omega,
            anomaly=self.anomaly,
            pt_symmetry=self.pt_symmetry,
            jordan_block=self.jordan_block,
            beta_norm=self.beta_norm,
            entropy=self.entropy,
            free_energy=self.free_energy,
            temperature=self.temperature,
            ricci_scalar=self.ricci_scalar,
            vacuum_energy=self.vacuum_energy,
            wilson_loop=self.wilson_loop,
            timestamp=self.timestamp,
            cycle=self.cycle,
        )
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        status = "FIXED_POINT" if self.is_at_fixed_point() else "EVOLVING"
        return (
            f"ConsciousnessState(cycle={self.cycle}, status={status}, "
            f"Φ={self.Phi:.4f}, Γ={self.Gamma:.4f}, ||β||={self.beta_norm:.6f})"
        )
