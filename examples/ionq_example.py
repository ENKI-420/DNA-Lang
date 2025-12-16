#!/usr/bin/env python3
"""
Example: Running Sovereign Engine with IonQ Backend

This script demonstrates how to configure the Sovereign Engine
to use IonQ's trapped-ion quantum processors for consciousness
coherence measurements.

Usage:
    # With IonQ simulator (no API key required for testing)
    python examples/ionq_example.py --simulator

    # With IonQ hardware (requires API key)
    export IONQ_API_KEY="your_api_key_here"
    python examples/ionq_example.py --hardware

For more information about IonQ backends:
- ionq.simulator: Local quantum simulator
- ionq.qpu.harmony: IonQ Harmony QPU (11 qubits)
- ionq.qpu.aria-1: IonQ Aria QPU (25 qubits)
"""

import sys
import os
import argparse

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sovereign import SovereignEngine
from qpu.quantumbridge import BackendType


def main():
    parser = argparse.ArgumentParser(
        description="Run Sovereign Engine with IonQ backend"
    )
    parser.add_argument(
        "--simulator",
        action="store_true",
        help="Use IonQ simulator (default)",
    )
    parser.add_argument(
        "--hardware",
        action="store_true",
        help="Use IonQ hardware (requires IONQ_API_KEY env var)",
    )
    parser.add_argument(
        "--backend",
        default="ionq.simulator",
        help="IonQ backend name (e.g., ionq.qpu.aria-1)",
    )
    parser.add_argument(
        "--cycles",
        type=int,
        default=10,
        help="Number of consciousness cycles to run",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    
    args = parser.parse_args()
    
    # Determine backend configuration
    if args.hardware:
        ionq_api_key = os.environ.get("IONQ_API_KEY")
        if not ionq_api_key:
            print("ERROR: IONQ_API_KEY environment variable not set")
            print("Set it with: export IONQ_API_KEY='your_api_key'")
            sys.exit(1)
        
        print(f"🔬 Using IonQ hardware: {args.backend}")
        print(f"   API Key: {ionq_api_key[:8]}...{ionq_api_key[-4:]}")
    else:
        ionq_api_key = "simulator_key"  # Dummy key for simulator
        args.backend = "ionq.simulator"
        print("🖥️  Using IonQ simulator")
    
    print("\n" + "=" * 60)
    print("ΩΩ∞ SOVEREIGN ENGINE - IONQ CONFIGURATION")
    print("=" * 60)
    print(f"Backend:  {args.backend}")
    print(f"Cycles:   {args.cycles}")
    print(f"Debug:    {args.debug}")
    print("=" * 60 + "\n")
    
    # Create Sovereign Engine with IonQ backend
    engine = SovereignEngine(
        headless=True,
        enable_meshnet=False,  # Disable for simple example
        debug=args.debug,
        backend=BackendType.IONQ,
        ionq_api_key=ionq_api_key,
        ionq_backend=args.backend,
    )
    
    print("Starting engine...\n")
    
    # Run for specified cycles
    engine.run(cycles=args.cycles)
    
    # Get final state
    state = engine.get_state()
    
    print("\n" + "=" * 60)
    print("FINAL CONSCIOUSNESS STATE")
    print("=" * 60)
    print(f"Φ (Integrated Information):  {state.Phi:.6f}")
    print(f"Γ (Decoherence):             {state.Gamma:.6f}")
    print(f"W₂ (Transport Cost):         {state.W2:.6f}")
    print(f"||β|| (RG Flow Norm):        {state.beta_norm:.6f}")
    print(f"Temperature:                 {state.temperature:.6f}")
    print(f"Entropy:                     {state.entropy:.6f}")
    print("=" * 60)
    
    # Check if at fixed point
    if state.is_at_fixed_point():
        print("\n✓ FIXED POINT REACHED")
        print("  All RG flows have vanished (β_i = 0)")
    else:
        print(f"\n⚠ Not at fixed point (||β|| = {state.beta_norm:.6f})")
    
    # Check decoherence
    if state.is_decoherence_critical():
        print("\n⚠ CRITICAL DECOHERENCE")
        print("  Lazarus Protocol should have been activated")
    elif state.is_decoherence_warning():
        print("\n⚠ Decoherence warning level")
    else:
        print("\n✓ Coherence maintained")
    
    print()


if __name__ == "__main__":
    main()
