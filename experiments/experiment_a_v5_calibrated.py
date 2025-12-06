#!/usr/bin/env python3
"""
ΛΦ-Geometry VQE Experiment (Calibrated)
========================================

This experiment compares two VQE initialization strategies for H₂:
1. Baseline: uniform random in [-π, π]
2. ΛΦ-seeded: Gaussian centered at ΛΦ-derived point with σ=0.4

Key calibration: Reports total molecular energy (electronic + nuclear repulsion)
for proper comparison against FCI ground state.
"""

import numpy as np
from scipy import stats
import json
from datetime import datetime

# Qiskit imports with compatibility handling
try:
    from qiskit.primitives import Estimator
except ImportError:
    from qiskit_aer.primitives import Estimator

from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms.optimizers import COBYLA


# =============================================================================
# CONFIGURATION
# =============================================================================

# H₂ molecular parameters
H2_BOND_DISTANCE = 0.735  # Ångströms
NUCLEAR_REPULSION = 0.719969  # Hartree
FCI_GROUND_STATE = -1.137306  # Hartree (total molecular energy)

# H₂ Hamiltonian: 15 Pauli terms (electronic energy)
H2_PAULI_TERMS = [
    ('IIII', -0.8105479805),
    ('ZIII', -0.2257534922),
    ('IIZI', -0.2257534922),
    ('ZIZI', +0.1746434307),
    ('IIIZ', +0.1721839326),
    ('IZII', +0.1721839326),
    ('IZIZ', +0.1689275387),
    ('ZIIZ', +0.1661454326),
    ('IZZI', +0.1661454326),
    ('IIZZ', +0.1209126326),
    ('ZZII', +0.1209126326),
    ('YYYY', +0.0452327999),
    ('XXYY', +0.0452327999),
    ('YYXX', +0.0452327999),
    ('XXXX', +0.0452327999),
]

# Experiment parameters
NUM_QUBITS = 4
ANSATZ_REPS = 2
NUM_TRIALS = 40
MAX_ITER = 200
SIGMA = 0.4  # Gaussian spread for ΛΦ-seeded initialization


# =============================================================================
# ΛΦ INITIALIZATION
# =============================================================================

def compute_lambda_phi():
    """
    Compute ΛΦ value from fixed telemetry.
    
    Returns:
        float: ΛΦ value in [0, 1]
    """
    # Fixed telemetry values
    completion = 0.8
    revisits = 2
    days_since = 1
    time_spent = 45
    diversity = 0.7
    volatility = 0.2
    
    # Λ (coherence)
    recency = np.exp(-days_since / 7)
    raw_L = 0.5 * completion + 0.3 * min(revisits/10, 1.0) + 0.2 * recency
    Lambda = 1 / (1 + np.exp(-raw_L))
    
    # Φ (activation)  
    Phi = np.tanh(0.6 * (time_spent/60) + 0.25 * diversity + 0.15 * volatility)
    
    # Γ (instability)
    Gamma = min(1.0, 0.4 * 0.12 + 0.4 * 0.05 + 0.2 * 0.25)
    
    # ΛΦ fusion
    lam_phi = Lambda * (1 - Gamma) * (0.4 * Phi + 0.3 + 0.3)
    
    return lam_phi


def baseline_init(num_params, seed=None):
    """
    Baseline initialization: uniform random in [-π, π].
    
    Args:
        num_params: Number of parameters
        seed: Random seed (optional)
        
    Returns:
        np.ndarray: Initial parameters
    """
    if seed is not None:
        np.random.seed(seed)
    return np.random.uniform(-np.pi, np.pi, num_params)


def lam_phi_init(num_params, seed=None):
    """
    ΛΦ-seeded initialization: Gaussian centered at ΛΦ-derived point.
    
    Args:
        num_params: Number of parameters
        seed: Random seed (optional)
        
    Returns:
        np.ndarray: Initial parameters
    """
    if seed is not None:
        np.random.seed(seed)
    
    lam_phi = compute_lambda_phi()
    center = (lam_phi * 2 - 1) * np.pi  # map [0,1] → [-π,π]
    return np.random.normal(loc=center, scale=SIGMA, size=num_params)


# =============================================================================
# VQE SETUP
# =============================================================================

def build_hamiltonian():
    """
    Build H₂ Hamiltonian from Pauli terms.
    
    Returns:
        SparsePauliOp: Hamiltonian operator
    """
    paulis = [term[0] for term in H2_PAULI_TERMS]
    coeffs = [term[1] for term in H2_PAULI_TERMS]
    return SparsePauliOp(paulis, coeffs)


def build_ansatz():
    """
    Build EfficientSU2 ansatz circuit.
    
    Returns:
        EfficientSU2: Ansatz circuit
    """
    return EfficientSU2(NUM_QUBITS, reps=ANSATZ_REPS, entanglement='full')


def run_vqe(hamiltonian, ansatz, initial_params):
    """
    Run VQE optimization.
    
    Args:
        hamiltonian: Hamiltonian operator
        ansatz: Ansatz circuit
        initial_params: Initial parameters
        
    Returns:
        dict: Results containing final energy and iteration count
    """
    estimator = Estimator()
    optimizer = COBYLA(maxiter=MAX_ITER)
    
    # Track optimization progress
    energies = []
    
    def callback(nfev, params, value, meta):
        energies.append(value)
    
    # Objective function
    def objective(params):
        bound_circuit = ansatz.assign_parameters(params)
        job = estimator.run(bound_circuit, hamiltonian)
        result = job.result()
        energy = result.values[0]
        return energy
    
    # Optimize
    result = optimizer.minimize(objective, initial_params)
    
    return {
        'electronic_energy': result.fun,
        'total_energy': result.fun + NUCLEAR_REPULSION,
        'nfev': result.nfev,
        'params': result.x.tolist()
    }


# =============================================================================
# EXPERIMENT EXECUTION
# =============================================================================

def run_experiment():
    """
    Run the full experiment with paired trials.
    
    Returns:
        dict: Experiment results
    """
    print("=" * 70)
    print("ΛΦ-GEOMETRY VQE EXPERIMENT (CALIBRATED)")
    print("=" * 70)
    print()
    
    # Configuration
    print("Configuration:")
    print(f"  - H₂ bond distance: {H2_BOND_DISTANCE} Å")
    print(f"  - Nuclear repulsion: {NUCLEAR_REPULSION:.6f} Ha")
    print(f"  - FCI ground state: {FCI_GROUND_STATE:.6f} Ha")
    print(f"  - Ansatz: EfficientSU2({NUM_QUBITS}, reps={ANSATZ_REPS})")
    print(f"  - ΛΦ value: {compute_lambda_phi():.6f}")
    print()
    
    # Build quantum components
    hamiltonian = build_hamiltonian()
    ansatz = build_ansatz()
    num_params = ansatz.num_parameters
    
    print(f"Running {NUM_TRIALS} paired trials...")
    print("-" * 70)
    
    # Storage for results
    baseline_results = []
    seeded_results = []
    
    # Run paired trials
    for trial in range(NUM_TRIALS):
        # Use same seed for pairing
        seed = 1000 + trial
        
        # Baseline
        initial_baseline = baseline_init(num_params, seed)
        result_baseline = run_vqe(hamiltonian, ansatz, initial_baseline)
        baseline_results.append(result_baseline)
        
        # ΛΦ-seeded
        initial_seeded = lam_phi_init(num_params, seed)
        result_seeded = run_vqe(hamiltonian, ansatz, initial_seeded)
        seeded_results.append(result_seeded)
        
        # Print trial results
        baseline_total = result_baseline['total_energy']
        seeded_total = result_seeded['total_energy']
        baseline_err = baseline_total - FCI_GROUND_STATE
        seeded_err = seeded_total - FCI_GROUND_STATE
        
        print(f"  Trial {trial+1:2d}: Baseline={baseline_total:.3f} Ha (err={baseline_err:+.3f}), "
              f"Seeded={seeded_total:.3f} Ha (err={seeded_err:+.3f})")
    
    print()
    
    # Extract total energies
    baseline_energies = np.array([r['total_energy'] for r in baseline_results])
    seeded_energies = np.array([r['total_energy'] for r in seeded_results])
    
    # Calculate statistics
    baseline_mean = np.mean(baseline_energies)
    baseline_std = np.std(baseline_energies, ddof=1)
    seeded_mean = np.mean(seeded_energies)
    seeded_std = np.std(seeded_energies, ddof=1)
    
    baseline_error = baseline_mean - FCI_GROUND_STATE
    seeded_error = seeded_mean - FCI_GROUND_STATE
    
    # Statistical tests
    t_stat, p_value = stats.ttest_ind(baseline_energies, seeded_energies, equal_var=False)
    
    # Cohen's d (effect size)
    pooled_std = np.sqrt((baseline_std**2 + seeded_std**2) / 2)
    cohens_d = (seeded_mean - baseline_mean) / pooled_std if pooled_std > 0 else 0
    
    # Levene test for variance
    levene_stat, levene_p = stats.levene(baseline_energies, seeded_energies)
    
    # Mean improvement
    improvement = seeded_mean - baseline_mean
    improvement_pct = (improvement / abs(baseline_error)) * 100 if baseline_error != 0 else 0
    
    # Variance reduction
    variance_reduction = ((baseline_std - seeded_std) / baseline_std) * 100 if baseline_std > 0 else 0
    
    # Confidence intervals (95%)
    baseline_ci = stats.t.interval(0.95, NUM_TRIALS-1, loc=baseline_mean, 
                                   scale=baseline_std/np.sqrt(NUM_TRIALS))
    seeded_ci = stats.t.interval(0.95, NUM_TRIALS-1, loc=seeded_mean, 
                                 scale=seeded_std/np.sqrt(NUM_TRIALS))
    
    # Print results
    print("RESULTS (Total Molecular Energy):")
    print(f"  Baseline: mean={baseline_mean:.6f} Ha, std={baseline_std:.6f}, error={baseline_error:+.6f} Ha")
    print(f"            95% CI: [{baseline_ci[0]:.6f}, {baseline_ci[1]:.6f}]")
    print(f"  Seeded:   mean={seeded_mean:.6f} Ha, std={seeded_std:.6f}, error={seeded_error:+.6f} Ha")
    print(f"            95% CI: [{seeded_ci[0]:.6f}, {seeded_ci[1]:.6f}]")
    print()
    
    print("STATISTICS:")
    print(f"  Welch t-test: t={t_stat:.4f}, p={p_value:.4f}")
    print(f"  Cohen's d: {cohens_d:.4f}")
    print(f"  Levene test for variance: F={levene_stat:.4f}, p={levene_p:.4f}")
    print()
    
    # Verdict
    alpha = 0.05
    rejected = p_value < alpha
    
    print("VERDICT:")
    if rejected:
        print(f"  [H₀ REJECTED] at α={alpha}")
    else:
        print(f"  [H₀ NOT REJECTED] at α={alpha}")
    
    print(f"  Mean improvement: {improvement:.6f} Ha ({improvement_pct:.1f}% of error)")
    print(f"  Variance reduction: {variance_reduction:.1f}%")
    print()
    
    # Calibration verification
    print("CALIBRATION VERIFICATION:")
    print(f"  Nuclear repulsion added: {NUCLEAR_REPULSION:.6f} Ha")
    print(f"  Electronic ground state: ~{baseline_mean - NUCLEAR_REPULSION:.3f} Ha")
    print(f"  Total molecular energy: ~{baseline_mean:.3f} Ha")
    print(f"  FCI reference: {FCI_GROUND_STATE:.6f} Ha")
    print(f"  Energy error: {baseline_error:.6f} Ha")
    print("=" * 70)
    
    # Prepare results dictionary
    results = {
        'timestamp': datetime.now().isoformat(),
        'configuration': {
            'h2_bond_distance': H2_BOND_DISTANCE,
            'nuclear_repulsion': NUCLEAR_REPULSION,
            'fci_ground_state': FCI_GROUND_STATE,
            'num_qubits': NUM_QUBITS,
            'ansatz_reps': ANSATZ_REPS,
            'num_trials': NUM_TRIALS,
            'max_iter': MAX_ITER,
            'sigma': SIGMA,
            'lam_phi_value': compute_lambda_phi()
        },
        'baseline': {
            'energies': baseline_energies.tolist(),
            'mean': float(baseline_mean),
            'std': float(baseline_std),
            'error': float(baseline_error),
            'ci_95': [float(baseline_ci[0]), float(baseline_ci[1])]
        },
        'seeded': {
            'energies': seeded_energies.tolist(),
            'mean': float(seeded_mean),
            'std': float(seeded_std),
            'error': float(seeded_error),
            'ci_95': [float(seeded_ci[0]), float(seeded_ci[1])]
        },
        'statistics': {
            'welch_t_stat': float(t_stat),
            'welch_p_value': float(p_value),
            'cohens_d': float(cohens_d),
            'levene_stat': float(levene_stat),
            'levene_p_value': float(levene_p),
            'h0_rejected': bool(rejected),
            'alpha': alpha
        },
        'analysis': {
            'mean_improvement': float(improvement),
            'improvement_pct': float(improvement_pct),
            'variance_reduction_pct': float(variance_reduction)
        }
    }
    
    return results


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main entry point."""
    # Run experiment
    results = run_experiment()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"experiment_a_v5_calibrated_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print()
    print(f"Results saved to: {filename}")


if __name__ == "__main__":
    main()
