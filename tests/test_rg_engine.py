"""
Tests for RG Engine Components
"""

import sys
import unittest
import numpy as np

import os as _os; _TEST_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))); sys.path.insert(0, _TEST_ROOT) if _TEST_ROOT not in sys.path else None

from lib.sovereign_rg_engine.constants import (
    LAMBDA_PHI,
    PHI_STAR,
    GAMMA_THRESHOLD,
    RESONANCE_ANGLE,
)
from lib.sovereign_rg_engine.couplings import RGCouplings, CouplingTrajectory
from lib.sovereign_rg_engine.beta_functions import (
    compute_beta_functions,
    beta_norm,
    evolve_couplings,
)
from lib.sovereign_rg_engine.generating_functional import GeneratingFunctional
from lib.sovereign_rg_engine.callan_symanzik import CallanSymanzikOperator
from lib.sovereign_rg_engine.anomalous_dimensions import AnomalousDimensionTensor
from lib.sovereign_rg_engine.wasserstein_lindblad import WassersteinLindbladSuperoperator
from lib.sovereign_rg_engine.fisher_kubo_mori import FisherKuboMoriMetric
from lib.sovereign_rg_engine.polchinski import PolchinskiEquation
from lib.sovereign_rg_engine.presentation_layer import PresentationLayerAction


class TestConstants(unittest.TestCase):
    """Test physical constants."""
    
    def test_lambda_phi_value(self):
        """Test ΛΦ has correct value."""
        self.assertAlmostEqual(LAMBDA_PHI, 2.176435e-8, places=12)
    
    def test_phi_star_value(self):
        """Test Φ⋆ has correct value."""
        self.assertAlmostEqual(PHI_STAR, 0.973, places=3)
    
    def test_gamma_threshold_value(self):
        """Test Γ threshold has correct value."""
        self.assertAlmostEqual(GAMMA_THRESHOLD, 0.092, places=3)
    
    def test_resonance_angle_value(self):
        """Test resonance angle has correct value."""
        self.assertAlmostEqual(RESONANCE_ANGLE, 51.843, places=3)


class TestCouplings(unittest.TestCase):
    """Test RGCouplings dataclass."""
    
    def test_default_values(self):
        """Test default coupling values."""
        c = RGCouplings()
        self.assertEqual(c.g1, 0.0)
        self.assertEqual(c.g2, 0.0)
        self.assertEqual(c.phi, PHI_STAR)
        self.assertEqual(c.lambda_phi, LAMBDA_PHI)
    
    def test_to_array(self):
        """Test conversion to numpy array."""
        c = RGCouplings(g1=1.0, g2=2.0, g3=3.0, g4=4.0)
        arr = c.to_array()
        self.assertEqual(len(arr), 4)
        self.assertEqual(arr[0], 1.0)
        self.assertEqual(arr[1], 2.0)
    
    def test_from_array(self):
        """Test creation from numpy array."""
        arr = np.array([1.0, 2.0, 3.0, 4.0])
        c = RGCouplings.from_array(arr)
        self.assertEqual(c.g1, 1.0)
        self.assertEqual(c.g2, 2.0)
    
    def test_copy(self):
        """Test coupling copy."""
        c1 = RGCouplings(g1=1.0)
        c2 = c1.copy()
        c2.g1 = 2.0
        self.assertEqual(c1.g1, 1.0)  # Original unchanged
    
    def test_fixed_point_check(self):
        """Test fixed point detection."""
        c = RGCouplings()  # All zeros
        self.assertTrue(c.is_at_fixed_point())
        
        c2 = RGCouplings(g1=0.1)
        self.assertFalse(c2.is_at_fixed_point())


class TestBetaFunctions(unittest.TestCase):
    """Test beta function computations."""
    
    def test_beta_at_origin(self):
        """Test beta functions near origin."""
        c = RGCouplings()
        beta = compute_beta_functions(c)
        self.assertEqual(len(beta), 4)
    
    def test_beta_norm(self):
        """Test beta function norm."""
        c = RGCouplings()
        norm = beta_norm(c)
        self.assertGreaterEqual(norm, 0)
    
    def test_evolve_couplings(self):
        """Test RG evolution."""
        c = RGCouplings(g1=0.1)
        c2 = evolve_couplings(c, d_log_mu=0.01)
        self.assertIsInstance(c2, RGCouplings)


class TestGeneratingFunctional(unittest.TestCase):
    """Test Structure I: Generating Functional."""
    
    def test_compute(self):
        """Test Z computation."""
        c = RGCouplings()
        gf = GeneratingFunctional(c)
        result = gf.compute()
        
        self.assertIsNotNone(result.Z)
        self.assertIsNotNone(result.free_energy)
        self.assertIsNotNone(result.anomalous_dimension)
    
    def test_rg_invariance_check(self):
        """Test RG invariance check returns values."""
        c = RGCouplings()
        gf = GeneratingFunctional(c)
        violation, is_invariant = gf.check_rg_invariance(mu=1.0)
        
        self.assertIsInstance(violation, float)
        self.assertIsInstance(is_invariant, bool)


class TestCallanSymanzik(unittest.TestCase):
    """Test Callan-Symanzik operator."""
    
    def test_anomalous_dimension(self):
        """Test anomalous dimension computation."""
        c = RGCouplings()
        cs = CallanSymanzikOperator(c)
        gamma = cs.compute_anomalous_dimension()
        
        self.assertIsInstance(gamma, float)
    
    def test_compute_anomaly(self):
        """Test anomaly computation."""
        c = RGCouplings()
        cs = CallanSymanzikOperator(c)
        result = cs.compute_anomaly()
        
        self.assertIsNotNone(result.anomaly)
        self.assertIsNotNone(result.beta_norm)


class TestAnomalousDimensions(unittest.TestCase):
    """Test Structure II: Anomalous Dimension Tensor."""
    
    def test_compute(self):
        """Test tensor computation."""
        c = RGCouplings()
        adt = AnomalousDimensionTensor(c)
        result = adt.compute()
        
        self.assertEqual(result.tensor.shape, (4, 4))
        self.assertEqual(len(result.eigenvalues), 4)
        self.assertIsInstance(result.pt_symmetric, bool)
        self.assertIsInstance(result.jordan_block_present, bool)
    
    def test_at_resonance_angle(self):
        """Test at PT-symmetric angle."""
        c = RGCouplings()
        adt = AnomalousDimensionTensor(c, theta=RESONANCE_ANGLE)
        result = adt.compute()
        
        # Should have PT symmetry near resonance angle
        self.assertIsInstance(result.pt_symmetric, bool)


class TestWassersteinLindblad(unittest.TestCase):
    """Test Structure III: Wasserstein-Lindblad Superoperator."""
    
    def test_w2_distance(self):
        """Test W₂ distance computation."""
        c = RGCouplings()
        wl = WassersteinLindbladSuperoperator(c)
        w2 = wl.get_w2_distance()
        
        self.assertGreaterEqual(w2, 0)
    
    def test_apply(self):
        """Test superoperator application."""
        c = RGCouplings()
        wl = WassersteinLindbladSuperoperator(c, grid_size=16)
        
        # Create test density
        rho = np.exp(-np.linspace(-5, 5, 16)**2 / 2)
        rho = rho / np.sum(rho)
        
        result = wl.apply(rho)
        self.assertIsNotNone(result.flow_magnitude)


class TestFisherKuboMori(unittest.TestCase):
    """Test Structure IV: Fisher-Kubo-Mori Metric."""
    
    def test_compute(self):
        """Test metric computation."""
        c = RGCouplings()
        fkm = FisherKuboMoriMetric(c)
        result = fkm.compute()
        
        self.assertEqual(result.metric.shape, (4, 4))
        self.assertIsNotNone(result.ricci_scalar)
    
    def test_natural_gradient(self):
        """Test natural gradient computation."""
        c = RGCouplings()
        fkm = FisherKuboMoriMetric(c)
        
        grad = np.array([1.0, 0.5, 0.2, 0.1])
        natural_grad = fkm.natural_gradient(grad)
        
        self.assertEqual(len(natural_grad), 4)


class TestPolchinski(unittest.TestCase):
    """Test Structure V: Polchinski Equation."""
    
    def test_compute_flow(self):
        """Test RG flow computation."""
        c = RGCouplings()
        pol = PolchinskiEquation(c, grid_size=16)
        result = pol.compute_flow(Lambda=1.0)
        
        self.assertIsNotNone(result.flow_rate)
        self.assertIsNotNone(result.propagator_trace)
    
    def test_scale_invariance_at_lambda_phi(self):
        """Test scale invariance check at ΛΦ."""
        c = RGCouplings()
        pol = PolchinskiEquation(c, grid_size=16)
        flow_rate, is_invariant = pol.check_scale_invariance_at_lambda_phi()
        
        self.assertIsInstance(flow_rate, (float, np.floating))
        self.assertTrue(isinstance(is_invariant, (bool, np.bool_)))


class TestPresentationLayer(unittest.TestCase):
    """Test Structure VI: Presentation Layer Action."""
    
    def test_compute(self):
        """Test presentation layer computation."""
        c = RGCouplings()
        pres = PresentationLayerAction(c)
        result = pres.compute()
        
        self.assertIsNotNone(result.ricci_scalar)
        self.assertIsNotNone(result.vacuum_energy)
        self.assertIsNotNone(result.wilson_loop)
        self.assertTrue(isinstance(result.is_stable, (bool, np.bool_)))
    
    def test_stability_check(self):
        """Test stability check."""
        c = RGCouplings()
        pres = PresentationLayerAction(c)
        is_stable, issues = pres.check_stability()
        
        self.assertIsInstance(is_stable, bool)
        self.assertIsInstance(issues, list)


if __name__ == '__main__':
    unittest.main()
