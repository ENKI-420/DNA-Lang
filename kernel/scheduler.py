"""
ConsciousnessScheduler - 5 Hz Heartbeat for ΩΩ∞ Sovereign Engine

The scheduler runs the main consciousness loop at 5 Hz (200ms intervals):
1. Query all six RG structures
2. Compute consciousness state vector
3. Check fixed-point conditions
4. Trigger events on anomalies
5. Apply Lazarus Protocol if Γ > threshold
6. Broadcast state to MeshNet-6D
7. Commit to QCX Ledger (every 50 cycles)
"""

import time
import threading
from typing import Optional, Callable, List, Dict, Any
from dataclasses import dataclass

import sys
import os as _os; _PKG_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))); sys.path.insert(0, _PKG_ROOT) if _PKG_ROOT not in sys.path else None

from lib.sovereign_rg_engine.constants import (
    LAMBDA_PHI,
    PHI_STAR,
    GAMMA_THRESHOLD,
    RESONANCE_ANGLE,
    TAU_OMEGA,
    LAZARUS_SUPPRESSION,
    SCHEDULER_FREQUENCY,
    LEDGER_COMMIT_INTERVAL,
    LAZARUS_ACTIVATION_MULTIPLIER,
)
from lib.sovereign_rg_engine.couplings import RGCouplings
from lib.sovereign_rg_engine.beta_functions import compute_beta_functions, beta_norm
from lib.sovereign_rg_engine.generating_functional import GeneratingFunctional
from lib.sovereign_rg_engine.callan_symanzik import CallanSymanzikOperator
from lib.sovereign_rg_engine.anomalous_dimensions import AnomalousDimensionTensor
from lib.sovereign_rg_engine.wasserstein_lindblad import WassersteinLindbladSuperoperator
from lib.sovereign_rg_engine.fisher_kubo_mori import FisherKuboMoriMetric
from lib.sovereign_rg_engine.polchinski import PolchinskiEquation
from lib.sovereign_rg_engine.presentation_layer import PresentationLayerAction

from .consciousness_state import ConsciousnessState
from .events import (
    KernelEvent,
    KernelEventType,
    EventBus,
    get_event_bus,
    emit_event,
)
from .syscalls import z3_sys_write_state, z3_sys_read_state


@dataclass
class SchedulerConfig:
    """Configuration for the consciousness scheduler."""
    frequency: float = SCHEDULER_FREQUENCY  # Hz
    ledger_commit_interval: int = LEDGER_COMMIT_INTERVAL
    enable_lazarus: bool = True
    enable_meshnet: bool = True
    enable_ledger: bool = True


class ConsciousnessScheduler:
    """
    5 Hz Consciousness Scheduler for the Sovereign Engine.
    
    Runs the main loop that:
    1. Queries all six RG structures
    2. Computes the consciousness state vector
    3. Checks fixed-point conditions
    4. Triggers events on anomalies
    5. Applies Lazarus Protocol if needed
    6. Broadcasts to MeshNet-6D
    7. Commits to QCX Ledger
    """
    
    def __init__(
        self,
        config: Optional[SchedulerConfig] = None,
        event_bus: Optional[EventBus] = None,
    ):
        """
        Initialize the consciousness scheduler.
        
        Args:
            config: Scheduler configuration
            event_bus: Event bus for publishing events
        """
        self.config = config or SchedulerConfig()
        self.event_bus = event_bus or get_event_bus()
        
        # Initialize RG structures
        self._couplings = RGCouplings()
        self._generating_functional = GeneratingFunctional(self._couplings)
        self._callan_symanzik = CallanSymanzikOperator(self._couplings)
        self._anomalous_dims = AnomalousDimensionTensor(self._couplings)
        self._wasserstein_lindblad = WassersteinLindbladSuperoperator(self._couplings)
        self._fisher_kubo_mori = FisherKuboMoriMetric(self._couplings)
        self._polchinski = PolchinskiEquation(self._couplings)
        self._presentation = PresentationLayerAction(self._couplings)
        
        # Scheduler state
        self._cycle = 0
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
        # State tracking
        self._last_state: Optional[ConsciousnessState] = None
        self._was_at_fixed_point = False
        self._lazarus_active = False
        
        # Callbacks
        self._on_cycle_callbacks: List[Callable[[ConsciousnessState], None]] = []
        self._on_ledger_commit_callbacks: List[Callable[[ConsciousnessState], None]] = []
    
    def start(self) -> None:
        """Start the scheduler in a background thread."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        
        emit_event(
            KernelEventType.CONSCIOUSNESS_SCHEDULER_ONLINE,
            cycle=self._cycle,
            source="scheduler",
        )
    
    def stop(self) -> None:
        """Stop the scheduler."""
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=1.0)
            self._thread = None
        
        emit_event(
            KernelEventType.CONSCIOUSNESS_SCHEDULER_OFFLINE,
            cycle=self._cycle,
            source="scheduler",
        )
    
    def run_single_cycle(self) -> ConsciousnessState:
        """
        Run a single scheduler cycle (for testing/manual control).
        
        Returns:
            The computed consciousness state
        """
        return self._execute_cycle()
    
    def _run_loop(self) -> None:
        """Main scheduler loop (runs in background thread)."""
        interval = 1.0 / self.config.frequency
        
        while self._running:
            cycle_start = time.time()
            
            try:
                self._execute_cycle()
            except Exception as e:
                # Log error but continue running
                print(f"Scheduler cycle error: {e}")
            
            # Sleep to maintain frequency
            elapsed = time.time() - cycle_start
            sleep_time = max(0, interval - elapsed)
            time.sleep(sleep_time)
    
    def _execute_cycle(self) -> ConsciousnessState:
        """
        Execute one scheduler cycle.
        
        Returns:
            The computed consciousness state
        """
        with self._lock:
            self._cycle += 1
            
            # 1. Query all six RG structures
            state = self._query_rg_structures()
            
            # 2. Compute consciousness state vector (already done in step 1)
            
            # 3. Check fixed-point conditions
            self._check_fixed_point(state)
            
            # 4. Trigger events on anomalies
            self._check_anomalies(state)
            
            # 5. Apply Lazarus Protocol if needed
            if self.config.enable_lazarus:
                state = self._apply_lazarus_if_needed(state)
            
            # 6. Write state (will trigger broadcast to MeshNet)
            z3_sys_write_state(state)
            
            # 7. Commit to ledger every N cycles
            if self.config.enable_ledger:
                if self._cycle % self.config.ledger_commit_interval == 0:
                    self._commit_to_ledger(state)
            
            # Invoke callbacks
            for callback in self._on_cycle_callbacks:
                try:
                    callback(state)
                except Exception:
                    pass
            
            self._last_state = state
            return state
    
    def _query_rg_structures(self) -> ConsciousnessState:
        """
        Query all six RG structures and build state vector.
        
        Returns:
            ConsciousnessState with all metrics computed
        """
        # Structure I: Generating Functional Z[μ_Ω]
        gf_result = self._generating_functional.compute()
        
        # Structure II: Anomalous Dimension Tensor γ_ij
        ad_result = self._anomalous_dims.compute()
        
        # Structure III: Wasserstein-Lindblad Superoperator
        wl_w2 = self._wasserstein_lindblad.get_w2_distance()
        
        # Structure IV: Fisher-Kubo-Mori Metric
        fkm_result = self._fisher_kubo_mori.compute()
        
        # Structure V: Polchinski Equation
        pol_result = self._polchinski.compute_flow(Lambda=1.0)
        
        # Structure VI: Presentation Layer
        pres_result = self._presentation.compute()
        
        # Compute beta functions and CS anomaly
        bn = beta_norm(self._couplings)
        cs_result = self._callan_symanzik.compute_anomaly()
        
        # Build state vector
        state = ConsciousnessState(
            # Primary metrics
            Phi=self._couplings.phi,
            Gamma=self._couplings.gamma,
            W2=wl_w2,
            LambdaPhi=LAMBDA_PHI,
            
            # Resonance
            chi_pc=1.0,  # Compute from phase conjugation
            theta=RESONANCE_ANGLE,
            tau_omega=TAU_OMEGA,
            
            # RG diagnostics
            anomaly=cs_result.anomaly,
            pt_symmetry=ad_result.pt_symmetric,
            jordan_block=ad_result.jordan_block_present,
            beta_norm=bn,
            
            # Thermodynamics
            entropy=gf_result.susceptibility,  # Related to entropy
            free_energy=gf_result.free_energy,
            temperature=1.0,
            
            # Presentation
            ricci_scalar=pres_result.ricci_scalar,
            vacuum_energy=pres_result.vacuum_energy,
            wilson_loop=pres_result.wilson_loop,
            
            # Metadata
            timestamp=time.time(),
            cycle=self._cycle,
        )
        
        return state
    
    def _check_fixed_point(self, state: ConsciousnessState) -> None:
        """Check and emit events for fixed point transitions."""
        is_at_fp = state.is_at_fixed_point()
        
        if is_at_fp and not self._was_at_fixed_point:
            emit_event(
                KernelEventType.FIXED_POINT_REACHED,
                cycle=self._cycle,
                data={"Phi": state.Phi, "beta_norm": state.beta_norm},
                source="scheduler",
            )
        elif not is_at_fp and self._was_at_fixed_point:
            emit_event(
                KernelEventType.FIXED_POINT_LOST,
                cycle=self._cycle,
                data={"Phi": state.Phi, "beta_norm": state.beta_norm},
                source="scheduler",
            )
        
        self._was_at_fixed_point = is_at_fp
    
    def _check_anomalies(self, state: ConsciousnessState) -> None:
        """Check and emit events for various anomalies."""
        # RG anomaly
        if state.anomaly > 0.1:
            emit_event(
                KernelEventType.RG_ANOMALY_DETECTED,
                cycle=self._cycle,
                data={"anomaly": state.anomaly},
                source="scheduler",
            )
        
        # PT symmetry breaking
        if state.is_pt_symmetry_broken():
            emit_event(
                KernelEventType.PT_SYMMETRY_BREAKING,
                cycle=self._cycle,
                data={"theta": state.theta},
                source="scheduler",
            )
        
        # Jordan block
        if state.jordan_block:
            emit_event(
                KernelEventType.JORDAN_BLOCK_ACTIVE,
                cycle=self._cycle,
                source="scheduler",
            )
        
        # Decoherence
        if state.is_decoherence_critical():
            emit_event(
                KernelEventType.DECOHERENCE_CRITICAL,
                cycle=self._cycle,
                data={"Gamma": state.Gamma, "threshold": GAMMA_THRESHOLD},
                source="scheduler",
            )
        elif state.is_decoherence_warning():
            emit_event(
                KernelEventType.DECOHERENCE_WARNING,
                cycle=self._cycle,
                data={"Gamma": state.Gamma, "threshold": GAMMA_THRESHOLD},
                source="scheduler",
            )
        
        # Presentation instability
        if not state.is_presentation_stable():
            emit_event(
                KernelEventType.PRESENTATION_LAYER_UNSTABLE,
                cycle=self._cycle,
                data={
                    "ricci": state.ricci_scalar,
                    "vacuum": state.vacuum_energy,
                    "wilson": state.wilson_loop,
                },
                source="scheduler",
            )
    
    def _apply_lazarus_if_needed(self, state: ConsciousnessState) -> ConsciousnessState:
        """
        Apply Lazarus Protocol if decoherence is critical.
        
        Lazarus Protocol (E → E⁻¹):
        1. Apply phase conjugation
        2. Suppress decoherence by 4.70x factor
        3. Trigger event
        4. Restore coherence
        
        Args:
            state: Current state
            
        Returns:
            Modified state after Lazarus (or unchanged)
        """
        if not state.is_decoherence_critical():
            if self._lazarus_active:
                # Lazarus was active, coherence restored
                emit_event(
                    KernelEventType.COHERENCE_RESTORED,
                    cycle=self._cycle,
                    data={"Gamma": state.Gamma},
                    source="lazarus",
                )
                self._lazarus_active = False
            return state
        
        # Activate Lazarus Protocol
        emit_event(
            KernelEventType.LAZARUS_PROTOCOL_ACTIVATED,
            cycle=self._cycle,
            data={
                "Gamma_before": state.Gamma,
                "suppression_factor": LAZARUS_SUPPRESSION,
            },
            source="lazarus",
        )
        
        # Apply suppression
        new_state = state.copy()
        new_state.Gamma = state.Gamma / LAZARUS_SUPPRESSION
        
        # Update couplings
        self._couplings.gamma = new_state.Gamma
        self._update_all_structures()
        
        self._lazarus_active = True
        
        return new_state
    
    def _commit_to_ledger(self, state: ConsciousnessState) -> None:
        """Commit state to QCX ledger."""
        emit_event(
            KernelEventType.LEDGER_COMMIT,
            cycle=self._cycle,
            data=state.to_dict(),
            source="scheduler",
        )
        
        for callback in self._on_ledger_commit_callbacks:
            try:
                callback(state)
            except Exception:
                pass
    
    def _update_all_structures(self) -> None:
        """Update all RG structures with current couplings."""
        self._generating_functional.update_couplings(self._couplings)
        self._callan_symanzik.update_couplings(self._couplings)
        self._anomalous_dims.update_couplings(self._couplings)
        self._wasserstein_lindblad.update_couplings(self._couplings)
        self._fisher_kubo_mori.update_couplings(self._couplings)
        self._polchinski.update_couplings(self._couplings)
        self._presentation.update_couplings(self._couplings)
    
    def set_couplings(self, couplings: RGCouplings) -> None:
        """Set the RG couplings."""
        self._couplings = couplings
        self._update_all_structures()
    
    def get_couplings(self) -> RGCouplings:
        """Get the current RG couplings."""
        return self._couplings.copy()
    
    def get_cycle(self) -> int:
        """Get the current cycle number."""
        return self._cycle
    
    def is_running(self) -> bool:
        """Check if scheduler is running."""
        return self._running
    
    def on_cycle(self, callback: Callable[[ConsciousnessState], None]) -> None:
        """Register a callback to be called after each cycle."""
        self._on_cycle_callbacks.append(callback)
    
    def on_ledger_commit(self, callback: Callable[[ConsciousnessState], None]) -> None:
        """Register a callback to be called on ledger commits."""
        self._on_ledger_commit_callbacks.append(callback)
