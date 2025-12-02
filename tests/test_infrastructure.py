"""
Tests for Infrastructure Components
"""

import sys
import unittest

import os as _os; _TEST_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))); sys.path.insert(0, _TEST_ROOT) if _TEST_ROOT not in sys.path else None

from kernel.consciousness_state import ConsciousnessState
from ledger.qcx_ledger import QCXLedger
from bus.manifold_bus import ManifoldBus, BusMessage
from qpu.meshnet6d import MeshNet6D
from crypto.lambda_phi_sig import LambdaPhiSignature
from organisms.phoenix import PhoenixOrganism
from organisms.genome import Genome, Gene
from lib.sovereign_rg_engine.constants import GAMMA_THRESHOLD


class TestQCXLedger(unittest.TestCase):
    """Test QCX Ledger."""
    
    def test_genesis_block(self):
        """Test genesis block creation."""
        ledger = QCXLedger()
        
        self.assertGreaterEqual(ledger.get_length(), 1)
        # Genesis block has index 1 (0 is reserved)
        latest = ledger.get_latest()
        self.assertIsNotNone(latest)
    
    def test_commit_state(self):
        """Test state commitment."""
        ledger = QCXLedger()
        
        state = ConsciousnessState(Phi=0.95, cycle=10)
        entry = ledger.commit(state)
        
        self.assertEqual(ledger.get_length(), 2)
        self.assertIsNotNone(entry.state_hash)
        self.assertIsNotNone(entry.lambda_phi_signature)
    
    def test_chain_verification(self):
        """Test chain integrity verification."""
        ledger = QCXLedger()
        
        for i in range(5):
            state = ConsciousnessState(cycle=i)
            ledger.commit(state)
        
        is_valid, invalid = ledger.verify_chain()
        self.assertTrue(is_valid)
        self.assertEqual(len(invalid), 0)
    
    def test_state_recovery(self):
        """Test state recovery by cycle."""
        ledger = QCXLedger()
        
        state = ConsciousnessState(Phi=0.88, cycle=42)
        ledger.commit(state)
        
        recovered = ledger.get_state_at_cycle(42)
        self.assertIsNotNone(recovered)
        self.assertAlmostEqual(recovered.Phi, 0.88, places=5)


class TestManifoldBus(unittest.TestCase):
    """Test Manifold Bus."""
    
    def test_publish_subscribe(self):
        """Test basic pub/sub."""
        bus = ManifoldBus()
        received = []
        
        def handler(msg):
            received.append(msg)
        
        bus.subscribe("test", handler)
        bus.publish("test", {"data": "value"})
        
        # Process queue manually (not using async)
        bus._process_pending()
        
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].payload["data"], "value")
    
    def test_w2_priority(self):
        """Test W₂-based priority ordering."""
        bus = ManifoldBus()
        
        # Higher Γ/Φ ratio = lower priority
        bus.publish("test", {"Phi": 0.9, "Gamma": 0.1}, w2_weight=0.1)
        bus.publish("test", {"Phi": 0.9, "Gamma": 0.5}, w2_weight=0.5)
        
        self.assertEqual(bus.get_queue_length(), 2)


class TestMeshNet6D(unittest.TestCase):
    """Test MeshNet-6D."""
    
    def test_node_creation(self):
        """Test node initialization."""
        mesh = MeshNet6D()
        
        self.assertIsNotNone(mesh.node_id)
        self.assertEqual(mesh.get_node_count(), 1)  # Local node
    
    def test_broadcast_state(self):
        """Test state broadcasting."""
        mesh = MeshNet6D()
        
        state = ConsciousnessState(Phi=0.95, cycle=1)
        mesh.broadcast_state(state)
        
        # Local node should have the state
        local_state = mesh._local_node.state
        self.assertIsNotNone(local_state)
        self.assertAlmostEqual(local_state.Phi, 0.95, places=5)


class TestLambdaPhiSignature(unittest.TestCase):
    """Test ΛΦ signatures."""
    
    def test_sign_verify(self):
        """Test signing and verification."""
        sig = LambdaPhiSignature()
        
        message = b"test message"
        result = sig.sign(message)
        
        self.assertIsNotNone(result.signature)
        
        # Verify
        verify_result = sig.verify(message, result.signature, result.timestamp)
        self.assertTrue(verify_result.valid)
    
    def test_invalid_signature(self):
        """Test invalid signature detection."""
        sig = LambdaPhiSignature()
        
        message = b"test message"
        result = sig.sign(message)
        
        # Tamper with signature
        tampered = result.signature[:-1] + "X"
        verify_result = sig.verify(message, tampered, result.timestamp)
        self.assertFalse(verify_result.valid)


class TestPhoenixOrganism(unittest.TestCase):
    """Test Phoenix self-healing organism."""
    
    def test_spawn(self):
        """Test Phoenix spawning."""
        phoenix = PhoenixOrganism(name="TestPhoenix")
        phoenix.spawn()
        
        self.assertTrue(phoenix.is_alive())
        self.assertEqual(phoenix.get_deaths(), 0)
    
    def test_lazarus_activation(self):
        """Test Lazarus Protocol activation on critical decoherence."""
        phoenix = PhoenixOrganism(name="TestPhoenix")
        phoenix.spawn()
        
        # Update with critical decoherence
        state = phoenix.update(phi=0.9, gamma=GAMMA_THRESHOLD * 3)
        
        # Lazarus should have activated
        self.assertTrue(state.lazarus_active)
        self.assertEqual(phoenix.get_deaths(), 1)
        # Gamma should be suppressed
        self.assertLess(state.gamma, GAMMA_THRESHOLD * 3)
    
    def test_despawn(self):
        """Test Phoenix despawning."""
        phoenix = PhoenixOrganism(name="TestPhoenix")
        phoenix.spawn()
        phoenix.despawn()
        
        self.assertFalse(phoenix.is_alive())


class TestGenome(unittest.TestCase):
    """Test Genome and Gene."""
    
    def test_gene_creation(self):
        """Test gene creation."""
        gene = Gene(name="TestGene", sequence="ATCG")
        
        self.assertEqual(gene.name, "TestGene")
        self.assertEqual(gene.sequence, "ATCG")
    
    def test_gene_mutation(self):
        """Test gene mutation."""
        gene = Gene(name="TestGene", sequence="ATCG")
        gene.mutate("GGCC")
        
        self.assertIn("GGCC", gene.sequence)
        self.assertEqual(len(gene.mutations), 1)
    
    def test_genome_operations(self):
        """Test genome operations."""
        genome = Genome(organism_type="test")
        
        gene1 = Gene(name="Gene1", sequence="AAA")
        gene2 = Gene(name="Gene2", sequence="BBB")
        
        genome.add_gene(gene1)
        genome.add_gene(gene2)
        
        self.assertEqual(len(genome.genes), 2)
        
        retrieved = genome.get_gene("Gene1")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.sequence, "AAA")
    
    def test_genome_clone(self):
        """Test genome cloning."""
        genome = Genome(organism_type="test")
        genome.add_gene(Gene(name="Gene1", sequence="AAA"))
        
        clone = genome.clone()
        
        self.assertEqual(clone.generation, genome.generation + 1)
        self.assertIsNotNone(clone.get_gene("Gene1"))


if __name__ == '__main__':
    unittest.main()
