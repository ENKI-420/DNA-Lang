# VQE Experiments

This directory contains quantum chemistry experiments using Variational Quantum Eigensolver (VQE) to study H₂ molecular ground states.

## Experiment A v5 (Calibrated)

### Overview
Compares two VQE initialization strategies for H₂:
- **Baseline**: Uniform random initialization in [-π, π]
- **ΛΦ-seeded**: Gaussian initialization centered at ΛΦ-derived point with σ=0.4

### Key Features
- ✅ Correct H₂ Hamiltonian with all 15 Pauli terms
- ✅ Nuclear repulsion energy (0.719969 Ha) added to all energies
- ✅ Total molecular energy reported for FCI comparison
- ✅ EfficientSU2 ansatz (4 qubits, 2 reps)
- ✅ 40 paired trials with COBYLA optimizer
- ✅ Statistical analysis (Welch's t-test, Cohen's d, Levene test)

### Installation

```bash
cd experiments
pip install -r requirements.txt
```

### Usage

Run the full experiment (40 trials):
```bash
python3 experiment_a_v5_calibrated.py
```

This will:
1. Run 40 paired VQE trials (Baseline vs ΛΦ-seeded)
2. Display real-time progress
3. Print statistical analysis
4. Save results to JSON with timestamp

### Output

The experiment produces:
- Console output with per-trial results
- Statistical analysis (t-test, effect size, variance comparison)
- Calibration verification
- JSON file: `experiment_a_v5_calibrated_results_YYYYMMDD_HHMMSS.json`

### Reference Values

- **H₂ bond distance**: 0.735 Å
- **Nuclear repulsion**: 0.719969 Ha
- **FCI ground state**: -1.137306 Ha (total molecular energy)
- **Electronic ground state**: ~-1.857 Ha

### ΛΦ Initialization

The ΛΦ value is computed from fixed telemetry:
- Completion: 0.8
- Revisits: 2
- Days since: 1
- Time spent: 45 min
- Diversity: 0.7
- Volatility: 0.2

This produces ΛΦ ≈ 0.478, which maps to a center point around -0.163π for parameter initialization.
