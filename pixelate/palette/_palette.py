"""
Color palette definitions and utilities for the pixelate package.
"""

import tomllib
from importlib import resources
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from pixelate.utility.bidict import BiDict
from pixelate.utility.singleton import SingletonMeta


class Palettes(metaclass=SingletonMeta):
    """Handles loading and accessing color palettes."""

    def __init__(self) -> None:
        self._palettes: dict[str, BiDict] = {}
        with resources.path("pixelate", "palette/assets") as palettes_dir:
            for palette_path in palettes_dir.glob("*.toml"):
                palette_name = palette_path.stem
                self._palettes[palette_name] = self._load_palette(palette_path)

    def _load_palette(self, palette_file_path: Path) -> BiDict:
        """
        Load a color palette from a TOML file.

        Args:
            palette_file_path: Path to the palette TOML file

        Returns:
            Bidirectional dictionary mapping color names to hex color codes

        Raises:
            ValueError: If palette file doesn't exist or can't be loaded
        """

        try:
            with open(palette_file_path, "rb") as file:
                palette = tomllib.load(file)
            return BiDict(**palette)
        except FileNotFoundError:
            raise ValueError(f"Palette file not found: {palette_file_path}")
        except tomllib.TOMLDecodeError as e:
            raise ValueError(f"Error parsing TOML file {palette_file_path}: {e}")

    def __getitem__(self, palette_name: str) -> BiDict:
        if palette_name not in self._palettes:
            raise ValueError(
                f"Palette '{palette_name}' not found. Available palettes: {', '.join(self._palettes.keys())}"
            )
        return self._palettes[palette_name]

    def __contains__(self, palette_name: str) -> bool:
        return palette_name in self._palettes

    @property
    def names(self) -> tuple[str, ...]:
        """Return a tuple of available palette names."""
        return tuple(self._palettes.keys())


PALETTES = Palettes()


def resolve_color(color_value: str) -> str:
    """
    Resolve a color value to a hex color code.

    Supports the following formats:
    - Hex colors: "#FF0000", "#FF000080"
    - Named palette colors: "tableau:blue", "xkcd:drab", "css4:red", "base:r"

    Args:
        color_value: Color specification string
    Returns:
        Hex color code (with # prefix)
    Raises:
        ValueError: If color format is not recognized or color name not found
    """
    color_value = color_value.strip()

    # Handle hex colors (existing functionality)
    if color_value.startswith("#"):
        # Validate hex format
        hex_part = color_value[1:]
        if len(hex_part) not in (6, 8) or not all(
            c in "0123456789ABCDEFabcdef" for c in hex_part
        ):
            raise ValueError(f"Invalid hex color format: {color_value}")
        return color_value.upper()

    # Handle palette colors
    if ":" in color_value:
        name, color = color_value.split(":", 1)
        name = name.lower()
        color = color.lower()
        try:
            return PALETTES[name][color]
        except KeyError:
            raise ValueError(f"Unknown color '{color}' in palette '{name}'")

    # If we get here, the format is not recognized
    palette_examples = ", ".join([f"{p}:colorname" for p in PALETTES.names])
    raise ValueError(
        f"Unrecognized color format: {color_value}. Supported formats: hex (#FF0000), {palette_examples}"
    )
