"""
ΩΩ∞ Sovereign Engine - Structure III: Wasserstein-Lindblad Superoperator

Implementation of the Wasserstein-Lindblad superoperator L̂^Γ_{W₂}
that governs the combined transport and decoherence dynamics.

L̂^Γ_{W₂}[ρ] = ∇·(ρ ∇_{W₂} Φ) - ∇·(Γ ∇ρ)

where:
- First term: Optimal transport drift (Wasserstein gradient flow)
- Second term: Decoherence diffusion (Lindblad dissipation)
- Fixed point: L̂^Γ_{W₂}[ρ_Ω*] = 0
"""

import numpy as np
from typing import Optional, Tuple, Callable
from dataclasses import dataclass

from .couplings import RGCouplings
from .constants import GAMMA_THRESHOLD, PHI_STAR, LAMBDA_PHI


@dataclass
class WassersteinLindbladResult:
    """Result of Wasserstein-Lindblad analysis."""
    flow_magnitude: float  # ||L̂[ρ]||
    transport_component: float  # Wasserstein drift contribution
    decoherence_component: float  # Lindblad diffusion contribution
    w2_distance: float  # W₂ distance from equilibrium
    is_at_equilibrium: bool  # Whether ρ is at fixed point


class WassersteinLindbladSuperoperator:
    """
    Structure III: Wasserstein-Lindblad Superoperator L̂^Γ_{W₂}
    
    Combines optimal transport (Wasserstein) with open quantum system
    dynamics (Lindblad) into a unified evolution equation:
    
    L̂^Γ_{W₂}[ρ] = ∇·(ρ ∇_{W₂} Φ) - ∇·(Γ ∇ρ)
    
    Components:
    - Transport drift: Moves probability mass optimally
    - Decoherence diffusion: Spreads phase information
    
    Fixed point condition: L̂^Γ_{W₂}[ρ_Ω*] = 0
    """
    
    def __init__(
        self,
        couplings: Optional[RGCouplings] = None,
        grid_size: int = 32,
    ):
        """
        Initialize the Wasserstein-Lindblad superoperator.
        
        Args:
            couplings: RG coupling constants
            grid_size: Discretization size for numerical computations
        """
        self.couplings = couplings or RGCouplings()
        self.grid_size = grid_size
        
        # Discretization
        self.x = np.linspace(-5, 5, grid_size)
        self.dx = self.x[1] - self.x[0]
    
    def apply(self, rho: np.ndarray) -> WassersteinLindbladResult:
        """
        Apply the Wasserstein-Lindblad superoperator to density ρ.
        
        L̂^Γ_{W₂}[ρ] = ∇·(ρ ∇_{W₂} Φ) - ∇·(Γ ∇ρ)
        
        Args:
            rho: Probability density (1D array on grid)
            
        Returns:
            WassersteinLindbladResult with flow analysis
        """
        # Ensure normalization
        rho = np.maximum(rho, 1e-10)  # Avoid log(0)
        rho = rho / np.sum(rho * self.dx)
        
        # Compute transport potential Φ(x)
        phi_potential = self._compute_transport_potential(rho)
        
        # Compute Wasserstein gradient ∇_{W₂} Φ
        grad_phi = np.gradient(phi_potential, self.dx)
        
        # Transport flux: j_transport = ρ ∇_{W₂} Φ
        j_transport = rho * grad_phi
        
        # Transport term: ∇·(ρ ∇_{W₂} Φ)
        transport_term = np.gradient(j_transport, self.dx)
        
        # Decoherence coefficient Γ
        gamma = self.couplings.gamma
        
        # Density gradient ∇ρ
        grad_rho = np.gradient(rho, self.dx)
        
        # Diffusion flux: j_diffusion = Γ ∇ρ
        j_diffusion = gamma * grad_rho
        
        # Diffusion term: -∇·(Γ ∇ρ)
        diffusion_term = -np.gradient(j_diffusion, self.dx)
        
        # Total flow L̂[ρ]
        L_rho = transport_term + diffusion_term
        
        # Compute metrics
        flow_magnitude = np.sqrt(np.sum(L_rho**2) * self.dx)
        transport_component = np.sqrt(np.sum(transport_term**2) * self.dx)
        decoherence_component = np.sqrt(np.sum(diffusion_term**2) * self.dx)
        
        # W₂ distance from equilibrium
        rho_eq = self._equilibrium_distribution()
        w2_distance = self._wasserstein_2_distance(rho, rho_eq)
        
        return WassersteinLindbladResult(
            flow_magnitude=float(flow_magnitude),
            transport_component=float(transport_component),
            decoherence_component=float(decoherence_component),
            w2_distance=float(w2_distance),
            is_at_equilibrium=flow_magnitude < 1e-6,
        )
    
    def _compute_transport_potential(self, rho: np.ndarray) -> np.ndarray:
        """
        Compute the transport potential Φ(x).
        
        The potential drives optimal transport toward the target
        distribution. We use a form that promotes coherence.
        """
        # Target is the equilibrium distribution
        rho_target = self._equilibrium_distribution()
        
        # Simple potential: difference in cumulative distributions
        cdf_rho = np.cumsum(rho * self.dx)
        cdf_target = np.cumsum(rho_target * self.dx)
        
        # Transport potential from Monge-Ampère
        phi = np.zeros_like(self.x)
        for i in range(len(self.x)):
            # Find optimal transport map
            phi[i] = 0.5 * (cdf_target[i] - cdf_rho[i])
        
        # Add consciousness-driven potential
        phi += LAMBDA_PHI * 1e6 * (1 - self.couplings.phi / PHI_STAR) * self.x**2
        
        return phi
    
    def _equilibrium_distribution(self) -> np.ndarray:
        """
        Compute the equilibrium (fixed point) distribution ρ_Ω*.
        
        At equilibrium, L̂^Γ_{W₂}[ρ_Ω*] = 0.
        """
        # Gaussian equilibrium centered at origin
        sigma = 1.0 / (1 + self.couplings.gamma / GAMMA_THRESHOLD)
        rho_eq = np.exp(-self.x**2 / (2 * sigma**2))
        rho_eq = rho_eq / np.sum(rho_eq * self.dx)
        
        return rho_eq
    
    def _wasserstein_2_distance(
        self,
        rho1: np.ndarray,
        rho2: np.ndarray,
    ) -> float:
        """
        Compute the Wasserstein-2 distance between two distributions.
        
        W₂(ρ₁, ρ₂) = (∫ |x - T(x)|² dρ₁(x))^(1/2)
        
        For 1D distributions, this simplifies to the L² distance
        between quantile functions.
        """
        # Compute CDFs
        cdf1 = np.cumsum(rho1 * self.dx)
        cdf1 = cdf1 / cdf1[-1]  # Normalize
        
        cdf2 = np.cumsum(rho2 * self.dx)
        cdf2 = cdf2 / cdf2[-1]  # Normalize
        
        # Compute quantile functions (inverse CDFs)
        p = np.linspace(0.01, 0.99, 100)
        
        q1 = np.interp(p, cdf1, self.x)
        q2 = np.interp(p, cdf2, self.x)
        
        # W₂ distance
        w2 = np.sqrt(np.mean((q1 - q2)**2))
        
        return w2
    
    def evolve(
        self,
        rho_initial: np.ndarray,
        dt: float = 0.01,
        num_steps: int = 100,
    ) -> Tuple[np.ndarray, WassersteinLindbladResult]:
        """
        Evolve density under Wasserstein-Lindblad dynamics.
        
        ∂ρ/∂t = -L̂^Γ_{W₂}[ρ]
        
        Args:
            rho_initial: Initial density
            dt: Time step
            num_steps: Number of evolution steps
            
        Returns:
            Tuple of (final_rho, final_result)
        """
        rho = rho_initial.copy()
        
        for _ in range(num_steps):
            # Compute flow
            result = self.apply(rho)
            
            # Numerical gradient of L_rho for evolution
            # Simplified: use explicit Euler
            grad_rho = np.gradient(rho, self.dx)
            laplacian_rho = np.gradient(grad_rho, self.dx)
            
            # Evolution: ∂ρ/∂t = Γ ∇²ρ (diffusion approximation)
            rho = rho + dt * self.couplings.gamma * laplacian_rho
            
            # Renormalize
            rho = np.maximum(rho, 1e-10)
            rho = rho / np.sum(rho * self.dx)
            
            # Check convergence
            if result.is_at_equilibrium:
                break
        
        final_result = self.apply(rho)
        return rho, final_result
    
    def compute_entropy_production(self, rho: np.ndarray) -> float:
        """
        Compute the entropy production rate.
        
        σ = ∫ ρ |∇(log ρ)|² dx
        
        This measures irreversibility in the evolution.
        """
        rho = np.maximum(rho, 1e-10)
        log_rho = np.log(rho)
        grad_log_rho = np.gradient(log_rho, self.dx)
        
        sigma = np.sum(rho * grad_log_rho**2 * self.dx)
        
        return float(sigma)
    
    def get_w2_distance(self) -> float:
        """
        Get current W₂ distance from equilibrium.
        
        Uses the current state implied by couplings.
        """
        # Create a Gaussian centered at current Φ deviation
        deviation = (self.couplings.phi - PHI_STAR) / PHI_STAR
        rho_current = np.exp(-(self.x - deviation)**2 / 2)
        rho_current = rho_current / np.sum(rho_current * self.dx)
        
        rho_eq = self._equilibrium_distribution()
        
        return self._wasserstein_2_distance(rho_current, rho_eq)
    
    def update_couplings(self, couplings: RGCouplings) -> None:
        """Update the coupling constants."""
        self.couplings = couplings
