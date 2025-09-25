"""
Pixelate - A pixel art generator from markdown files with TOML frontmatter.
"""

from typing import Final
from importlib import metadata

__version__: Final[str] = metadata.version("pixelate")