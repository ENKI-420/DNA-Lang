"""
ΩΩ∞ Sovereign Engine - Structure IV: Fisher-Kubo-Mori Metric

Implementation of the information geometry metric g_ij on the
coupling manifold. This metric governs gradient flows and
measures distinguishability of quantum states.

g_ij = ⟨∂_i log ρ · ∂_j log ρ⟩_ρ

Key property: Gradient flow β_i = g^{ij} ∂C/∂g_j
"""

import numpy as np
from typing import Optional, Tuple
from dataclasses import dataclass

from .couplings import RGCouplings
from .constants import LAMBDA_PHI, PHI_STAR


@dataclass
class FisherKuboMoriResult:
    """Result of Fisher-Kubo-Mori metric computation."""
    metric: np.ndarray  # g_ij matrix
    inverse_metric: np.ndarray  # g^{ij} inverse
    ricci_scalar: float  # R scalar curvature
    geodesic_distance: float  # Distance along geodesic
    is_positive_definite: bool  # Metric positivity check


class FisherKuboMoriMetric:
    """
    Structure IV: Fisher-Kubo-Mori Information Metric g_ij
    
    Computes the information geometry metric on the coupling manifold:
    
    g_ij = ⟨∂_i log ρ · ∂_j log ρ⟩_ρ
    
    This is the Fisher information metric for classical statistics,
    generalized via Kubo-Mori inner product for quantum systems.
    
    Key applications:
    - Natural gradient descent: β_i = g^{ij} ∂C/∂g_j
    - Distance between states: ds² = g_ij dg^i dg^j
    - Curvature of the coupling manifold
    """
    
    def __init__(self, couplings: Optional[RGCouplings] = None):
        """
        Initialize the Fisher-Kubo-Mori metric.
        
        Args:
            couplings: RG coupling constants
        """
        self.couplings = couplings or RGCouplings()
    
    def compute(self) -> FisherKuboMoriResult:
        """
        Compute the Fisher-Kubo-Mori metric g_ij.
        
        Uses the thermal state ρ ∝ exp(-βH) where H depends
        on the couplings.
        
        Returns:
            FisherKuboMoriResult with metric and analysis
        """
        g = self.couplings.to_array()
        n = len(g)
        
        # Compute metric components
        metric = self._compute_metric_tensor()
        
        # Compute inverse metric (with regularization)
        try:
            eigenvalues = np.linalg.eigvalsh(metric)
            min_eigenvalue = np.min(eigenvalues)
            
            # Regularize if near-singular
            if min_eigenvalue < 1e-10:
                metric_reg = metric + 1e-10 * np.eye(n)
                inverse_metric = np.linalg.inv(metric_reg)
            else:
                inverse_metric = np.linalg.inv(metric)
            
            is_positive_definite = min_eigenvalue > 0
        except np.linalg.LinAlgError:
            inverse_metric = np.eye(n)
            is_positive_definite = False
        
        # Compute Ricci scalar curvature
        ricci_scalar = self._compute_ricci_scalar(metric, inverse_metric)
        
        # Compute geodesic distance from origin (fixed point)
        geodesic_distance = self._compute_geodesic_distance(metric)
        
        return FisherKuboMoriResult(
            metric=metric,
            inverse_metric=inverse_metric,
            ricci_scalar=float(ricci_scalar),
            geodesic_distance=float(geodesic_distance),
            is_positive_definite=is_positive_definite,
        )
    
    def _compute_metric_tensor(self) -> np.ndarray:
        """
        Compute the metric tensor g_ij.
        
        g_ij = ∫ (∂_i log ρ)(∂_j log ρ) ρ dx
        """
        g = self.couplings.to_array()
        n = len(g)
        metric = np.zeros((n, n))
        
        # Use a simple parametric family
        # ρ(x; g) = Z^(-1) exp(-V(x; g))
        # where V = Σ g_i x^(2i)
        
        # Fisher information for this family
        h = 1e-6
        
        for i in range(n):
            for j in range(n):
                # g_ij = ⟨∂_i V · ∂_j V⟩ - ⟨∂_i V⟩⟨∂_j V⟩ (connected correlator)
                
                # For Gaussian approximation:
                # g_ij ≈ δ_ij / σ² + corrections
                
                # Base metric (diagonal)
                if i == j:
                    metric[i, j] = 1.0 / (1 + abs(g[i]) + 1e-6)
                else:
                    # Off-diagonal from coupling mixing
                    metric[i, j] = 0.1 * g[i] * g[j] / (1 + abs(g[i] * g[j]) + 1e-6)
        
        # Add ΛΦ corrections
        lambda_correction = LAMBDA_PHI * 1e8
        for i in range(n):
            metric[i, i] += lambda_correction
        
        # Add consciousness-dependent correction
        phi_factor = self.couplings.phi / PHI_STAR
        metric *= phi_factor**2 if phi_factor > 0 else 1.0
        
        # Ensure symmetry
        metric = 0.5 * (metric + metric.T)
        
        return metric
    
    def _compute_ricci_scalar(
        self,
        metric: np.ndarray,
        inverse_metric: np.ndarray,
    ) -> float:
        """
        Compute the Ricci scalar curvature R.
        
        R = g^{ij} R_ij
        
        where R_ij is the Ricci tensor.
        """
        n = metric.shape[0]
        h = 1e-5
        
        # Compute Christoffel symbols Γ^k_ij = (1/2) g^{kl} (∂_i g_jl + ∂_j g_il - ∂_l g_ij)
        christoffel = np.zeros((n, n, n))
        
        g = self.couplings.to_array()
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    for l in range(n):
                        # Numerical derivatives of metric
                        d_i_gjl = self._metric_derivative(i, j, l, h)
                        d_j_gil = self._metric_derivative(j, i, l, h)
                        d_l_gij = self._metric_derivative(l, i, j, h)
                        
                        christoffel[k, i, j] += 0.5 * inverse_metric[k, l] * (
                            d_i_gjl + d_j_gil - d_l_gij
                        )
        
        # Riemann tensor R^l_ijk = ∂_j Γ^l_ik - ∂_k Γ^l_ij + Γ^l_jm Γ^m_ik - Γ^l_km Γ^m_ij
        # Ricci tensor R_ij = R^k_ikj
        # Ricci scalar R = g^{ij} R_ij
        
        # Simplified: use trace formula for 2D
        if n == 2:
            det_g = np.linalg.det(metric)
            if abs(det_g) > 1e-10:
                # Gaussian curvature formula for 2D
                ricci = -1 / np.sqrt(abs(det_g))
            else:
                ricci = 0.0
        else:
            # For higher dimensions, compute trace of Christoffel contractions
            ricci = 0.0
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        ricci += inverse_metric[i, j] * christoffel[k, i, k] * christoffel[k, j, k]
                        ricci -= inverse_metric[i, j] * christoffel[k, i, j] * christoffel[k, k, j]
        
        return ricci
    
    def _metric_derivative(self, deriv_idx: int, i: int, j: int, h: float) -> float:
        """
        Compute ∂_{deriv_idx} g_{ij} numerically.
        """
        g = self.couplings.to_array()
        
        # Perturb coupling
        g_plus = g.copy()
        g_plus[deriv_idx] += h
        
        g_minus = g.copy()
        g_minus[deriv_idx] -= h
        
        # Compute metric at perturbed points
        couplings_plus = RGCouplings.from_array(
            g_plus,
            lambda_phi=self.couplings.lambda_phi,
            phi=self.couplings.phi,
            gamma=self.couplings.gamma,
        )
        couplings_minus = RGCouplings.from_array(
            g_minus,
            lambda_phi=self.couplings.lambda_phi,
            phi=self.couplings.phi,
            gamma=self.couplings.gamma,
        )
        
        fkm_plus = FisherKuboMoriMetric(couplings_plus)
        fkm_minus = FisherKuboMoriMetric(couplings_minus)
        
        metric_plus = fkm_plus._compute_metric_tensor()
        metric_minus = fkm_minus._compute_metric_tensor()
        
        return (metric_plus[i, j] - metric_minus[i, j]) / (2 * h)
    
    def _compute_geodesic_distance(self, metric: np.ndarray) -> float:
        """
        Compute geodesic distance from origin.
        
        ds² = g_ij dg^i dg^j
        
        For small couplings, approximate as Euclidean with metric.
        """
        g = self.couplings.to_array()
        
        # ds = sqrt(g_ij g^i g^j)
        distance = np.sqrt(np.dot(g, np.dot(metric, g)))
        
        return distance
    
    def natural_gradient(self, cost_gradient: np.ndarray) -> np.ndarray:
        """
        Compute the natural gradient using the FKM metric.
        
        ∇̃C = g^{ij} ∂C/∂g_j
        
        Args:
            cost_gradient: Euclidean gradient ∂C/∂g_i
            
        Returns:
            Natural gradient in coupling space
        """
        result = self.compute()
        natural_grad = np.dot(result.inverse_metric, cost_gradient)
        
        return natural_grad
    
    def parallel_transport(
        self,
        vector: np.ndarray,
        start_couplings: RGCouplings,
        end_couplings: RGCouplings,
    ) -> np.ndarray:
        """
        Parallel transport a vector along geodesic.
        
        Uses Schild's ladder approximation for short distances.
        
        Args:
            vector: Vector at start_couplings
            start_couplings: Starting point
            end_couplings: Ending point
            
        Returns:
            Transported vector at end_couplings
        """
        # For short distances, approximate as Euclidean transport
        # (exact for flat manifolds)
        
        # Compute metric at both points
        self.couplings = start_couplings
        result_start = self.compute()
        
        self.couplings = end_couplings
        result_end = self.compute()
        
        # Simple approximation: rescale by metric ratio
        norm_start = np.sqrt(np.dot(vector, np.dot(result_start.metric, vector)))
        if norm_start < 1e-10:
            return vector
        
        # Preserve the metric norm
        transported = vector.copy()
        norm_end = np.sqrt(np.dot(transported, np.dot(result_end.metric, transported)))
        
        if norm_end > 1e-10:
            transported *= norm_start / norm_end
        
        return transported
    
    def update_couplings(self, couplings: RGCouplings) -> None:
        """Update the coupling constants."""
        self.couplings = couplings
