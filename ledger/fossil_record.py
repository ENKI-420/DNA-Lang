"""
Fossil Record: IPFS-Anchored State History

Provides distributed, immutable storage of historical state
snapshots anchored to IPFS for long-term preservation.
"""

import hashlib
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

import sys
import os as _os; _PKG_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))); sys.path.insert(0, _PKG_ROOT) if _PKG_ROOT not in sys.path else None

from kernel.consciousness_state import ConsciousnessState


@dataclass
class FossilEntry:
    """
    A fossilized (IPFS-anchored) state snapshot.
    
    Attributes:
        fossil_id: Unique identifier (simulated IPFS CID)
        timestamp: When the fossil was created
        cycle: Source scheduler cycle
        state_hash: Hash of the original state
        metadata: Additional metadata
    """
    fossil_id: str
    timestamp: float
    cycle: int
    state_hash: str
    metadata: Dict[str, Any]


class FossilRecord:
    """
    IPFS-Anchored Historical State Record.
    
    Provides:
    - Long-term state preservation
    - Distributed storage (simulated IPFS)
    - Content-addressed retrieval
    - State archaeology (finding old states)
    """
    
    def __init__(self):
        """Initialize the Fossil Record."""
        self._fossils: Dict[str, FossilEntry] = {}
        self._by_cycle: Dict[int, str] = {}  # cycle -> fossil_id mapping
    
    def fossilize(
        self,
        state: ConsciousnessState,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> FossilEntry:
        """
        Create a fossil record of a state.
        
        Args:
            state: State to fossilize
            metadata: Additional metadata to store
            
        Returns:
            Created FossilEntry
        """
        # Generate content-addressed ID (simulated IPFS CID)
        state_json = state.to_json()
        content_hash = hashlib.sha256(state_json.encode()).hexdigest()
        fossil_id = f"Qm{content_hash[:44]}"  # IPFS-like CID format
        
        fossil = FossilEntry(
            fossil_id=fossil_id,
            timestamp=time.time(),
            cycle=state.cycle,
            state_hash=content_hash,
            metadata=metadata or {},
        )
        
        self._fossils[fossil_id] = fossil
        self._by_cycle[state.cycle] = fossil_id
        
        return fossil
    
    def retrieve(self, fossil_id: str) -> Optional[FossilEntry]:
        """
        Retrieve a fossil by ID.
        
        Args:
            fossil_id: The IPFS-like CID
            
        Returns:
            FossilEntry or None if not found
        """
        return self._fossils.get(fossil_id)
    
    def find_by_cycle(self, cycle: int) -> Optional[FossilEntry]:
        """
        Find fossil for a specific cycle.
        
        Args:
            cycle: Scheduler cycle number
            
        Returns:
            FossilEntry or None if not fossilized
        """
        fossil_id = self._by_cycle.get(cycle)
        if fossil_id:
            return self._fossils.get(fossil_id)
        return None
    
    def list_fossils(
        self,
        start_cycle: Optional[int] = None,
        end_cycle: Optional[int] = None,
        limit: int = 100,
    ) -> List[FossilEntry]:
        """
        List fossils within a cycle range.
        
        Args:
            start_cycle: Minimum cycle (inclusive)
            end_cycle: Maximum cycle (inclusive)
            limit: Maximum number to return
            
        Returns:
            List of FossilEntry objects
        """
        fossils = list(self._fossils.values())
        
        if start_cycle is not None:
            fossils = [f for f in fossils if f.cycle >= start_cycle]
        if end_cycle is not None:
            fossils = [f for f in fossils if f.cycle <= end_cycle]
        
        fossils.sort(key=lambda f: f.cycle, reverse=True)
        return fossils[:limit]
    
    def get_fossil_count(self) -> int:
        """Get total number of fossils."""
        return len(self._fossils)
    
    def verify(self, fossil_id: str, state: ConsciousnessState) -> bool:
        """
        Verify a state matches a fossil record.
        
        Args:
            fossil_id: Fossil to verify against
            state: State to check
            
        Returns:
            True if state matches fossil
        """
        fossil = self._fossils.get(fossil_id)
        if not fossil:
            return False
        
        state_json = state.to_json()
        content_hash = hashlib.sha256(state_json.encode()).hexdigest()
        
        return content_hash == fossil.state_hash
