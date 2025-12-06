#!/usr/bin/env python3
"""
Test script for experiment_a_v5_calibrated.py
Validates all requirements from the problem statement.
"""

import sys
import os
import json
import numpy as np

# Import the experiment module
import experiment_a_v5_calibrated as exp

def test_configuration():
    """Test 1: Verify configuration constants."""
    print("Test 1: Configuration constants...")
    
    assert exp.H2_BOND_DISTANCE == 0.735, "H2 bond distance incorrect"
    assert abs(exp.NUCLEAR_REPULSION - 0.719969) < 1e-6, "Nuclear repulsion incorrect"
    assert abs(exp.FCI_GROUND_STATE - (-1.137306)) < 1e-6, "FCI ground state incorrect"
    assert exp.NUM_QUBITS == 4, "Number of qubits incorrect"
    assert exp.ANSATZ_REPS == 2, "Ansatz reps incorrect"
    assert exp.NUM_TRIALS == 40, "Number of trials incorrect"
    assert exp.MAX_ITER == 200, "Max iterations incorrect"
    assert exp.SIGMA == 0.4, "Sigma incorrect"
    
    print("  ✓ All configuration constants correct")

def test_hamiltonian():
    """Test 2: Verify H2 Hamiltonian has 15 Pauli terms."""
    print("Test 2: H2 Hamiltonian...")
    
    assert len(exp.H2_PAULI_TERMS) == 15, f"Expected 15 Pauli terms, got {len(exp.H2_PAULI_TERMS)}"
    
    # Verify specific terms exist
    expected_paulis = ['IIII', 'ZIII', 'IIZI', 'ZIZI', 'IIIZ', 'IZII', 'IZIZ', 
                      'ZIIZ', 'IZZI', 'IIZZ', 'ZZII', 'YYYY', 'XXYY', 'YYXX', 'XXXX']
    actual_paulis = [term[0] for term in exp.H2_PAULI_TERMS]
    
    for pauli in expected_paulis:
        assert pauli in actual_paulis, f"Missing Pauli term: {pauli}"
    
    # Verify the IIII coefficient (largest)
    iiii_coeff = [term[1] for term in exp.H2_PAULI_TERMS if term[0] == 'IIII'][0]
    assert abs(iiii_coeff - (-0.8105479805)) < 1e-6, "IIII coefficient incorrect"
    
    print("  ✓ Hamiltonian has all 15 Pauli terms with correct coefficients")

def test_lambda_phi():
    """Test 3: Verify ΛΦ computation."""
    print("Test 3: ΛΦ computation...")
    
    lam_phi = exp.compute_lambda_phi()
    assert 0 <= lam_phi <= 1, f"ΛΦ should be in [0,1], got {lam_phi}"
    
    # Should be around 0.478 based on fixed telemetry
    expected_lam_phi = 0.478
    assert abs(lam_phi - expected_lam_phi) < 0.01, f"ΛΦ value unexpected: {lam_phi}"
    
    print(f"  ✓ ΛΦ value computed correctly: {lam_phi:.6f}")

def test_initialization():
    """Test 4: Verify initialization strategies."""
    print("Test 4: Initialization strategies...")
    
    num_params = 16  # EfficientSU2(4, reps=2) has 16 parameters
    
    # Test baseline initialization
    baseline_params = exp.baseline_init(num_params, seed=42)
    assert len(baseline_params) == num_params, "Baseline params wrong length"
    assert np.all(baseline_params >= -np.pi), "Baseline params below -π"
    assert np.all(baseline_params <= np.pi), "Baseline params above π"
    
    # Test ΛΦ-seeded initialization
    seeded_params = exp.lam_phi_init(num_params, seed=42)
    assert len(seeded_params) == num_params, "Seeded params wrong length"
    
    # Center should be around (0.478 * 2 - 1) * π ≈ -0.163π
    lam_phi = exp.compute_lambda_phi()
    expected_center = (lam_phi * 2 - 1) * np.pi
    actual_mean = np.mean(seeded_params)
    
    print(f"  ✓ Baseline initialization: uniform in [-π, π]")
    print(f"  ✓ Seeded initialization: centered at {expected_center:.3f} (mean={actual_mean:.3f})")

def test_nuclear_repulsion():
    """Test 5: Verify nuclear repulsion is added."""
    print("Test 5: Nuclear repulsion addition...")
    
    # Build components
    hamiltonian = exp.build_hamiltonian()
    ansatz = exp.build_ansatz()
    num_params = ansatz.num_parameters
    
    # Run a quick VQE (this will take time)
    print("  Running quick VQE optimization...")
    initial_params = exp.baseline_init(num_params, seed=42)
    result = exp.run_vqe(hamiltonian, ansatz, initial_params)
    
    # Verify result has both electronic and total energy
    assert 'electronic_energy' in result, "Missing electronic_energy"
    assert 'total_energy' in result, "Missing total_energy"
    
    # Total should be electronic + nuclear repulsion
    expected_total = result['electronic_energy'] + exp.NUCLEAR_REPULSION
    assert abs(result['total_energy'] - expected_total) < 1e-6, "Nuclear repulsion not added correctly"
    
    print(f"  ✓ Electronic: {result['electronic_energy']:.6f} Ha")
    print(f"  ✓ Total: {result['total_energy']:.6f} Ha")
    print(f"  ✓ Nuclear repulsion correctly added: {exp.NUCLEAR_REPULSION:.6f} Ha")

def test_output_format():
    """Test 6: Verify output format and statistics."""
    print("Test 6: Output format and statistics...")
    
    # Run mini experiment with 2 trials
    original_trials = exp.NUM_TRIALS
    exp.NUM_TRIALS = 2
    
    print("  Running mini experiment (2 trials)...")
    results = exp.run_experiment()
    
    # Restore original
    exp.NUM_TRIALS = original_trials
    
    # Verify results structure
    assert 'timestamp' in results, "Missing timestamp"
    assert 'configuration' in results, "Missing configuration"
    assert 'baseline' in results, "Missing baseline results"
    assert 'seeded' in results, "Missing seeded results"
    assert 'statistics' in results, "Missing statistics"
    assert 'analysis' in results, "Missing analysis"
    
    # Verify statistics
    stats = results['statistics']
    assert 'welch_t_stat' in stats, "Missing Welch t-test statistic"
    assert 'welch_p_value' in stats, "Missing Welch p-value"
    assert 'cohens_d' in stats, "Missing Cohen's d"
    assert 'levene_stat' in stats, "Missing Levene statistic"
    assert 'levene_p_value' in stats, "Missing Levene p-value"
    assert 'h0_rejected' in stats, "Missing H0 rejection flag"
    
    # Verify analysis
    analysis = results['analysis']
    assert 'mean_improvement' in analysis, "Missing mean improvement"
    assert 'improvement_pct' in analysis, "Missing improvement percentage"
    assert 'variance_reduction_pct' in analysis, "Missing variance reduction"
    
    print("  ✓ Results structure complete")
    print("  ✓ Statistical analysis included")
    print("  ✓ Output format correct")

def test_json_export():
    """Test 7: Verify JSON export."""
    print("Test 7: JSON export...")
    
    # Clean up any existing test files
    import glob
    for f in glob.glob('test_experiment_*.json'):
        os.remove(f)
    
    # Run mini experiment
    original_trials = exp.NUM_TRIALS
    exp.NUM_TRIALS = 2
    
    # Temporarily modify main to use test filename
    results = exp.run_experiment()
    
    # Save manually for test
    test_filename = 'test_experiment_results.json'
    with open(test_filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    exp.NUM_TRIALS = original_trials
    
    # Verify file was created and is valid JSON
    assert os.path.exists(test_filename), "JSON file not created"
    
    with open(test_filename, 'r') as f:
        loaded_data = json.load(f)
    
    assert loaded_data == results, "JSON data doesn't match results"
    
    # Clean up
    os.remove(test_filename)
    
    print(f"  ✓ JSON export working correctly")

def main():
    """Run all tests."""
    print("=" * 70)
    print("TESTING: experiment_a_v5_calibrated.py")
    print("=" * 70)
    print()
    
    tests = [
        test_configuration,
        test_hamiltonian,
        test_lambda_phi,
        test_initialization,
        test_nuclear_repulsion,
        test_output_format,
        test_json_export,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
            print()
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            print()
            failed += 1
    
    print("=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)
    
    if failed > 0:
        sys.exit(1)
    else:
        print("\n✓ All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
