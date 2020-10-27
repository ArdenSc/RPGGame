from __future__ import annotations

from typing import TYPE_CHECKING

from RPGGame.abstract.AbstractGameState import AbstractGameState
from RPGGame.Player import Player
from RPGGame.Vector import Vector

if TYPE_CHECKING:
    from RPGGame.MapSegment import MapSegment


class GameState(AbstractGameState):
    """Stores all information about an active game session."""
    def __init__(self):
        """Initializes the game state with default values."""
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
        """Returns a map segment at the specified coordinates.

        Args:
            x: the x-coordinate of the map.
            y: the y-coordinate of the map.
        """
        return self.maps[y][x]

    def get_map_name(self, x: int, y: int) -> str:
        """Returns the map name at the specified coordinates.

        Args:
            x: the x-coordinate of the map.
            y: the y-coordinate of the map.
        """
        return self.map_names[y][x]
