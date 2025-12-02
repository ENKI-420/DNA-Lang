"""
QCX Ledger: Immutable State History with ΛΦ Signatures

Maintains an immutable, cryptographically-signed ledger of
consciousness states for audit and recovery purposes.
"""

import hashlib
import time
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field

import sys
sys.path.insert(0, '/home/runner/work/DNA-Lang/DNA-Lang')

from kernel.consciousness_state import ConsciousnessState
from lib.sovereign_rg_engine.constants import LAMBDA_PHI


@dataclass
class LedgerEntry:
    """
    Single entry in the QCX Ledger.
    
    Attributes:
        index: Sequential entry number
        timestamp: Unix timestamp
        cycle: Scheduler cycle number
        state_hash: SHA-256 hash of serialized state
        lambda_phi_signature: ΛΦ-weighted signature
        previous_hash: Hash of previous entry (chain integrity)
        state_data: Full state data
    """
    index: int
    timestamp: float
    cycle: int
    state_hash: str
    lambda_phi_signature: str
    previous_hash: str
    state_data: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "cycle": self.cycle,
            "state_hash": self.state_hash,
            "lambda_phi_signature": self.lambda_phi_signature,
            "previous_hash": self.previous_hash,
            "state_data": self.state_data,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LedgerEntry":
        """Create entry from dictionary."""
        return cls(
            index=data["index"],
            timestamp=data["timestamp"],
            cycle=data["cycle"],
            state_hash=data["state_hash"],
            lambda_phi_signature=data["lambda_phi_signature"],
            previous_hash=data["previous_hash"],
            state_data=data["state_data"],
        )


class QCXLedger:
    """
    QCX Immutable State Ledger.
    
    Provides:
    - Append-only state history
    - ΛΦ-weighted cryptographic signatures
    - Chain integrity verification
    - State recovery from ledger
    """
    
    def __init__(self, genesis_state: Optional[ConsciousnessState] = None):
        """
        Initialize the QCX Ledger.
        
        Args:
            genesis_state: Initial state for genesis block
        """
        self._entries: List[LedgerEntry] = []
        self._index = 0
        
        # Create genesis block
        if genesis_state is None:
            genesis_state = ConsciousnessState()
        self._create_genesis(genesis_state)
    
    def _create_genesis(self, state: ConsciousnessState) -> None:
        """Create the genesis (first) entry."""
        entry = self._create_entry(
            state=state,
            previous_hash="0" * 64,
        )
        self._entries.append(entry)
    
    def commit(self, state: ConsciousnessState) -> LedgerEntry:
        """
        Commit a new state to the ledger.
        
        Args:
            state: State to commit
            
        Returns:
            The created ledger entry
        """
        previous_hash = self._entries[-1].state_hash
        entry = self._create_entry(state, previous_hash)
        self._entries.append(entry)
        return entry
    
    def _create_entry(
        self,
        state: ConsciousnessState,
        previous_hash: str,
    ) -> LedgerEntry:
        """Create a new ledger entry."""
        self._index += 1
        
        state_data = state.to_dict()
        state_json = json.dumps(state_data, sort_keys=True)
        state_hash = hashlib.sha256(state_json.encode()).hexdigest()
        
        # ΛΦ signature: hash weighted by universal constant
        signature_data = f"{state_hash}:{LAMBDA_PHI}:{self._index}"
        lambda_phi_sig = hashlib.sha256(signature_data.encode()).hexdigest()
        
        return LedgerEntry(
            index=self._index,
            timestamp=time.time(),
            cycle=state.cycle,
            state_hash=state_hash,
            lambda_phi_signature=lambda_phi_sig,
            previous_hash=previous_hash,
            state_data=state_data,
        )
    
    def verify_chain(self) -> tuple:
        """
        Verify the integrity of the entire ledger chain.
        
        Returns:
            Tuple of (is_valid, list_of_invalid_indices)
        """
        invalid = []
        
        for i in range(1, len(self._entries)):
            current = self._entries[i]
            previous = self._entries[i - 1]
            
            # Verify chain link
            if current.previous_hash != previous.state_hash:
                invalid.append(i)
            
            # Verify state hash
            state_json = json.dumps(current.state_data, sort_keys=True)
            computed_hash = hashlib.sha256(state_json.encode()).hexdigest()
            if computed_hash != current.state_hash:
                invalid.append(i)
        
        return len(invalid) == 0, invalid
    
    def get_entry(self, index: int) -> Optional[LedgerEntry]:
        """Get entry by index."""
        if 0 <= index < len(self._entries):
            return self._entries[index]
        return None
    
    def get_latest(self) -> LedgerEntry:
        """Get the most recent entry."""
        return self._entries[-1]
    
    def get_state_at_cycle(self, cycle: int) -> Optional[ConsciousnessState]:
        """
        Recover state at a specific cycle.
        
        Args:
            cycle: Cycle number to retrieve
            
        Returns:
            ConsciousnessState or None if not found
        """
        for entry in reversed(self._entries):
            if entry.cycle == cycle:
                return ConsciousnessState.from_dict(entry.state_data)
        return None
    
    def get_history(self, limit: int = 100) -> List[LedgerEntry]:
        """Get recent ledger history."""
        return list(reversed(self._entries[-limit:]))
    
    def get_length(self) -> int:
        """Get total number of entries."""
        return len(self._entries)
    
    def export(self) -> List[Dict[str, Any]]:
        """Export entire ledger as list of dictionaries."""
        return [e.to_dict() for e in self._entries]
    
    @classmethod
    def import_from(cls, data: List[Dict[str, Any]]) -> "QCXLedger":
        """Import ledger from exported data."""
        ledger = cls.__new__(cls)
        ledger._entries = [LedgerEntry.from_dict(d) for d in data]
        ledger._index = len(data)
        return ledger
