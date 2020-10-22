from abc import ABC, abstractmethod

from RPGGame.GameState import GameState
from RPGGame.Vector import Vector


class AbstractBehaviorHandler(ABC):
    @abstractmethod
    def on_move_callback(self, state: GameState, pos: Vector) -> None:
        ...
