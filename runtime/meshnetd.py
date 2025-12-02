"""
MeshNet Daemon (meshnetd)

System daemon for MeshNet-6D distributed coherence network.
"""

import os
import sys
import signal
import time
import threading
from typing import Optional
import logging

import os as _os; _PKG_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))); sys.path.insert(0, _PKG_ROOT) if _PKG_ROOT not in sys.path else None

from qpu.meshnet6d import MeshNet6D
from kernel.events import get_event_bus


class MeshNetDaemon:
    """
    System daemon for MeshNet-6D network.
    
    Provides:
    - P2P state broadcasting
    - Node discovery
    - Consensus coordination
    """
    
    def __init__(
        self,
        node_id: Optional[str] = None,
        pidfile: str = "/tmp/meshnet.pid",
    ):
        """
        Initialize the daemon.
        
        Args:
            node_id: This node's identifier
            pidfile: Path to PID file
        """
        self.node_id = node_id
        self.pidfile = pidfile
        
        self._meshnet: Optional[MeshNet6D] = None
        self._running = False
        self._logger = logging.getLogger("meshnetd")
    
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
        
        # Initialize and start meshnet
        self._meshnet = MeshNet6D(node_id=self.node_id)
        self._running = True
        self._meshnet.start()
        
        self._logger.info(f"MeshNet daemon started (node: {self._meshnet.node_id})")
    
    def stop(self) -> None:
        """Stop the daemon gracefully."""
        if not self._running:
            return
        
        self._running = False
        
        if self._meshnet:
            self._meshnet.stop()
            self._meshnet = None
        
        # Remove PID file
        self._remove_pid()
        
        self._logger.info("MeshNet daemon stopped")
    
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
            "node_id": self._meshnet.node_id if self._meshnet else None,
            "node_count": self._meshnet.get_node_count() if self._meshnet else 0,
        }
    
    def get_meshnet(self) -> Optional[MeshNet6D]:
        """Get meshnet instance."""
        return self._meshnet


def main():
    """Entry point for daemon."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )
    
    daemon = MeshNetDaemon()
    daemon.run_forever()


if __name__ == "__main__":
    main()
