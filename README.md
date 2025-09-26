# PIXELATE

A CLI tool that generates pixel art PNG images from markdown files with TOML front-matter.

## Installation

### Prerequisites
This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python package management. Install uv first:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
# or with pip: pip install uv
```

### From source
```bash
git clone https://github.com/hanson-hschang/pixelate.git
cd pixelate
uv sync
```

## Development

<details>
<summary>Setup Development Environment</summary>

For development, install with dev dependencies:
```bash
uv sync --group dev
```

This installs all required development tools:
- pytest (testing framework)
- mypy (static type checking)
- types-toml, types-Pillow (type stubs)
- black (code formatting)
- isort (import sorting)
- flake8 (linting)
- bandit (security checking)
- pre-commit (git hooks)
</details>

### Pre-commit Hooks
This project uses pre-commit hooks to ensure code quality. Install them with:
```bash
uv run pre-commit install
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
uv run python -m pytest tests/ -v

# Run type checking
uv run mypy pixelate/ tests/

# Run all quality checks manually
uv run pre-commit run --all-files
```

### Code Quality
- **Formatting**: Code is automatically formatted with [black](https://black.readthedocs.io/)
- **Import sorting**: Imports are sorted with [isort](https://pycqa.github.io/isort/)
- **Linting**: Code is linted with [flake8](https://flake8.pycqa.org/)
- **Type checking**: Static type checking with [mypy](https://mypy.readthedocs.io/)
- **Security**: Security checks with [bandit](https://bandit.readthedocs.io/)

### CI/CD
This project uses GitHub Actions for continuous integration:
- Tests run on Python 3.9-3.12
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
