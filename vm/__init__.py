"""
VM Package for ΩΩ∞ Sovereign Engine

Provides the Z3braVM bytecode interpreter for executing
compiled DNA-Lang programs.
"""

from .z3bravm import Z3braVM, VMState

__all__ = [
    "Z3braVM",
    "VMState",
]
