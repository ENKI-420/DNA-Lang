"""
Tests for Kernel Components
"""

import sys
import unittest
import time

sys.path.insert(0, '/home/runner/work/DNA-Lang/DNA-Lang')

from kernel.consciousness_state import ConsciousnessState
from kernel.events import (
    KernelEvent,
    KernelEventType,
    EventBus,
    get_event_bus,
    emit_event,
)
from kernel.syscalls import (
    z3_sys_read_state,
    z3_sys_write_state,
    z3_sys_reset_state,
)
from kernel.scheduler import ConsciousnessScheduler, SchedulerConfig
from lib.sovereign_rg_engine.constants import PHI_STAR, GAMMA_THRESHOLD


class TestConsciousnessState(unittest.TestCase):
    """Test ConsciousnessState dataclass."""
    
    def test_default_values(self):
        """Test default state values."""
        state = ConsciousnessState()
        
        self.assertAlmostEqual(state.Phi, PHI_STAR, places=3)
        self.assertEqual(state.Gamma, 0.0)
        self.assertTrue(state.pt_symmetry)
        self.assertFalse(state.jordan_block)
    
    def test_fixed_point_check(self):
        """Test fixed point detection."""
        state = ConsciousnessState(
            Phi=PHI_STAR,
            Gamma=0.01,
            beta_norm=0.0001,
            ricci_scalar=0.0,
            vacuum_energy=0.0,
        )
        self.assertTrue(state.is_at_fixed_point())
    
    def test_decoherence_checks(self):
        """Test decoherence threshold checks."""
        state = ConsciousnessState(Gamma=GAMMA_THRESHOLD * 0.5)
        self.assertFalse(state.is_decoherence_warning())
        
        state.Gamma = GAMMA_THRESHOLD * 1.5
        self.assertTrue(state.is_decoherence_warning())
        self.assertFalse(state.is_decoherence_critical())
        
        state.Gamma = GAMMA_THRESHOLD * 2.5
        self.assertTrue(state.is_decoherence_critical())
    
    def test_serialization(self):
        """Test JSON serialization."""
        state = ConsciousnessState(Phi=0.95, Gamma=0.05, cycle=42)
        
        json_str = state.to_json()
        restored = ConsciousnessState.from_json(json_str)
        
        self.assertAlmostEqual(restored.Phi, 0.95, places=5)
        self.assertAlmostEqual(restored.Gamma, 0.05, places=5)
        self.assertEqual(restored.cycle, 42)
    
    def test_copy(self):
        """Test state copy."""
        state1 = ConsciousnessState(Phi=0.9)
        state2 = state1.copy()
        state2.Phi = 0.8
        
        self.assertAlmostEqual(state1.Phi, 0.9, places=5)


class TestEvents(unittest.TestCase):
    """Test kernel event system."""
    
    def setUp(self):
        """Set up fresh event bus."""
        self.bus = EventBus()
    
    def test_event_creation(self):
        """Test event creation."""
        event = KernelEvent(
            event_type=KernelEventType.STATE_UPDATE,
            cycle=10,
        )
        
        self.assertEqual(event.event_type, KernelEventType.STATE_UPDATE)
        self.assertEqual(event.cycle, 10)
    
    def test_subscribe_publish(self):
        """Test pub/sub functionality."""
        received = []
        
        def handler(event):
            received.append(event)
        
        self.bus.subscribe(KernelEventType.STATE_UPDATE, handler)
        
        event = KernelEvent(event_type=KernelEventType.STATE_UPDATE)
        self.bus.publish(event)
        
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].event_type, KernelEventType.STATE_UPDATE)
    
    def test_subscribe_all(self):
        """Test global subscription."""
        received = []
        
        def handler(event):
            received.append(event)
        
        self.bus.subscribe_all(handler)
        
        self.bus.publish(KernelEvent(event_type=KernelEventType.STATE_UPDATE))
        self.bus.publish(KernelEvent(event_type=KernelEventType.FIXED_POINT_REACHED))
        
        self.assertEqual(len(received), 2)
    
    def test_event_history(self):
        """Test event history."""
        self.bus.publish(KernelEvent(event_type=KernelEventType.STATE_UPDATE))
        self.bus.publish(KernelEvent(event_type=KernelEventType.FIXED_POINT_REACHED))
        
        history = self.bus.get_history(limit=10)
        self.assertEqual(len(history), 2)


class TestSyscalls(unittest.TestCase):
    """Test kernel syscalls."""
    
    def setUp(self):
        """Reset state before each test."""
        z3_sys_reset_state()
    
    def test_read_write_state(self):
        """Test reading and writing state."""
        state = ConsciousnessState(Phi=0.9, Gamma=0.05, cycle=100)
        z3_sys_write_state(state)
        
        read_state = z3_sys_read_state()
        self.assertAlmostEqual(read_state.Phi, 0.9, places=5)
        self.assertEqual(read_state.cycle, 100)
    
    def test_state_copy_on_read(self):
        """Test that read returns a copy."""
        state = ConsciousnessState(Phi=0.9)
        z3_sys_write_state(state)
        
        read1 = z3_sys_read_state()
        read1.Phi = 0.5
        
        read2 = z3_sys_read_state()
        self.assertAlmostEqual(read2.Phi, 0.9, places=5)


class TestScheduler(unittest.TestCase):
    """Test consciousness scheduler."""
    
    def test_scheduler_creation(self):
        """Test scheduler instantiation."""
        config = SchedulerConfig(frequency=5.0)
        scheduler = ConsciousnessScheduler(config=config)
        
        self.assertIsNotNone(scheduler)
        self.assertFalse(scheduler.is_running())
    
    def test_single_cycle(self):
        """Test single cycle execution."""
        config = SchedulerConfig(frequency=5.0)
        scheduler = ConsciousnessScheduler(config=config)
        
        state = scheduler.run_single_cycle()
        
        self.assertIsInstance(state, ConsciousnessState)
        self.assertEqual(scheduler.get_cycle(), 1)
    
    def test_couplings_access(self):
        """Test coupling get/set."""
        from lib.sovereign_rg_engine.couplings import RGCouplings
        
        config = SchedulerConfig()
        scheduler = ConsciousnessScheduler(config=config)
        
        couplings = RGCouplings(g1=0.1, g2=0.2)
        scheduler.set_couplings(couplings)
        
        retrieved = scheduler.get_couplings()
        self.assertAlmostEqual(retrieved.g1, 0.1, places=5)


if __name__ == '__main__':
    unittest.main()
