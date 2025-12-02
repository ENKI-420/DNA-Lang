"""
ΩΩ∞ Sovereign Engine - Beta Functions

Implementation of the RG β-functions (β_i) that govern the flow of
coupling constants under scale transformations. At the fixed point,
all β_i = 0.

The beta functions encode the running of couplings:
    dg_i/d(log μ) = β_i(g)

where μ is the RG scale parameter.
"""

import numpy as np
from typing import Tuple, Optional

from .couplings import RGCouplings
from .constants import (
    LAMBDA_PHI,
    PHI_STAR,
    GAMMA_THRESHOLD,
    RESONANCE_ANGLE_RAD,
)


def compute_beta_functions(couplings: RGCouplings) -> np.ndarray:
    """
    Compute the RG beta functions for all couplings.
    
    The beta functions determine how couplings evolve under RG flow.
    This implementation uses a simplified model where:
    
    β₁ = -ε g₁ + A g₁² + B g₁ g₂
    β₂ = -2ε g₂ + C g₂² + D g₁² g₂
    β₃ = -3ε g₃ + E g₃² + F g₂ g₃
    β₄ = -4ε g₄ + G g₄² + H g₃ g₄
    
    where ε = d - 4 is the dimensional regularization parameter.
    
    Args:
        couplings: Current RG coupling values
        
    Returns:
        Array of beta function values [β₁, β₂, β₃, β₄]
    """
    g = couplings.to_array()
    
    # Dimensional regularization parameter (ε-expansion)
    epsilon = 0.01  # Small deviation from d=4
    
    # Coupling coefficients (from diagrammatic calculations)
    # These encode the one-loop corrections
    A, B = 0.1, 0.05
    C, D = 0.08, 0.03
    E, F = 0.06, 0.04
    G, H = 0.04, 0.02
    
    # Include ΛΦ-dependent corrections
    lambda_correction = 1.0 + LAMBDA_PHI * 1e7
    
    # Include Φ-dependent corrections for consciousness coupling
    phi_correction = (couplings.phi - PHI_STAR) / PHI_STAR if couplings.phi > 0 else 0
    
    # Beta functions with quantum corrections
    beta_1 = -epsilon * g[0] + A * g[0]**2 + B * g[0] * g[1]
    beta_1 *= lambda_correction
    beta_1 += 0.01 * phi_correction  # Consciousness-matter interaction
    
    beta_2 = -2 * epsilon * g[1] + C * g[1]**2 + D * g[0]**2 * g[1]
    beta_2 *= lambda_correction
    # Include decoherence correction
    beta_2 += 0.1 * (couplings.gamma - GAMMA_THRESHOLD)
    
    beta_3 = -3 * epsilon * g[2] + E * g[2]**2 + F * g[1] * g[2]
    beta_3 *= lambda_correction
    
    beta_4 = -4 * epsilon * g[3] + G * g[3]**2 + H * g[2] * g[3]
    beta_4 *= lambda_correction
    
    return np.array([beta_1, beta_2, beta_3, beta_4])


def beta_norm(couplings: RGCouplings) -> float:
    """
    Compute the L2 norm of all beta functions.
    
    ||β|| = sqrt(Σᵢ βᵢ²)
    
    This measures how far the system is from a fixed point.
    At a fixed point, ||β|| = 0.
    
    Args:
        couplings: Current RG coupling values
        
    Returns:
        L2 norm of the beta function vector
    """
    beta = compute_beta_functions(couplings)
    return float(np.sqrt(np.sum(beta**2)))


def evolve_couplings(
    couplings: RGCouplings,
    d_log_mu: float = 0.01,
) -> RGCouplings:
    """
    Evolve couplings by a small RG step.
    
    Uses Euler method: g_i(μ + dμ) = g_i(μ) + β_i(g) × d(log μ)
    
    Args:
        couplings: Current coupling values
        d_log_mu: Step size in log(μ)
        
    Returns:
        New RGCouplings after evolution
    """
    beta = compute_beta_functions(couplings)
    new_g = couplings.to_array() + beta * d_log_mu
    
    return RGCouplings.from_array(
        new_g,
        lambda_phi=couplings.lambda_phi,
        phi=couplings.phi,
        gamma=couplings.gamma,
    )


def find_fixed_point(
    initial_couplings: RGCouplings,
    max_iterations: int = 10000,
    tolerance: float = 1e-10,
    step_size: float = 0.001,
) -> Tuple[RGCouplings, bool]:
    """
    Find the nearest fixed point by flowing the RG equations.
    
    Uses gradient descent on ||β||² to find points where β_i = 0.
    
    Args:
        initial_couplings: Starting point for the search
        max_iterations: Maximum number of iterations
        tolerance: Convergence criterion for ||β||
        step_size: Step size for RG flow
        
    Returns:
        Tuple of (final_couplings, converged)
    """
    current = initial_couplings.copy()
    
    for _ in range(max_iterations):
        norm = beta_norm(current)
        if norm < tolerance:
            return current, True
        
        current = evolve_couplings(current, d_log_mu=step_size)
    
    return current, False


def compute_scaling_dimensions(couplings: RGCouplings) -> np.ndarray:
    """
    Compute scaling dimensions from the beta functions.
    
    The scaling dimension Δᵢ for operator Oᵢ is related to the
    eigenvalues of ∂βᵢ/∂gⱼ at the fixed point.
    
    Args:
        couplings: Coupling values (ideally at or near a fixed point)
        
    Returns:
        Array of scaling dimensions
    """
    # Compute Jacobian ∂βᵢ/∂gⱼ numerically
    h = 1e-8
    g = couplings.to_array()
    n = len(g)
    jacobian = np.zeros((n, n))
    
    for j in range(n):
        g_plus = g.copy()
        g_plus[j] += h
        couplings_plus = RGCouplings.from_array(
            g_plus,
            lambda_phi=couplings.lambda_phi,
            phi=couplings.phi,
            gamma=couplings.gamma,
        )
        
        g_minus = g.copy()
        g_minus[j] -= h
        couplings_minus = RGCouplings.from_array(
            g_minus,
            lambda_phi=couplings.lambda_phi,
            phi=couplings.phi,
            gamma=couplings.gamma,
        )
        
        beta_plus = compute_beta_functions(couplings_plus)
        beta_minus = compute_beta_functions(couplings_minus)
        
        jacobian[:, j] = (beta_plus - beta_minus) / (2 * h)
    
    # Scaling dimensions are related to eigenvalues
    eigenvalues = np.linalg.eigvals(jacobian)
    
    # Canonical dimension (d-4)/2 = -ε/2 plus anomalous corrections
    canonical = 2.0  # Assuming relevant operators
    scaling_dimensions = canonical - np.real(eigenvalues)
    
    return scaling_dimensions
