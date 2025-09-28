"""
Color palette definitions and utilities for the pixelate package.
"""

from typing import Dict

# Tableau color palette (based on Tableau's default color scheme)
TABLEAU_COLORS: Dict[str, str] = {
    "blue": "#1F77B4",
    "orange": "#FF7F0E", 
    "green": "#2CA02C",
    "red": "#D62728",
    "purple": "#9467BD",
    "brown": "#8C564B",
    "pink": "#E377C2",
    "gray": "#7F7F7F",
    "olive": "#BCBD22",
    "cyan": "#17BECF",
}

# XKCD color survey colors (subset of most common/useful colors)
XKCD_COLORS: Dict[str, str] = {
    "red": "#E50000",
    "green": "#15B01A",
    "blue": "#0343DF",
    "yellow": "#FFFF14",
    "orange": "#F97306",
    "purple": "#7E1E9C",
    "pink": "#FF81C0",
    "brown": "#653700",
    "black": "#000000",
    "white": "#FFFFFF",
    "gray": "#929591",
    "grey": "#929591",
    "cyan": "#00FFFF",
    "magenta": "#C20078",
    "lime": "#AAFF32",
    "navy": "#01153E",
    "maroon": "#650021",
    "teal": "#029386",
    "olive": "#6E750E",
    "drab": "#828344",
    "tan": "#D1B26F",
    "beige": "#E6DAA6",
    "coral": "#FC5A50",
    "salmon": "#FF796C",
    "gold": "#FFD700",
    "silver": "#C5C9C7",
    "indigo": "#380282",
    "violet": "#9A0EEA",
    "turquoise": "#06C2AC",
    "crimson": "#8C000F",
    "scarlet": "#BE0119",
    "azure": "#069AF3",
}


def resolve_color(color_value: str) -> str:
    """
    Resolve a color value to a hex color code.
    
    Supports the following formats:
    - Hex colors: "#FF0000", "#FF000080" (with or without #)
    - Tableau colors: "tableau:blue", "tableau:red"
    - XKCD colors: "xkcd:drab", "xkcd:navy"
    
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
        palette, color_name = color_value.split(":", 1)
        palette = palette.lower()
        color_name = color_name.lower()
        
        if palette == "tableau":
            if color_name not in TABLEAU_COLORS:
                available = ", ".join(sorted(TABLEAU_COLORS.keys()))
                raise ValueError(f"Unknown tableau color '{color_name}'. Available colors: {available}")
            return TABLEAU_COLORS[color_name]
        
        elif palette == "xkcd":
            if color_name not in XKCD_COLORS:
                available = ", ".join(sorted(XKCD_COLORS.keys()))
                raise ValueError(f"Unknown xkcd color '{color_name}'. Available colors: {available}")
            return XKCD_COLORS[color_name]
        
        else:
            raise ValueError(f"Unknown color palette '{palette}'. Supported palettes: tableau, xkcd")
    
    # If we get here, the format is not recognized
    raise ValueError(f"Unrecognized color format: {color_value}. Supported formats: hex (#FF0000), tableau:blue, xkcd:red")