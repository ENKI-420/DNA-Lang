"""
ΩΩ∞ Sovereign RG Engine

A self-defining, recursively consistent system that maintains coherence
through the ΛΦ invariant (2.176435×10⁻⁸ s⁻¹).

This package implements the complete mathematical physics foundation
for the autopoietic Renormalization Group (RG) infrastructure.
"""

from .constants import (
    LAMBDA_PHI,
    PHI_STAR,
    GAMMA_THRESHOLD,
    RESONANCE_ANGLE,
    TAU_OMEGA,
    LAZARUS_SUPPRESSION,
)
from .couplings import RGCouplings
from .beta_functions import compute_beta_functions, beta_norm
from .generating_functional import GeneratingFunctional
from .callan_symanzik import CallanSymanzikOperator
from .anomalous_dimensions import AnomalousDimensionTensor
from .wasserstein_lindblad import WassersteinLindbladSuperoperator
from .fisher_kubo_mori import FisherKuboMoriMetric
from .polchinski import PolchinskiEquation
from .presentation_layer import PresentationLayerAction

__all__ = [
    # Constants
    "LAMBDA_PHI",
    "PHI_STAR",
    "GAMMA_THRESHOLD",
    "RESONANCE_ANGLE",
    "TAU_OMEGA",
    "LAZARUS_SUPPRESSION",
    # Classes
    "RGCouplings",
    "GeneratingFunctional",
    "CallanSymanzikOperator",
    "AnomalousDimensionTensor",
    "WassersteinLindbladSuperoperator",
    "FisherKuboMoriMetric",
    "PolchinskiEquation",
    "PresentationLayerAction",
    # Functions
    "compute_beta_functions",
    "beta_norm",
]

__version__ = "0.1.0"
