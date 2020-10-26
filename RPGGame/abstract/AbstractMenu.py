from abc import ABC, abstractmethod
from typing import List

from RPGGame.MapSegment import MapSegment
from RPGGame.Vector import Vector


class AbstractMenu(ABC):
    @abstractmethod
    def navigate(self, game_map: MapSegment, pos: Vector) -> int:
        ...

    @abstractmethod
    def mainmenu(self) -> int:
        ...

    @abstractmethod
    def select(self, game_map: List[List[str]], options: List[str]) -> int:
        ...
