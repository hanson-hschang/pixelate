# pixel-icon
Create your own pixel icon

A Python script that generates pixel art PNG images from markdown files with TOML frontmatter.

## Usage

```bash
python generate.py <folder_name> [--pixel-size SIZE]
```

- `folder_name`: Path to folder containing markdown files with pixel art data
- `--pixel-size`: Size of each pixel in the output image (default: 10)

## Format

The markdown file should have the following format:

```markdown
+++
# TOML frontmatter with color definitions
"1" = "#FF0000FF"  # Red with full opacity (RRGGBBAA)
"2" = "#00FF0080"  # Green with 50% transparency  
"0" = "#00000000"  # Transparent (empty pixels)
+++

# CSV-like pixel grid (position indicates row/column)
1,1,1,1,1
1,2,0,2,1
1,0,2,0,1
1,2,2,2,1
1,1,1,1,1
```

## Installation

```bash
pip install -r requirements.txt
```

## Example

```bash
python generate.py examples
```

This will process all `.md` files in the `examples` folder and generate corresponding PNG files with the same names (e.g., `heart.md` → `heart.png`).
