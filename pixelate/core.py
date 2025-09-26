"""
Core classes for the pixelate package.
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import toml
from PIL import Image, ImageDraw


class PixelArtParser:
    """Handles parsing of markdown files with TOML frontmatter and pixel data."""

    def parse_markdown_file(
        self, file_path: Path
    ) -> Tuple[Dict[str, str], List[List[str]]]:
        """
        Parse a markdown file with TOML frontmatter and CSV content.

        Returns:
            Tuple of (color_dict, pixel_grid)
            - color_dict: mapping of number strings to hex color codes
            - pixel_grid: 2D list of strings representing the pixel grid
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content: str = f.read()

        # Split content by +++ to extract frontmatter
        parts: List[str] = content.split("+++")
        if len(parts) < 3:
            raise ValueError("Markdown file must have TOML frontmatter wrapped in +++")

        # Parse TOML frontmatter (second part, first part is empty)
        toml_content: str = parts[1].strip()
        try:
            toml_data: Dict[str, str] = toml.loads(toml_content)
        except toml.TomlDecodeError as e:
            raise ValueError(f"Invalid TOML in frontmatter: {e}")

        # Extract color dictionary
        color_dict: Dict[str, str] = {}
        for key, value in toml_data.items():
            if isinstance(value, str) and value.startswith("#"):
                color_dict[key] = value

        # Parse CSV content (everything after the second +++)
        csv_content: str = "+++".join(parts[2:]).strip()
        pixel_grid: List[List[str]] = []

        for line in csv_content.split("\n"):
            line = line.strip()
            if line:
                # Split by comma and clean up each cell
                row: List[str] = [cell.strip() for cell in line.split(",")]
                if row:  # Only add non-empty rows
                    pixel_grid.append(row)

        return color_dict, pixel_grid


class ImageGenerator:
    """Handles generating images from pixel data."""

    def hex_to_rgba(self, hex_color: str) -> Tuple[int, int, int, int]:
        """Convert hex color string to RGBA tuple."""
        hex_color = hex_color.lstrip("#")

        if len(hex_color) == 6:
            # RGB format: #RRGGBB
            r: int = int(hex_color[0:2], 16)
            g: int = int(hex_color[2:4], 16)
            b: int = int(hex_color[4:6], 16)
            a: int = 255  # Fully opaque
        elif len(hex_color) == 8:
            # RGBA format: #RRGGBBAA
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            a = int(hex_color[6:8], 16)
        else:
            raise ValueError(f"Invalid hex color format: {hex_color}")

        return (r, g, b, a)

    def generate_pixel_image(
        self,
        color_dict: Dict[str, str],
        pixel_grid: List[List[str]],
        output_path: Path,
        pixel_size: int = 10,
        format: str = "png",
    ) -> None:
        """
        Generate an image from the pixel grid and color dictionary.

        Args:
            color_dict: Mapping of number strings to hex colors
            pixel_grid: 2D list representing the pixel art
            output_path: Path where to save the image file
            pixel_size: Size of each pixel in the output image (default: 10x10)
            format: The format of the output image
        """
        if not pixel_grid:
            raise ValueError("Pixel grid is empty")

        rows: int = len(pixel_grid)
        cols: int = max(len(row) for row in pixel_grid)

        # Create image with RGBA mode for transparency support
        img_width: int = cols * pixel_size
        img_height: int = rows * pixel_size
        image: Image.Image = Image.new(
            "RGBA", (img_width, img_height), (255, 255, 255, 0)
        )  # Transparent background
        draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)

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

        # Save the image
        image.save(output_path, format.upper())
        print(f"Pixel icon saved to: {output_path}")


class FileProcessor:
    """Handles file and folder operations."""

    def __init__(self) -> None:
        self._parser: PixelArtParser = PixelArtParser()
        self._generator: ImageGenerator = ImageGenerator()

    def find_markdown_files(self, folder_path: Path) -> List[Path]:
        """Find all markdown files in the given folder."""
        return list(folder_path.glob("*.md"))

    def process_markdown_file(
        self,
        markdown_file: Path,
        output_dir: Optional[Path] = None,
        pixel_size: int = 10,
        format: str = "png",
    ) -> None:
        """Process a single markdown file and generate its image."""
        try:
            print(f"Processing file: {markdown_file}")

            # Parse the markdown file
            color_dict: Dict[str, str]
            pixel_grid: List[List[str]]
            color_dict, pixel_grid = self._parser.parse_markdown_file(markdown_file)

            print(f"Found {len(color_dict)} colors: {list(color_dict.keys())}")
            grid_cols = max(len(row) for row in pixel_grid) if pixel_grid else 0
            print(f"Pixel grid size: {len(pixel_grid)} rows, {grid_cols} columns")

            # Generate output filename with same name as markdown file
            output_filename: str = markdown_file.stem + f".{format}"
            if output_dir is None:
                output_dir = markdown_file.parent
            output_path: Path = output_dir / output_filename

            # Generate the pixel image
            self._generator.generate_pixel_image(
                color_dict, pixel_grid, output_path, pixel_size, format
            )

        except Exception as e:
            print(f"Error processing {markdown_file}: {e}")

    def process_folder(
        self, folder_path: Path, pixel_size: int = 10, format: str = "png"
    ) -> None:
        """Process all markdown files in a folder."""
        # Find all markdown files
        markdown_files: List[Path] = self.find_markdown_files(folder_path)
        if not markdown_files:
            print(f"Error: No markdown files found in folder '{folder_path}'")
            sys.exit(1)

        print(f"Found {len(markdown_files)} markdown file(s) to process\n")

        # Process each markdown file
        for markdown_file in markdown_files:
            self.process_markdown_file(markdown_file, folder_path, pixel_size, format)
            print()  # Blank line between files


class PixelateApp:
    """Main application class for the Pixelate CLI tool."""

    def __init__(self) -> None:
        self._processor: FileProcessor = FileProcessor()

    def run(self, input_path: str, pixel_size: int = 10, format: str = "png") -> None:
        """
        Run the pixelate application.

        Args:
            input_path: Path to a file or folder to process
            pixel_size: Size of each pixel in the output image (default: 10)
            format: Output image format (default: png)
        """
        path: Path = Path(input_path)

        if not path.exists():
            print(f"Error: Path '{input_path}' does not exist")
            sys.exit(1)

        if path.is_file():
            if path.suffix.lower() != ".md":
                print(f"Error: File '{input_path}' is not a markdown file")
                sys.exit(1)
            self._processor.process_markdown_file(path, None, pixel_size, format)
        elif path.is_dir():
            self._processor.process_folder(path, pixel_size, format)
        else:
            print(f"Error: Path '{input_path}' is neither a file nor a directory")
            sys.exit(1)
