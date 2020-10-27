from __future__ import annotations

from typing import TYPE_CHECKING

from RPGGame.abstract.AbstractGameState import AbstractGameState
from RPGGame.Player import Player
from RPGGame.Vector import Vector

if TYPE_CHECKING:
    from RPGGame.MapSegment import MapSegment


class GameState(AbstractGameState):
    def __init__(self):
        self.map_pos = Vector(0, 0)
        self.pos = Vector(5, 3)
        self.player = Player()
        self.gameplay_state = 'start'
        self.fight_state = None
        self.message = ''
        self.message_timeout = 0
        self.pending_messages = []
        self.pending_message_timeouts = []

    def get_map(self, x: int, y: int) -> MapSegment:
        return self.maps[y][x]

    def get_map_name(self, x: int, y: int) -> str:
        return self.map_names[y][x]
