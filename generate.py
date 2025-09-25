#!/usr/bin/env python3
"""
Pixel Icon Generator

A script that takes a folder name as argument, finds markdown files within that folder
containing TOML frontmatter with color definitions and CSV-like pixel data, then generates
PNG pixel art images.

Format expected:
- Markdown file with TOML frontmatter wrapped in +++
- TOML contains color mappings: number = "hex_color_with_transparency"
- After frontmatter: CSV-like format with numbers indicating colors
- Position of numbers indicates row/column in the pixel grid
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple
import toml
import click
from PIL import Image, ImageDraw


def find_markdown_files(folder_path: Path) -> List[Path]:
    """Find all markdown files in the given folder."""
    return list(folder_path.glob("*.md"))


def parse_markdown_file(file_path: Path) -> Tuple[Dict[str, str], List[List[str]]]:
    """
    Parse a markdown file with TOML frontmatter and CSV content.
    
    Returns:
        Tuple of (color_dict, pixel_grid)
        - color_dict: mapping of number strings to hex color codes
        - pixel_grid: 2D list of strings representing the pixel grid
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content by +++ to extract frontmatter
    parts = content.split('+++')
    if len(parts) < 3:
        raise ValueError("Markdown file must have TOML frontmatter wrapped in +++")
    
    # Parse TOML frontmatter (second part, first part is empty)
    toml_content = parts[1].strip()
    try:
        toml_data = toml.loads(toml_content)
    except toml.TomlDecodeError as e:
        raise ValueError(f"Invalid TOML in frontmatter: {e}")
    
    # Extract color dictionary
    color_dict = {}
    for key, value in toml_data.items():
        if isinstance(value, str) and (value.startswith('#') or value.startswith('rgba')):
            color_dict[key] = value
    
    # Parse CSV content (everything after the second +++)
    csv_content = '+++'.join(parts[2:]).strip()
    pixel_grid = []
    
    for line in csv_content.split('\n'):
        line = line.strip()
        if line:
            # Split by comma and clean up each cell
            row = [cell.strip() for cell in line.split(',')]
            if row:  # Only add non-empty rows
                pixel_grid.append(row)
    
    return color_dict, pixel_grid


def hex_to_rgba(hex_color: str) -> Tuple[int, int, int, int]:
    """Convert hex color string to RGBA tuple."""
    hex_color = hex_color.lstrip('#')
    
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


def generate_pixel_image(color_dict: Dict[str, str], pixel_grid: List[List[str]], 
                        output_path: Path, pixel_size: int = 10) -> None:
    """
    Generate a PNG image from the pixel grid and color dictionary.
    
    Args:
        color_dict: Mapping of number strings to hex colors
        pixel_grid: 2D list representing the pixel art
        output_path: Path where to save the PNG file
        pixel_size: Size of each pixel in the output image (default: 10x10)
    """
    if not pixel_grid:
        raise ValueError("Pixel grid is empty")
    
    rows = len(pixel_grid)
    cols = max(len(row) for row in pixel_grid)
    
    # Create image with RGBA mode for transparency support
    img_width = cols * pixel_size
    img_height = rows * pixel_size
    image = Image.new('RGBA', (img_width, img_height), (255, 255, 255, 0))  # Transparent background
    draw = ImageDraw.Draw(image)
    
    for row_idx, row in enumerate(pixel_grid):
        for col_idx, cell_value in enumerate(row):
            cell_value = cell_value.strip()
            
            # Skip empty cells
            if not cell_value or cell_value == '0':
                continue
                
            # Get color from dictionary
            if cell_value in color_dict:
                hex_color = color_dict[cell_value]
                try:
                    rgba_color = hex_to_rgba(hex_color)
                except ValueError as e:
                    print(f"Warning: {e}, skipping cell at ({row_idx}, {col_idx})")
                    continue
            else:
                print(f"Warning: Color not found for value '{cell_value}', skipping cell at ({row_idx}, {col_idx})")
                continue
            
            # Draw pixel
            x1 = col_idx * pixel_size
            y1 = row_idx * pixel_size
            x2 = x1 + pixel_size
            y2 = y1 + pixel_size
            
            draw.rectangle([x1, y1, x2, y2], fill=rgba_color)
    
    # Save the image
    image.save(output_path, 'PNG')
    print(f"Pixel icon saved to: {output_path}")


def process_markdown_file(markdown_file: Path, folder_path: Path, pixel_size: int) -> None:
    """Process a single markdown file and generate its PNG."""
    try:
        print(f"Processing file: {markdown_file}")
        
        # Parse the markdown file
        color_dict, pixel_grid = parse_markdown_file(markdown_file)
        
        print(f"Found {len(color_dict)} colors: {list(color_dict.keys())}")
        print(f"Pixel grid size: {len(pixel_grid)} rows, {max(len(row) for row in pixel_grid) if pixel_grid else 0} columns")
        
        # Generate output filename with same name as markdown file
        output_filename = markdown_file.stem + '.png'
        output_path = folder_path / output_filename
        
        # Generate the pixel image
        generate_pixel_image(color_dict, pixel_grid, output_path, pixel_size)
        
    except Exception as e:
        print(f"Error processing {markdown_file}: {e}")


@click.command()
@click.option('--folder', type=click.Path(exists=True, file_okay=False, dir_okay=True), help='The folder containing markdown files for pixel art generation.')
@click.option('--pixel-size', type=int, default=10, help='Size of each pixel in the output image (default: 10)')
def main(folder: str, pixel_size: int) -> None:
    """Generate pixel icons from markdown files with TOML frontmatter."""
    # Convert folder argument to Path
    folder_path = Path(folder)
    
    if not folder_path.exists():
        print(f"Error: Folder '{folder_path}' does not exist")
        sys.exit(1)
    
    if not folder_path.is_dir():
        print(f"Error: '{folder_path}' is not a directory")
        sys.exit(1)
    
    # Find all markdown files
    markdown_files = find_markdown_files(folder_path)
    if not markdown_files:
        print(f"Error: No markdown files found in folder '{folder_path}'")
        sys.exit(1)
    
    print(f"Found {len(markdown_files)} markdown file(s) to process")
    
    # Process each markdown file
    for markdown_file in markdown_files:
        process_markdown_file(markdown_file, folder_path, pixel_size)


if __name__ == '__main__':
    main()