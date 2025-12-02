"""
Cockpit Package for ΩΩ∞ Sovereign Engine

Provides display and rendering infrastructure:
- Display Server: ASCII framebuffer renderer
"""

from .display_server import DisplayServer, Frame

__all__ = [
    "DisplayServer",
    "Frame",
]
