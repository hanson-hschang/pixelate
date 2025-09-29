# Copilot Instructions for Pixelate

## Project Overview

Pixelate is a CLI tool that generates pixel art PNG images from markdown files with TOML front-matter. 
The tool processes markdown files containing color definitions in TOML format and CSV-like pixel grids to produce PNG images.


## Repository Structure

```
pixelate/
├── pixelate/           # Main package
│   ├── __init__.py    # Package initialization  
│   ├── cli.py         # Command-line interface using Click
│   ├── app.py         # Main application class
│   ├── parser.py      # TOML frontmatter and CSV parsing
│   ├── pixelator.py   # Core pixel art generation logic
│   ├── generator.py   # Image generation utilities
│   ├── palette/       # Color palette system
│   │   ├── __init__.py
│   │   ├── _palette.py # Palette loading and management
│   │   └── assets/    # TOML palette files
│   │       ├── base.toml
│   │       ├── css4.toml
│   │       ├── tableau.toml
│   │       └── xkcd.toml
│   └── utility/       # Utility classes
│       ├── bidict.py  # Bidirectional dictionary
│       └── singleton.py # Singleton pattern implementation
├── tests/             # Test suite
│   ├── __init__.py    
│   ├── test_palettes.py # Palette system tests
│   └── test_pixelate.py # Core functionality tests
├── examples/          # Example markdown files and generated PNGs
│   ├── bird.md
│   ├── penguin.md
│   ├── pixelate.md
│   └── palette-demo.md
├── Makefile          # Development automation
├── pyproject.toml    # Modern Python packaging configuration
└── README.md         # Documentation
```

## Core Components

1. **PixelArtParser**: Parses markdown files with TOML frontmatter and CSV pixel data
2. **Pixelator**: Core pixel art generation logic and image processing
3. **Generator**: Image generation utilities using PIL/Pillow
4. **Palette System**: Comprehensive color palette management supporting 1,115+ named colors
   - Tableau colors (10 colors)
   - CSS4 colors (148 colors)  
   - Base colors (8 colors)
   - XKCD colors (949 colors)
5. **PixelateApp**: Main application orchestrator
6. **CLI**: Click-based command-line interface

## Development Guidelines

### Code Style
- Use Python type hints throughout the code base
- Follow PEP 8 conventions
- Use meaningful variable names with type annotations
- Maintain docstrings for classes and public methods
- Use f-strings for string formatting

### Architecture Patterns
- **Separation of concerns**: Each class has a single responsibility
- **Dependency injection**: Classes are composed, not tightly coupled
- **Error handling**: Use try/catch blocks with meaningful error messages
- **Path handling**: Use `pathlib.Path` for file operations

### Key Dependencies
- `pillow>=10.0.0` - Image generation
- `click>=8.0.0` - CLI framework
- `matplotlib` - Color palette generation (matplotlib color definitions)
- `pytest>=8.0.0` - Testing (dev dependency)
- `mypy>=1.0.0` - Static type checking (dev dependency)
- `types-toml` - Type stubs for TOML library
- `types-Pillow` - Type stubs for Pillow/PIL library
- `black>=23.0.0` - Code formatting (dev dependency)
- `isort>=5.12.0` - Import sorting (dev dependency)
- `flake8>=6.0.0` - Linting (dev dependency)
- `bandit[toml]>=1.7.0` - Security checking (dev dependency)
- `pre-commit>=3.0.0` - Pre-commit hooks (dev dependency)
- `pyupgrade>=3.15.2` - Code modernization (dev dependency)


### Markdown File Format Support
The tool processes markdown files with this structure:
```markdown
+++
# Hex colors (traditional format)
"1" = "#FF0000"  # Red
"0" = "#00000000"  # Transparent

# Named palette colors (new format)
"2" = "tableau:blue"    # Tableau palette
"3" = "xkcd:drab"      # XKCD color survey  
"4" = "css4:coral"     # CSS4 web colors
"5" = "base:g"         # Base matplotlib colors
+++

1,0,1
0,2,0
3,4,5
```

### Color Palette System
The application supports 1,115+ named colors across 4 palette types:
- **tableau**: 10 standard visualization colors
- **css4**: 148 standard web colors  
- **base**: 8 basic matplotlib colors (r, g, b, c, m, y, k, w)
- **xkcd**: 949 colors from the XKCD color survey

### Development Tools & Commands
```bash
# Setup development environment
uv sync --group dev

# Run tests  
make test
uv run pytest tests/ -v

# Fix formatting issues
make formatting
uv run black --config pyproject.toml ./
uv run isort --settings-path pyproject.toml ./

# Type checking
uv run mypy pixelate/ tests/

# Run all quality checks
uv run pre-commit run --all-files
```



### Build & Package Management
- Uses modern `pyproject.toml` configuration with uv for dependency management
- Package built with setuptools
- Entry point: `pixelate = "pixelate.cli:main"`
- Supports Python 3.11+ (updated from 3.9+)
- Uses `tomllib` (Python 3.11+) instead of external `toml` library

## When Making Changes

1. **Maintain backwards compatibility** for CLI interface
2. **Add tests** for new functionality in `tests/`
3. **Update documentation** in `README.md` if adding features
4. **Use existing patterns** - follow the established class structure
5. **Handle errors gracefully** with user-friendly messages
6. **Validate file formats** - ensure TOML frontmatter is properly parsed
7. **Test with example files** in the `examples/` directory
8. **Update dependencies consistently** - when adding or changing package dependencies:
   - Update `pyproject.toml` [project.dependencies] or [project.optional-dependencies]
   - Update `README.md` installation instructions
   - Update this file's Key Dependencies section
   - Update any relevant CI/CD configurations

## Common Tasks

### Adding a new image format:
- Modify `ImageGenerator.generate_pixel_image()` method
- Update CLI `--format` option validation
- Add tests for the new format

### Adding new CLI options:
- Update `cli.py` with new Click options
- Pass parameters through `PixelateApp.run()`
- Update help text and documentation

### Extending parser functionality:
- Modify `PixelArtParser.parse_markdown_file()`
- Ensure error handling for malformed files
- Add corresponding tests

### Performance considerations:
- Large pixel grids should be handled efficiently
- File I/O should use appropriate buffering
- Image generation should be memory-conscious for large outputs

## Security Considerations
- Validate file paths to prevent directory traversal
- Sanitize TOML input to prevent code execution
- Limit image dimensions to prevent memory exhaustion
- Handle malformed files gracefully without crashes