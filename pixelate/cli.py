#!/usr/bin/env python3
"""
Command line interface for the pixelate package.
"""

import click
from .core import PixelateApp


@click.command()
@click.argument('input_path', type=str, required=True)
@click.option('--pixel-size', type=int, default=10, help='Size of each pixel in the output image (default: 10)')
@click.option('--format', type=str, default='png', help='Output image format (default: png)')
def main(input_path: str, pixel_size: int, format: str) -> None:
    """
    Generate pixel art images from markdown files with TOML frontmatter.
    
    INPUT_PATH can be either:
    - A single markdown file (e.g., filename.md)
    - A folder containing markdown files
    
    Examples:
        pixelate filename.md
        pixelate foldername
        pixelate filename.md --pixel-size 20 --format png
    """
    app: PixelateApp = PixelateApp()
    app.run(input_path, pixel_size, format)


if __name__ == '__main__':
    main()