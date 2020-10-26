from abc import ABC, abstractmethod

from RPGGame.MapSegment import MapSegment
from RPGGame.Vector import Vector


class AbstractMenu(ABC):
    @abstractmethod
    def navigate(self, game_map: MapSegment, pos: Vector) -> int:
        ...

    @abstractmethod
    def mainmenu(self) -> int:
        ...
