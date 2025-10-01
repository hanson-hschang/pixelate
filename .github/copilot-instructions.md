# Copilot Instructions for Pixelate

This document provides comprehensive instructions for GitHub Copilot to generate code that is idiomatic, consistent, and high-quality according to this project's specific conventions.

---

## 📜 Project Overview & Core Technologies

### Project Goal

**Current (Python CLI):**
Pixelate is a command-line interface (CLI) tool that generates pixel art PNG images from markdown files with TOML front-matter. The tool processes markdown files containing color definitions in TOML format and CSV-like pixel grids to produce high-quality PNG images with transparency support. It features a comprehensive color palette system with 1,115+ named colors from multiple sources (Tableau, CSS4, XKCD, and base matplotlib colors).

**Future (Tauri+Vue App):**
The project will evolve into a cross-platform desktop application using Tauri (Rust backend) and Vue.js (TypeScript frontend). The desktop app will provide a graphical user interface for creating, editing, and exporting pixel art, with real-time preview, an integrated color palette picker, and enhanced export options including multiple formats and resolutions.

### Technology Stack

**Current:**
- **Python 3.11+**: Core programming language
- **Click**: CLI framework for command-line interface
- **Pillow (PIL)**: Image generation and manipulation
- **matplotlib**: Color palette definitions
- **tomllib**: TOML parsing (Python 3.11+ standard library)
- **pytest**: Testing framework
- **mypy**: Static type checking
- **ruff**: Linting and code formatting
- **bandit**: Security analysis
- **uv**: Fast Python package and project manager

**Future:**
- **Tauri**: Desktop application framework (Rust backend)
- **Vue.js 3**: Frontend framework with Composition API
- **TypeScript**: Type-safe JavaScript for frontend
- **Rust**: Systems programming language for backend
- **Pinia**: State management for Vue.js
- **Tailwind CSS**: Utility-first CSS framework

---

## 🏗️ High-Level Architecture & Project Structure

### Directory Structure

```
pixelate/
├── .github/                    # GitHub configuration and workflows
│   ├── copilot-instructions.md # This file - Copilot instructions
│   └── workflows/              # CI/CD workflows
│       ├── test.yml            # Automated testing
│       ├── quality.yml         # Code quality checks
│       ├── security.yml        # Security scanning
│       └── release.yml         # Release automation
├── src/pixelate/               # Main package source code
│   ├── __init__.py            # Package initialization and version
│   ├── cli.py                 # CLI entry point using Click
│   ├── app.py                 # Main application orchestrator (PixelateApp)
│   ├── parser.py              # TOML frontmatter and CSV parsing (PixelArtParser)
│   ├── pixelator.py           # File processing orchestration (Pixelator)
│   ├── generator.py           # Image generation using PIL (ImageGenerator)
│   ├── palette/               # Color palette system
│   │   ├── __init__.py        # Palette module exports
│   │   ├── _palette.py        # Palette loading and management (Palettes, resolve_color)
│   │   └── assets/            # TOML palette files and generation script
│   │       ├── base.toml      # 8 base matplotlib colors
│   │       ├── css4.toml      # 148 CSS4 web colors
│   │       ├── tableau.toml   # 10 Tableau visualization colors
│   │       ├── xkcd.toml      # 949 XKCD color survey colors
│   │       └── create.py      # Script to generate palette TOML files
│   └── utility/               # Utility classes
│       ├── __init__.py
│       ├── bidict.py          # Bidirectional dictionary implementation
│       └── singleton.py       # Singleton metaclass pattern
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── pixelate_test.py       # Core functionality tests
│   └── palettes_test.py       # Palette system tests
├── examples/                  # Example markdown files and generated PNGs
│   ├── bird.md                # Example: colorful bird
│   ├── penguin.md             # Example: cute penguin
│   ├── pixelate.md            # Example: Pixelate logo
│   └── palette-demo.md        # Example: palette demonstration
├── releases/                  # Release notes and documentation
│   ├── RELEASE.md             # Release template
│   └── v0.0.1.md              # Initial release notes
├── pyproject.toml             # Modern Python packaging configuration
├── uv.lock                    # uv lockfile for reproducible dependencies
├── Makefile                   # Development automation commands
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
├── README.md                  # User documentation
├── CONTRIBUTING.md            # Contribution guidelines
└── LICENSE                    # MIT License

```

### Key File Purposes

- **`src/pixelate/__init__.py`**: Package initialization, exports `PixelateApp`, and defines `__version__` using importlib.metadata
- **`src/pixelate/cli.py`**: Defines the `main()` function decorated with `@click.command()` that serves as the CLI entry point
- **`src/pixelate/app.py`**: Contains `PixelateApp` class that orchestrates the application flow, handles file/folder validation, and calls the pixelator
- **`src/pixelate/parser.py`**: Contains `PixelArtParser` class with methods to parse TOML frontmatter and CSV pixel grids from markdown files
- **`src/pixelate/pixelator.py`**: Contains `Pixelator` class that coordinates parsing and image generation for individual files
- **`src/pixelate/generator.py`**: Contains `ImageGenerator` class with PIL/Pillow-based image rendering logic
- **`src/pixelate/palette/_palette.py`**: Implements the `Palettes` singleton class for loading color palettes and `resolve_color()` function for color resolution
- **`pyproject.toml`**: Central configuration file for project metadata, dependencies, tools (pytest, mypy, ruff, bandit), and build system
- **`Makefile`**: Provides convenient commands for common development tasks (install, test, lint, format, type-check, etc.)

### Code Flow

1. User invokes `pixelate` command → `cli.py:main()`
2. `main()` creates a `PixelateApp` instance and calls `app.run()`
3. `PixelateApp` validates paths and determines if input is a file or directory
4. For each markdown file, `Pixelator.process()` is called
5. `PixelArtParser.parse()` extracts color definitions and pixel grid
6. Colors are resolved via `palette.resolve_color()` (supports hex or named colors)
7. `ImageGenerator.generate()` creates PIL Image from color dictionary and pixel grid
8. Image is saved as PNG in the output directory

---

## ✍️ Coding Conventions & Style Guide

### Formatting & Linting

All code MUST be compliant with **Ruff** configuration specified in `pyproject.toml`:
- **Line length**: 79 characters maximum
- **Target Python version**: 3.11
- **Rules enabled**: E (pycodestyle errors), F (Pyflakes), W (pycodestyle warnings)
- Run `make formatting` or `uv run ruff format . && uv run ruff check . --fix` before committing
- Pre-commit hooks automatically run ruff formatting and checks

### Type Hinting

**MANDATORY** - All code must use Python type hints:
- Use modern Python 3.11+ type syntax: `list[str]`, `dict[str, int]`, `tuple[int, ...]` (NOT `List`, `Dict`, `Tuple` from typing)
- Use `from typing import` only for: `Final`, `Protocol`, `TypeVar`, `Generic`, `Callable`, `Generator`
- All function/method signatures must include parameter types and return types
- All class attributes should have type annotations
- Use `Path` from `pathlib` for file paths, never string paths
- Use `| None` for optional types (NOT `Optional[T]`)
- Example:
  ```python
  def parse(self, file_path: Path) -> tuple[dict[str, str], list[list[str]]]:
      """Parse a markdown file."""
      color_dict: dict[str, str] = {}
      return color_dict, []
  ```

**mypy Configuration**: Code must pass `mypy` with strict settings (see `pyproject.toml`):
- `disallow_untyped_defs = true`
- `disallow_incomplete_defs = true`
- `check_untyped_defs = true`
- Run `make typing` or `uv run mypy src tests` to verify

### Docstrings

**MANDATORY** - All public modules, classes, and functions MUST have complete docstrings:

**Style**: Use **Google Style** docstrings

**Format**:
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief one-line description.

    More detailed description if needed. Can span multiple
    lines and paragraphs.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When and why this is raised
        FileNotFoundError: When and why this is raised
    """
```

**Class Docstrings**:
```python
class MyClass:
    """Brief description of the class.

    More detailed description of the class purpose,
    behavior, and usage patterns.
    """
```

**Module Docstrings**: Every Python file should start with a module-level docstring:
```python
"""
Brief description of the module's purpose.
"""
```

### Naming Conventions

Follow PEP 8 naming conventions strictly:
- **Variables and functions**: `snake_case` (e.g., `pixel_size`, `parse_color()`)
- **Classes**: `PascalCase` (e.g., `PixelateApp`, `ImageGenerator`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `PALETTES`, `MAX_IMAGE_SIZE`)
- **Private attributes/methods**: Prefix with single underscore `_name` (e.g., `_parser`, `_parse_grid()`)
- **File names**: `snake_case.py` for modules, append `_test.py` for test files

### Import Organization

Imports MUST be organized in this order (enforced by ruff):
1. **Standard library imports** (e.g., `import sys`, `from pathlib import Path`)
2. **Third-party imports** (e.g., `import click`, `from PIL import Image`)
3. **Local application imports** (e.g., `from pixelate.parser import PixelArtParser`)

Within each group, imports should be sorted alphabetically. Use absolute imports for intra-project imports (e.g., `from pixelate.palette import resolve_color`, not `from .palette import resolve_color`).

Example:
```python
"""Module docstring."""

import sys
from pathlib import Path

import click
from PIL import Image

from pixelate.generator import ImageGenerator
from pixelate.parser import PixelArtParser
```

### Code Style Rules

- **Use f-strings** for all string formatting (NOT `%` or `.format()`)
- **No bare `except:`** - always catch specific exceptions
- **Use context managers** (`with` statements) for file operations
- **Prefer explicit over implicit** - be clear about intentions
- **Single responsibility** - each function/class should do one thing well
- **DRY principle** - Don't Repeat Yourself, extract common patterns
- **Use `pathlib.Path`** for all file/directory operations, never raw strings

---

## 📦 Dependencies & Libraries Usage

### Core Dependencies (Production)

**Pillow (`pillow>=10.0.0`)**:
- Use for all image generation and manipulation
- Always create images in RGBA mode for transparency: `Image.new("RGBA", (width, height), (255, 255, 255, 0))`
- Use `ImageDraw.Draw()` for drawing rectangles (pixels)
- Save images with `.save(path, format.upper())` where format is "PNG", "ICO", etc.
- Import: `from PIL import Image, ImageDraw`

**Click (`click>=8.0.0`)**:
- Use for all CLI commands and options
- Decorate main function with `@click.command()`
- Use `@click.argument()` for required positional arguments
- Use `@click.option()` for optional flags with `--name` syntax
- Always provide `help` text for options
- Type all parameters with Click types: `type=str`, `type=int`, etc.
- Example:
  ```python
  @click.command()
  @click.argument("input_path", type=str, required=True)
  @click.option("--pixel-size", type=int, default=10, help="Size of each pixel")
  def main(input_path: str, pixel_size: int) -> None:
      """Command docstring becomes CLI help text."""
  ```

**matplotlib**:
- Used ONLY for color definitions, not for plotting
- Import color constants: `import matplotlib.colors as mcolors`
- Access color dictionaries: `mcolors.TABLEAU_COLORS`, `mcolors.CSS4_COLORS`, `mcolors.XKCD_COLORS`, `mcolors.BASE_COLORS`
- Color values are returned as hex strings

**tomllib** (Python 3.11+ standard library):
- Use for parsing TOML files (frontmatter and palette files)
- Always open files in binary mode: `open(path, "rb")`
- Parse with: `tomllib.load(file)` or `tomllib.loads(string)`
- Catch `tomllib.TOMLDecodeError` for parse errors
- Import: `import tomllib`

### Development Dependencies

**pytest (`pytest>=8.0.0`)**:
- See Testing Philosophy section below for detailed instructions

**mypy (`mypy>=1.0.0`)**:
- Run with: `uv run mypy src tests`
- Configuration in `[tool.mypy]` section of `pyproject.toml`
- All code must pass strict mypy checks

**ruff**:
- Run linting: `uv run ruff check src tests`
- Run formatting: `uv run ruff format src tests`
- Auto-fix issues: `uv run ruff check src tests --fix`
- Configuration in `[tool.ruff]` section of `pyproject.toml`

**bandit (`bandit[toml]>=1.7.0`)**:
- Security linter for Python code
- Run with: `uv run bandit -r src/`
- Configuration in `[tool.bandit]` section of `pyproject.toml`
- Test directories excluded from scans

---

## 🧪 Testing Philosophy

### Framework & Configuration

**Framework**: pytest with plugins:
- `pytest-cov` for coverage reports
- `pytest-mock` for mocking utilities
- Configuration in `[tool.pytest.ini_options]` in `pyproject.toml`

### Test Organization

**Test Location**: All tests in `tests/` directory
- Test files MUST be named `*_test.py` (e.g., `pixelate_test.py`, `palettes_test.py`)
- Test functions MUST start with `test_` (e.g., `test_parse_markdown_file`)
- Test classes MUST start with `Test` (e.g., `TestPixelArtParser`)

**Test Structure**: Mirror the `src/` directory structure
- `tests/pixelate_test.py` tests `src/pixelate/` core modules
- `tests/palettes_test.py` tests `src/pixelate/palette/`

### Test Writing Style

**MANDATORY**: Every new function or feature must be accompanied by unit tests

**Use pytest fixtures** for test setup and teardown:
```python
@pytest.fixture
def sample_markdown_content() -> str:
    """Fixture docstring."""
    return """+++
"1" = "#FF0000"
+++
1,0,1
"""

def test_parser(sample_markdown_content: str) -> None:
    """Test docstring."""
    # Test implementation
```

**Use pytest-mock's `mocker` fixture** for all mocking:
```python
def test_with_mock(mocker: MockerFixture) -> None:
    """Test with mocked dependency."""
    mock_parser = mocker.Mock()
    mock_parser.parse.return_value = ({}, [])
    # Use the mock
```

**Use temporary files for file-based tests**:
```python
import tempfile
from pathlib import Path

@pytest.fixture
def temp_md_file() -> Generator[Path, None, None]:
    """Create temporary markdown file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(content)
        temp_file = Path(f.name)
    yield temp_file
    # Cleanup
    if temp_file.exists():
        temp_file.unlink()
```

**Test Assertions**:
- Use explicit assertions: `assert result == expected`
- Use `pytest.raises()` for exception testing:
  ```python
  with pytest.raises(ValueError, match="Invalid hex color"):
      resolve_color("#GG0000")
  ```

**Coverage Requirements**:
- Minimum coverage: 30% (configured in `pyproject.toml`)
- Aim for higher coverage on new code
- Run coverage: `make test` or `uv run pytest --cov=src --cov-branch`

---

## 🚀 Future Architecture Guidelines (Tauri + Vue)

**NOTE**: These are foundational rules for future development. The desktop application is not yet implemented.

### Frontend (Vue.js 3 / TypeScript)

**Component Structure**:
- All components MUST use Vue 3 `<script setup>` syntax with TypeScript
- Use Composition API, not Options API
- Example structure:
  ```vue
  <script setup lang="ts">
  import { ref, computed } from 'vue'
  
  interface Props {
    pixelSize: number
  }
  
  const props = defineProps<Props>()
  const pixels = ref<string[][]>([])
  </script>
  
  <template>
    <div class="pixel-canvas">
      <!-- Template content -->
    </div>
  </template>
  
  <style scoped>
  /* Component-specific styles */
  </style>
  ```

**State Management**:
- Global application state MUST be managed with **Pinia**
- Create new stores in `src/stores/` directory
- Use actions for all state mutations (NOT direct state modification)
- Example store structure:
  ```typescript
  import { defineStore } from 'pinia'
  
  export const usePixelArtStore = defineStore('pixelArt', {
    state: () => ({
      pixels: [] as string[][],
      colorPalette: {} as Record<string, string>
    }),
    actions: {
      setPixels(newPixels: string[][]) {
        this.pixels = newPixels
      }
    }
  })
  ```

**Styling**:
- Use **Tailwind CSS** utility classes for all styling
- Avoid writing custom CSS files unless absolutely necessary
- Use `@apply` directive in `<style scoped>` sections sparingly
- Configure Tailwind in `tailwind.config.js`

**TypeScript**:
- All `.ts` and `.vue` files must use TypeScript
- Enable strict mode in `tsconfig.json`
- Define interfaces for all props, emits, and data structures
- No `any` types - use `unknown` and type guards if needed

### Backend (Rust / Tauri)

**API Layer**:
- All functions exposed to the frontend MUST be Tauri commands
- Use `#[tauri::command]` attribute to mark commands
- Example command:
  ```rust
  #[tauri::command]
  fn generate_pixel_art(
      input_path: String,
      pixel_size: u32
  ) -> Result<String, String> {
      // Implementation
      Ok(output_path)
  }
  ```

**Error Handling**:
- All fallible operations MUST return `Result<T, E>`
- Propagate errors to frontend using `Result<T, String>` for Tauri commands
- Use `?` operator for error propagation
- Never use `panic!()` or `unwrap()` in production code
- Use `expect()` only when failure is truly impossible

**State Management**:
- Use Tauri's `State` manager for backend state
- Define state in `main.rs` with `.manage()`
- Access state in commands with `State<'_, MyState>` parameter
- Example:
  ```rust
  struct AppState {
      config: Mutex<Config>
  }
  
  #[tauri::command]
  fn get_config(state: State<'_, AppState>) -> Result<Config, String> {
      let config = state.config.lock().unwrap();
      Ok(config.clone())
  }
  ```

**File Operations**:
- Use Tauri's dialog API for file pickers
- Use Tauri's fs API for file operations (respects security scope)
- Never use std::fs directly for user-accessible files

---

## ✅ General Dos and ❌ Don'ts

### ✅ DO

- **DO** write comprehensive type hints for all functions, methods, and class attributes
- **DO** write complete docstrings (Google style) for all public modules, classes, and functions
- **DO** ensure all new code is covered by unit tests with meaningful assertions
- **DO** run `make formatting` (ruff format + fix) before committing code
- **DO** run `make typing` (mypy) to verify type correctness
- **DO** run `make test` to ensure all tests pass with coverage
- **DO** use `pathlib.Path` for all file and directory operations
- **DO** use f-strings for all string formatting
- **DO** use context managers (`with` statements) for file I/O
- **DO** catch specific exceptions, never bare `except:`
- **DO** keep functions small and focused on a single responsibility (typically < 30 lines)
- **DO** use meaningful variable names that clearly indicate purpose
- **DO** validate user inputs and provide clear error messages
- **DO** handle edge cases (empty files, missing colors, invalid formats)
- **DO** use the existing palette resolution system via `palette.resolve_color()`
- **DO** follow the existing code patterns and class structure

### ❌ DON'T

- **DON'T** add secrets, API keys, credentials, or sensitive data to the codebase
- **DON'T** commit commented-out code blocks - remove them instead
- **DON'T** introduce new third-party dependencies without:
  - Adding to `dependencies` or `dev` group in `pyproject.toml`
  - Documenting in this file's Dependencies section
  - Updating `README.md` if it affects users
- **DON'T** use old-style type hints (`List`, `Dict`, `Optional` from typing module)
- **DON'T** use `from typing import List, Dict, Tuple` - use built-in `list`, `dict`, `tuple`
- **DON'T** skip writing tests for new functionality
- **DON'T** skip docstrings for public APIs
- **DON'T** use string paths - always use `pathlib.Path`
- **DON'T** use `%` or `.format()` for strings - use f-strings
- **DON'T** modify existing tests without understanding their purpose
- **DON'T** break backwards compatibility of the CLI interface
- **DON'T** add print statements for debugging - use logging or remove before committing
- **DON'T** catch exceptions without handling them appropriately
- **DON'T** create functions longer than ~50 lines - refactor into smaller functions
- **DON'T** commit code that doesn't pass ruff, mypy, or pytest checks

---

## 🔧 Common Development Tasks

### Running Quality Checks

```bash
# Run all checks at once
make formatting  # Format code with ruff
make linting     # Check for linting issues
make typing      # Run mypy type checking
make security    # Run bandit security checks
make test        # Run tests with coverage

# Or run pre-commit on all files
uv run pre-commit run --all-files
```

### Adding a New CLI Option

1. Add option to `cli.py`:
   ```python
   @click.option("--new-option", type=str, default="value", help="Description")
   def main(input_path: str, new_option: str) -> None:
   ```
2. Pass parameter through `PixelateApp.run()` method signature
3. Update `app.py` to use the new parameter
4. Update CLI help text and documentation
5. Add tests for the new option

### Adding a New Image Format

1. Update `ImageGenerator.generate()` method if needed
2. Update `Pixelator.process()` to handle new format
3. Validate format in CLI (optional)
4. Add tests for the new format in `tests/pixelate_test.py`
5. Update `README.md` usage documentation

### Adding a New Color Palette

1. Create new `.toml` file in `src/pixelate/palette/assets/`
2. Format: `"color_name" = "#HEXCODE"`
3. Run `python src/pixelate/palette/assets/create.py` to regenerate (if using the script)
4. Or manually create and the `Palettes` class will auto-load it
5. Add tests in `tests/palettes_test.py`
6. Update documentation in `README.md`

### Debugging Markdown Parse Errors

1. Check TOML frontmatter is wrapped in `+++` delimiters
2. Validate TOML syntax (no bare keys, proper string quoting)
3. Ensure color definitions are valid hex codes or named colors
4. Verify CSV grid uses only defined color keys
5. Check for consistent column counts in all rows

---

## 📚 Additional Resources

- **Project Repository**: https://github.com/hanson-hschang/pixelate
- **Issue Tracker**: https://github.com/hanson-hschang/pixelate/issues
- **Contributing Guide**: `CONTRIBUTING.md`
- **User Documentation**: `README.md`
- **Release Notes**: `releases/`

---

**Last Updated**: 2024
**Maintained By**: Pixelate Project Contributors