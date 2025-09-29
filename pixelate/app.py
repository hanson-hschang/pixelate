"""
Main application class for the Pixelate CLI tool.
"""

import sys
from pathlib import Path

from pixelate.pixelator import Pixelator


class PixelateApp:
    """Main application class for the Pixelate CLI tool."""

    def __init__(self) -> None:
        self._pixelator = Pixelator()

    def run(self, input_path_name: str, pixel_size: int, format: str) -> None:
        """
        Run the pixelate application.

        Args:
            input_path_name: Path to a file or folder to process
            pixel_size: Size of each pixel in the output image
            format: Output image format
        """
        input_path = Path(input_path_name)

        # Validate input file/folder path exists
        if not input_path.exists():
            print(f"Error: Path '{input_path_name}' does not exist")
            sys.exit(1)

        # Process single markdown file
        if input_path.is_file() and input_path.suffix.lower() == ".md":
            self._pixelator.process(input_path, None, pixel_size, format)

        # Process all markdown files in folder
        elif input_path.is_dir():
            # Find all markdown files
            files = list(input_path.glob("*.md"))

            if not files:
                print(f"Error: No markdown files found in folder '{input_path_name}'")
                sys.exit(1)

            print(f"Found {len(files)} markdown file(s) to process\n")

            for path in files:
                self._pixelator.process(path, input_path, pixel_size, format)

        # Invalid input path
        else:
            print(
                f"Error: Path '{input_path_name}' is neither a markdown file nor a directory"
            )
            sys.exit(1)
