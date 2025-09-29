"""
Handles file and folder operations.
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

from pixelate.generator import ImageGenerator
from pixelate.parser import PixelArtParser


class Pixelator:
    """Handles pixel art processing."""

    def __init__(self) -> None:
        self._parser = PixelArtParser()
        self._generator = ImageGenerator()

    def process(
        self,
        markdown_file: Path,
        output_dir: Optional[Path] = None,
        pixel_size: int = 10,
        format: str = "png",
    ) -> None:
        """
        Process a single markdown file and generate its image.

        Args:
            markdown_file: Path to the markdown file to process
            output_dir: Optional path to the output directory
            pixel_size: Size of each pixel in the output image
            format: Output image format (e.g., "png", "ico")
        Returns:
            None
        Raises:
            Exception: If any error occurs during processing
        """
        try:
            print(f"Processing file: {markdown_file}")

            # Parse the markdown file
            color_dict, pixel_grid = self._parser.parse(markdown_file)

            # Generate the pixel image
            image = self._generator.generate(color_dict, pixel_grid, pixel_size)

            # Generate output filename with same name as markdown file
            output_filename = markdown_file.stem + f".{format}"
            if output_dir is None:
                output_dir = markdown_file.parent
            output_path = output_dir / output_filename

            # Save the image
            image.save(output_path, format.upper())
            print(f"Pixel icon saved to: {output_path}")

        except Exception as e:
            print(f"Error processing {markdown_file}: {e}")
