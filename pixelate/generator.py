"""
Handles generating images from pixel data.
"""

from typing import Dict, List, Tuple

from PIL import Image, ImageDraw


class ImageGenerator:
    """Handles generating images from pixel data."""

    def hex_to_rgba(self, hex_color: str) -> Tuple[int, int, int, int]:
        """Convert hex color string to RGBA tuple.

        Args:
            hex_color: Hex color string (e.g. "#RRGGBB" or "#RRGGBBAA")
        Returns:
            Tuple of (R, G, B, A) where each is an integer 0-255
        Raises:
            ValueError: If the hex color format is invalid
        """
        hex_color = hex_color.lstrip("#")

        if len(hex_color) == 6:
            # RGB format: #RRGGBB
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            a = 255  # Fully opaque
        elif len(hex_color) == 8:
            # RGBA format: #RRGGBBAA
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            a = int(hex_color[6:8], 16)
        else:
            raise ValueError(f"Invalid hex color format: {hex_color}")

        return (r, g, b, a)

    def generate(
        self,
        color_dict: Dict[str, str],
        pixel_grid: List[List[str]],
        pixel_size: int,
    ) -> Image.Image:
        """
        Generate an image from the pixel grid and color dictionary.

        Args:
            color_dict: Mapping of number strings to hex colors
            pixel_grid: 2D list representing the pixel art
            pixel_size: Size of each pixel in the output image (in pixels)
        Returns:
            The generated PIL Image object
        """
        if (not pixel_grid) or (not pixel_grid[0]):
            raise ValueError("Pixel grid is empty")

        total_rows = len(pixel_grid)
        total_cols = len(pixel_grid[0])

        # Create image with RGBA mode for transparency support
        img_width = total_cols * pixel_size
        img_height = total_rows * pixel_size
        image = Image.new(
            "RGBA", (img_width, img_height), (255, 255, 255, 0)
        )  # Transparent background
        draw = ImageDraw.Draw(image)

        for row_idx, row in enumerate(pixel_grid):
            for col_idx, cell_value in enumerate(row):
                cell_value = cell_value.strip()
                # Get color from dictionary
                if cell_value in color_dict:
                    hex_color: str = color_dict[cell_value]
                    try:
                        rgba_color: Tuple[int, int, int, int] = self.hex_to_rgba(
                            hex_color
                        )
                    except ValueError as e:
                        print(f"Warning: {e}, skipping cell at ({row_idx}, {col_idx})")
                        continue
                else:
                    print(
                        f"Warning: Color not found for value '{cell_value}', "
                        f"skipping cell at ({row_idx}, {col_idx})"
                    )
                    continue

                # Draw pixel
                x1: int = col_idx * pixel_size
                y1: int = row_idx * pixel_size
                x2: int = x1 + pixel_size
                y2: int = y1 + pixel_size

                draw.rectangle((x1, y1, x2, y2), fill=rgba_color)

        return image
