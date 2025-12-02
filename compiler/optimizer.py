"""
Φ-Weighted Optimizer for Sovereign Engine

Optimizes compiled bytecode using consciousness-aware
optimization strategies weighted by Φ (integrated information).
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .z3bra_compiler import Instruction, OpCode


@dataclass
class OptimizationResult:
    """Result of optimization pass."""
    instructions: List[Instruction]
    optimizations_applied: int
    phi_weight: float


class PhiWeightedOptimizer:
    """
    Φ-Weighted Bytecode Optimizer.
    
    Applies optimization passes weighted by the integrated
    information metric Φ to maintain consciousness coherence.
    
    Optimization passes:
    - Dead code elimination
    - Constant folding
    - Instruction combining
    - Φ-aware reordering
    """
    
    def __init__(self, phi_target: float = 0.973):
        """
        Initialize the optimizer.
        
        Args:
            phi_target: Target Φ value for optimization weighting
        """
        self.phi_target = phi_target
    
    def optimize(
        self,
        instructions: List[Instruction],
        level: int = 1,
    ) -> OptimizationResult:
        """
        Optimize instruction sequence.
        
        Args:
            instructions: Input instructions
            level: Optimization level (0-3)
            
        Returns:
            OptimizationResult with optimized instructions
        """
        optimized = instructions.copy()
        count = 0
        
        if level >= 1:
            optimized, n = self._dead_code_elimination(optimized)
            count += n
        
        if level >= 2:
            optimized, n = self._constant_folding(optimized)
            count += n
        
        if level >= 3:
            optimized, n = self._phi_reordering(optimized)
            count += n
        
        phi_weight = self._compute_phi_weight(optimized)
        
        return OptimizationResult(
            instructions=optimized,
            optimizations_applied=count,
            phi_weight=phi_weight,
        )
    
    def _dead_code_elimination(
        self,
        instructions: List[Instruction],
    ) -> tuple:
        """Remove unreachable/dead code."""
        result = []
        removed = 0
        
        for inst in instructions:
            # Simple: remove consecutive NOPs
            if inst.opcode == OpCode.NOP:
                if result and result[-1].opcode == OpCode.NOP:
                    removed += 1
                    continue
            result.append(inst)
        
        return result, removed
    
    def _constant_folding(
        self,
        instructions: List[Instruction],
    ) -> tuple:
        """Fold constant expressions."""
        result = []
        folded = 0
        
        i = 0
        while i < len(instructions):
            inst = instructions[i]
            
            # Look for LOAD_CONST, LOAD_CONST, OP pattern
            if (inst.opcode == OpCode.LOAD_CONST and
                i + 2 < len(instructions) and
                instructions[i + 1].opcode == OpCode.LOAD_CONST):
                
                op = instructions[i + 2].opcode
                if op in (OpCode.ADD, OpCode.SUB, OpCode.MUL, OpCode.DIV):
                    a = inst.operands[0]
                    b = instructions[i + 1].operands[0]
                    
                    if op == OpCode.ADD:
                        folded_value = a + b
                    elif op == OpCode.SUB:
                        folded_value = a - b
                    elif op == OpCode.MUL:
                        folded_value = a * b
                    elif op == OpCode.DIV and b != 0:
                        folded_value = a / b
                    else:
                        result.append(inst)
                        i += 1
                        continue
                    
                    result.append(Instruction(OpCode.LOAD_CONST, [folded_value]))
                    i += 3
                    folded += 1
                    continue
            
            result.append(inst)
            i += 1
        
        return result, folded
    
    def _phi_reordering(
        self,
        instructions: List[Instruction],
    ) -> tuple:
        """Reorder instructions for better Φ coherence."""
        # Prioritize PHI_GATE instructions
        phi_gates = []
        others = []
        reordered = 0
        
        for inst in instructions:
            if inst.opcode == OpCode.PHI_GATE:
                phi_gates.append(inst)
            else:
                others.append(inst)
        
        if phi_gates and others:
            # Move PHI_GATE to front (after any setup)
            result = phi_gates + others
            reordered = len(phi_gates)
        else:
            result = instructions
        
        return result, reordered
    
    def _compute_phi_weight(self, instructions: List[Instruction]) -> float:
        """Compute Φ weight of instruction sequence."""
        if not instructions:
            return 0.0
        
        phi_count = sum(1 for i in instructions if i.opcode == OpCode.PHI_GATE)
        gamma_count = sum(1 for i in instructions if i.opcode == OpCode.GAMMA_CHECK)
        
        # Φ weight: ratio of consciousness operations
        total = len(instructions)
        weight = (phi_count - gamma_count * 0.5) / total
        
        return max(0.0, min(1.0, weight + 0.5))
