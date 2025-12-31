"""Rendering context for drawable objects."""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class RenderContext:
    """
    Context providing rendering helpers and constants to drawable objects.

    This encapsulates all the information needed to render game objects,
    including colors, sizes, and helper functions. Can be extended for theming.
    """

    # Size constants
    cell_size: int
    cell_spacing: int
    padding: int

    # Colors - can be customized for different themes
    grid_color: Tuple[int, int, int]
    ship_color: Tuple[int, int, int]
    bullet_color: Tuple[int, int, int]
    enemy_colors: dict[int, Tuple[int, int, int]]  # Maps health level to color

    def get_cell_position(self, week: int, day: int) -> tuple[int, int]:
        """
        Get the pixel position (x, y) of a cell.

        Args:
            week: Week index
            day: Day index

        Returns:
            Tuple of (x, y) pixel coordinates
        """
        x = self.padding + week * (self.cell_size + self.cell_spacing)
        y = self.padding + day * (self.cell_size + self.cell_spacing)
        return (x, y)

    @staticmethod
    def darkmode() -> "RenderContext":
        """Predefined dark mode rendering context."""
        return RenderContext(
            cell_size=12,
            cell_spacing=2,
            padding=40,
            grid_color=(22, 27, 34),
            enemy_colors={1: (0, 109, 50), 2: (38, 166, 65), 3: (57, 211, 83), 4: (87, 242, 135)},
            ship_color=(88, 166, 255),
            bullet_color=(255, 223, 0),
        )
