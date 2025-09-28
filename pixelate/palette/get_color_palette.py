"""
Script to generate color palette TOML files from matplotlib color definitions.

This script creates TOML files for different color palettes that can be used
by the pixelate package. It converts matplotlib color definitions to hex format
and saves them as TOML files.
"""

from typing import Dict

import matplotlib.colors as mcolors


def rgb_to_hex(rgb) -> str:
    """
    Convert RGB color values (0-1) to a hexadecimal color code string.
    
    Args:
        rgb: RGB color values as tuple (r, g, b) where values are 0-1
        
    Returns:
        Hexadecimal color code string with # prefix
    """
    # Ensure values are within the valid 0-255 range
    r = int(max(0, min(255, rgb[0] * 255)))
    g = int(max(0, min(255, rgb[1] * 255)))
    b = int(max(0, min(255, rgb[2] * 255)))

    # Format each component as a two-digit uppercase hexadecimal string
    return f"#{r:02X}{g:02X}{b:02X}"


PALETTES: Dict[str, Dict[str, str]] = {
    "tableau": mcolors.TABLEAU_COLORS,
    "css4": mcolors.CSS4_COLORS,
    "xkcd": mcolors.XKCD_COLORS,
    "base": mcolors.BASE_COLORS,
}


def get_colors(palette: Dict[str, str]) -> Dict[str, str]:
    """
    Retrieve a color palette and convert its colors to hexadecimal format.

    Args:
        palette: Dictionary mapping color names to color definitions

    Returns:
        Dictionary mapping color names to their hexadecimal color codes
    """
    return {
        color_name.split(":")[1] if ":" in color_name else color_name: rgb_to_hex(mcolors.to_rgb(color))
        for color_name, color in palette.items()
    }


def main() -> None:
    """Generate TOML files for all color palettes."""
    for name, palette in PALETTES.items():
        colors = get_colors(palette)

        # Create TOML file for each palette
        with open(f'{name}.toml', 'w', encoding='utf-8') as f:
            for color_name, hex_code in colors.items():
                f.write(f'"{color_name}" = "{hex_code}"\n')
        
        print(f"Generated {name}.toml with {len(colors)} colors")


if __name__ == "__main__":
    main()

