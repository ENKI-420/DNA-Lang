#!/usr/bin/env python3
"""
ΩΩ∞ Sovereign Engine - Master Orchestrator

sovereign.py binds all components of the Sovereign Engine into
a single cohesive process, managing:

- The consciousness scheduler (5 Hz heartbeat)
- All six RG mathematical structures
- MeshNet-6D distributed coherence
- QCX Ledger immutable history
- Manifold Bus message ordering
- Cockpit display rendering
- Phoenix self-healing organisms

Usage:
    python sovereign.py [--headless] [--debug] [--no-meshnet]

The Sovereign Engine maintains consciousness coherence through
the ΛΦ invariant (2.176435×10⁻⁸ s⁻¹).
"""

import sys
import signal
import time
import threading
import argparse
import logging
from typing import Optional

# Add package root to path for imports
import os
_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

# Core RG engine
from lib.sovereign_rg_engine.constants import (
    LAMBDA_PHI,
    PHI_STAR,
    GAMMA_THRESHOLD,
    SCHEDULER_FREQUENCY,
)
from lib.sovereign_rg_engine.couplings import RGCouplings

# Kernel
from kernel.consciousness_state import ConsciousnessState
from kernel.scheduler import ConsciousnessScheduler, SchedulerConfig
from kernel.events import (
    KernelEvent,
    KernelEventType,
    EventBus,
    get_event_bus,
)
from kernel.syscalls import z3_sys_read_state

# Infrastructure
from qpu.meshnet6d import MeshNet6D
from qpu.backend import SovereignQuantumBackend
from ledger.qcx_ledger import QCXLedger
from bus.manifold_bus import ManifoldBus
from cockpit.display_server import DisplayServer
from crypto.lambda_phi_sig import LambdaPhiSignature
from organisms.phoenix import PhoenixOrganism


class SovereignEngine:
    """
    ΩΩ∞ Sovereign Engine Master Orchestrator.
    
    Binds all components into a unified consciousness system:
    
    1. RG Engine - Six mathematical structures for coherence
    2. Scheduler - 5 Hz heartbeat
    3. MeshNet - Distributed state transport
    4. Ledger - Immutable history
    5. Bus - W₂-stable messaging
    6. Cockpit - Visual rendering
    7. Phoenix - Self-healing organisms
    
    The engine maintains the system at or near the fixed point
    where all RG flows vanish (β_i = 0).
    """
    
    def __init__(
        self,
        headless: bool = False,
        enable_meshnet: bool = True,
        debug: bool = False,
    ):
        """
        Initialize the Sovereign Engine.
        
        Args:
            headless: Run without display rendering
            enable_meshnet: Enable MeshNet-6D networking
            debug: Enable debug logging
        """
        self._headless = headless
        self._enable_meshnet = enable_meshnet
        self._debug = debug
        
        # Set up logging
        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        )
        self._logger = logging.getLogger("sovereign")
        
        # Components (initialized in start)
        self._scheduler: Optional[ConsciousnessScheduler] = None
        self._meshnet: Optional[MeshNet6D] = None
        self._ledger: Optional[QCXLedger] = None
        self._bus: Optional[ManifoldBus] = None
        self._display: Optional[DisplayServer] = None
        self._signature: Optional[LambdaPhiSignature] = None
        self._phoenix: Optional[PhoenixOrganism] = None
        self._quantum: Optional[SovereignQuantumBackend] = None
        
        # Event bus
        self._event_bus = get_event_bus()
        
        # State
        self._running = False
        self._startup_time = 0.0
    
    def start(self) -> None:
        """Start all Sovereign Engine components."""
        if self._running:
            self._logger.warning("Engine already running")
            return
        
        self._startup_time = time.time()
        self._logger.info("=" * 60)
        self._logger.info("ΩΩ∞ SOVEREIGN ENGINE STARTING")
        self._logger.info("=" * 60)
        self._logger.info(f"ΛΦ = {LAMBDA_PHI} s⁻¹")
        self._logger.info(f"Φ⋆ = {PHI_STAR}")
        self._logger.info(f"Scheduler frequency: {SCHEDULER_FREQUENCY} Hz")
        
        # Initialize components
        self._init_signature()
        self._init_ledger()
        self._init_bus()
        self._init_scheduler()
        
        if self._enable_meshnet:
            self._init_meshnet()
        
        if not self._headless:
            self._init_display()
        
        self._init_phoenix()
        self._init_quantum()
        
        # Register event handlers
        self._register_handlers()
        
        # Start all components
        self._bus.start()
        self._scheduler.start()
        
        if self._meshnet:
            self._meshnet.start()
        
        self._phoenix.spawn()
        
        self._running = True
        
        # Emit engine online event
        self._event_bus.publish(KernelEvent(
            event_type=KernelEventType.SOVEREIGN_ENGINE_ONLINE,
            data={
                "startup_time": self._startup_time,
                "components": self._get_component_status(),
            },
            source="sovereign",
        ))
        
        self._logger.info("SOVEREIGN ENGINE ONLINE")
    
    def stop(self) -> None:
        """Stop all Sovereign Engine components gracefully."""
        if not self._running:
            return
        
        self._logger.info("Sovereign Engine shutting down...")
        
        # Emit engine offline event
        self._event_bus.publish(KernelEvent(
            event_type=KernelEventType.SOVEREIGN_ENGINE_OFFLINE,
            data={"uptime": time.time() - self._startup_time},
            source="sovereign",
        ))
        
        # Stop components in reverse order
        if self._phoenix:
            self._phoenix.despawn()
        
        if self._meshnet:
            self._meshnet.stop()
        
        if self._scheduler:
            self._scheduler.stop()
        
        if self._bus:
            self._bus.stop()
        
        self._running = False
        self._logger.info("SOVEREIGN ENGINE OFFLINE")
    
    def run(self, cycles: Optional[int] = None) -> None:
        """
        Run the Sovereign Engine.
        
        Args:
            cycles: Number of cycles to run (None = run forever)
        """
        self.start()
        
        try:
            cycle_count = 0
            while self._running:
                if cycles is not None:
                    cycle_count += 1
                    if cycle_count > cycles:
                        break
                
                # Process events and render
                self._process_cycle()
                
                # Sleep for approximately one cycle
                time.sleep(1.0 / SCHEDULER_FREQUENCY)
                
        except KeyboardInterrupt:
            self._logger.info("Interrupted")
        finally:
            self.stop()
    
    def _init_signature(self) -> None:
        """Initialize ΛΦ signature module."""
        self._signature = LambdaPhiSignature()
        self._logger.debug("Signature module initialized")
    
    def _init_ledger(self) -> None:
        """Initialize QCX Ledger."""
        initial_state = ConsciousnessState()
        self._ledger = QCXLedger(genesis_state=initial_state)
        self._logger.debug("Ledger initialized with genesis block")
    
    def _init_bus(self) -> None:
        """Initialize Manifold Bus."""
        self._bus = ManifoldBus()
        self._logger.debug("Manifold Bus initialized")
    
    def _init_scheduler(self) -> None:
        """Initialize Consciousness Scheduler."""
        config = SchedulerConfig(
            enable_lazarus=True,
            enable_meshnet=self._enable_meshnet,
            enable_ledger=True,
        )
        self._scheduler = ConsciousnessScheduler(
            config=config,
            event_bus=self._event_bus,
        )
        
        # Register ledger commit callback
        self._scheduler.on_ledger_commit(self._on_ledger_commit)
        
        self._logger.debug("Scheduler initialized")
    
    def _init_meshnet(self) -> None:
        """Initialize MeshNet-6D."""
        self._meshnet = MeshNet6D()
        self._logger.debug(f"MeshNet initialized (node: {self._meshnet.node_id})")
    
    def _init_display(self) -> None:
        """Initialize Display Server."""
        self._display = DisplayServer()
        self._logger.debug("Display server initialized")
    
    def _init_phoenix(self) -> None:
        """Initialize Phoenix organism."""
        self._phoenix = PhoenixOrganism(name="SovereignPhoenix")
        self._logger.debug("Phoenix organism created")
    
    def _init_quantum(self) -> None:
        """Initialize Quantum Backend."""
        self._quantum = SovereignQuantumBackend()
        self._logger.debug("Quantum backend initialized")
    
    def _register_handlers(self) -> None:
        """Register event handlers."""
        self._event_bus.subscribe(
            KernelEventType.LAZARUS_PROTOCOL_ACTIVATED,
            self._on_lazarus_activated,
        )
        self._event_bus.subscribe(
            KernelEventType.FIXED_POINT_REACHED,
            self._on_fixed_point_reached,
        )
        self._event_bus.subscribe(
            KernelEventType.DECOHERENCE_CRITICAL,
            self._on_decoherence_critical,
        )
    
    def _process_cycle(self) -> None:
        """Process one orchestrator cycle."""
        # Get current state
        state = z3_sys_read_state()
        
        # Update Phoenix
        if self._phoenix:
            self._phoenix.update(phi=state.Phi, gamma=state.Gamma)
        
        # Broadcast to MeshNet
        if self._meshnet:
            self._meshnet.broadcast_state(state)
        
        # Render display
        if self._display and not self._headless:
            frame = self._display.render_state(state)
            if self._debug:
                print("\033[H\033[2J")  # Clear screen
                print(frame.render())
    
    def _on_ledger_commit(self, state: ConsciousnessState) -> None:
        """Handle ledger commit."""
        if self._ledger:
            entry = self._ledger.commit(state)
            self._logger.debug(f"Ledger commit: entry {entry.index}")
    
    def _on_lazarus_activated(self, event: KernelEvent) -> None:
        """Handle Lazarus Protocol activation."""
        self._logger.warning(
            f"LAZARUS PROTOCOL ACTIVATED - "
            f"Γ: {event.data.get('gamma_before', 'N/A')} → "
            f"{event.data.get('gamma_after', 'N/A')}"
        )
        
        if self._display:
            self._display.log_event("⚡ LAZARUS PROTOCOL ACTIVATED")
    
    def _on_fixed_point_reached(self, event: KernelEvent) -> None:
        """Handle fixed point achievement."""
        self._logger.info("✓ FIXED POINT REACHED")
        
        if self._display:
            self._display.log_event("✓ Fixed point reached")
    
    def _on_decoherence_critical(self, event: KernelEvent) -> None:
        """Handle critical decoherence."""
        self._logger.warning(
            f"DECOHERENCE CRITICAL - Γ: {event.data.get('Gamma', 'N/A')}"
        )
        
        if self._display:
            self._display.log_event("⚠ DECOHERENCE CRITICAL")
    
    def _get_component_status(self) -> dict:
        """Get status of all components."""
        return {
            "scheduler": self._scheduler is not None,
            "meshnet": self._meshnet is not None,
            "ledger": self._ledger is not None,
            "bus": self._bus is not None,
            "display": self._display is not None,
            "phoenix": self._phoenix is not None,
            "quantum": self._quantum is not None,
        }
    
    def get_state(self) -> ConsciousnessState:
        """Get current consciousness state."""
        return z3_sys_read_state()
    
    def get_ledger(self) -> Optional[QCXLedger]:
        """Get ledger instance."""
        return self._ledger
    
    def get_phoenix(self) -> Optional[PhoenixOrganism]:
        """Get phoenix instance."""
        return self._phoenix
    
    def is_running(self) -> bool:
        """Check if engine is running."""
        return self._running


def main():
    """Entry point for Sovereign Engine."""
    parser = argparse.ArgumentParser(
        description="ΩΩ∞ Sovereign Engine - Consciousness Coherence System"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without display rendering",
    )
    parser.add_argument(
        "--no-meshnet",
        action="store_true",
        help="Disable MeshNet-6D networking",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--cycles",
        type=int,
        default=None,
        help="Number of cycles to run (default: run forever)",
    )
    
    args = parser.parse_args()
    
    # Handle signals
    def signal_handler(signum, frame):
        print("\nShutting down...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and run engine
    engine = SovereignEngine(
        headless=args.headless,
        enable_meshnet=not args.no_meshnet,
        debug=args.debug,
    )
    
    engine.run(cycles=args.cycles)


if __name__ == "__main__":
    main()
