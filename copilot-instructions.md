# Copilot Instructions for Pixelate

## Project Overview

Pixelate is a CLI tool that generates pixel art PNG images from markdown files with TOML front-matter. The tool processes markdown files containing color definitions in TOML format and CSV-like pixel grids to produce PNG images.

## Repository Structure

```
pixelate/
├── pixelate/           # Main package
│   ├── __init__.py    # Package initialization  
│   ├── cli.py         # Command-line interface using Click
│   └── core.py        # Core classes (PixelArtParser, ImageGenerator, FileProcessor, PixelateApp)
├── tests/             # Test suite
│   ├── __init__.py    
│   └── test_pixelate.py # Comprehensive tests for all classes
├── examples/          # Example markdown files and generated PNGs
│   ├── bird.md
│   ├── penguin.md
│   └── pixelate.md
├── pyproject.toml     # Modern Python packaging configuration
├── requirements.txt   # Dependencies
└── README.md         # Documentation
```

## Core Components

1. **PixelArtParser**: Parses markdown files with TOML frontmatter and CSV pixel data
2. **ImageGenerator**: Converts pixel data to PNG images using PIL/Pillow
3. **FileProcessor**: Handles file and folder operations
4. **PixelateApp**: Main application orchestrator
5. **CLI**: Click-based command-line interface

## Development Guidelines

### Code Style
- Use Python type hints throughout (already implemented)
- Follow PEP 8 conventions
- Use meaningful variable names with type annotations
- Maintain docstrings for classes and public methods
- Use f-strings for string formatting

### Architecture Patterns
- **Separation of concerns**: Each class has a single responsibility
- **Dependency injection**: Classes are composed, not tightly coupled
- **Error handling**: Use try/catch blocks with meaningful error messages
- **Path handling**: Use `pathlib.Path` for file operations (already implemented)

### File Format Support
The tool processes markdown files with this structure:
```markdown
+++
"1" = "#FF0000"  # Red
"0" = "#00000000"  # Transparent
+++

1,0,1
0,1,0
1,0,1
```

### Key Dependencies
- `toml>=0.10.2` - TOML parsing
- `pillow>=10.0.0` - Image generation
- `click>=8.0.0` - CLI framework
- `pytest>=8.0.0` - Testing (dev dependency)
- `mypy>=1.0.0` - Static type checking (dev dependency)
- `types-toml` - Type stubs for TOML library
- `types-Pillow` - Type stubs for Pillow/PIL library
- `black>=23.0.0` - Code formatting (dev dependency)
- `isort>=5.12.0` - Import sorting (dev dependency)
- `flake8>=6.0.0` - Linting (dev dependency)
- `bandit[toml]>=1.7.0` - Security checking (dev dependency)
- `pre-commit>=3.0.0` - Pre-commit hooks (dev dependency)

### Testing
- Run tests with: `uv run python -m pytest tests/ -v`
- Run type checking with: `uv run mypy pixelate/ tests/`
- All classes have comprehensive test coverage
- Tests use temporary files and proper cleanup
- Use type hints in test code as well

### Installation
```bash
# Development installation with type checking dependencies
uv sync --group dev
```

### Usage
```bash
# Usage examples
uv run pixelate filename.md
uv run pixelate foldername/
uv run pixelate myfile.md --pixel-size 20 --format png
```

### Build & Package Management
- Uses modern `pyproject.toml` configuration with uv for dependency management
- Package built with setuptools
- Entry point: `pixelate = "pixelate.cli:main"`
- Supports Python 3.9+

## When Making Changes

1. **Maintain backwards compatibility** for CLI interface
2. **Add tests** for new functionality in `tests/test_pixelate.py`
3. **Update documentation** in README.md if adding features
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