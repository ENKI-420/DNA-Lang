"""
ΩΩ∞ Sovereign Engine - Structure V: Polchinski Equation

Implementation of the exact Renormalization Group equation for
the effective action (Polchinski/Wilson-Polchinski formulation).

∂S_Λ/∂Λ = (1/2) Tr[G_Λ · (∂²S/∂φ² - (∂S/∂φ)·(∂S/∂φ)ᵀ)]

where:
- S_Λ is the Wilsonian effective action at cutoff Λ
- G_Λ = (K + iΓ)⁻¹ is the regularized propagator
- Scale invariance at ΛΦ: ∂S_Λ/∂Λ|_{ΛΦ} = 0
"""

import numpy as np
from typing import Optional, Tuple, Callable
from dataclasses import dataclass

from .couplings import RGCouplings
from .constants import LAMBDA_PHI, PHI_STAR, GAMMA_THRESHOLD


@dataclass
class PolchinskiResult:
    """Result of Polchinski equation analysis."""
    flow_rate: float  # |∂S_Λ/∂Λ|
    propagator_trace: float  # Tr[G_Λ]
    scale: float  # Current cutoff Λ
    is_scale_invariant: bool  # Whether at fixed point
    effective_action_value: float  # S_Λ evaluated


class PolchinskiEquation:
    """
    Structure V: Polchinski Exact RG Equation
    
    Implements the exact RG flow for the effective action:
    
    ∂S_Λ/∂Λ = (1/2) Tr[Ġ_Λ · (∂²S/∂φ² - ∂S/∂φ ⊗ ∂S/∂φ)]
    
    where Ġ_Λ = ∂G_Λ/∂Λ is the scale derivative of the propagator.
    
    Key properties:
    - Exact (non-perturbative) RG flow
    - Scale invariance at ΛΦ: ∂S_Λ/∂Λ|_{ΛΦ} = 0
    - Propagator: G_Λ = (K + iΓ)⁻¹ with decoherence
    """
    
    def __init__(
        self,
        couplings: Optional[RGCouplings] = None,
        grid_size: int = 32,
    ):
        """
        Initialize the Polchinski equation solver.
        
        Args:
            couplings: RG coupling constants
            grid_size: Discretization size for field space
        """
        self.couplings = couplings or RGCouplings()
        self.grid_size = grid_size
        
        # Field discretization
        self.phi_max = 5.0
        self.phi = np.linspace(-self.phi_max, self.phi_max, grid_size)
        self.dphi = self.phi[1] - self.phi[0]
    
    def compute_propagator(self, Lambda: float) -> np.ndarray:
        """
        Compute the regularized propagator G_Λ = (K + iΓ)⁻¹.
        
        The kinetic operator K is modified by:
        - Cutoff regularization at scale Λ
        - Decoherence term iΓ
        
        Args:
            Lambda: Cutoff scale
            
        Returns:
            Propagator matrix G_Λ
        """
        n = self.grid_size
        
        # Kinetic operator (discretized Laplacian)
        K = np.zeros((n, n))
        for i in range(n):
            K[i, i] = 2.0 / self.dphi**2
            if i > 0:
                K[i, i - 1] = -1.0 / self.dphi**2
            if i < n - 1:
                K[i, i + 1] = -1.0 / self.dphi**2
        
        # Add mass term (from RG scale)
        mass_squared = Lambda**2
        K += mass_squared * np.eye(n)
        
        # Add decoherence (imaginary part)
        gamma = self.couplings.gamma
        K_complex = K + 1j * gamma * np.eye(n)
        
        # Cutoff function: smooth suppression of high momenta
        cutoff = np.exp(-np.arange(n)**2 / (Lambda * n)**2)
        K_complex = np.diag(cutoff) @ K_complex @ np.diag(cutoff)
        
        # Regularize and invert
        try:
            G = np.linalg.inv(K_complex)
        except np.linalg.LinAlgError:
            G = np.linalg.pinv(K_complex)
        
        return G
    
    def compute_effective_action(self, phi_field: np.ndarray, Lambda: float) -> float:
        """
        Compute the effective action S_Λ[φ].
        
        S_Λ = ∫ [(1/2)(∂φ)² + V_Λ(φ)] dx
        
        where V_Λ is the effective potential at scale Λ.
        
        Args:
            phi_field: Field configuration
            Lambda: Cutoff scale
            
        Returns:
            Effective action value
        """
        g = self.couplings.to_array()
        
        # Kinetic term: (1/2) (∂φ/∂x)²
        grad_phi = np.gradient(phi_field, self.dphi)
        kinetic = 0.5 * np.sum(grad_phi**2) * self.dphi
        
        # Potential term: V_Λ(φ) = (1/2) m² φ² + (1/4!) λ φ⁴ + ...
        # Coefficients depend on couplings and scale
        m_squared = Lambda**2 * (1 + g[0])
        lambda_4 = g[1] + 0.1
        lambda_6 = g[2] * 0.01
        
        potential = (
            0.5 * m_squared * np.sum(phi_field**2) * self.dphi
            + (lambda_4 / 24) * np.sum(phi_field**4) * self.dphi
            + (lambda_6 / 720) * np.sum(phi_field**6) * self.dphi
        )
        
        # ΛΦ correction term
        lambda_phi_correction = LAMBDA_PHI * Lambda * np.sum(phi_field**2) * self.dphi
        
        return kinetic + potential + lambda_phi_correction
    
    def compute_flow(self, Lambda: float) -> PolchinskiResult:
        """
        Compute the Polchinski flow ∂S_Λ/∂Λ.
        
        Uses the functional derivative formula:
        ∂S_Λ/∂Λ = (1/2) Tr[Ġ_Λ · (δ²S/δφ² - δS/δφ ⊗ δS/δφ)]
        
        Args:
            Lambda: Cutoff scale
            
        Returns:
            PolchinskiResult with flow analysis
        """
        # Propagator and its derivative
        dLambda = 1e-6
        G_Lambda = self.compute_propagator(Lambda)
        G_Lambda_plus = self.compute_propagator(Lambda + dLambda)
        
        G_dot = (G_Lambda_plus - G_Lambda) / dLambda
        
        # Effective action at reference field configuration
        phi_ref = 0.1 * np.sin(np.pi * np.arange(self.grid_size) / self.grid_size)
        S_Lambda = self.compute_effective_action(phi_ref, Lambda)
        
        # Compute second variation δ²S/δφ²
        h = 1e-5
        second_variation = np.zeros((self.grid_size, self.grid_size))
        
        for i in range(self.grid_size):
            phi_plus = phi_ref.copy()
            phi_plus[i] += h
            phi_minus = phi_ref.copy()
            phi_minus[i] -= h
            
            S_plus = self.compute_effective_action(phi_plus, Lambda)
            S_minus = self.compute_effective_action(phi_minus, Lambda)
            S_0 = self.compute_effective_action(phi_ref, Lambda)
            
            second_variation[i, i] = (S_plus + S_minus - 2 * S_0) / h**2
        
        # First variation δS/δφ
        first_variation = np.zeros(self.grid_size)
        for i in range(self.grid_size):
            phi_plus = phi_ref.copy()
            phi_plus[i] += h
            phi_minus = phi_ref.copy()
            phi_minus[i] -= h
            
            S_plus = self.compute_effective_action(phi_plus, Lambda)
            S_minus = self.compute_effective_action(phi_minus, Lambda)
            
            first_variation[i] = (S_plus - S_minus) / (2 * h)
        
        # Outer product term
        outer_product = np.outer(first_variation, first_variation)
        
        # Polchinski equation RHS
        bracket = second_variation - outer_product
        flow_matrix = np.dot(np.real(G_dot), bracket)
        flow_rate = 0.5 * np.abs(np.trace(flow_matrix))
        
        # Propagator trace
        prop_trace = np.abs(np.trace(G_Lambda))
        
        # Check scale invariance
        is_scale_invariant = flow_rate < 1e-6
        
        return PolchinskiResult(
            flow_rate=float(flow_rate),
            propagator_trace=float(prop_trace),
            scale=Lambda,
            is_scale_invariant=is_scale_invariant,
            effective_action_value=float(S_Lambda),
        )
    
    def evolve_to_scale(
        self,
        Lambda_initial: float,
        Lambda_final: float,
        num_steps: int = 100,
    ) -> Tuple[np.ndarray, PolchinskiResult]:
        """
        Evolve the effective action from one scale to another.
        
        Args:
            Lambda_initial: Starting cutoff
            Lambda_final: Ending cutoff
            num_steps: Number of RG steps
            
        Returns:
            Tuple of (couplings_trajectory, final_result)
        """
        dLambda = (Lambda_final - Lambda_initial) / num_steps
        Lambda = Lambda_initial
        
        trajectory = []
        
        for _ in range(num_steps):
            result = self.compute_flow(Lambda)
            trajectory.append({
                "Lambda": Lambda,
                "flow_rate": result.flow_rate,
                "action": result.effective_action_value,
            })
            
            Lambda += dLambda
            
            if result.is_scale_invariant:
                break
        
        final_result = self.compute_flow(Lambda)
        
        return np.array([(t["Lambda"], t["flow_rate"], t["action"]) for t in trajectory]), final_result
    
    def check_scale_invariance_at_lambda_phi(self) -> Tuple[float, bool]:
        """
        Check scale invariance at the ΛΦ scale.
        
        At ΛΦ = 2.176435×10⁻⁸ s⁻¹, the theory should be scale invariant:
        ∂S_Λ/∂Λ|_{ΛΦ} = 0
        
        Returns:
            Tuple of (flow_magnitude, is_invariant)
        """
        result = self.compute_flow(LAMBDA_PHI)
        
        return result.flow_rate, result.is_scale_invariant
    
    def compute_beta_from_flow(self) -> np.ndarray:
        """
        Extract beta functions from the Polchinski flow.
        
        The beta functions can be read off from the flow of
        the coupling constants in the effective potential.
        """
        g = self.couplings.to_array()
        n = len(g)
        
        # Compute flow at reference scale
        Lambda = 1.0
        result = self.compute_flow(Lambda)
        
        # Extract beta from dimensional analysis
        # β_i = Λ ∂g_i/∂Λ
        beta = np.zeros(n)
        
        # Simplified: relate to flow rate
        beta[0] = -result.flow_rate * g[0] / (Lambda + 1e-10)
        beta[1] = -result.flow_rate * g[1] / (Lambda + 1e-10) * 2
        beta[2] = -result.flow_rate * g[2] / (Lambda + 1e-10) * 3
        beta[3] = -result.flow_rate * g[3] / (Lambda + 1e-10) * 4
        
        return beta
    
    def update_couplings(self, couplings: RGCouplings) -> None:
        """Update the coupling constants."""
        self.couplings = couplings
