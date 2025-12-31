"""Animator for generating GIF animations from game strategies."""

from typing import List

from PIL import Image


from ..constants import FRAME_DURATION_MS
from ..github_client import ContributionData
from .game_state import GameState
from .renderer import Renderer
from .strategies.base_strategy import BaseStrategy
from .render_context import RenderContext


class Animator:
    """Generates animated GIFs from game strategies."""

    def __init__(
        self,
        contribution_data: ContributionData,
        strategy: BaseStrategy,
        frame_duration: int = FRAME_DURATION_MS,
    ):
        """
        Initialize animator.

        Args:
            contribution_data: The GitHub contribution data
            strategy: The strategy to use for clearing enemies
            frame_duration: Duration of each frame in milliseconds
        """
        self.contribution_data = contribution_data
        self.strategy = strategy
        self.frame_duration = frame_duration

    def generate_gif(self, output_path: str) -> None:
        """
        Generate animated GIF and save to file.

        Args:
            output_path: Path where GIF should be saved
        """
        # Initialize game state
        game_state = GameState(self.contribution_data)
        renderer = Renderer(game_state, RenderContext.darkmode())

        frames = self._generate_frames(game_state, renderer)

        # Save as GIF
        if frames:
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=self.frame_duration,
                loop=0,  # Loop forever
                optimize=False,
            )

    def _generate_frames(
        self, game_state: GameState, renderer: Renderer
    ) -> List[Image.Image]:
        """
        Generate all animation frames.

        Args:
            game_state: The game state
            renderer: The renderer

        Returns:
            List of PIL Images representing animation frames
        """
        frames = []

        # Add initial frame showing starting state
        frames.append(renderer.render_frame())

        # Process each action from the strategy
        for action in self.strategy.generate_actions(self.contribution_data):
            game_state.ship.move_to(action.week)
            while game_state.can_take_action() is False:
                game_state.animate()
                frames.append(renderer.render_frame())

            if action.shoot:
                game_state.shoot()
                game_state.animate()
                frames.append(renderer.render_frame())

        # Add final frames showing completion
        while not game_state.is_complete():
            game_state.animate()
        for _ in range(5):
            frames.append(renderer.render_frame())

        return frames
