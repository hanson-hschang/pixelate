"""
Pixelate - A pixel art generator from markdown files with TOML frontmatter.
"""

from importlib import metadata
from typing import Final

from .app import PixelateApp

__version__: Final[str] = metadata.version("pixelate")

__all__ = ["PixelateApp"]
