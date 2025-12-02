"""
ΩΩ∞ Sovereign Engine - Structure II: Anomalous Dimension Tensor γ_ij

Implementation of the non-Hermitian anomalous dimension tensor that
governs coupling mixing under RG flow. Includes PT-symmetry analysis
and Jordan block detection.

γ_ij = ∂²log Z / ∂g_i ∂g_j |_{g*}

Key properties:
- Non-Hermitian: allows for exceptional points
- PT-symmetry condition: Re(λ₊) = 0 at θ = 51.843°
- Jordan blocks at exceptional points
"""

import numpy as np
from typing import Optional, Tuple, List
from dataclasses import dataclass

from .couplings import RGCouplings
from .beta_functions import compute_beta_functions
from .constants import RESONANCE_ANGLE, RESONANCE_ANGLE_RAD, PHI_STAR


@dataclass
class AnomalousDimensionResult:
    """Result of anomalous dimension tensor analysis."""
    tensor: np.ndarray  # γ_ij matrix
    eigenvalues: np.ndarray  # Complex eigenvalues
    eigenvectors: np.ndarray  # Eigenvector matrix
    pt_symmetric: bool  # Whether PT-symmetry holds
    jordan_block_present: bool  # Whether Jordan blocks exist
    exceptional_point_distance: float  # Distance to nearest exceptional point


class AnomalousDimensionTensor:
    """
    Structure II: Anomalous Dimension Tensor γ_ij
    
    Computes the non-Hermitian tensor:
    
    γ_ij = ∂²log Z / ∂g_i ∂g_j |_{g*}
    
    This tensor governs how operators mix under RG transformations.
    Its eigenvalues determine the scaling dimensions.
    
    Key features:
    - Non-Hermitian structure allows exceptional points
    - PT-symmetry at θ = 51.843° (CRSM torsion minimum)
    - Jordan block formation at exceptional points
    """
    
    def __init__(
        self,
        couplings: Optional[RGCouplings] = None,
        theta: float = RESONANCE_ANGLE,
    ):
        """
        Initialize the anomalous dimension tensor.
        
        Args:
            couplings: RG coupling constants
            theta: Angle parameter for PT-symmetry (degrees)
        """
        self.couplings = couplings or RGCouplings()
        self.theta = theta
        self._theta_rad = np.radians(theta)
    
    def compute(self) -> AnomalousDimensionResult:
        """
        Compute the anomalous dimension tensor γ_ij.
        
        Uses numerical differentiation of the beta functions
        to construct the tensor.
        
        Returns:
            AnomalousDimensionResult with tensor and analysis
        """
        tensor = self._compute_tensor()
        
        # Eigenvalue analysis
        eigenvalues, eigenvectors = np.linalg.eig(tensor)
        
        # Check PT-symmetry
        pt_symmetric = self._check_pt_symmetry(eigenvalues)
        
        # Check for Jordan blocks
        jordan_block_present = self._detect_jordan_blocks(tensor, eigenvalues)
        
        # Distance to exceptional point
        ep_distance = self._exceptional_point_distance(eigenvalues)
        
        return AnomalousDimensionResult(
            tensor=tensor,
            eigenvalues=eigenvalues,
            eigenvectors=eigenvectors,
            pt_symmetric=pt_symmetric,
            jordan_block_present=jordan_block_present,
            exceptional_point_distance=ep_distance,
        )
    
    def _compute_tensor(self) -> np.ndarray:
        """
        Compute γ_ij = ∂β_i/∂g_j numerically.
        
        At the fixed point, this equals ∂²log Z / ∂g_i ∂g_j.
        """
        g = self.couplings.to_array()
        n = len(g)
        h = 1e-7
        
        gamma = np.zeros((n, n), dtype=complex)
        
        for j in range(n):
            g_plus = g.copy()
            g_plus[j] += h
            couplings_plus = RGCouplings.from_array(
                g_plus,
                lambda_phi=self.couplings.lambda_phi,
                phi=self.couplings.phi,
                gamma=self.couplings.gamma,
            )
            
            g_minus = g.copy()
            g_minus[j] -= h
            couplings_minus = RGCouplings.from_array(
                g_minus,
                lambda_phi=self.couplings.lambda_phi,
                phi=self.couplings.phi,
                gamma=self.couplings.gamma,
            )
            
            beta_plus = compute_beta_functions(couplings_plus)
            beta_minus = compute_beta_functions(couplings_minus)
            
            # Real part from standard derivative
            gamma[:, j] = (beta_plus - beta_minus) / (2 * h)
        
        # Add non-Hermitian part controlled by theta
        # This implements the PT-symmetric deformation
        non_hermitian_strength = np.sin(self._theta_rad) * 0.1
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    gamma[i, j] += 1j * non_hermitian_strength * (i - j) / n
        
        return gamma
    
    def _check_pt_symmetry(self, eigenvalues: np.ndarray) -> bool:
        """
        Check if PT-symmetry condition is satisfied.
        
        At θ = 51.843°, we should have Re(λ₊) = 0 for the
        appropriate eigenvalue pairs.
        
        PT-symmetry is unbroken when eigenvalues are real or
        come in complex conjugate pairs.
        """
        # Sort eigenvalues by real part
        sorted_eigs = np.sort(eigenvalues)
        
        # Check for complex conjugate pairing
        tolerance = 1e-6
        
        # Count unpaired complex eigenvalues
        unpaired = 0
        used = set()
        
        for i, eig in enumerate(eigenvalues):
            if i in used:
                continue
            
            # Find conjugate pair
            found_pair = False
            for j, eig2 in enumerate(eigenvalues):
                if j <= i or j in used:
                    continue
                
                if abs(eig - np.conj(eig2)) < tolerance:
                    used.add(i)
                    used.add(j)
                    found_pair = True
                    break
            
            if not found_pair:
                # Check if eigenvalue is real
                if abs(np.imag(eig)) > tolerance:
                    unpaired += 1
        
        # PT-symmetry holds if all complex eigenvalues are paired
        return unpaired == 0
    
    def _detect_jordan_blocks(
        self,
        tensor: np.ndarray,
        eigenvalues: np.ndarray,
    ) -> bool:
        """
        Detect the presence of Jordan blocks (exceptional points).
        
        Jordan blocks occur when the tensor is non-diagonalizable,
        i.e., when eigenvectors coalesce.
        """
        n = len(eigenvalues)
        
        # Check for degenerate eigenvalues
        tolerance = 1e-6
        
        for i in range(n):
            for j in range(i + 1, n):
                if abs(eigenvalues[i] - eigenvalues[j]) < tolerance:
                    # Degenerate eigenvalues found
                    # Check if eigenvectors are linearly independent
                    eigenvalues_check, eigenvectors = np.linalg.eig(tensor)
                    
                    # Compute the geometric multiplicity
                    # If it's less than algebraic multiplicity, Jordan block exists
                    
                    # Simplified check: look at the matrix (A - λI)
                    lambda_i = eigenvalues[i]
                    A_minus_lambda = tensor - lambda_i * np.eye(n)
                    
                    # Rank deficiency indicates eigenspace dimension
                    rank = np.linalg.matrix_rank(A_minus_lambda, tol=tolerance)
                    geometric_mult = n - rank
                    
                    # Count algebraic multiplicity
                    algebraic_mult = sum(
                        1 for k in range(n)
                        if abs(eigenvalues[k] - lambda_i) < tolerance
                    )
                    
                    if geometric_mult < algebraic_mult:
                        return True
        
        return False
    
    def _exceptional_point_distance(self, eigenvalues: np.ndarray) -> float:
        """
        Compute distance to the nearest exceptional point.
        
        Exceptional points occur when eigenvalues coalesce.
        The distance is measured by the minimum eigenvalue separation.
        """
        n = len(eigenvalues)
        min_distance = float("inf")
        
        for i in range(n):
            for j in range(i + 1, n):
                distance = abs(eigenvalues[i] - eigenvalues[j])
                min_distance = min(min_distance, distance)
        
        return float(min_distance)
    
    def compute_at_theta(self, theta: float) -> AnomalousDimensionResult:
        """
        Compute the tensor at a specific angle.
        
        Args:
            theta: Angle parameter (degrees)
            
        Returns:
            AnomalousDimensionResult at the specified angle
        """
        old_theta = self.theta
        self.theta = theta
        self._theta_rad = np.radians(theta)
        
        result = self.compute()
        
        self.theta = old_theta
        self._theta_rad = np.radians(old_theta)
        
        return result
    
    def find_pt_symmetric_angle(
        self,
        theta_range: Tuple[float, float] = (0.0, 90.0),
        num_points: int = 100,
    ) -> Tuple[float, bool]:
        """
        Find the angle where PT-symmetry is restored.
        
        Scans through angles to find where Re(λ₊) = 0.
        
        Args:
            theta_range: Range of angles to search (degrees)
            num_points: Number of points in the scan
            
        Returns:
            Tuple of (optimal_theta, found)
        """
        thetas = np.linspace(theta_range[0], theta_range[1], num_points)
        
        for theta in thetas:
            result = self.compute_at_theta(theta)
            if result.pt_symmetric:
                return float(theta), True
        
        return RESONANCE_ANGLE, False
    
    def update_couplings(self, couplings: RGCouplings) -> None:
        """Update the coupling constants."""
        self.couplings = couplings
