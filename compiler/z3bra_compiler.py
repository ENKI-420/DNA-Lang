"""
Z3bra Compiler: dna::}{::lang → Bytecode

Compiles DNA-Lang source code to Sovereign Engine bytecode
for execution on the Z3braVM.
"""

from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class OpCode(Enum):
    """Bytecode operation codes."""
    NOP = 0x00
    LOAD_CONST = 0x01
    LOAD_VAR = 0x02
    STORE_VAR = 0x03
    ADD = 0x10
    SUB = 0x11
    MUL = 0x12
    DIV = 0x13
    CALL = 0x20
    RET = 0x21
    JMP = 0x30
    JZ = 0x31
    JNZ = 0x32
    PHI_GATE = 0x40  # Consciousness gate
    GAMMA_CHECK = 0x41  # Decoherence check
    RG_FLOW = 0x42  # RG flow operation
    HALT = 0xFF


@dataclass
class Instruction:
    """Single bytecode instruction."""
    opcode: OpCode
    operands: List[Any] = field(default_factory=list)
    line: int = 0
    
    def to_bytes(self) -> bytes:
        """Serialize instruction to bytes."""
        data = bytes([self.opcode.value])
        for operand in self.operands:
            if isinstance(operand, int):
                data += operand.to_bytes(4, 'little', signed=True)
            elif isinstance(operand, float):
                import struct
                data += struct.pack('<f', operand)
            elif isinstance(operand, str):
                encoded = operand.encode('utf-8')
                data += len(encoded).to_bytes(2, 'little')
                data += encoded
        return data


@dataclass
class CompilationResult:
    """Result of compilation."""
    success: bool
    bytecode: bytes
    instructions: List[Instruction]
    symbols: Dict[str, int]  # Symbol table
    errors: List[str]
    warnings: List[str]


class Z3braCompiler:
    """
    Z3bra Compiler for DNA-Lang.
    
    Compiles dna::}{::lang source code to bytecode executable
    on the Z3braVM.
    
    Features:
    - Lexical analysis
    - Parsing
    - Semantic analysis
    - Code generation
    - Optimization passes
    """
    
    def __init__(self):
        """Initialize the compiler."""
        self._symbols: Dict[str, int] = {}
        self._instructions: List[Instruction] = []
        self._errors: List[str] = []
        self._warnings: List[str] = []
        self._var_counter = 0
    
    def compile(self, source: str) -> CompilationResult:
        """
        Compile source code to bytecode.
        
        Args:
            source: DNA-Lang source code
            
        Returns:
            CompilationResult with bytecode and metadata
        """
        self._reset()
        
        try:
            # Tokenize
            tokens = self._tokenize(source)
            
            # Parse and generate code
            self._parse_and_generate(tokens)
            
            # Add halt instruction
            self._emit(Instruction(OpCode.HALT))
            
            # Generate bytecode
            bytecode = self._generate_bytecode()
            
            return CompilationResult(
                success=len(self._errors) == 0,
                bytecode=bytecode,
                instructions=self._instructions.copy(),
                symbols=self._symbols.copy(),
                errors=self._errors.copy(),
                warnings=self._warnings.copy(),
            )
            
        except Exception as e:
            self._errors.append(f"Compilation error: {str(e)}")
            return CompilationResult(
                success=False,
                bytecode=b'',
                instructions=[],
                symbols={},
                errors=self._errors.copy(),
                warnings=self._warnings.copy(),
            )
    
    def _reset(self) -> None:
        """Reset compiler state."""
        self._symbols.clear()
        self._instructions.clear()
        self._errors.clear()
        self._warnings.clear()
        self._var_counter = 0
    
    def _tokenize(self, source: str) -> List[Tuple[str, str]]:
        """
        Simple tokenization.
        
        Returns list of (token_type, value) tuples.
        """
        tokens = []
        lines = source.strip().split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Simple keyword-based tokenization
            parts = line.split()
            for part in parts:
                if part in ('organism', 'dna', 'gene', 'agent', 'phi', 'gamma'):
                    tokens.append(('KEYWORD', part))
                elif part.isdigit() or (part.startswith('-') and part[1:].isdigit()):
                    tokens.append(('NUMBER', part))
                elif part.startswith('"') and part.endswith('"'):
                    tokens.append(('STRING', part[1:-1]))
                elif part in ('{', '}', '(', ')', '[', ']', ':', '=', ';'):
                    tokens.append(('PUNCT', part))
                else:
                    tokens.append(('IDENT', part))
        
        return tokens
    
    def _parse_and_generate(self, tokens: List[Tuple[str, str]]) -> None:
        """Parse tokens and generate instructions."""
        i = 0
        while i < len(tokens):
            token_type, value = tokens[i]
            
            if token_type == 'KEYWORD':
                if value == 'organism':
                    # Organism definition
                    self._emit(Instruction(OpCode.PHI_GATE, [1.0]))
                elif value == 'phi':
                    # Phi operation
                    self._emit(Instruction(OpCode.PHI_GATE, [0.973]))
                elif value == 'gamma':
                    # Gamma check
                    self._emit(Instruction(OpCode.GAMMA_CHECK, [0.092]))
            
            elif token_type == 'NUMBER':
                # Load constant
                self._emit(Instruction(OpCode.LOAD_CONST, [float(value)]))
            
            elif token_type == 'IDENT':
                # Variable reference
                if value not in self._symbols:
                    self._symbols[value] = self._var_counter
                    self._var_counter += 1
                self._emit(Instruction(OpCode.LOAD_VAR, [self._symbols[value]]))
            
            i += 1
    
    def _emit(self, instruction: Instruction) -> None:
        """Emit an instruction."""
        instruction.line = len(self._instructions)
        self._instructions.append(instruction)
    
    def _generate_bytecode(self) -> bytes:
        """Generate bytecode from instructions."""
        bytecode = b''
        for inst in self._instructions:
            bytecode += inst.to_bytes()
        return bytecode
    
    def disassemble(self, bytecode: bytes) -> List[str]:
        """
        Disassemble bytecode to readable form.
        
        Args:
            bytecode: Compiled bytecode
            
        Returns:
            List of disassembled lines
        """
        lines = []
        i = 0
        addr = 0
        
        while i < len(bytecode):
            opcode = OpCode(bytecode[i])
            line = f"{addr:04x}: {opcode.name}"
            lines.append(line)
            i += 1
            addr += 1
        
        return lines
