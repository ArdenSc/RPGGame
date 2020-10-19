from typing import List
from RPGGame.GameState import Vector
from RPGGame.MapSegment import MapSegment
from abc import ABC, abstractmethod


class AbstractMenu(ABC):
    @abstractmethod
    def navigate(self, game_map: MapSegment, pos: Vector) -> int:
        ...

    @abstractmethod
    def select(self, game_map: List[List[str]], options: List[str]) -> int:
        ...
