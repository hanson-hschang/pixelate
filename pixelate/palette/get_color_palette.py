import os


import matplotlib.colors as mcolors

def rgb_to_hex(rgb) -> str:
    """
    Converts RGB color values (0-255) to a hexadecimal color code string.
    """
    # Ensure values are within the valid 0-255 range
    r = int(max(0, min(255, rgb[0] * 255)))
    g = int(max(0, min(255, rgb[1] * 255)))
    b = int(max(0, min(255, rgb[2] * 255)))

    # Format each component as a two-digit uppercase hexadecimal string
    # and concatenate them
    return f"#{r:02X}{g:02X}{b:02X}"

PALETTES = {
    "tableau": mcolors.TABLEAU_COLORS,
    "css4": mcolors.CSS4_COLORS,
    "xkcd": mcolors.XKCD_COLORS,
    "base": mcolors.BASE_COLORS,
}

def get_colors(palette) -> dict[str, str]:
    """
    Retrieves a color palette by name and converts its colors to hexadecimal format.

    Args:
        name (str): The name of the palette to retrieve. Must be one of the keys in PALETTES.

    Returns:
        dict[str, str]: A dictionary mapping color names to their hexadecimal color codes.

    Raises:
        ValueError: If the specified palette name is not found in PALETTES.
    """

    return {color_name.split(":")[1] if ":" in color_name else color_name: rgb_to_hex(mcolors.to_rgb(color)) for color_name, color in palette.items()}


for name, palette in PALETTES.items():
    colors = get_colors(palette)

        
    # Create TOML file for each palette
    with open(f'{name}.toml', 'w') as f:
        for color_name, hex_code in colors.items():
            f.write(f'"{color_name}" = "{hex_code}"\n')

