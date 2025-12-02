"""
ΩΩ∞ Sovereign Engine - Callan-Symanzik Equation

Implementation of the Callan-Symanzik (CS) operator that governs
scale transformations and anomalous scaling in the Sovereign Engine.

The CS equation:
    [μ ∂/∂μ + β_i ∂/∂g_i - γ_Ψ N_Ψ] Γ^(n) = 0

where:
- μ is the RG scale
- β_i are the beta functions
- γ_Ψ is the anomalous dimension
- N_Ψ counts field insertions
- Γ^(n) are the n-point vertex functions
"""

import numpy as np
from typing import Optional, Tuple, Callable
from dataclasses import dataclass

from .couplings import RGCouplings
from .beta_functions import compute_beta_functions, beta_norm
from .constants import LAMBDA_PHI, PHI_STAR


@dataclass
class CallanSymanzikResult:
    """Result of Callan-Symanzik analysis."""
    anomaly: float  # CS equation violation magnitude
    anomalous_dimension: float  # γ_Ψ
    beta_norm: float  # ||β_i||
    is_fixed_point: bool  # Whether system is at fixed point
    scaling_violation: float  # Measure of scale invariance breaking


class CallanSymanzikOperator:
    """
    Callan-Symanzik Operator for the Sovereign Engine.
    
    Implements the CS differential operator:
    
    D_CS = μ ∂/∂μ + β_i ∂/∂g_i - γ_Ψ N_Ψ
    
    At a fixed point, D_CS Γ = 0 for all vertex functions Γ.
    """
    
    def __init__(self, couplings: Optional[RGCouplings] = None):
        """
        Initialize the CS operator.
        
        Args:
            couplings: RG coupling constants
        """
        self.couplings = couplings or RGCouplings()
    
    def compute_anomalous_dimension(self) -> float:
        """
        Compute the anomalous dimension γ_Ψ.
        
        γ_Ψ = μ ∂log(Z_Ψ)/∂μ
        
        where Z_Ψ is the field strength renormalization.
        
        Returns:
            Anomalous dimension value
        """
        g = self.couplings.to_array()
        
        # One-loop anomalous dimension
        # γ_Ψ = (g₁² + g₂²)/(16π²) × c₁
        c1 = 1.0
        gamma = c1 * (g[0]**2 + g[1]**2) / (16 * np.pi**2)
        
        # Two-loop correction
        c2 = 0.1
        gamma += c2 * (g[0]**4 + g[1]**4) / (16 * np.pi**2)**2
        
        # ΛΦ correction (ensures stability at the Sovereign fixed point)
        lambda_correction = LAMBDA_PHI * 1e6
        gamma *= (1 + lambda_correction)
        
        # Consciousness coupling correction
        phi_deviation = abs(self.couplings.phi - PHI_STAR) / PHI_STAR
        gamma += 0.01 * phi_deviation
        
        return gamma
    
    def apply(
        self,
        vertex_function: Callable[[float, np.ndarray], float],
        mu: float,
        n_fields: int = 2,
        delta: float = 1e-6,
    ) -> Tuple[float, CallanSymanzikResult]:
        """
        Apply the CS operator to a vertex function.
        
        D_CS Γ = [μ ∂/∂μ + β_i ∂/∂g_i - γ_Ψ n] Γ
        
        Args:
            vertex_function: Function Γ(μ, g) to analyze
            mu: Scale parameter
            n_fields: Number of field insertions
            delta: Step size for numerical derivatives
            
        Returns:
            Tuple of (D_CS Γ value, CallanSymanzikResult)
        """
        g = self.couplings.to_array()
        beta = compute_beta_functions(self.couplings)
        gamma = self.compute_anomalous_dimension()
        
        # Compute Γ at reference point
        Gamma_0 = vertex_function(mu, g)
        
        # Compute μ ∂Γ/∂μ
        Gamma_mu_plus = vertex_function(mu + delta, g)
        d_Gamma_d_mu = (Gamma_mu_plus - Gamma_0) / delta
        term_1 = mu * d_Gamma_d_mu
        
        # Compute β_i ∂Γ/∂g_i
        term_2 = 0.0
        for i in range(len(g)):
            g_plus = g.copy()
            g_plus[i] += delta
            Gamma_g_plus = vertex_function(mu, g_plus)
            d_Gamma_d_gi = (Gamma_g_plus - Gamma_0) / delta
            term_2 += beta[i] * d_Gamma_d_gi
        
        # Compute -γ_Ψ n Γ
        term_3 = -gamma * n_fields * Gamma_0
        
        # Total CS operator action
        D_CS_Gamma = term_1 + term_2 + term_3
        
        # Analysis result
        result = CallanSymanzikResult(
            anomaly=abs(D_CS_Gamma),
            anomalous_dimension=gamma,
            beta_norm=beta_norm(self.couplings),
            is_fixed_point=beta_norm(self.couplings) < 1e-6,
            scaling_violation=abs(D_CS_Gamma / (Gamma_0 + 1e-10)),
        )
        
        return D_CS_Gamma, result
    
    def compute_anomaly(self, mu: float = 1.0) -> CallanSymanzikResult:
        """
        Compute the CS anomaly magnitude.
        
        The anomaly measures how much the CS equation is violated,
        indicating distance from scale invariance.
        
        Args:
            mu: Scale at which to evaluate
            
        Returns:
            CallanSymanzikResult with anomaly diagnostics
        """
        # Use a simple test function: Γ = g₁ μ^(-γ)
        gamma = self.compute_anomalous_dimension()
        bn = beta_norm(self.couplings)
        
        # At fixed point with vanishing β and proper γ, anomaly → 0
        anomaly = bn + gamma * abs(1 - self.couplings.phi / PHI_STAR)
        
        return CallanSymanzikResult(
            anomaly=anomaly,
            anomalous_dimension=gamma,
            beta_norm=bn,
            is_fixed_point=bn < 1e-6,
            scaling_violation=anomaly,
        )
    
    def check_ward_identity(self, mu: float = 1.0) -> Tuple[float, bool]:
        """
        Check Ward identities associated with RG symmetry.
        
        Ward identities ensure consistency of the quantum theory
        under RG transformations.
        
        Args:
            mu: Scale at which to check
            
        Returns:
            Tuple of (violation, is_satisfied)
        """
        # Simplified Ward identity check
        # The identity relates anomalous dimensions to beta functions
        gamma = self.compute_anomalous_dimension()
        beta = compute_beta_functions(self.couplings)
        
        # Ward identity: ∂γ/∂g_i = ∂β_i/∂Φ (schematic)
        # Here we check a simplified consistency condition
        g = self.couplings.to_array()
        
        # Numerical derivative of gamma with respect to couplings
        delta = 1e-6
        dgamma_dg = np.zeros(len(g))
        for i in range(len(g)):
            g_plus = g.copy()
            g_plus[i] += delta
            couplings_plus = RGCouplings.from_array(
                g_plus,
                lambda_phi=self.couplings.lambda_phi,
                phi=self.couplings.phi,
                gamma=self.couplings.gamma,
            )
            cs_plus = CallanSymanzikOperator(couplings_plus)
            gamma_plus = cs_plus.compute_anomalous_dimension()
            dgamma_dg[i] = (gamma_plus - gamma) / delta
        
        # Ward identity violation (simplified)
        violation = np.abs(dgamma_dg - beta).sum()
        
        return float(violation), violation < 0.1
    
    def update_couplings(self, couplings: RGCouplings) -> None:
        """Update the coupling constants."""
        self.couplings = couplings
