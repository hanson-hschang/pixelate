"""
Tests for the color palettes module.
"""

import pytest

from pixelate.palettes import resolve_color, get_available_palettes


class TestResolveColor:
    """Test the resolve_color function."""

    def test_hex_colors(self) -> None:
        """Test that hex colors are handled correctly."""
        # Test with # prefix
        assert resolve_color("#FF0000") == "#FF0000"
        assert resolve_color("#00FF00") == "#00FF00"
        assert resolve_color("#0000FF") == "#0000FF"
        assert resolve_color("#FF000080") == "#FF000080"  # RGBA
        
        # Test without # prefix
        assert resolve_color("FF0000") == "#FF0000"
        assert resolve_color("00FF00") == "#00FF00"
        assert resolve_color("0000FF") == "#0000FF"
        assert resolve_color("FF000080") == "#FF000080"  # RGBA
        
    def test_invalid_hex_colors(self) -> None:
        """Test that invalid hex colors raise ValueError."""
        with pytest.raises(ValueError, match="Invalid hex color format"):
            resolve_color("#FF00")  # Too short
            
        with pytest.raises(ValueError, match="Invalid hex color format"):
            resolve_color("#FF00000")  # Wrong length
            
        with pytest.raises(ValueError, match="Invalid hex color format"):
            resolve_color("#GG0000")  # Invalid characters
            
    def test_tableau_colors(self) -> None:
        """Test tableau color palette."""
        # Test specific tableau colors from the TOML file
        assert resolve_color("tableau:blue") == "#1F77B4"
        assert resolve_color("tableau:red") == "#D62728"
        assert resolve_color("tableau:green") == "#2CA02C"
        assert resolve_color("tableau:orange") == "#FF7F0E"
        
        # Test case insensitive
        assert resolve_color("TABLEAU:BLUE") == "#1F77B4"
        assert resolve_color("Tableau:Red") == "#D62728"
        
    def test_xkcd_colors(self) -> None:
        """Test XKCD color palette."""
        # Test specific XKCD colors that should exist in the TOML file
        assert resolve_color("xkcd:red") == "#E50000"
        assert resolve_color("xkcd:blue") == "#0343DF"
        assert resolve_color("xkcd:green") == "#15B01A"
        
        # Test case insensitive
        assert resolve_color("XKCD:RED") == "#E50000"
        assert resolve_color("Xkcd:Blue") == "#0343DF"
        
    def test_css4_colors(self) -> None:
        """Test CSS4 color palette."""
        # Test specific CSS4 colors
        assert resolve_color("css4:red") == "#FF0000"
        assert resolve_color("css4:blue") == "#0000FF"
        assert resolve_color("css4:green") == "#008000"
        
        # Test case insensitive
        assert resolve_color("CSS4:RED") == "#FF0000"
        assert resolve_color("Css4:Blue") == "#0000FF"
        
    def test_base_colors(self) -> None:
        """Test base color palette."""
        # Test specific base colors
        assert resolve_color("base:r") == "#FF0000"
        assert resolve_color("base:g") == "#007F00"
        assert resolve_color("base:b") == "#0000FF"
        
        # Test case insensitive
        assert resolve_color("BASE:R") == "#FF0000"
        assert resolve_color("Base:G") == "#007F00"
        
    def test_get_available_palettes(self) -> None:
        """Test that get_available_palettes returns expected palettes."""
        palettes = get_available_palettes()
        assert isinstance(palettes, list)
        assert "tableau" in palettes
        assert "xkcd" in palettes
        assert "css4" in palettes
        assert "base" in palettes
        
    def test_unknown_palette(self) -> None:
        """Test that unknown palettes raise ValueError."""
        with pytest.raises(ValueError, match="Palette 'unknown' not found"):
            resolve_color("unknown:blue")
            
    def test_unknown_tableau_color(self) -> None:
        """Test that unknown tableau colors raise ValueError."""
        with pytest.raises(ValueError, match="Unknown tableau color 'unknown'"):
            resolve_color("tableau:unknown")
            
    def test_unknown_xkcd_color(self) -> None:
        """Test that unknown XKCD colors raise ValueError."""
        with pytest.raises(ValueError, match="Unknown xkcd color 'unknown'"):
            resolve_color("xkcd:unknown")
            
    def test_unrecognized_format(self) -> None:
        """Test that unrecognized formats raise ValueError."""
        with pytest.raises(ValueError, match="Unrecognized color format"):
            resolve_color("justred")
            
        with pytest.raises(ValueError, match="Unrecognized color format"):
            resolve_color("rgb(255,0,0)")


if __name__ == "__main__":
    pytest.main([__file__])