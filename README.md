<div align=center>
  <h1>PIXELATE</h1>

![Python](https://img.shields.io/badge/Python-3776AB?logo=Python&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-EE4C2C?logo=python&logoColor=white)
![Click](https://img.shields.io/badge/Click-0E7E3E?logo=python&logoColor=white)
![TOML](https://img.shields.io/badge/TOML-9C4121?logo=toml&logoColor=white)

[![CI: pre-commit](https://img.shields.io/badge/CI-pre--commit-FAB040?logo=pre-commit)](https://pre-commit.com/)
[![unit test: pytest](https://img.shields.io/badge/unit_test-pytest-0A9EDC?logo=pytest)](https://docs.pytest.org/)
[![code style: black](https://img.shields.io/badge/code_style-black-black)](https://github.com/psf/black)
[![imports: isort](https://img.shields.io/badge/imports-isort-blue?labelColor=orange)](https://pycqa.github.io/isort/)
[![linting: flake8](https://img.shields.io/badge/linting-flake8-yellowgreen)](https://flake8.pycqa.org/)
[![static type: mypy](https://img.shields.io/badge/static_type-mypy-blue)](https://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow)](https://bandit.readthedocs.io/)
[![security: CodeQL](https://img.shields.io/badge/security-CodeQL-blue)](https://codeql.github.com/)

[![Test](https://github.com/hanson-hschang/pixelate/actions/workflows/test.yml/badge.svg)](https://github.com/hanson-hschang/pixelate/actions/workflows/test.yml)
[![Security](https://github.com/hanson-hschang/pixelate/actions/workflows/security.yml/badge.svg)](https://github.com/hanson-hschang/pixelate/actions/workflows/security.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-yellow)](https://opensource.org/licenses/MIT)

</div>

A CLI tool that generates pixel art PNG images from markdown files with TOML front-matter.

## Installation

### From GitHub
Install directly from GitHub using pip:

```bash
pip install git+https://github.com/hanson-hschang/pixelate.git
```

### From source
```bash
git clone https://github.com/hanson-hschang/pixelate.git
cd pixelate
pip install .
```

## Development

<details>
<summary>Setup Development Environment</summary>

### Prerequisites
This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python package management during development. Install uv first:

```bash
# Install uv with pip (recommended)
pip install uv
# or with curl: curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Development Installation
Clone the repository and install with dev dependencies:
```bash
git clone https://github.com/hanson-hschang/pixelate.git
cd pixelate
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

### Pre-commit Hooks
Install pre-commit hooks to ensure code quality:
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
This project uses GitHub Actions for continuous integration with separate workflows:
- **Test workflow**: Tests run on Python 3.9-3.12, code quality checks (formatting, linting, type checking)
- **Security workflow**: CodeQL security scanning with write permissions for security results
- All checks must pass before merging to main branch

</details>

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
