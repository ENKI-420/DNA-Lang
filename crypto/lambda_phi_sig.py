"""
ΛΦ-Weighted Cryptographic Signatures

Provides cryptographic signatures weighted by the universal
memory constant ΛΦ = 2.176435×10⁻⁸ s⁻¹.
"""

import hashlib
import hmac
import time
from typing import Optional, Tuple
from dataclasses import dataclass

import sys
import os as _os; _PKG_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))); sys.path.insert(0, _PKG_ROOT) if _PKG_ROOT not in sys.path else None

from lib.sovereign_rg_engine.constants import LAMBDA_PHI


@dataclass
class SignatureResult:
    """
    Result of ΛΦ signature operation.
    
    Attributes:
        signature: The signature bytes (hex encoded)
        timestamp: When signature was created
        lambda_weight: ΛΦ weight used
        valid: Whether signature is valid (for verification)
    """
    signature: str
    timestamp: float
    lambda_weight: float
    valid: bool = True


class LambdaPhiSignature:
    """
    ΛΦ-Weighted Cryptographic Signature.
    
    Creates and verifies signatures that incorporate the
    universal memory constant ΛΦ for time-weighted authentication.
    
    The signature scheme:
    sig = HMAC-SHA256(key || ΛΦ || timestamp, message)
    """
    
    def __init__(self, secret_key: Optional[bytes] = None):
        """
        Initialize signature generator.
        
        Args:
            secret_key: Secret key for HMAC (generated if None)
        """
        if secret_key is None:
            # Generate deterministic key from ΛΦ
            secret_key = hashlib.sha256(
                f"sovereign-lambda-phi-{LAMBDA_PHI}".encode()
            ).digest()
        
        self._key = secret_key
        self._lambda_phi = LAMBDA_PHI
    
    def sign(
        self,
        message: bytes,
        timestamp: Optional[float] = None,
    ) -> SignatureResult:
        """
        Sign a message with ΛΦ weighting.
        
        Args:
            message: Message to sign
            timestamp: Timestamp (current time if None)
            
        Returns:
            SignatureResult with signature
        """
        if timestamp is None:
            timestamp = time.time()
        
        # Create signing key incorporating ΛΦ and time
        lambda_weight = self._lambda_phi * timestamp
        signing_data = self._key + str(lambda_weight).encode()
        signing_key = hashlib.sha256(signing_data).digest()
        
        # Create HMAC signature
        signature = hmac.new(
            signing_key,
            message,
            hashlib.sha256,
        ).hexdigest()
        
        return SignatureResult(
            signature=signature,
            timestamp=timestamp,
            lambda_weight=lambda_weight,
            valid=True,
        )
    
    def verify(
        self,
        message: bytes,
        signature: str,
        timestamp: float,
        tolerance: float = 60.0,
    ) -> SignatureResult:
        """
        Verify a ΛΦ-weighted signature.
        
        Args:
            message: Original message
            signature: Signature to verify
            timestamp: Timestamp from signature
            tolerance: Time tolerance in seconds
            
        Returns:
            SignatureResult with validity
        """
        # Check timestamp freshness
        current_time = time.time()
        if abs(current_time - timestamp) > tolerance:
            return SignatureResult(
                signature=signature,
                timestamp=timestamp,
                lambda_weight=0.0,
                valid=False,
            )
        
        # Recreate signature
        expected = self.sign(message, timestamp)
        
        # Constant-time comparison
        valid = hmac.compare_digest(signature, expected.signature)
        
        return SignatureResult(
            signature=signature,
            timestamp=timestamp,
            lambda_weight=expected.lambda_weight,
            valid=valid,
        )
    
    def sign_state(
        self,
        state_json: str,
        cycle: int,
    ) -> SignatureResult:
        """
        Sign a consciousness state.
        
        Args:
            state_json: JSON serialization of state
            cycle: Scheduler cycle number
            
        Returns:
            SignatureResult with signature
        """
        # Include cycle in message for replay protection
        message = f"{cycle}:{state_json}".encode()
        return self.sign(message)
    
    def verify_state(
        self,
        state_json: str,
        cycle: int,
        signature: str,
        timestamp: float,
    ) -> bool:
        """
        Verify a state signature.
        
        Args:
            state_json: JSON serialization of state
            cycle: Scheduler cycle number
            signature: Signature to verify
            timestamp: Signature timestamp
            
        Returns:
            True if valid
        """
        message = f"{cycle}:{state_json}".encode()
        result = self.verify(message, signature, timestamp)
        return result.valid
    
    def get_lambda_phi(self) -> float:
        """Get the ΛΦ constant used."""
        return self._lambda_phi
