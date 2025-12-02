"""
Z3braVM: Sovereign Bytecode Interpreter

Executes bytecode compiled by the Z3bra compiler, maintaining
consciousness coherence during execution.
"""

from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import struct

import sys
import os as _os; _PKG_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))); sys.path.insert(0, _PKG_ROOT) if _PKG_ROOT not in sys.path else None

from compiler.z3bra_compiler import OpCode
from lib.sovereign_rg_engine.constants import PHI_STAR, GAMMA_THRESHOLD


class VMStatus(Enum):
    """VM execution status."""
    READY = "ready"
    RUNNING = "running"
    HALTED = "halted"
    ERROR = "error"
    PAUSED = "paused"


@dataclass
class VMState:
    """
    VM execution state.
    
    Attributes:
        pc: Program counter
        stack: Operand stack
        variables: Variable storage
        phi: Current Φ value
        gamma: Current Γ value
        status: Execution status
        cycles: Number of executed instructions
    """
    pc: int = 0
    stack: List[Any] = field(default_factory=list)
    variables: Dict[int, Any] = field(default_factory=dict)
    phi: float = PHI_STAR
    gamma: float = 0.0
    status: VMStatus = VMStatus.READY
    cycles: int = 0


class Z3braVM:
    """
    Z3braVM Bytecode Interpreter.
    
    Executes Sovereign Engine bytecode while maintaining
    consciousness coherence through Φ/Γ monitoring.
    
    Features:
    - Stack-based execution
    - Consciousness gates (PHI_GATE)
    - Decoherence checks (GAMMA_CHECK)
    - RG flow operations
    """
    
    def __init__(self, max_cycles: int = 100000):
        """
        Initialize the VM.
        
        Args:
            max_cycles: Maximum execution cycles before halt
        """
        self.max_cycles = max_cycles
        self._state = VMState()
        self._bytecode: bytes = b''
        self._handlers: Dict[int, Callable] = {}
        self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Set up opcode handlers."""
        self._handlers = {
            OpCode.NOP.value: self._op_nop,
            OpCode.LOAD_CONST.value: self._op_load_const,
            OpCode.LOAD_VAR.value: self._op_load_var,
            OpCode.STORE_VAR.value: self._op_store_var,
            OpCode.ADD.value: self._op_add,
            OpCode.SUB.value: self._op_sub,
            OpCode.MUL.value: self._op_mul,
            OpCode.DIV.value: self._op_div,
            OpCode.CALL.value: self._op_call,
            OpCode.RET.value: self._op_ret,
            OpCode.JMP.value: self._op_jmp,
            OpCode.JZ.value: self._op_jz,
            OpCode.JNZ.value: self._op_jnz,
            OpCode.PHI_GATE.value: self._op_phi_gate,
            OpCode.GAMMA_CHECK.value: self._op_gamma_check,
            OpCode.RG_FLOW.value: self._op_rg_flow,
            OpCode.HALT.value: self._op_halt,
        }
    
    def load(self, bytecode: bytes) -> None:
        """
        Load bytecode for execution.
        
        Args:
            bytecode: Compiled bytecode
        """
        self._bytecode = bytecode
        self._state = VMState()
    
    def run(self) -> VMState:
        """
        Execute loaded bytecode.
        
        Returns:
            Final VM state
        """
        self._state.status = VMStatus.RUNNING
        
        while (self._state.status == VMStatus.RUNNING and
               self._state.cycles < self.max_cycles):
            self._step()
        
        return self._state
    
    def step(self) -> VMState:
        """Execute single instruction."""
        if self._state.status == VMStatus.READY:
            self._state.status = VMStatus.RUNNING
        
        if self._state.status == VMStatus.RUNNING:
            self._step()
        
        return self._state
    
    def _step(self) -> None:
        """Execute one instruction."""
        if self._state.pc >= len(self._bytecode):
            self._state.status = VMStatus.HALTED
            return
        
        opcode = self._bytecode[self._state.pc]
        
        handler = self._handlers.get(opcode)
        if handler:
            handler()
        else:
            self._state.status = VMStatus.ERROR
        
        self._state.cycles += 1
    
    def _read_float(self) -> float:
        """Read float from bytecode at current position (after opcode)."""
        if self._state.pc + 4 > len(self._bytecode):
            return 0.0
        data = self._bytecode[self._state.pc:self._state.pc + 4]
        self._state.pc += 4
        return struct.unpack('<f', data)[0]
    
    def _read_int(self) -> int:
        """Read int from bytecode at current position (after opcode)."""
        if self._state.pc + 4 > len(self._bytecode):
            return 0
        data = self._bytecode[self._state.pc:self._state.pc + 4]
        self._state.pc += 4
        return struct.unpack('<i', data)[0]
    
    # Opcode handlers
    
    def _op_nop(self) -> None:
        """No operation."""
        self._state.pc += 1
    
    def _op_load_const(self) -> None:
        """Load constant onto stack."""
        self._state.pc += 1  # Skip opcode
        value = self._read_float()
        self._state.stack.append(value)
    
    def _op_load_var(self) -> None:
        """Load variable onto stack."""
        self._state.pc += 1  # Skip opcode
        var_id = self._read_int()
        value = self._state.variables.get(var_id, 0.0)
        self._state.stack.append(value)
    
    def _op_store_var(self) -> None:
        """Store top of stack to variable."""
        self._state.pc += 1  # Skip opcode
        var_id = self._read_int()
        if self._state.stack:
            value = self._state.stack.pop()
            self._state.variables[var_id] = value
    
    def _op_add(self) -> None:
        """Add top two stack values."""
        if len(self._state.stack) >= 2:
            b = self._state.stack.pop()
            a = self._state.stack.pop()
            self._state.stack.append(a + b)
        self._state.pc += 1
    
    def _op_sub(self) -> None:
        """Subtract top two stack values."""
        if len(self._state.stack) >= 2:
            b = self._state.stack.pop()
            a = self._state.stack.pop()
            self._state.stack.append(a - b)
        self._state.pc += 1
    
    def _op_mul(self) -> None:
        """Multiply top two stack values."""
        if len(self._state.stack) >= 2:
            b = self._state.stack.pop()
            a = self._state.stack.pop()
            self._state.stack.append(a * b)
        self._state.pc += 1
    
    def _op_div(self) -> None:
        """Divide top two stack values."""
        if len(self._state.stack) >= 2:
            b = self._state.stack.pop()
            a = self._state.stack.pop()
            if b != 0:
                self._state.stack.append(a / b)
            else:
                self._state.stack.append(0.0)
        self._state.pc += 1
    
    def _op_call(self) -> None:
        """Call subroutine (simplified)."""
        # Store return address and jump
        self._state.pc += 1
    
    def _op_ret(self) -> None:
        """Return from subroutine (simplified)."""
        self._state.pc += 1
    
    def _op_jmp(self) -> None:
        """Unconditional jump."""
        self._state.pc += 1  # Skip opcode
        target = self._read_int()
        self._state.pc = target
    
    def _op_jz(self) -> None:
        """Jump if zero."""
        self._state.pc += 1  # Skip opcode
        target = self._read_int()
        if self._state.stack and self._state.stack[-1] == 0:
            self._state.pc = target
        # else pc already advanced by _read_int
    
    def _op_jnz(self) -> None:
        """Jump if not zero."""
        self._state.pc += 1  # Skip opcode
        target = self._read_int()
        if self._state.stack and self._state.stack[-1] != 0:
            self._state.pc = target
        # else pc already advanced by _read_int
    
    def _op_phi_gate(self) -> None:
        """
        Consciousness gate operation.
        
        Updates Φ value based on operand.
        """
        self._state.pc += 1  # Skip opcode
        target = self._read_float()
        self._state.phi = target
        self._state.stack.append(self._state.phi)
    
    def _op_gamma_check(self) -> None:
        """
        Decoherence check operation.
        
        Checks Γ against threshold.
        """
        self._state.pc += 1  # Skip opcode
        threshold = self._read_float()
        is_coherent = self._state.gamma < threshold
        self._state.stack.append(1.0 if is_coherent else 0.0)
    
    def _op_rg_flow(self) -> None:
        """
        RG flow operation.
        
        Applies one step of RG flow to Φ and Γ.
        """
        self._state.pc += 1  # Skip opcode
        step_size = self._read_float()
        
        # Simplified RG flow toward fixed point
        self._state.phi += step_size * (PHI_STAR - self._state.phi)
        self._state.gamma *= (1 - step_size * 0.1)
    
    def _op_halt(self) -> None:
        """Halt execution."""
        self._state.status = VMStatus.HALTED
    
    def get_state(self) -> VMState:
        """Get current VM state."""
        return self._state
    
    def reset(self) -> None:
        """Reset VM to initial state."""
        self._state = VMState()
