"""
ΩΩ∞ Sovereign Engine - Structure I: Generating Functional Z[μ_Ω]

Implementation of the generating functional for the Sovereign Engine.
This is the path integral over all configurations that encodes the
complete quantum information of the system.

Z[μ_Ω] = ∫ DΨ exp(-S[Ψ, μ_Ω])

where:
- Ψ represents all field configurations
- S is the effective action
- μ_Ω is the RG scale parameter

RG invariance condition:
    μ(dZ/dμ) = (β_i ∂_{g_i} - γ_Ψ N_Ψ)Z = 0
"""

import numpy as np
from typing import Optional, Tuple
from dataclasses import dataclass

from .couplings import RGCouplings
from .constants import LAMBDA_PHI, PHI_STAR


@dataclass
class GeneratingFunctionalResult:
    """Result of generating functional computation."""
    Z: complex  # Partition function value
    free_energy: float  # F = -log(Z)
    susceptibility: float  # χ = ∂²F/∂J²
    anomalous_dimension: float  # γ_Ψ


class GeneratingFunctional:
    """
    Structure I: The Generating Functional Z[μ_Ω]
    
    Computes the path integral over all configurations:
    
    Z[μ_Ω] = ∫ DΨ exp(-S[Ψ, μ_Ω])
    
    Key properties:
    - Anomalous scaling dimension γ_Ψ
    - RG invariance: μ(dZ/dμ) = (β_i ∂_{g_i} - γ_Ψ N_Ψ)Z = 0
    - Connected correlators via log(Z)
    """
    
    def __init__(self, couplings: Optional[RGCouplings] = None):
        """
        Initialize the generating functional.
        
        Args:
            couplings: RG coupling constants (uses defaults if None)
        """
        self.couplings = couplings or RGCouplings()
        self._cache: dict = {}
    
    def compute(
        self,
        mu: float = 1.0,
        num_modes: int = 100,
    ) -> GeneratingFunctionalResult:
        """
        Compute the generating functional at scale μ.
        
        Uses a Gaussian approximation with corrections from
        the coupling constants.
        
        Z ≈ exp(-V × F(μ)) × (det M)^(-1/2) × corrections
        
        where V is the system volume and F is the free energy density.
        
        Args:
            mu: RG scale parameter
            num_modes: Number of modes in the discretized path integral
            
        Returns:
            GeneratingFunctionalResult with Z, free_energy, etc.
        """
        g = self.couplings.to_array()
        
        # Free energy density (Ginzburg-Landau form)
        # F = r φ² + u φ⁴ + ... with coefficients from couplings
        r = 1.0 + g[0] + LAMBDA_PHI * mu**2
        u = g[1] + 0.1
        v = g[2] * 0.01
        
        # Mean field: minimize F with respect to φ
        # At minimum: 2rφ + 4uφ³ = 0
        if r < 0:
            phi_min = np.sqrt(-r / (2 * u))
        else:
            phi_min = 0.0
        
        # Free energy at minimum
        if r < 0:
            f_min = r * phi_min**2 + u * phi_min**4
        else:
            f_min = 0.0
        
        # Fluctuation determinant (one-loop correction)
        mass_squared = 2 * r + 12 * u * phi_min**2
        if mass_squared > 0:
            det_correction = -0.5 * np.log(mass_squared) * num_modes
        else:
            det_correction = 0.0
        
        # ΛΦ correction term
        lambda_correction = -LAMBDA_PHI * mu * num_modes
        
        # Partition function
        total_log_Z = -num_modes * f_min + det_correction + lambda_correction
        Z = complex(np.exp(total_log_Z))
        
        # Free energy (extensive)
        free_energy = -total_log_Z
        
        # Susceptibility (response to external field)
        if mass_squared > 0:
            susceptibility = 1.0 / mass_squared
        else:
            susceptibility = float("inf")
        
        # Anomalous dimension γ_Ψ
        # γ_Ψ = β_g ∂/∂g (log Z_Ψ) where Z_Ψ is wavefunction renormalization
        anomalous_dimension = self._compute_anomalous_dimension(mu)
        
        return GeneratingFunctionalResult(
            Z=Z,
            free_energy=free_energy,
            susceptibility=susceptibility,
            anomalous_dimension=anomalous_dimension,
        )
    
    def _compute_anomalous_dimension(self, mu: float) -> float:
        """
        Compute the anomalous scaling dimension γ_Ψ.
        
        γ_Ψ = d log Z_Ψ / d log μ
        
        where Z_Ψ is the field strength renormalization.
        """
        g = self.couplings.to_array()
        
        # One-loop result: γ_Ψ = c × g²/(16π²) + O(g⁴)
        c = 0.1  # Numerical coefficient
        gamma = c * (g[0]**2 + g[1]**2) / (16 * np.pi**2)
        
        # ΛΦ correction
        gamma += LAMBDA_PHI * 1e6 * (1 - self.couplings.phi / PHI_STAR)
        
        return gamma
    
    def check_rg_invariance(
        self,
        mu: float,
        delta_mu: float = 1e-6,
    ) -> Tuple[float, bool]:
        """
        Check the RG invariance condition.
        
        μ(dZ/dμ) = (β_i ∂_{g_i} - γ_Ψ N_Ψ)Z should equal 0
        
        Args:
            mu: Scale at which to check
            delta_mu: Step size for numerical derivative
            
        Returns:
            Tuple of (violation_magnitude, is_invariant)
        """
        # Compute Z at μ and μ + δμ
        result_1 = self.compute(mu=mu)
        result_2 = self.compute(mu=mu + delta_mu)
        
        # μ dZ/dμ
        dZ_dmu = (result_2.Z - result_1.Z) / delta_mu
        lhs = mu * dZ_dmu
        
        # In the ideal case (at fixed point), this should be zero
        violation = abs(lhs)
        
        # Check if invariance holds (within numerical precision)
        tolerance = 1e-6 * abs(result_1.Z)
        is_invariant = violation < tolerance
        
        return float(violation), is_invariant
    
    def compute_connected_correlator(
        self,
        n: int,
        mu: float = 1.0,
    ) -> float:
        """
        Compute the n-point connected correlation function.
        
        ⟨Ψ(x₁)...Ψ(xₙ)⟩_c = ∂ⁿ log Z / ∂J^n |_{J=0}
        
        Args:
            n: Number of field insertions
            mu: RG scale
            
        Returns:
            n-point connected correlator
        """
        result = self.compute(mu=mu)
        log_Z = np.log(abs(result.Z)) if abs(result.Z) > 0 else 0
        
        # For Gaussian theory, only n=2 is non-zero
        if n == 2:
            return result.susceptibility
        elif n == 4:
            # Four-point from quartic coupling
            g = self.couplings.to_array()
            return -24 * g[1] * result.susceptibility**4
        else:
            return 0.0
    
    def update_couplings(self, couplings: RGCouplings) -> None:
        """Update the coupling constants."""
        self.couplings = couplings
        self._cache.clear()
