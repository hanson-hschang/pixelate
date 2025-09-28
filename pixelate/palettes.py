"""
Color palette definitions and utilities for the pixelate package.
"""

import toml
from pathlib import Path
from typing import Dict, List, Optional

# Path to the palette directory
_PALETTE_DIR = Path(__file__).parent / "palette"

# Cache for loaded palettes to avoid repeated file I/O
_palette_cache: Dict[str, Dict[str, str]] = {}


def _load_palette(palette_name: str) -> Dict[str, str]:
    """
    Load a color palette from a TOML file.
    
    Args:
        palette_name: Name of the palette (corresponds to filename without .toml)
        
    Returns:
        Dictionary mapping color names to hex color codes
        
    Raises:
        ValueError: If palette file doesn't exist or can't be loaded
    """
    if palette_name in _palette_cache:
        return _palette_cache[palette_name]
    
    palette_file = _PALETTE_DIR / f"{palette_name}.toml"
    
    if not palette_file.exists():
        available_palettes = [f.stem for f in _PALETTE_DIR.glob("*.toml")]
        raise ValueError(f"Palette '{palette_name}' not found. Available palettes: {', '.join(sorted(available_palettes))}")
    
    try:
        with open(palette_file, "r", encoding="utf-8") as f:
            palette_data = toml.load(f)
        _palette_cache[palette_name] = palette_data
        return palette_data
    except Exception as e:
        raise ValueError(f"Error loading palette '{palette_name}': {e}")


def get_available_palettes() -> List[str]:
    """
    Get list of available color palettes.
    
    Returns:
        List of available palette names
    """
    if not _PALETTE_DIR.exists():
        return []
    
    return sorted([f.stem for f in _PALETTE_DIR.glob("*.toml")])


def resolve_color(color_value: str) -> str:
    """
    Resolve a color value to a hex color code.
    
    Supports the following formats:
    - Hex colors: "#FF0000", "#FF000080" (with or without #)
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
    if color_value.startswith("#") or (len(color_value) in [6, 8] and all(c in "0123456789ABCDEFabcdef" for c in color_value)):
        if not color_value.startswith("#"):
            color_value = "#" + color_value
        # Validate hex format
        hex_part = color_value[1:]
        if len(hex_part) not in [6, 8] or not all(c in "0123456789ABCDEFabcdef" for c in hex_part):
            raise ValueError(f"Invalid hex color format: {color_value}")
        return color_value
    
    # Handle palette colors
    if ":" in color_value:
        palette_name, color_name = color_value.split(":", 1)
        palette_name = palette_name.lower()
        color_name = color_name.lower()
        
        try:
            palette = _load_palette(palette_name)
        except ValueError as e:
            raise ValueError(str(e))
        
        if color_name not in palette:
            available = ", ".join(sorted(palette.keys())[:10])  # Show first 10 for readability
            more_count = len(palette) - 10
            if more_count > 0:
                available += f" (and {more_count} more)"
            raise ValueError(f"Unknown {palette_name} color '{color_name}'. Available colors: {available}")
        
        return palette[color_name]
    
    # If we get here, the format is not recognized
    available_palettes = get_available_palettes()
    palette_examples = ", ".join([f"{p}:colorname" for p in available_palettes[:3]])
    raise ValueError(f"Unrecognized color format: {color_value}. Supported formats: hex (#FF0000), {palette_examples}")