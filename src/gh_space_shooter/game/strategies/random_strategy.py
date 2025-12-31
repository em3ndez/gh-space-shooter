"""Random strategy: Pick random columns and shoot from bottom up."""

import random
from typing import TYPE_CHECKING, Iterator

from .base_strategy import Action, BaseStrategy

if TYPE_CHECKING:
    from ..game_state import GameState


class RandomStrategy(BaseStrategy):
    """
    Ship picks random columns with living enemies and shoots the bottom-most enemy.

    This creates an unpredictable clearing pattern, shooting enemies from
    bottom to top in randomly selected columns.
    """

    def generate_actions(self, game_state: "GameState") -> Iterator[Action]:
        """
        Generate actions by randomly selecting columns and shooting bottom enemies.

        The ship continuously picks a random column (week) that has living enemies,
        then shoots at the bottom-most enemy (highest y value) in that column.

        Args:
            game_state: The current game state with living enemies

        Yields:
            Action objects representing ship movements and shots
        """
        while game_state.enemies:
            columns_with_enemies = list(set(e.x for e in game_state.enemies))
            target_column = random.choice(columns_with_enemies)

            enemies_in_column = [e for e in game_state.enemies if e.x == target_column]
            lowest_enemy = max(enemies_in_column, key=lambda e: e.y)

            for _ in range(lowest_enemy.health):
                yield Action(x=target_column, shoot=True)
