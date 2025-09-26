# PIXELATE

A CLI tool that generates pixel art PNG images from markdown files with TOML front-matter.

## Installation

### From source
```bash
git clone https://github.com/hanson-hschang/pixelate.git
cd pixelate
pip install .
```

### Development installation
```bash
git clone https://github.com/hanson-hschang/pixelate.git
cd pixelate
pip install -e ".[dev]"
```

## Development

### Setup
For development, install with dev dependencies:
```bash
pip install -e .[dev]
```

Or install them individually:
```bash
pip install pytest mypy types-toml types-Pillow
```

### Pre-commit Hooks
This project uses pre-commit hooks to ensure code quality. Install them with:
```bash
pip install pre-commit
pre-commit install
```

The pre-commit hooks will automatically run:
- Code formatting (black)
- Import sorting (isort)
- Linting (flake8)
- Type checking (mypy)
- Security checks (bandit)
- Tests (pytest)

### Testing
```bash
# Run tests
python -m pytest tests/ -v

# Run type checking
mypy pixelate/ tests/

# Run all quality checks manually
pre-commit run --all-files
```

### Code Quality
- **Formatting**: Code is automatically formatted with [black](https://black.readthedocs.io/)
- **Import sorting**: Imports are sorted with [isort](https://pycqa.github.io/isort/)
- **Linting**: Code is linted with [flake8](https://flake8.pycqa.org/)
- **Type checking**: Static type checking with [mypy](https://mypy.readthedocs.io/)
- **Security**: Security checks with [bandit](https://bandit.readthedocs.io/)

### CI/CD
This project uses GitHub Actions for continuous integration:
- Tests run on Python 3.7-3.12
- Code quality checks (formatting, linting, type checking)
- Security scanning with CodeQL
- All checks must pass before merging to main branch

## Usage

### Single file usage
```bash
pixelate filename.md
```
This generates `filename.png` in the same directory as the markdown file.

### Folder usage
```bash
pixelate foldername
```
This processes all `.md` files in the `foldername` folder and generates corresponding PNG files with the same names (e.g., `pixelate.md` -> `pixelate.png`) in the same folder.

### Optional arguments
- `--pixel-size SIZE`: Size of each pixel in the output image (default: 10)
- `--format FORMAT`: Output image format (default: png)

### Examples
```bash
pixelate examples/bird.md
pixelate examples/
pixelate myfile.md --pixel-size 20 --format png
```

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
