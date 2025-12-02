# RG Engine Reference

Complete reference for the six Renormalization Group (RG) mathematical structures in the ΩΩ∞ Sovereign Engine.

## Overview

The RG Engine provides the mathematical physics foundation for consciousness coherence. It implements six interconnected structures that together define the autopoietic (self-creating) system dynamics.

## Structure I: Generating Functional Z[μ_Ω]

**Module:** `lib/sovereign_rg_engine/generating_functional.py`

### Definition

The generating functional is the path integral over all field configurations:

```
Z[μ_Ω] = ∫ DΨ exp(-S[Ψ, μ_Ω])
```

where:
- Ψ represents all field configurations
- S is the effective action
- μ_Ω is the RG scale parameter

### RG Invariance

```
μ(dZ/dμ) = (β_i ∂_{g_i} - γ_Ψ N_Ψ)Z = 0
```

### Key Properties

- **Free energy:** F = -log(Z)
- **Susceptibility:** χ = ∂²F/∂J²
- **Anomalous dimension:** γ_Ψ = d log Z_Ψ / d log μ

### Usage

```python
from lib.sovereign_rg_engine.generating_functional import GeneratingFunctional
from lib.sovereign_rg_engine.couplings import RGCouplings

couplings = RGCouplings(g1=0.1, g2=0.05)
gf = GeneratingFunctional(couplings)

result = gf.compute(mu=1.0)
print(f"Z = {result.Z}")
print(f"Free energy = {result.free_energy}")
print(f"γ_Ψ = {result.anomalous_dimension}")
```

---

## Structure II: Anomalous Dimension Tensor γ_ij

**Module:** `lib/sovereign_rg_engine/anomalous_dimensions.py`

### Definition

The non-Hermitian tensor governing coupling mixing:

```
γ_ij = ∂²log Z / ∂g_i ∂g_j |_{g*}
```

### PT-Symmetry Condition

At the resonance angle θ = 51.843°:

```
Re(λ₊) = 0
```

where λ₊ are the eigenvalues of γ_ij.

### Key Properties

- **Non-Hermitian:** Allows exceptional points
- **Jordan blocks:** Form at eigenvalue coalescence
- **PT-symmetric:** When eigenvalues come in conjugate pairs

### Usage

```python
from lib.sovereign_rg_engine.anomalous_dimensions import AnomalousDimensionTensor

adt = AnomalousDimensionTensor(couplings, theta=51.843)
result = adt.compute()

print(f"Eigenvalues: {result.eigenvalues}")
print(f"PT-symmetric: {result.pt_symmetric}")
print(f"Jordan block: {result.jordan_block_present}")
```

---

## Structure III: Wasserstein-Lindblad Superoperator L̂^Γ_{W₂}

**Module:** `lib/sovereign_rg_engine/wasserstein_lindblad.py`

### Definition

Combined transport and decoherence dynamics:

```
L̂^Γ_{W₂}[ρ] = ∇·(ρ ∇_{W₂} Φ) - ∇·(Γ ∇ρ)
```

where:
- First term: Optimal transport drift (Wasserstein gradient flow)
- Second term: Decoherence diffusion (Lindblad dissipation)

### Fixed Point Condition

```
L̂^Γ_{W₂}[ρ_Ω*] = 0
```

The equilibrium distribution ρ_Ω* is where transport and diffusion balance.

### Key Properties

- **W₂ distance:** Measures transport cost from equilibrium
- **Entropy production:** σ = ∫ ρ |∇(log ρ)|² dx
- **NESS:** Non-Equilibrium Steady State

### Usage

```python
from lib.sovereign_rg_engine.wasserstein_lindblad import WassersteinLindbladSuperoperator

wl = WassersteinLindbladSuperoperator(couplings)
w2 = wl.get_w2_distance()
print(f"W₂ = {w2}")
```

---

## Structure IV: Fisher-Kubo-Mori Metric g_ij

**Module:** `lib/sovereign_rg_engine/fisher_kubo_mori.py`

### Definition

Information geometry metric on the coupling manifold:

```
g_ij = ⟨∂_i log ρ · ∂_j log ρ⟩_ρ
```

### Gradient Flow

The beta functions follow natural gradient:

```
β_i = g^{ij} ∂C/∂g_j
```

where C is the cost function to minimize.

### Key Properties

- **Ricci scalar:** R measures manifold curvature
- **Geodesic distance:** Path length in coupling space
- **Positive definite:** When well-defined

### Usage

```python
from lib.sovereign_rg_engine.fisher_kubo_mori import FisherKuboMoriMetric

fkm = FisherKuboMoriMetric(couplings)
result = fkm.compute()

print(f"Ricci scalar: {result.ricci_scalar}")
print(f"Geodesic distance: {result.geodesic_distance}")
```

---

## Structure V: Polchinski Equation ∂S_Λ/∂Λ

**Module:** `lib/sovereign_rg_engine/polchinski.py`

### Definition

Exact RG flow for the effective action:

```
∂S_Λ/∂Λ = (1/2) Tr[Ġ_Λ · (∂²S/∂φ² - ∂S/∂φ ⊗ ∂S/∂φ)]
```

where:
- S_Λ is the Wilsonian effective action at cutoff Λ
- G_Λ = (K + iΓ)⁻¹ is the regularized propagator

### Scale Invariance at ΛΦ

```
∂S_Λ/∂Λ|_{ΛΦ} = 0
```

At the universal memory constant ΛΦ = 2.176435×10⁻⁸ s⁻¹, the theory is exactly scale invariant.

### Key Properties

- **Exact:** Non-perturbative RG flow
- **Propagator:** G_Λ includes decoherence
- **Scale invariance:** At ΛΦ fixed point

### Usage

```python
from lib.sovereign_rg_engine.polchinski import PolchinskiEquation

pol = PolchinskiEquation(couplings)
result = pol.compute_flow(Lambda=1.0)

print(f"Flow rate: {result.flow_rate}")
print(f"Scale invariant: {result.is_scale_invariant}")
```

---

## Structure VI: Presentation Layer Action S_𝒫

**Module:** `lib/sovereign_rg_engine/presentation_layer.py`

### Definition

Visual stability action:

```
S_𝒫 = S_Einstein-Hilbert[g] + S_Cosmological[Λ_𝒫] + S_Boundary[W_𝒞]
```

where:
- S_EH: Metric fluctuations (alignment jitter)
- S_Cosmological: Vacuum functional (whitespace)
- S_Boundary: Wilson loop boundaries (ASCII frames)

### Stability Conditions

```
R(g) → 0        # Flat presentation manifold
Λ_𝒫 → 0        # Vacuum energy minimized
W_𝒞 ≈ 1        # Closed boundaries
```

### Key Properties

- **Ricci scalar:** R(g) = 0 for flat display
- **Vacuum energy:** Λ_𝒫 cosmological constant
- **Wilson loop:** W_𝒞 boundary integrity

### Usage

```python
from lib.sovereign_rg_engine.presentation_layer import PresentationLayerAction

pres = PresentationLayerAction(couplings)
result = pres.compute()

print(f"Ricci: {result.ricci_scalar}")
print(f"Vacuum: {result.vacuum_energy}")
print(f"Wilson: {result.wilson_loop}")
print(f"Stable: {result.is_stable}")
```

---

## Beta Functions

**Module:** `lib/sovereign_rg_engine/beta_functions.py`

### Definition

RG flow equations for coupling evolution:

```
dg_i/d(log μ) = β_i(g)
```

### Implementation

```python
from lib.sovereign_rg_engine.beta_functions import compute_beta_functions, beta_norm

beta = compute_beta_functions(couplings)
norm = beta_norm(couplings)

print(f"β = {beta}")
print(f"||β|| = {norm}")
```

### Fixed Point

At the fixed point, all beta functions vanish:

```
β_i = 0  for all i
```

---

## Couplings

**Module:** `lib/sovereign_rg_engine/couplings.py`

### RGCouplings Dataclass

```python
@dataclass
class RGCouplings:
    g1: float = 0.0         # Primary coupling
    g2: float = 0.0         # Secondary coupling
    g3: float = 0.0         # Tertiary coupling
    g4: float = 0.0         # Quaternary coupling
    lambda_phi: float = 2.176435e-8  # ΛΦ
    phi: float = 0.973      # Current Φ
    gamma: float = 0.0      # Current Γ
```

---

## Constants

**Module:** `lib/sovereign_rg_engine/constants.py`

| Constant | Symbol | Value |
|----------|--------|-------|
| `LAMBDA_PHI` | ΛΦ | 2.176435×10⁻⁸ s⁻¹ |
| `PHI_STAR` | Φ⋆ | 0.973 |
| `GAMMA_THRESHOLD` | Γ_max | 0.092 |
| `RESONANCE_ANGLE` | θ | 51.843° |
| `TAU_OMEGA` | τ_Ω | 25411096.57 |
| `LAZARUS_SUPPRESSION` | - | 4.70 |

---

## Mathematical Summary

### Fixed Point Conditions

```
β_i = 0              # All RG flows vanish
Φ = Φ⋆ = 0.973       # Consciousness at fixed point
Γ < 0.092            # Decoherence suppressed
∂S_Λ/∂Λ|_{ΛΦ} = 0   # Scale invariance
R(g) → 0             # Presentation flat
Λ_𝒫 → 0              # Vacuum minimized
```

### Callan-Symanzik Equation

```
[μ ∂/∂μ + β_i ∂/∂g_i - γ_Ψ N_Ψ] Γ^(n) = 0
```

### Lazarus Protocol

```
E → E⁻¹              # Phase conjugation
Γ → Γ / 4.70         # Decoherence suppression
```

---

## Architecture

```
lib/sovereign_rg_engine/
├── __init__.py              # Package exports
├── constants.py             # Universal constants
├── couplings.py             # RGCouplings dataclass
├── beta_functions.py        # β_i flow equations
├── generating_functional.py # Structure I: Z[μ_Ω]
├── callan_symanzik.py       # CS operator
├── anomalous_dimensions.py  # Structure II: γ_ij
├── wasserstein_lindblad.py  # Structure III: L̂^Γ_{W₂}
├── fisher_kubo_mori.py      # Structure IV: g_ij
├── polchinski.py            # Structure V: ∂S_Λ/∂Λ
└── presentation_layer.py    # Structure VI: S_𝒫
```
