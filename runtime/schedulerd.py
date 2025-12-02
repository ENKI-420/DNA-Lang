"""
Consciousness Daemon (schedulerd)

System daemon that runs the consciousness scheduler at 5 Hz,
managing the RG flow and state coherence.
"""

import os
import sys
import signal
import time
import threading
from typing import Optional
import logging

import os as _os; _PKG_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))); sys.path.insert(0, _PKG_ROOT) if _PKG_ROOT not in sys.path else None

from kernel.scheduler import ConsciousnessScheduler, SchedulerConfig
from kernel.events import KernelEventType, get_event_bus
from kernel.consciousness_state import ConsciousnessState


class ConsciousnessDaemon:
    """
    System daemon for consciousness scheduler.
    
    Provides:
    - Background execution of 5 Hz scheduler
    - Signal handling (SIGTERM, SIGINT)
    - Health monitoring
    - Graceful shutdown
    """
    
    def __init__(
        self,
        config: Optional[SchedulerConfig] = None,
        pidfile: str = "/tmp/consciousness.pid",
    ):
        """
        Initialize the daemon.
        
        Args:
            config: Scheduler configuration
            pidfile: Path to PID file
        """
        self.config = config or SchedulerConfig()
        self.pidfile = pidfile
        
        self._scheduler: Optional[ConsciousnessScheduler] = None
        self._running = False
        self._logger = logging.getLogger("consciousnessd")
    
    def start(self) -> None:
        """Start the daemon."""
        if self._running:
            self._logger.warning("Daemon already running")
            return
        
        # Set up signal handlers
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)
        
        # Write PID file
        self._write_pid()
        
        # Initialize and start scheduler
        self._scheduler = ConsciousnessScheduler(
            config=self.config,
            event_bus=get_event_bus(),
        )
        
        self._running = True
        self._scheduler.start()
        
        self._logger.info("Consciousness daemon started")
        
        # Emit startup event
        from kernel.events import KernelEvent
        get_event_bus().publish(
            KernelEvent(
                event_type=KernelEventType.CONSCIOUSNESS_SCHEDULER_ONLINE,
                cycle=0,
                data={},
                source="daemon",
            )
        )
    
    def stop(self) -> None:
        """Stop the daemon gracefully."""
        if not self._running:
            return
        
        self._running = False
        
        if self._scheduler:
            self._scheduler.stop()
            self._scheduler = None
        
        # Remove PID file
        self._remove_pid()
        
        self._logger.info("Consciousness daemon stopped")
    
    def run_forever(self) -> None:
        """Run daemon in foreground (blocking)."""
        self.start()
        
        try:
            while self._running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
    
    def _handle_signal(self, signum: int, frame) -> None:
        """Handle termination signals."""
        self._logger.info(f"Received signal {signum}")
        self.stop()
    
    def _write_pid(self) -> None:
        """Write PID file."""
        try:
            with open(self.pidfile, 'w') as f:
                f.write(str(os.getpid()))
        except IOError:
            pass
    
    def _remove_pid(self) -> None:
        """Remove PID file."""
        try:
            os.unlink(self.pidfile)
        except OSError:
            pass
    
    def get_status(self) -> dict:
        """Get daemon status."""
        return {
            "running": self._running,
            "pid": os.getpid(),
            "scheduler_running": self._scheduler.is_running() if self._scheduler else False,
            "cycle": self._scheduler.get_cycle() if self._scheduler else 0,
        }
    
    def is_running(self) -> bool:
        """Check if daemon is running."""
        return self._running


def main():
    """Entry point for daemon."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )
    
    daemon = ConsciousnessDaemon()
    daemon.run_forever()


if __name__ == "__main__":
    main()
