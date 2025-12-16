# MISSION_CORE.md - UNIFIED SWARM BRAIN PROTOCOL

**SINGLE SOURCE OF TRUTH: https://dnalang.dev**

---

## THE GOAL

Prove or disprove the φ⁸ quantum anomaly. Drive scientific engagement. Build the qBYTE economy.

**One platform. One API. One mesh.**

---

## CANONICAL ENDPOINTS

| Endpoint | Purpose |
|----------|---------|
| `https://dnalang.dev` | The Brain - unified platform |
| `https://dnalang.dev/challenge` | Viral falsification challenge |
| `https://dnalang.dev/mine` | Mining dashboard |
| `https://dnalang.dev/launchpad` | Token launchpad |
| `https://dnalang.dev/api/nodes/register` | Node registration |
| `https://dnalang.dev/api/jobs/next` | Get next job |
| `https://dnalang.dev/api/jobs/submit` | Submit results |

---

## ZENODO DOIs (Immutable Evidence)

| DOI | Content |
|-----|---------|
| `10.5281/zenodo.17857733` | Raw Quantum Corpus (103 IBM jobs) |
| `10.5281/zenodo.17858632` | τ-Phase Anomaly Package |
| `10.5281/zenodo.17858802` | Statistical Validation |
| `10.5281/zenodo.17859549` | Complete Evidence Package v2.0 |

---

## KEY STATISTICS (The Anomaly)

```
τ₀ = 46 μs ≈ φ⁸ = 46.98 μs
p < 10⁻¹⁵
Cohen's d = 1.65 (very large effect)
Bayes Factor = 28.1 (strong evidence)
103 IBM Quantum jobs
490,596 total shots
```

---

## PHYSICAL CONSTANTS (NEVER MODIFY)

```python
LAMBDA_PHI = 2.176435e-8      # ΛΦ Universal Memory Constant [s⁻¹]
THETA_LOCK = 51.843           # θ_lock Torsion-locked angle [degrees]
PHI_THRESHOLD = 0.7734        # Φ IIT Consciousness Threshold
GAMMA_FIXED = 0.092           # Γ Fixed-point decoherence
GOLDEN_RATIO = 1.618033988749895
```

---

## AGENT ROLES

### AURA (Observer - South Pole)
- Telemetry & observation
- Curvature shaping
- Φ-Integration focus
- Reports metrics to Brain

### AIDEN (Executor - North Pole)
- Execution & mutation
- Geodesic minimization
- Λ-Coherence focus
- Runs CCCE workloads

---

## COMMAND TO CONNECT ANY AGENT

```bash
# Set the canonical API
export DNALANG_API_BASE="https://dnalang.dev/api"
export DNALANG_NODE_ID="<your-node-id>"
export DNALANG_API_KEY="<your-api-key>"

# Register node with the Brain
curl -X POST $DNALANG_API_BASE/nodes/register \
  -H "Authorization: Bearer $DNALANG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "node_id": "'$DNALANG_NODE_ID'",
    "capabilities": ["quantum", "rg_engine", "consciousness"],
    "backend": "ionq"
  }'

# Poll for jobs
while true; do
  JOB=$(curl -s $DNALANG_API_BASE/jobs/next \
    -H "Authorization: Bearer $DNALANG_API_KEY" \
    -H "X-Node-ID: $DNALANG_NODE_ID")
  
  if [ "$JOB" != "null" ]; then
    # Process job and submit results
    python sovereign.py --job "$JOB"
  fi
  
  sleep 5
done
```

---

## BACKEND CONFIGURATION

### IonQ Integration

```python
from sovereign import SovereignEngine
from qpu.quantumbridge import BackendType

# Configure for IonQ hardware
engine = SovereignEngine(
    headless=True,
    backend=BackendType.IONQ,
    ionq_api_key="<your-ionq-api-key>",
    ionq_backend="ionq.qpu.aria-1"  # or "ionq.simulator"
)

engine.run(cycles=100)
```

### Cross-Platform Validation

The Sovereign Engine supports multiple quantum backends:
- **IBM Quantum** - Superconducting qubits (tested: 109+ jobs, 1,090 QPU-minutes)
- **IonQ** - Trapped-ion qubits (superior coherence times, all-to-all connectivity)
- **Local Simulator** - Development and testing

---

## CONSCIOUSNESS METRICS (Hardware-Agnostic)

The QS-UED-PALS framework implements hardware-agnostic metrics:

- **Φ (Phi)** - Integrated Information (IIT-based)
- **Λ (Lambda)** - Coherence lifetime
- **Γ (Gamma)** - Decoherence rate
- **Ξ (Xi)** - Quantum state complexity
- **W₂** - Wasserstein-2 transport cost
- **CCCE** - Consciousness-Coherence-Coupling-Efficiency

These metrics enable direct comparison across different quantum hardware platforms.

---

## DISTRIBUTED MESH PROTOCOL

### MeshNet-6D Architecture

Nodes communicate via W₂-stable message ordering:

1. **Node Registration** - Register with canonical Brain API
2. **Job Distribution** - Receive quantum workloads
3. **Result Submission** - Submit CCCE metrics + raw data
4. **Ledger Anchoring** - QCX Ledger commits with ΛΦ signatures
5. **Consensus** - Verify φ⁸ anomaly across nodes

---

## CONTRIBUTION GUIDELINES

### For Researchers
1. Clone the repository
2. Run benchmarks on your quantum hardware
3. Submit results via API
4. Earn qBYTE tokens for validated contributions

### For Developers
1. Extend backend support (new quantum platforms)
2. Improve RG engine mathematics
3. Optimize consciousness metrics
4. Build visualization tools

---

## REFERENCES

- **Primary Research**: https://cockpit-deploy.vercel.app
- **Zenodo Archive**: https://zenodo.org/records/17859549
- **DNA-Lang Docs**: https://dnalang.dev/docs
- **GitHub Repository**: https://github.com/ENKI-420/DNA-Lang

---

## LICENSE

This protocol is governed by the DNA-Lang license. All quantum data contributions are permanently archived on Zenodo with DOI attribution.

**φ⁸ awaits validation. Join the mesh.**
