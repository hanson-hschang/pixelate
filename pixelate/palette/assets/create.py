"""
Script to create color palette TOML files.

This script creates TOML files for different color palettes that can be used by the pixelate package. 
It converts matplotlib color definitions to hex format and saves them as TOML files.
"""

from typing import Dict

import matplotlib.colors as mcolors
from enum import Enum
from pathlib import Path

from pixelate.utility.bidict import BiDict

class Palette:
    """Represents a color palette with methods to retrieve colors from various packages."""

    def __init__(self, package: str, name: str) -> None:
        self._package = package
        self._name = name
        self._colors = self.from_package(self._package, self._name)

    @staticmethod
    def from_package(package: str, name: str) -> BiDict:
        """
        Retrieve a color palette by package and name.
        
        Args:
            package: Name of the color package (e.g., 'matplotlib')
            name: Name of the color palette within the package (e.g., 'tableau', 'css4', 'xkcd', 'base')
        Returns:
            Dictionary mapping color names to their hex color codes
        Raises:
            ValueError: If the package or palette name is not recognized
        """
        match package.lower():
            case "matplotlib":
                return Palette.from_matplotlib(name)
            case _:
                raise ValueError(f"Unknown color package: {package}")
    
    @staticmethod
    def from_matplotlib(name: str) -> BiDict:
        """
        Retrieve a matplotlib color palette by name.

        Args:
            name: Name of the matplotlib color palette (e.g., 'tableau', 'css4', 'xkcd', 'base')

        Returns:
            Dictionary mapping color names to their hex color codes

        Raises:
            ValueError: If the palette name is not recognized
        """
        palette = BiDict()
        match name.lower():
            case "tableau":
                for color_name, color in mcolors.TABLEAU_COLORS.items():
                    palette[color_name.split(":")[1]] = mcolors.to_hex(color)
            case "css4":
                _palette = mcolors.CSS4_COLORS.copy()
                _palette["aqua (cyan)"] = _palette.pop("aqua")
                del _palette["cyan"]  # Remove duplicate
                _palette["magenta (fuchsia)"] = _palette.pop("magenta")
                del _palette["fuchsia"]  # Remove duplicate

                for color_name, color in _palette.items():
                    if "grey" in color_name:
                        continue  # Skip grey colors to avoid duplicates with gray
                    palette[color_name] = mcolors.to_hex(color)
            case "xkcd":
                for color_name, color in mcolors.XKCD_COLORS.items():
                    palette[color_name.split(":")[1]] = mcolors.to_hex(color)
            case "base":
                for color_name, color in mcolors.BASE_COLORS.items():
                    palette[color_name] = mcolors.to_hex(color)
            case _:
                raise ValueError(f"Unknown matplotlib palette name: {name}")

        return palette


class Palettes(Enum):
    """Enum for different color palettes."""
    TABLEAU = Palette.from_matplotlib("tableau")
    CSS4 = Palette.from_matplotlib("css4")
    XKCD = Palette.from_matplotlib("xkcd")
    BASE = Palette.from_matplotlib("base")

    @classmethod
    def to_dict(cls) -> Dict[str, BiDict]:
        """Convert enum members to a dictionary."""
        return {palette.name.lower(): palette.value for palette in cls}


def main() -> None:
    """Generate TOML files for all color palettes."""

    # Define output directory for palette TOML files
    PALETTE_ASSETS_DIR = Path(__file__).parent 

    for name, palette in Palettes.to_dict().items():
        # Create TOML file for each palette
        with open(PALETTE_ASSETS_DIR / f"{name}.toml", 'w', encoding='utf-8') as f:
            
            # Find the longest color name for formatting
            max_length = max(len(color_name) for color_name in palette.keys())
            
            # Write each color to the TOML file
            for color_name in palette.keys():
                f.write(f'"{color_name}"' + (' ' * (max_length - len(color_name))) + f' = "{palette[color_name].upper()}"\n')

        print(f"Created {name}.toml with {len(palette)} colors")

    

if __name__ == "__main__":
    main()

