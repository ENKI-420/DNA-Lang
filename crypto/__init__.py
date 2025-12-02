"""
Crypto Package for ΩΩ∞ Sovereign Engine

Provides cryptographic infrastructure:
- ΛΦ-weighted signatures
"""

from .lambda_phi_sig import LambdaPhiSignature, SignatureResult

__all__ = [
    "LambdaPhiSignature",
    "SignatureResult",
]
