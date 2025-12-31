"""Game state management for tracking enemies, ship, and bullets."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

from PIL import ImageDraw

from ..constants import BULLET_SPEED, NUM_DAYS, NUM_WEEKS, SHIP_POSITION_Y, SHIP_SPEED
from ..github_client import ContributionData

if TYPE_CHECKING:
    from .render_context import RenderContext

class Drawable(ABC):
    """Interface for objects that can be animated and drawn."""

    @abstractmethod
    def animate(self) -> None:
        """Update the object's state for the next animation frame."""
        pass

    @abstractmethod
    def draw(self, draw: ImageDraw.ImageDraw, context: "RenderContext") -> None:
        """
        Draw the object on the image.

        Args:
            draw: PIL ImageDraw object
            context: Rendering context with helper functions and constants
        """
        pass


class Enemy(Drawable):
    """Represents an enemy at a specific position."""

    def __init__(self, x: int, y: int, health: int, game_state: "GameState"):
        """
        Initialize an enemy.

        Args:
            x: Week position in contribution grid (0-51)
            y: Day position in contribution grid (0-6, Sun-Sat)
            health: Initial health/lives (1-4)
            game_state: Reference to game state for self-removal when destroyed
        """
        self.x = x
        self.y = y
        self.health = health
        self.game_state = game_state

    def take_damage(self) -> None:
        """
        Enemy takes 1 damage and removes itself from game if destroyed.
        """
        self.health -= 1
        if self.health <= 0:
            self.game_state.enemies.remove(self)

    def animate(self) -> None:
        """Update enemy state for next frame (enemies don't animate currently)."""
        pass

    def draw(self, draw: ImageDraw.ImageDraw, context: "RenderContext") -> None:
        """Draw the enemy at its position."""        
        x, y = context.get_cell_position(self.x, self.y)
        color = context.enemy_colors.get(self.health, context.enemy_colors[1])

        draw.rectangle(
            [x, y, x + context.cell_size, y + context.cell_size],
            fill=color,
        )


class Bullet(Drawable):
    """Represents a bullet fired by the ship."""

    def __init__(self, x: int, game_state: "GameState"):
        """
        Initialize a bullet at ship's firing position.

        Args:
            x: Week position where bullet is fired (0-51)
            game_state: Reference to game state for collision detection and self-removal
        """
        self.x = x
        self.y: float = SHIP_POSITION_Y - 1
        self.game_state = game_state


    def _check_collision(self) -> Enemy | None:
        """Check if bullet has hit an enemy at its current position."""
        for enemy in self.game_state.enemies:
            if enemy.x == self.x and enemy.y >= self.y:
                return enemy
        return None

    def animate(self) -> None:
        """Update bullet position, check for collisions, and remove on hit."""
        self.y -= BULLET_SPEED
        hit_enemy = self._check_collision()
        if hit_enemy:
            hit_enemy.take_damage()
            self.game_state.bullets.remove(self)

    def draw(self, draw: ImageDraw.ImageDraw, context: "RenderContext") -> None:
        """Draw the bullet at its animated position."""
        x, y = context.get_cell_position(self.x, self.y)
        x += context.cell_size // 2
        y += context.cell_size // 2

        radius = 3
        draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=context.bullet_color,
        )


class Ship(Drawable):
    """Represents the player's ship."""

    def __init__(self, game_state: "GameState"):
        """Initialize the ship at starting position."""
        self.x: float = 25  # Start middle of screen
        self.target_x = self.x
        self.game_state = game_state

    def move_to(self, x: int):
        """
        Move ship to a new x position.

        Args:
            x: Target x position
        """
        self.target_x = x

    def is_moving(self) -> bool:
        """Check if ship is moving to a new position."""
        return self.x != self.target_x

    def animate(self) -> None:
        """Update ship position, moving toward target at constant speed."""
        if self.x < self.target_x:
            self.x = min(self.x + SHIP_SPEED, self.target_x)
        elif self.x > self.target_x:
            self.x = max(self.x - SHIP_SPEED, self.target_x)

    def draw(self, draw: ImageDraw.ImageDraw, context: "RenderContext") -> None:
        """Draw the ship below the grid."""
        # Ship stays below the grid at a fixed vertical position
        x, y = context.get_cell_position(self.x, SHIP_POSITION_Y)

        # Draw simple ship shape (triangle pointing up)
        draw.polygon(
            [
                (x + context.cell_size // 2, y),  # Top point (front)
                (x, y + context.cell_size),  # Bottom left
                (x + context.cell_size, y + context.cell_size),  # Bottom right
            ],
            fill=context.ship_color,
        )


class GameState(Drawable):
    """Manages the current state of the game."""

    def __init__(self, contribution_data: ContributionData):
        """
        Initialize game state from contribution data.

        Args:
            contribution_data: The GitHub contribution data
        """
        self.contribution_data = contribution_data
        self.ship = Ship(self)
        self.enemies: List[Enemy] = []
        self.bullets: List[Bullet] = []

        # Initialize enemies from contribution data
        self._initialize_enemies()

    def _initialize_enemies(self):
        """Create enemies based on contribution levels."""
        weeks = self.contribution_data["weeks"]
        for week_idx, week in enumerate(weeks):
            for day_idx, day in enumerate(week["days"]):
                level = day["level"]
                if level <= 0:
                    continue
                enemy = Enemy(x=week_idx, y=day_idx, health=level, game_state=self)
                self.enemies.append(enemy)

    def shoot(self) -> None:
        """
        Ship shoots a bullet at target position.
        """
        bullet = Bullet(int(self.ship.x), game_state=self)
        self.bullets.append(bullet)

    def is_complete(self) -> bool:
        """Check if game is complete (all enemies destroyed)."""
        return len(self.enemies) == 0

    def can_take_action(self) -> bool:
        """Check if ship can take an action (not moving)."""
        return not self.ship.is_moving()

    def animate(self) -> None:
        """Update all game objects for next frame."""
        self.ship.animate()
        for enemy in self.enemies:
            enemy.animate()
        for bullet in self.bullets:
            bullet.animate()

    def draw(self, draw: ImageDraw.ImageDraw, context: "RenderContext") -> None:
        """Draw all game objects including the grid."""
        self._draw_grid(draw, context)
        for enemy in self.enemies:
            enemy.draw(draw, context)
        for bullet in self.bullets:
            bullet.draw(draw, context)
        self.ship.draw(draw, context)

    def _draw_grid(self, draw: ImageDraw.ImageDraw, context: "RenderContext") -> None:
        """Draw the empty grid cells."""
        for week in range(NUM_WEEKS):
            for day in range(NUM_DAYS):
                x, y = context.get_cell_position(week, day)
                draw.rectangle(
                    [x, y, x + context.cell_size, y + context.cell_size],
                    fill=context.grid_color,
                )
