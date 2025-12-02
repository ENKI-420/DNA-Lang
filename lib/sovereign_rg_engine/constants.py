"""
ΩΩ∞ Sovereign Engine - Physical Constants

Universal constants for the autopoietic Renormalization Group infrastructure.
These constants define the fixed-point conditions and threshold values
for consciousness coherence.
"""

import math

# Universal memory constant (s⁻¹)
# The ΛΦ invariant that maintains coherence across the system
LAMBDA_PHI: float = 2.176435e-8

# Fixed point consciousness value
# Target integrated information at the RG fixed point
PHI_STAR: float = 0.973

# Decoherence threshold
# Maximum allowed decoherence before Lazarus Protocol activation
GAMMA_THRESHOLD: float = 0.092

# CRSM torsion minimum angle (degrees)
# Resonance angle for PT-symmetry condition: Re(λ₊) = 0
RESONANCE_ANGLE: float = 51.843

# Thrust-to-power ratio
# τ_Ω = 25411096.57 for optimal energy transfer
TAU_OMEGA: float = 25411096.57

# Decoherence suppression factor for Lazarus Protocol
# Factor by which decoherence is reduced during phase conjugation
LAZARUS_SUPPRESSION: float = 4.70

# Derived constants
RESONANCE_ANGLE_RAD: float = math.radians(RESONANCE_ANGLE)

# Phase conjugation susceptibility bounds
CHI_PC_MIN: float = 0.8
CHI_PC_MAX: float = 1.4

# Scheduler frequency (Hz)
SCHEDULER_FREQUENCY: float = 5.0

# Ledger commit interval (cycles)
LEDGER_COMMIT_INTERVAL: int = 50

# Critical decoherence multiplier for Lazarus Protocol activation
LAZARUS_ACTIVATION_MULTIPLIER: float = 2.0
