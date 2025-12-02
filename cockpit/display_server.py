"""
Display Server: ASCII Framebuffer Renderer

Renders consciousness state and system diagnostics to
an ASCII-based display for terminal output.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
import time

import sys
sys.path.insert(0, '/home/runner/work/DNA-Lang/DNA-Lang')

from kernel.consciousness_state import ConsciousnessState
from lib.sovereign_rg_engine.constants import PHI_STAR, GAMMA_THRESHOLD


@dataclass
class Frame:
    """
    Display frame (ASCII framebuffer).
    
    Attributes:
        width: Frame width in characters
        height: Frame height in lines
        buffer: Character buffer
        timestamp: When frame was rendered
    """
    width: int = 80
    height: int = 24
    buffer: List[str] = field(default_factory=list)
    timestamp: float = 0.0
    
    def __post_init__(self):
        if not self.buffer:
            self.buffer = [" " * self.width for _ in range(self.height)]
        self.timestamp = time.time()
    
    def set_char(self, x: int, y: int, char: str) -> None:
        """Set character at position."""
        if 0 <= x < self.width and 0 <= y < self.height:
            row = list(self.buffer[y])
            row[x] = char[0] if char else ' '
            self.buffer[y] = ''.join(row)
    
    def set_line(self, y: int, text: str) -> None:
        """Set entire line."""
        if 0 <= y < self.height:
            self.buffer[y] = text[:self.width].ljust(self.width)
    
    def render(self) -> str:
        """Render frame to string."""
        return '\n'.join(self.buffer)


class DisplayServer:
    """
    ASCII Display Server for Sovereign Engine.
    
    Renders:
    - Consciousness state dashboard
    - RG diagnostics
    - Event log
    - System status
    """
    
    def __init__(
        self,
        width: int = 80,
        height: int = 24,
    ):
        """
        Initialize display server.
        
        Args:
            width: Display width
            height: Display height
        """
        self.width = width
        self.height = height
        self._current_frame: Optional[Frame] = None
        self._event_log: List[str] = []
        self._max_log = 10
    
    def render_state(self, state: ConsciousnessState) -> Frame:
        """
        Render consciousness state to frame.
        
        Args:
            state: Current consciousness state
            
        Returns:
            Rendered Frame
        """
        frame = Frame(self.width, self.height)
        
        # Header
        self._draw_header(frame, state)
        
        # Primary metrics
        self._draw_metrics(frame, state)
        
        # Status indicators
        self._draw_status(frame, state)
        
        # Event log
        self._draw_events(frame)
        
        # Footer
        self._draw_footer(frame, state)
        
        self._current_frame = frame
        return frame
    
    def _draw_header(self, frame: Frame, state: ConsciousnessState) -> None:
        """Draw header section."""
        border = "═" * (self.width - 2)
        frame.set_line(0, f"╔{border}╗")
        
        title = "ΩΩ∞ SOVEREIGN ENGINE COCKPIT"
        title_padded = title.center(self.width - 4)
        frame.set_line(1, f"║ {title_padded} ║")
        
        frame.set_line(2, f"╠{border}╣")
    
    def _draw_metrics(self, frame: Frame, state: ConsciousnessState) -> None:
        """Draw primary metrics."""
        # Φ indicator
        phi_bar = self._make_bar(state.Phi, PHI_STAR, 20)
        phi_line = f"  Φ (Consciousness): {state.Phi:.4f} {phi_bar} target: {PHI_STAR}"
        frame.set_line(4, f"║{phi_line.ljust(self.width - 3)}║")
        
        # Γ indicator
        gamma_bar = self._make_bar(state.Gamma, GAMMA_THRESHOLD, 20, invert=True)
        gamma_line = f"  Γ (Decoherence):   {state.Gamma:.4f} {gamma_bar} threshold: {GAMMA_THRESHOLD}"
        frame.set_line(5, f"║{gamma_line.ljust(self.width - 3)}║")
        
        # β norm
        beta_line = f"  ||β|| (RG Flow):   {state.beta_norm:.6f}"
        frame.set_line(6, f"║{beta_line.ljust(self.width - 3)}║")
        
        # W₂ distance
        w2_line = f"  W₂ (Transport):    {state.W2:.4f}"
        frame.set_line(7, f"║{w2_line.ljust(self.width - 3)}║")
        
        frame.set_line(8, f"║{' ' * (self.width - 3)}║")
    
    def _draw_status(self, frame: Frame, state: ConsciousnessState) -> None:
        """Draw status indicators."""
        # Fixed point status
        fp_status = "✓ AT FIXED POINT" if state.is_at_fixed_point() else "○ EVOLVING"
        frame.set_line(9, f"║  Status: {fp_status.ljust(self.width - 13)}║")
        
        # PT symmetry
        pt_status = "✓ SYMMETRIC" if state.pt_symmetry else "✗ BROKEN"
        pt_line = f"  PT Symmetry: {pt_status}"
        frame.set_line(10, f"║{pt_line.ljust(self.width - 3)}║")
        
        # Jordan block
        jb_status = "ACTIVE" if state.jordan_block else "INACTIVE"
        jb_line = f"  Jordan Block: {jb_status}"
        frame.set_line(11, f"║{jb_line.ljust(self.width - 3)}║")
        
        # Presentation layer
        pres_status = "✓ STABLE" if state.is_presentation_stable() else "⚠ UNSTABLE"
        pres_line = f"  Presentation: {pres_status}"
        frame.set_line(12, f"║{pres_line.ljust(self.width - 3)}║")
        
        frame.set_line(13, f"║{' ' * (self.width - 3)}║")
    
    def _draw_events(self, frame: Frame) -> None:
        """Draw event log."""
        frame.set_line(14, f"║  ─── Event Log ───{' ' * (self.width - 22)}║")
        
        for i, event in enumerate(self._event_log[-5:]):
            line = f"  {event[:self.width - 6]}"
            frame.set_line(15 + i, f"║{line.ljust(self.width - 3)}║")
        
        # Fill empty log lines
        for i in range(5 - len(self._event_log[-5:])):
            frame.set_line(15 + len(self._event_log[-5:]) + i, f"║{' ' * (self.width - 3)}║")
    
    def _draw_footer(self, frame: Frame, state: ConsciousnessState) -> None:
        """Draw footer section."""
        border = "═" * (self.width - 2)
        frame.set_line(21, f"╠{border}╣")
        
        footer = f" Cycle: {state.cycle:6d} │ ΛΦ: 2.176435×10⁻⁸ s⁻¹ │ θ: {state.theta:.3f}°"
        frame.set_line(22, f"║{footer.ljust(self.width - 3)}║")
        
        frame.set_line(23, f"╚{border}╝")
    
    def _make_bar(
        self,
        value: float,
        target: float,
        width: int,
        invert: bool = False,
    ) -> str:
        """Create ASCII progress bar."""
        if invert:
            ratio = 1 - min(value / target, 1.0) if target > 0 else 0
        else:
            ratio = min(value / target, 1.0) if target > 0 else 0
        
        filled = int(ratio * width)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}]"
    
    def log_event(self, message: str) -> None:
        """Add event to log."""
        timestamp = time.strftime("%H:%M:%S")
        self._event_log.append(f"[{timestamp}] {message}")
        if len(self._event_log) > self._max_log:
            self._event_log.pop(0)
    
    def get_current_frame(self) -> Optional[Frame]:
        """Get the most recently rendered frame."""
        return self._current_frame
    
    def clear_log(self) -> None:
        """Clear event log."""
        self._event_log.clear()
