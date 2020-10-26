from __future__ import annotations

from typing import List, Union

from typing_extensions import Literal

from RPGGame.abstract.AbstractEnemy import AbstractEnemy
from RPGGame.abstract.AbstractMenu import AbstractMenu
from RPGGame.Inventory import Inventory
from RPGGame.MapSegment import MapSegment
from RPGGame.Vector import Vector

GameplayState = Union[Literal['start'], Literal['navigate'], Literal['fight'],
                      Literal['inventory']]


class GameState:
    maps: List[List[MapSegment]]
    menu: AbstractMenu
    target: AbstractEnemy
    gameplay_state: GameplayState

    def __init__(self):
        self.map_pos = Vector(0, 0)
        self.pos = Vector(5, 3)
        self.inventory = Inventory()
        self.health = 100
        self.gameplay_state = 'start'

    def get_map(self, x: int, y: int) -> MapSegment:
        return self.maps[y][x]
