# PIXELATE

A Python script that generates pixel art PNG images from markdown files with TOML front-matter.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python generate.py --folder <FOLDER-PATH> [--pixel-size SIZE] [--format FORMAT]
```

- `--folder`: Path to folder containing markdown files with pixel art data
- `--pixel-size`: Size of each pixel in the output image (default: 10)
- `--format`: Output image format (default: png)

This will process all `.md` files in the `<FOLDER-PATH>` folder and generate corresponding files with the same names (e.g., `pixelate.md` -> `pixelate.png`) in the same folder.

## Format

The markdown file should have the following format:

```markdown
+++
# TOML front-matter with color definitions
"1" = "#00FF0080"  # Green with 50% transparency  
"0" = "#00000000"  # Transparent (empty pixels)
+++

# CSV-like pixel grid (position indicates row/column)
1,1,1,1,0,0,1,1,1,1,1,0,1,0,0,0,1,0,1,1,1,1,1,0,1,0,0,0,0,0,0,1,1,1,0,0,1,1,1,1,1,0,1,1,1,1,1
1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,1,0,1,1,0,0,0,1,0,0,0,1,0,0,0,0
1,1,1,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,1,1,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,1,1,1
1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,0,0,0,1,0,0,0,0
1,0,0,0,0,0,1,1,1,1,1,0,1,0,0,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,1,1,1
```

![pixelate.png](examples/pixelate.png)
