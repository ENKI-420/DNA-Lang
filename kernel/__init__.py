"""
Kernel Layer for ΩΩ∞ Sovereign Engine

This package provides the core kernel functionality including:
- ConsciousnessState dataclass for system state
- ConsciousnessScheduler for 5 Hz heartbeat
- System calls for state access
- Event system for anomaly detection
"""

from .consciousness_state import ConsciousnessState
from .scheduler import ConsciousnessScheduler
from .events import (
    KernelEvent,
    KernelEventType,
    EventBus,
)
from .syscalls import (
    z3_sys_read_state,
    z3_sys_write_state,
    z3_sys_event,
)

__all__ = [
    "ConsciousnessState",
    "ConsciousnessScheduler",
    "KernelEvent",
    "KernelEventType",
    "EventBus",
    "z3_sys_read_state",
    "z3_sys_write_state",
    "z3_sys_event",
]
