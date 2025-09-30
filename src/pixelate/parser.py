"""
Handles parsing of markdown files with TOML frontmatter and pixel data.
"""

import tomllib
from pathlib import Path

from pixelate import palette


class PixelArtParser:
    """
    Handles parsing of markdown files with TOML frontmatter and pixel data.
    """

    def parse(self, file_path: Path) -> tuple[dict[str, str], list[list[str]]]:
        """
        Parse a markdown file with TOML frontmatter and CSV content.

        Returns:
            Tuple of (color_dict, pixel_grid)
            - color_dict: mapping of number strings to hex color codes
            - pixel_grid: 2D list of strings representing the pixel grid
        """
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Split content by +++ to extract frontmatter
        parts = content.split("+++")
        if len(parts) < 3:
            raise ValueError(
                "Markdown file must have TOML frontmatter wrapped in +++"
            )

        # Parse TOML frontmatter (second part, first part is empty)
        color_dict = self._parse_color(parts[1].strip())

        # Parse CSV content (everything after the second +++)
        pixel_grid = self._parse_grid(
            "".join(parts[2:]).strip(), set(color_dict.keys())
        )

        return color_dict, pixel_grid

    def _parse_color(self, toml_content: str) -> dict[str, str]:
        """
        Parse a color definition from the TOML frontmatter.

        Args:
            toml_content: The TOML content as a string
        Returns:
            A dictionary mapping keys to their hex codes
        Raises:
            ValueError: If the color definition is invalid
        """
        try:
            toml_data: dict[str, str] = tomllib.loads(toml_content)
        except tomllib.TOMLDecodeError as e:
            raise ValueError(f"Invalid TOML in frontmatter: {e}")

        # Extract color dictionary
        color_dict: dict[str, str] = {}
        for key, color_name in toml_data.items():
            if isinstance(color_name, str):
                try:
                    color_dict[key] = palette.resolve_color(color_name)
                except ValueError as e:
                    raise ValueError(
                        f"Warning: {e}, "
                        f"color definition '{key}' = '{color_name}' is invalid"
                    )

        print(f"Found {len(color_dict)} colors:")

        return color_dict

    def _parse_grid(
        self, csv_content: str, color_keys: set[str]
    ) -> list[list[str]]:
        """
        Parse CSV content into a 2D list representing the pixel grid.

        Args:
            csv_content: The CSV content as a string
            color_keys: A set of valid color keys
        Returns:
            A 2D list of strings representing the pixel grid
        """
        pixel_grid: list[list[str]] = []
        keys: set[str] = set()

        total_cols = None
        for line in csv_content.split("\n"):
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Split by comma and clean up each cell
            row = [cell.strip() for cell in line.split(",")]

            # Add all keys in this row to the set of keys found
            keys.update(row)

            if total_cols is None:
                total_cols = len(row)
            elif len(row) != total_cols:
                raise ValueError(
                    f"Inconsistent number of columns in pixel grid: "
                    f"expected {total_cols}, found {len(row)}"
                )

            pixel_grid.append(row)

        # Validate that all keys in the grid are already defined
        if undefined_keys := keys - color_keys:
            raise ValueError(
                f"Undefined color keys in pixel grid: {undefined_keys}"
            )

        print(
            f"Pixel grid size: "
            f"{len(pixel_grid)} rows, {len(pixel_grid[0])} columns"
        )

        return pixel_grid
