"""
Tests for the color palettes module.
"""

import pytest

from pixelate.palettes import resolve_color, TABLEAU_COLORS, XKCD_COLORS


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
        assert resolve_color("tableau:blue") == TABLEAU_COLORS["blue"]
        assert resolve_color("tableau:red") == TABLEAU_COLORS["red"]
        assert resolve_color("tableau:green") == TABLEAU_COLORS["green"]
        
        # Test case insensitive
        assert resolve_color("TABLEAU:BLUE") == TABLEAU_COLORS["blue"]
        assert resolve_color("Tableau:Red") == TABLEAU_COLORS["red"]
        
    def test_xkcd_colors(self) -> None:
        """Test XKCD color palette."""
        assert resolve_color("xkcd:drab") == XKCD_COLORS["drab"]
        assert resolve_color("xkcd:navy") == XKCD_COLORS["navy"]
        assert resolve_color("xkcd:red") == XKCD_COLORS["red"]
        
        # Test case insensitive
        assert resolve_color("XKCD:DRAB") == XKCD_COLORS["drab"]
        assert resolve_color("Xkcd:Navy") == XKCD_COLORS["navy"]
        
    def test_unknown_palette(self) -> None:
        """Test that unknown palettes raise ValueError."""
        with pytest.raises(ValueError, match="Unknown color palette 'unknown'"):
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