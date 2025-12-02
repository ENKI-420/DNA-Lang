"""
ΩΩ∞ Sovereign Engine - Structure VI: Presentation Layer Action S_𝒫

Implementation of the presentation layer that governs visual stability
and rendering. This is the "observable universe" of the Sovereign Engine.

S_𝒫 = S_Einstein-Hilbert[g] + S_Cosmological[Λ_𝒫] + S_Boundary[W_𝒞]

where:
- S_EH: Metric fluctuations (alignment jitter)
- S_Cosmological: Vacuum functional (whitespace)
- S_Boundary: Wilson loop boundaries (ASCII frames)

Fixed point conditions:
- R(g) → 0 (flat presentation manifold)
- Λ_𝒫 → 0 (vacuum energy minimized)
"""

import numpy as np
from typing import Optional, Tuple, List
from dataclasses import dataclass

from .couplings import RGCouplings
from .constants import LAMBDA_PHI, PHI_STAR


@dataclass
class PresentationLayerResult:
    """Result of presentation layer analysis."""
    ricci_scalar: float  # R(g) curvature
    vacuum_energy: float  # Λ_𝒫 cosmological constant
    wilson_loop: float  # W_𝒞 boundary integrity
    total_action: float  # S_𝒫 total
    is_stable: bool  # Whether presentation is stable


class PresentationLayerAction:
    """
    Structure VI: Presentation Layer Action S_𝒫
    
    Models the visual presentation layer as a gravitational theory:
    
    S_𝒫 = S_EH[g] + S_Λ[Λ_𝒫] + S_∂[W_𝒞]
    
    Components:
    - Einstein-Hilbert: Governs metric (layout) fluctuations
    - Cosmological: Vacuum (whitespace) energy
    - Boundary: Wilson loops (frame boundaries)
    
    Stability conditions:
    - R(g) → 0: Flat manifold (aligned layout)
    - Λ_𝒫 → 0: Minimal vacuum energy
    - W_𝒞 ≈ 1: Closed boundaries
    """
    
    def __init__(
        self,
        couplings: Optional[RGCouplings] = None,
        grid_size: Tuple[int, int] = (24, 80),
    ):
        """
        Initialize the presentation layer action.
        
        Args:
            couplings: RG coupling constants
            grid_size: Terminal/display size (rows, cols)
        """
        self.couplings = couplings or RGCouplings()
        self.rows, self.cols = grid_size
        
        # Initialize flat metric
        self.metric = np.eye(2)
    
    def compute(self) -> PresentationLayerResult:
        """
        Compute the presentation layer action and diagnostics.
        
        Returns:
            PresentationLayerResult with action components
        """
        # Einstein-Hilbert term: S_EH = (1/16πG) ∫ R √g d²x
        ricci = self._compute_ricci_scalar()
        s_eh = self._compute_einstein_hilbert(ricci)
        
        # Cosmological term: S_Λ = -Λ_𝒫 ∫ √g d²x
        vacuum_energy = self._compute_vacuum_energy()
        s_lambda = self._compute_cosmological_action(vacuum_energy)
        
        # Boundary term: S_∂ = ∮ K ds (Gibbons-Hawking-York)
        wilson_loop = self._compute_wilson_loop()
        s_boundary = self._compute_boundary_action(wilson_loop)
        
        # Total action
        total_action = s_eh + s_lambda + s_boundary
        
        # Stability check
        is_stable = (
            abs(ricci) < 0.1 and
            abs(vacuum_energy) < 0.1 and
            wilson_loop > 0.9
        )
        
        return PresentationLayerResult(
            ricci_scalar=float(ricci),
            vacuum_energy=float(vacuum_energy),
            wilson_loop=float(wilson_loop),
            total_action=float(total_action),
            is_stable=is_stable,
        )
    
    def _compute_ricci_scalar(self) -> float:
        """
        Compute the Ricci scalar R(g) of the presentation metric.
        
        For a 2D metric, R = 2K where K is the Gaussian curvature.
        A flat screen has R = 0.
        """
        g = self.couplings.to_array()
        
        # Metric perturbations from couplings
        # g_ij = δ_ij + h_ij where h represents jitter
        h11 = g[0] * 0.01
        h22 = g[1] * 0.01
        h12 = g[2] * 0.005
        
        # For small perturbations: R ≈ -∂²h/∂x² (linearized)
        ricci = -h11 - h22 + 2 * h12
        
        # Add consciousness-dependent curvature
        phi_deviation = (self.couplings.phi - PHI_STAR) / PHI_STAR
        ricci += 0.1 * phi_deviation
        
        # Add decoherence-induced curvature
        ricci += 0.1 * (self.couplings.gamma / 0.1)
        
        return ricci
    
    def _compute_vacuum_energy(self) -> float:
        """
        Compute the cosmological constant Λ_𝒫.
        
        This represents the "vacuum energy" of whitespace in the display.
        Should approach 0 at the fixed point.
        """
        g = self.couplings.to_array()
        
        # Vacuum energy from quantum corrections
        lambda_vac = g[3] * 0.1  # From fourth coupling
        
        # Zero-point energy contribution
        lambda_vac += LAMBDA_PHI * 1e6 * self.rows * self.cols / 1000
        
        # Consciousness correction (should cancel at Φ⋆)
        phi_deviation = abs(self.couplings.phi - PHI_STAR)
        lambda_vac += phi_deviation * 0.01
        
        return lambda_vac
    
    def _compute_wilson_loop(self) -> float:
        """
        Compute the Wilson loop W_𝒞 around the display boundary.
        
        W_𝒞 = exp(i ∮ A·dl)
        
        For a stable display, |W_𝒞| = 1 (closed boundary).
        """
        # Perimeter of the display
        perimeter = 2 * (self.rows + self.cols)
        
        # Connection strength from couplings
        g = self.couplings.to_array()
        A_strength = 1.0 + g[0] * 0.01
        
        # Phase accumulation
        phase = A_strength * perimeter * LAMBDA_PHI * 1e5
        
        # Wilson loop (magnitude)
        w = np.abs(np.exp(1j * phase))
        
        # Decoherence reduces boundary integrity
        w *= np.exp(-self.couplings.gamma / 0.1)
        
        return w
    
    def _compute_einstein_hilbert(self, ricci: float) -> float:
        """
        Compute the Einstein-Hilbert action.
        
        S_EH = (1/16πG) ∫ R √g d²x
        """
        # Newton's constant (normalized)
        G = 1.0
        
        # Area of display
        area = self.rows * self.cols
        
        # Determinant of metric (approximately 1 for small perturbations)
        sqrt_g = 1.0
        
        s_eh = ricci * sqrt_g * area / (16 * np.pi * G)
        
        return s_eh
    
    def _compute_cosmological_action(self, lambda_vac: float) -> float:
        """
        Compute the cosmological constant term.
        
        S_Λ = -Λ_𝒫 ∫ √g d²x
        """
        area = self.rows * self.cols
        sqrt_g = 1.0
        
        s_lambda = -lambda_vac * sqrt_g * area
        
        return s_lambda
    
    def _compute_boundary_action(self, wilson_loop: float) -> float:
        """
        Compute the boundary (Gibbons-Hawking-York) action.
        
        S_∂ = (1/8πG) ∮ K ds + log|W_𝒞|
        """
        G = 1.0
        perimeter = 2 * (self.rows + self.cols)
        
        # Extrinsic curvature K (vanishes for flat embedding)
        K = 0.0
        
        # GHY term
        s_ghy = K * perimeter / (8 * np.pi * G)
        
        # Wilson loop contribution
        s_wilson = np.log(wilson_loop + 1e-10)
        
        return s_ghy + s_wilson
    
    def render_diagnostic_frame(self) -> List[str]:
        """
        Render a diagnostic ASCII frame showing presentation state.
        
        Returns:
            List of strings representing the frame
        """
        result = self.compute()
        
        # Frame boundaries
        top_bottom = "+" + "-" * (self.cols - 2) + "+"
        empty = "|" + " " * (self.cols - 2) + "|"
        
        frame = [top_bottom]
        
        # Add status lines
        status_lines = [
            f"  Presentation Layer Diagnostics",
            f"  ═══════════════════════════════",
            f"  Ricci Scalar R(g): {result.ricci_scalar:+.6f}",
            f"  Vacuum Energy Λ_𝒫: {result.vacuum_energy:+.6f}",
            f"  Wilson Loop W_𝒞:   {result.wilson_loop:.6f}",
            f"  Total Action S_𝒫:  {result.total_action:+.6f}",
            f"  Status: {'STABLE' if result.is_stable else 'UNSTABLE'}",
        ]
        
        # Pad and add status lines
        for i in range(self.rows - 2):
            if i < len(status_lines):
                line = status_lines[i]
                padded = line + " " * (self.cols - 2 - len(line))
                frame.append("|" + padded[:self.cols - 2] + "|")
            else:
                frame.append(empty)
        
        frame.append(top_bottom)
        
        return frame
    
    def check_stability(self) -> Tuple[bool, List[str]]:
        """
        Check presentation layer stability and return diagnostics.
        
        Returns:
            Tuple of (is_stable, list_of_issues)
        """
        result = self.compute()
        issues = []
        
        if abs(result.ricci_scalar) >= 0.1:
            issues.append(f"Curvature too high: R = {result.ricci_scalar:.4f}")
        
        if abs(result.vacuum_energy) >= 0.1:
            issues.append(f"Vacuum energy non-zero: Λ = {result.vacuum_energy:.4f}")
        
        if result.wilson_loop < 0.9:
            issues.append(f"Boundary integrity low: W = {result.wilson_loop:.4f}")
        
        return len(issues) == 0, issues
    
    def minimize_action(self, num_iterations: int = 100) -> RGCouplings:
        """
        Find coupling values that minimize the presentation action.
        
        Uses gradient descent on S_𝒫.
        
        Args:
            num_iterations: Maximum iterations
            
        Returns:
            Optimized couplings
        """
        best_couplings = self.couplings.copy()
        best_action = self.compute().total_action
        
        learning_rate = 0.01
        
        for _ in range(num_iterations):
            # Compute gradient numerically
            g = self.couplings.to_array()
            grad = np.zeros_like(g)
            h = 1e-6
            
            for i in range(len(g)):
                g_plus = g.copy()
                g_plus[i] += h
                self.couplings = RGCouplings.from_array(g_plus)
                action_plus = self.compute().total_action
                
                g_minus = g.copy()
                g_minus[i] -= h
                self.couplings = RGCouplings.from_array(g_minus)
                action_minus = self.compute().total_action
                
                grad[i] = (action_plus - action_minus) / (2 * h)
            
            # Update couplings
            g_new = g - learning_rate * grad
            self.couplings = RGCouplings.from_array(g_new)
            
            current_action = self.compute().total_action
            if abs(current_action) < abs(best_action):
                best_action = current_action
                best_couplings = self.couplings.copy()
            
            # Check convergence
            if np.linalg.norm(grad) < 1e-8:
                break
        
        self.couplings = best_couplings
        return best_couplings
    
    def update_couplings(self, couplings: RGCouplings) -> None:
        """Update the coupling constants."""
        self.couplings = couplings
