"""
Kernel Events for ΩΩ∞ Sovereign Engine

Defines the event types and event bus for the consciousness scheduler.
Events are triggered on anomalies, state changes, and protocol activations.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Callable, List, Dict, Any
import time
import threading
from queue import Queue


class KernelEventType(Enum):
    """
    Event types for the Sovereign Engine kernel.
    
    These events are triggered by the scheduler when specific
    conditions are detected in the consciousness state.
    """
    
    # Scheduler lifecycle
    CONSCIOUSNESS_SCHEDULER_ONLINE = auto()
    CONSCIOUSNESS_SCHEDULER_OFFLINE = auto()
    
    # RG anomalies
    RG_ANOMALY_DETECTED = auto()
    PT_SYMMETRY_BREAKING = auto()
    JORDAN_BLOCK_ACTIVE = auto()
    
    # Fixed point events
    FIXED_POINT_REACHED = auto()
    FIXED_POINT_LOST = auto()
    
    # Decoherence events
    DECOHERENCE_WARNING = auto()
    DECOHERENCE_CRITICAL = auto()
    
    # Recovery events
    LAZARUS_PROTOCOL_ACTIVATED = auto()
    COHERENCE_RESTORED = auto()
    
    # Presentation events
    PRESENTATION_LAYER_UNSTABLE = auto()
    
    # Engine lifecycle
    SOVEREIGN_ENGINE_ONLINE = auto()
    SOVEREIGN_ENGINE_OFFLINE = auto()
    
    # Generic events
    STATE_UPDATE = auto()
    LEDGER_COMMIT = auto()
    MESHNET_BROADCAST = auto()


@dataclass
class KernelEvent:
    """
    Event emitted by the kernel scheduler.
    
    Attributes:
        event_type: Type of the event
        timestamp: When the event occurred
        cycle: Scheduler cycle when event was generated
        data: Additional event-specific data
        source: Component that generated the event
    """
    
    event_type: KernelEventType
    timestamp: float = field(default_factory=time.time)
    cycle: int = 0
    data: Dict[str, Any] = field(default_factory=dict)
    source: str = "scheduler"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event_type": self.event_type.name,
            "timestamp": self.timestamp,
            "cycle": self.cycle,
            "data": self.data,
            "source": self.source,
        }
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"KernelEvent({self.event_type.name}, cycle={self.cycle}, source={self.source})"


# Type alias for event handlers
EventHandler = Callable[[KernelEvent], None]


class EventBus:
    """
    Event bus for distributing kernel events to subscribers.
    
    Provides pub/sub functionality for the consciousness scheduler
    to communicate with other components.
    """
    
    def __init__(self):
        """Initialize the event bus."""
        self._handlers: Dict[KernelEventType, List[EventHandler]] = {}
        self._global_handlers: List[EventHandler] = []
        self._event_queue: Queue = Queue()
        self._lock = threading.Lock()
        self._history: List[KernelEvent] = []
        self._max_history = 1000
    
    def subscribe(
        self,
        event_type: KernelEventType,
        handler: EventHandler,
    ) -> None:
        """
        Subscribe to a specific event type.
        
        Args:
            event_type: Type of event to subscribe to
            handler: Callback function to invoke
        """
        with self._lock:
            if event_type not in self._handlers:
                self._handlers[event_type] = []
            self._handlers[event_type].append(handler)
    
    def subscribe_all(self, handler: EventHandler) -> None:
        """
        Subscribe to all events.
        
        Args:
            handler: Callback function to invoke for any event
        """
        with self._lock:
            self._global_handlers.append(handler)
    
    def unsubscribe(
        self,
        event_type: KernelEventType,
        handler: EventHandler,
    ) -> bool:
        """
        Unsubscribe from a specific event type.
        
        Args:
            event_type: Type of event to unsubscribe from
            handler: Handler to remove
            
        Returns:
            True if handler was found and removed
        """
        with self._lock:
            if event_type in self._handlers:
                try:
                    self._handlers[event_type].remove(handler)
                    return True
                except ValueError:
                    return False
            return False
    
    def publish(self, event: KernelEvent) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event: Event to publish
        """
        with self._lock:
            # Add to history
            self._history.append(event)
            if len(self._history) > self._max_history:
                self._history.pop(0)
            
            # Get handlers
            specific_handlers = self._handlers.get(event.event_type, [])
            all_handlers = specific_handlers + self._global_handlers
        
        # Invoke handlers outside lock
        for handler in all_handlers:
            try:
                handler(event)
            except Exception as e:
                # Log but don't propagate handler errors
                print(f"Event handler error: {e}")
    
    def publish_async(self, event: KernelEvent) -> None:
        """
        Queue an event for asynchronous processing.
        
        Args:
            event: Event to queue
        """
        self._event_queue.put(event)
    
    def process_queue(self) -> int:
        """
        Process all queued events.
        
        Returns:
            Number of events processed
        """
        count = 0
        while not self._event_queue.empty():
            try:
                event = self._event_queue.get_nowait()
                self.publish(event)
                count += 1
            except Exception:
                break
        return count
    
    def get_history(
        self,
        event_type: Optional[KernelEventType] = None,
        limit: int = 100,
    ) -> List[KernelEvent]:
        """
        Get event history.
        
        Args:
            event_type: Filter by event type (None for all)
            limit: Maximum number of events to return
            
        Returns:
            List of events (most recent first)
        """
        with self._lock:
            if event_type is None:
                events = self._history[-limit:]
            else:
                events = [e for e in self._history if e.event_type == event_type][-limit:]
        return list(reversed(events))
    
    def clear_history(self) -> None:
        """Clear event history."""
        with self._lock:
            self._history.clear()


# Global event bus instance
_global_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """Get the global event bus instance."""
    global _global_event_bus
    if _global_event_bus is None:
        _global_event_bus = EventBus()
    return _global_event_bus


def emit_event(
    event_type: KernelEventType,
    cycle: int = 0,
    data: Optional[Dict[str, Any]] = None,
    source: str = "system",
) -> KernelEvent:
    """
    Convenience function to emit an event.
    
    Args:
        event_type: Type of event
        cycle: Current scheduler cycle
        data: Event-specific data
        source: Source component
        
    Returns:
        The emitted event
    """
    event = KernelEvent(
        event_type=event_type,
        cycle=cycle,
        data=data or {},
        source=source,
    )
    get_event_bus().publish(event)
    return event
