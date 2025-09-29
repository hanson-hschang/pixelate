"""
Tests for the pixelate package.
"""

import tempfile
from pathlib import Path
from typing import Generator

import pytest

from pixelate.app import PixelateApp
from pixelate.generator import ImageGenerator
from pixelate.parser import PixelArtParser
from pixelate.pixelator import Pixelator


@pytest.fixture
def sample_markdown_content() -> str:
    """Sample markdown content for testing."""
    return """+++
"1" = "#FF0000"  # Red
"0" = "#00000000"  # Transparent
+++

1,0,1
0,1,0
1,0,1
"""


@pytest.fixture
def temp_md_file(sample_markdown_content: str) -> Generator[Path, None, None]:
    """Create a temporary markdown file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(sample_markdown_content)
        temp_file: Path = Path(f.name)
    yield temp_file
    # Cleanup
    if temp_file.exists():
        temp_file.unlink()
    # Also cleanup generated image if it exists
    image_file: Path = temp_file.with_suffix(".png")
    if image_file.exists():
        image_file.unlink()


class TestPixelArtParser:
    """Test the PixelArtParser class."""

    def test_parse_markdown_file(self, temp_md_file: Path) -> None:
        parser: PixelArtParser = PixelArtParser()
        color_dict, pixel_grid = parser.parse(temp_md_file)

        assert color_dict == {"1": "#FF0000", "0": "#00000000"}
        assert pixel_grid == [["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]]

    def test_parse_markdown_with_named_colors(self) -> None:
        """Test parsing markdown with named colors from palettes."""
        content = """+++
"1" = "tableau:blue"
"2" = "xkcd:drab"
"0" = "#00000000"
+++

1,2,0
0,1,2
2,0,1
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content)
            temp_file = Path(f.name)

        try:
            parser = PixelArtParser()
            color_dict, pixel_grid = parser.parse(temp_file)

            # Check that named colors are resolved to hex codes
            assert color_dict["1"] == "#1F77B4"  # tableau:blue
            assert color_dict["2"] == "#828344"  # xkcd:drab
            assert color_dict["0"] == "#00000000"  # hex color
            assert pixel_grid == [["1", "2", "0"], ["0", "1", "2"], ["2", "0", "1"]]

        finally:
            # Cleanup
            if temp_file.exists():
                temp_file.unlink()


class TestImageGenerator:
    """Test the ImageGenerator class."""

    def test_hex_to_rgba(self) -> None:
        generator: ImageGenerator = ImageGenerator()

        # Test RGB format
        assert generator.hex_to_rgba("#FF0000") == (255, 0, 0, 255)
        assert generator.hex_to_rgba("FF0000") == (255, 0, 0, 255)

        # Test RGBA format
        assert generator.hex_to_rgba("#FF000080") == (255, 0, 0, 128)
        assert generator.hex_to_rgba("FF000080") == (255, 0, 0, 128)

    def test_generate_pixel_image(self, temp_md_file: Path) -> None:
        generator: ImageGenerator = ImageGenerator()
        parser: PixelArtParser = PixelArtParser()

        color_dict, pixel_grid = parser.parse(temp_md_file)
        output_path: Path = temp_md_file.with_suffix(".png")

        image = generator.generate(color_dict, pixel_grid, pixel_size=10)

        image.save(output_path, format="png")

        assert output_path.exists()
        # Cleanup
        output_path.unlink()


class TestFileProcessor:
    """Test the FileProcessor class."""

    def test_process_markdown_file(self, temp_md_file: Path) -> None:
        processor: Pixelator = Pixelator()

        processor.process(temp_md_file)

        output_path: Path = temp_md_file.with_suffix(".png")
        assert output_path.exists()

        # Cleanup
        output_path.unlink()


class TestPixelateApp:
    """Test the main PixelateApp class."""

    def test_run_single_file(self, temp_md_file: Path) -> None:
        app: PixelateApp = PixelateApp()

        app.run(str(temp_md_file), pixel_size=10, format="png")

        output_path: Path = temp_md_file.with_suffix(".png")
        assert output_path.exists()

        # Cleanup
        output_path.unlink()

    def test_run_folder(self, temp_md_file: Path) -> None:
        app: PixelateApp = PixelateApp()

        app.run(str(temp_md_file.parent), pixel_size=10, format="png")

        output_path: Path = temp_md_file.with_suffix(".png")
        assert output_path.exists()

        # Cleanup
        output_path.unlink()


if __name__ == "__main__":
    pytest.main([__file__])
