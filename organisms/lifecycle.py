"""
Organism Lifecycle Manager

Manages the lifecycle of software organisms including
spawn, despawn, and mutation operations.
"""

from enum import Enum
from typing import Optional, Dict, Any, Callable, List
from dataclasses import dataclass, field
import time


class LifecycleState(Enum):
    """Organism lifecycle states."""
    DORMANT = "dormant"
    SPAWNING = "spawning"
    ALIVE = "alive"
    MUTATING = "mutating"
    HEALING = "healing"
    DESPAWNING = "despawning"
    DEAD = "dead"


@dataclass
class OrganismMetadata:
    """Metadata for an organism instance."""
    organism_id: str
    name: str
    version: str
    created_at: float
    state: LifecycleState
    generation: int = 0
    parent_id: Optional[str] = None
    properties: Dict[str, Any] = field(default_factory=dict)


class OrganismLifecycle:
    """
    Organism Lifecycle Manager.
    
    Handles:
    - Spawning new organisms
    - Despawning existing organisms
    - Triggering mutations
    - State transitions
    """
    
    def __init__(self):
        """Initialize lifecycle manager."""
        self._organisms: Dict[str, OrganismMetadata] = {}
        self._id_counter = 0
        self._callbacks: Dict[str, List[Callable]] = {
            "spawn": [],
            "despawn": [],
            "mutate": [],
            "state_change": [],
        }
    
    def spawn(
        self,
        name: str,
        version: str = "1.0.0",
        properties: Optional[Dict[str, Any]] = None,
        parent_id: Optional[str] = None,
    ) -> OrganismMetadata:
        """
        Spawn a new organism.
        
        Args:
            name: Organism name
            version: Version string
            properties: Initial properties
            parent_id: Parent organism (for reproduction)
            
        Returns:
            Created OrganismMetadata
        """
        self._id_counter += 1
        organism_id = f"org_{self._id_counter}_{int(time.time())}"
        
        # Determine generation
        generation = 0
        if parent_id and parent_id in self._organisms:
            generation = self._organisms[parent_id].generation + 1
        
        metadata = OrganismMetadata(
            organism_id=organism_id,
            name=name,
            version=version,
            created_at=time.time(),
            state=LifecycleState.SPAWNING,
            generation=generation,
            parent_id=parent_id,
            properties=properties or {},
        )
        
        self._organisms[organism_id] = metadata
        
        # Transition to alive
        self._set_state(organism_id, LifecycleState.ALIVE)
        
        # Invoke callbacks
        self._invoke_callbacks("spawn", metadata)
        
        return metadata
    
    def despawn(self, organism_id: str) -> bool:
        """
        Despawn an organism.
        
        Args:
            organism_id: ID of organism to despawn
            
        Returns:
            True if successfully despawned
        """
        if organism_id not in self._organisms:
            return False
        
        metadata = self._organisms[organism_id]
        
        # Can't despawn already dead organisms
        if metadata.state == LifecycleState.DEAD:
            return False
        
        # Transition through despawning
        self._set_state(organism_id, LifecycleState.DESPAWNING)
        self._set_state(organism_id, LifecycleState.DEAD)
        
        # Invoke callbacks
        self._invoke_callbacks("despawn", metadata)
        
        return True
    
    def mutate(
        self,
        organism_id: str,
        mutations: Dict[str, Any],
    ) -> Optional[OrganismMetadata]:
        """
        Apply mutations to an organism.
        
        Args:
            organism_id: ID of organism to mutate
            mutations: Property mutations to apply
            
        Returns:
            Updated metadata or None if failed
        """
        if organism_id not in self._organisms:
            return None
        
        metadata = self._organisms[organism_id]
        
        # Can only mutate alive organisms
        if metadata.state != LifecycleState.ALIVE:
            return None
        
        # Enter mutating state
        self._set_state(organism_id, LifecycleState.MUTATING)
        
        # Apply mutations
        metadata.properties.update(mutations)
        
        # Increment version (simple semver patch)
        parts = metadata.version.split('.')
        if len(parts) == 3:
            parts[2] = str(int(parts[2]) + 1)
            metadata.version = '.'.join(parts)
        
        # Return to alive state
        self._set_state(organism_id, LifecycleState.ALIVE)
        
        # Invoke callbacks
        self._invoke_callbacks("mutate", metadata)
        
        return metadata
    
    def _set_state(self, organism_id: str, state: LifecycleState) -> None:
        """Set organism state and invoke callbacks."""
        if organism_id in self._organisms:
            old_state = self._organisms[organism_id].state
            self._organisms[organism_id].state = state
            
            self._invoke_callbacks(
                "state_change",
                self._organisms[organism_id],
                old_state=old_state,
                new_state=state,
            )
    
    def _invoke_callbacks(
        self,
        event: str,
        metadata: OrganismMetadata,
        **kwargs,
    ) -> None:
        """Invoke registered callbacks."""
        for callback in self._callbacks.get(event, []):
            try:
                callback(metadata, **kwargs)
            except Exception:
                pass
    
    def on_spawn(self, callback: Callable) -> None:
        """Register spawn callback."""
        self._callbacks["spawn"].append(callback)
    
    def on_despawn(self, callback: Callable) -> None:
        """Register despawn callback."""
        self._callbacks["despawn"].append(callback)
    
    def on_mutate(self, callback: Callable) -> None:
        """Register mutation callback."""
        self._callbacks["mutate"].append(callback)
    
    def on_state_change(self, callback: Callable) -> None:
        """Register state change callback."""
        self._callbacks["state_change"].append(callback)
    
    def get_organism(self, organism_id: str) -> Optional[OrganismMetadata]:
        """Get organism by ID."""
        return self._organisms.get(organism_id)
    
    def list_organisms(
        self,
        state: Optional[LifecycleState] = None,
    ) -> List[OrganismMetadata]:
        """List all organisms, optionally filtered by state."""
        organisms = list(self._organisms.values())
        if state is not None:
            organisms = [o for o in organisms if o.state == state]
        return organisms
    
    def get_alive_count(self) -> int:
        """Get count of alive organisms."""
        return sum(
            1 for o in self._organisms.values()
            if o.state == LifecycleState.ALIVE
        )
