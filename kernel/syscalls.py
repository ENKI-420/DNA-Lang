"""
System Calls for ΩΩ∞ Sovereign Engine

Provides kernel-level system calls for reading and writing
consciousness state, and emitting events.

System call interface:
- z3_sys_read_state(): Read current consciousness state
- z3_sys_write_state(state): Write/update consciousness state
- z3_sys_event(type, data): Emit kernel event
"""

from typing import Optional, Dict, Any
import threading
import time

from .consciousness_state import ConsciousnessState
from .events import (
    KernelEvent,
    KernelEventType,
    get_event_bus,
    emit_event,
)


# Global state storage with thread safety
_state_lock = threading.Lock()
_current_state: Optional[ConsciousnessState] = None
_state_history: list = []
_max_history = 10000


def z3_sys_read_state() -> ConsciousnessState:
    """
    System call to read the current consciousness state.
    
    Returns:
        Current ConsciousnessState (copy)
        
    Raises:
        RuntimeError: If state has not been initialized
    """
    global _current_state
    
    with _state_lock:
        if _current_state is None:
            # Initialize with default state
            _current_state = ConsciousnessState()
        return _current_state.copy()


def z3_sys_write_state(state: ConsciousnessState) -> bool:
    """
    System call to write/update the consciousness state.
    
    This is typically called by the scheduler after computing
    the new state from all RG structures.
    
    Args:
        state: New consciousness state to set
        
    Returns:
        True if write was successful
        
    Side effects:
        - Updates global state
        - Adds to state history
        - May trigger STATE_UPDATE event
    """
    global _current_state, _state_history
    
    with _state_lock:
        # Store in history
        if _current_state is not None:
            _state_history.append(_current_state.copy())
            if len(_state_history) > _max_history:
                _state_history.pop(0)
        
        # Update current state
        _current_state = state.copy()
        _current_state.timestamp = time.time()
    
    # Emit state update event
    emit_event(
        KernelEventType.STATE_UPDATE,
        cycle=state.cycle,
        data={"Phi": state.Phi, "Gamma": state.Gamma, "beta_norm": state.beta_norm},
        source="syscall",
    )
    
    return True


def z3_sys_event(
    event_type: KernelEventType,
    cycle: int = 0,
    data: Optional[Dict[str, Any]] = None,
    source: str = "syscall",
) -> KernelEvent:
    """
    System call to emit a kernel event.
    
    Args:
        event_type: Type of event to emit
        cycle: Current scheduler cycle
        data: Event-specific data
        source: Source component
        
    Returns:
        The emitted KernelEvent
    """
    return emit_event(event_type, cycle, data, source)


def z3_sys_get_history(limit: int = 100) -> list:
    """
    System call to retrieve state history.
    
    Args:
        limit: Maximum number of states to return
        
    Returns:
        List of ConsciousnessState objects (most recent last)
    """
    global _state_history
    
    with _state_lock:
        return [s.copy() for s in _state_history[-limit:]]


def z3_sys_clear_history() -> int:
    """
    System call to clear state history.
    
    Returns:
        Number of states cleared
    """
    global _state_history
    
    with _state_lock:
        count = len(_state_history)
        _state_history.clear()
        return count


def z3_sys_reset_state() -> None:
    """
    System call to reset state to defaults.
    
    Used during initialization or recovery.
    """
    global _current_state, _state_history
    
    with _state_lock:
        _current_state = ConsciousnessState()
        _state_history.clear()
    
    emit_event(
        KernelEventType.STATE_UPDATE,
        cycle=0,
        data={"action": "reset"},
        source="syscall",
    )


def z3_sys_lock_state() -> threading.Lock:
    """
    System call to get the state lock for atomic operations.
    
    Use with caution - holding the lock blocks state updates.
    
    Returns:
        The state lock (context manager)
    """
    return _state_lock


def z3_sys_compare_and_swap(
    expected_cycle: int,
    new_state: ConsciousnessState,
) -> bool:
    """
    Atomic compare-and-swap for state updates.
    
    Only updates state if current cycle matches expected.
    
    Args:
        expected_cycle: Expected current cycle number
        new_state: State to set if cycle matches
        
    Returns:
        True if swap occurred, False if cycle mismatch
    """
    global _current_state, _state_history
    
    with _state_lock:
        if _current_state is None or _current_state.cycle == expected_cycle:
            if _current_state is not None:
                _state_history.append(_current_state.copy())
                if len(_state_history) > _max_history:
                    _state_history.pop(0)
            
            _current_state = new_state.copy()
            _current_state.timestamp = time.time()
            return True
        return False
