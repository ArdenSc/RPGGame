from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from RPGGame.abstract.AbstractGameState import AbstractGameState


class AbstractBehaviorHandler(ABC):
    """Dispatches all game behaviors triggered by the player position.

    Must be extended by an actual implementation.
    """
    @abstractmethod
    def on_move_callback(self, state: AbstractGameState) -> None:
        """To be called when a movement is made"""
        ...
