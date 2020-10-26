from abc import ABC, abstractmethod

from RPGGame.GameState import GameState


class AbstractBehaviorHandler(ABC):
    @abstractmethod
    def on_move_callback(self, state: GameState) -> None:
        ...
