from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from typing_extensions import TypedDict

if TYPE_CHECKING:
    from typing import List, Optional

    from RPGGame.Enemy import Enemy
    from RPGGame.MapSegment import MapSegment
    from RPGGame.Player import Player
    from RPGGame.Vector import Vector
    from typing_extensions import Literal

    GameplayState = Literal['start', 'navigate', 'fight']


class FightState(TypedDict):
    menu: Literal['action', 'attack', 'heal']
    run_failed: bool
    amt_options: int


class AbstractGameState(ABC):
    """Stores all information about an active game session.

    Must be extended by an actual implementation.
    """
    maps: List[List[MapSegment]]
    map_names: List[List[str]]
    target: Enemy
    gameplay_state: GameplayState
    player: Player
    message: str
    message_timeout: int
    pending_messages: List[str]
    pending_message_timeouts: List[int]
    map_pos: Vector
    pos: Vector
    fight_state: Optional[FightState]

    @abstractmethod
    def get_map(self, x: int, y: int) -> MapSegment:
        """Returns the map at the specified coordinates."""
        ...

    @abstractmethod
    def get_map_name(self, x: int, y: int) -> str:
        """Returns the map name at the specified coordinates."""
        ...
