"""
ManifoldBus: W₂-Stable Message Ordering Bus

Provides a message bus with Wasserstein-2 stable ordering
to ensure coherent communication between engine components.
"""

import time
import threading
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
from queue import PriorityQueue
import heapq


@dataclass(order=True)
class BusMessage:
    """
    Message on the Manifold Bus.
    
    Ordering is based on W₂ weight to maintain stable ordering.
    
    Attributes:
        priority: W₂-derived priority (lower = higher priority)
        timestamp: When message was created
        topic: Message topic/channel
        payload: Message data
        source: Source component
        message_id: Unique identifier
    """
    priority: float
    timestamp: float = field(compare=False)
    topic: str = field(compare=False)
    payload: Dict[str, Any] = field(compare=False)
    source: str = field(compare=False)
    message_id: str = field(compare=False, default="")
    
    def __post_init__(self):
        if not self.message_id:
            self.message_id = f"{self.topic}_{self.timestamp}_{id(self)}"


# Type alias for message handlers
MessageHandler = Callable[[BusMessage], None]


class ManifoldBus:
    """
    W₂-Stable Message Bus for the Sovereign Engine.
    
    Features:
    - Priority queue based on Wasserstein-2 metric
    - Topic-based pub/sub
    - Async message processing
    - Message history for replay
    """
    
    def __init__(self, max_history: int = 1000):
        """
        Initialize the Manifold Bus.
        
        Args:
            max_history: Maximum messages to keep in history
        """
        self._queue: List[BusMessage] = []  # Heap-based priority queue
        self._handlers: Dict[str, List[MessageHandler]] = {}
        self._global_handlers: List[MessageHandler] = []
        self._history: List[BusMessage] = []
        self._max_history = max_history
        
        self._lock = threading.Lock()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._message_counter = 0
    
    def start(self) -> None:
        """Start the bus processor."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._process_loop, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop the bus processor."""
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=1.0)
            self._thread = None
    
    def _process_loop(self) -> None:
        """Main message processing loop."""
        while self._running:
            self._process_pending()
            time.sleep(0.01)  # 100 Hz processing
    
    def _process_pending(self) -> None:
        """Process all pending messages in W₂ order."""
        while True:
            message = self._pop_message()
            if message is None:
                break
            self._dispatch(message)
    
    def _pop_message(self) -> Optional[BusMessage]:
        """Pop highest priority message from queue."""
        with self._lock:
            if not self._queue:
                return None
            return heapq.heappop(self._queue)
    
    def _dispatch(self, message: BusMessage) -> None:
        """Dispatch message to handlers."""
        # Add to history
        with self._lock:
            self._history.append(message)
            if len(self._history) > self._max_history:
                self._history.pop(0)
            
            # Get handlers
            topic_handlers = self._handlers.get(message.topic, [])
            all_handlers = topic_handlers + self._global_handlers
        
        # Invoke handlers
        for handler in all_handlers:
            try:
                handler(message)
            except Exception as e:
                print(f"Bus handler error: {e}")
    
    def publish(
        self,
        topic: str,
        payload: Dict[str, Any],
        source: str = "anonymous",
        w2_weight: Optional[float] = None,
    ) -> BusMessage:
        """
        Publish a message to the bus.
        
        Args:
            topic: Message topic
            payload: Message data
            source: Source component
            w2_weight: W₂ priority weight (auto-computed if None)
            
        Returns:
            The published message
        """
        self._message_counter += 1
        
        # Compute W₂ weight if not provided
        if w2_weight is None:
            # Base priority on state coherence data in payload
            phi = payload.get("Phi", 0.5)
            gamma = payload.get("Gamma", 0.5)
            w2_weight = gamma / (phi + 0.001)  # Higher Γ/Φ = lower priority
        
        message = BusMessage(
            priority=w2_weight,
            timestamp=time.time(),
            topic=topic,
            payload=payload,
            source=source,
            message_id=f"msg_{self._message_counter}",
        )
        
        with self._lock:
            heapq.heappush(self._queue, message)
        
        return message
    
    def subscribe(self, topic: str, handler: MessageHandler) -> None:
        """
        Subscribe to a topic.
        
        Args:
            topic: Topic to subscribe to
            handler: Callback for messages
        """
        with self._lock:
            if topic not in self._handlers:
                self._handlers[topic] = []
            self._handlers[topic].append(handler)
    
    def subscribe_all(self, handler: MessageHandler) -> None:
        """Subscribe to all topics."""
        with self._lock:
            self._global_handlers.append(handler)
    
    def unsubscribe(self, topic: str, handler: MessageHandler) -> bool:
        """Unsubscribe from a topic."""
        with self._lock:
            if topic in self._handlers:
                try:
                    self._handlers[topic].remove(handler)
                    return True
                except ValueError:
                    pass
        return False
    
    def get_history(
        self,
        topic: Optional[str] = None,
        limit: int = 100,
    ) -> List[BusMessage]:
        """Get message history."""
        with self._lock:
            if topic is None:
                messages = self._history[-limit:]
            else:
                messages = [m for m in self._history if m.topic == topic][-limit:]
        return list(reversed(messages))
    
    def get_queue_length(self) -> int:
        """Get current queue length."""
        with self._lock:
            return len(self._queue)
    
    def clear_queue(self) -> int:
        """Clear pending messages."""
        with self._lock:
            count = len(self._queue)
            self._queue.clear()
            return count
