from __future__ import annotations
from copy import deepcopy

from os import system
from sys import platform
from typing import Any, List, overload

from typing_extensions import Literal

from RPGGame.abstract.AbstractBehaviorHandler import AbstractBehaviorHandler
from RPGGame.abstract.AbstractMenu import AbstractMenu
from RPGGame.GameState import GameState, Vector
from RPGGame.MapSegment import MapSegment


class StopGame(Exception):
    ...


def _terminal_resize(columns: int, lines: int):
    """Internal function that resizes the terminal to the specific dimensions.

    Args:
        columns: The amount of vertical columns.
        lines: The amount of horizontal lines.
    """
    if platform == 'win32':
        system(f"mode con: cols={columns} lines={lines}")
    else:
        system(f"resize -s {columns} {lines}")


def _invalid_register_type():
    """Internal function to be used as a default value for the
    register_switch in the Game class.
    """
    raise AttributeError("Invalid type registered to Game object.")


def _invalid_gameplay_state():
    raise AttributeError("Invalid gameplay state.")


class Game:
    """A semi-modular framework for a terminal rpg game.

    Requires at least maps and a menu, add them using the register method.
    """
    _state: GameState

    def __init__(self) -> None:
        """Creates an instance of the game framework"""
        self._state = GameState()
        self._register_switch = {
            "menu": self._register_menu,
            "maps": self._register_maps,
            "behaviors": self._register_behaviors,
        }
        self._dir_switch = {
            0: Vector.North(),
            1: Vector.East(),
            2: Vector.South(),
            3: Vector.West(),
        }
        self._state_switch = {
            "start": self._mainmenu,
            "navigate": self._navigate,
            "fight": lambda: None,
            "inventory": lambda: None,
        }

    def _register_menu(self, menu: AbstractMenu) -> None:
        """Internal method for registering a menu"""
        self._state.menu = menu

    def _register_maps(self, maps: List[List[MapSegment]]) -> None:
        """Internal method for registering maps"""
        self._state.maps = maps

    def _register_behaviors(self, handler: AbstractBehaviorHandler) -> None:
        self._behaviors = handler

    @overload
    def register(self, type: Literal['menu'], menu: AbstractMenu) -> None:
        """Registers a menu handler to the game.

        Args:
            type: Must be a string of value 'menu'.
            menu: An instance of an AbstractMenu subclass.
        """
        ...

    @overload
    def register(self, type: Literal['maps'],
                 maps: List[List[MapSegment]]) -> None:
        """Registers maps to the game.

        Args:
            type: Must be a string of value 'maps'.
            maps: 2D list of MapSegments.
        """
        ...

    @overload
    def register(self, type: Literal['behaviors'],
                 handler: AbstractBehaviorHandler) -> None:
        ...

    def register(self, type: str, *args: Any) -> None:
        """Base method for registering maps or a handler.
        See overloads for details specific to each registerable item.
        """
        self._register_switch.get(type, _invalid_register_type)(*args)

    def _navigate(self) -> None:
        dir = self._state.menu.navigate(
            self._state.get_map(*self._state.map_pos), self._state.pos)
        if dir == 4:
            raise StopGame
        self._move(self._dir_switch[dir])
        self._behaviors.on_move_callback(self._state)

    def _mainmenu(self) -> None:
        result = self._state.menu.mainmenu()
        if result == 1:
            raise StopGame
        self._state.gameplay_state = "navigate"

    def _move(self, movement: Vector):
        old_pos = deepcopy(self._state.pos)
        self._state.pos += movement
        x, y = self._state.pos
        mx, my = self._state.map_pos
        if x < 0:
            if mx >= 1:
                self._state.map_pos += Vector(-1, 0)
                self._state.pos[0] = self._state.get_map(mx - 1, my).width - 1
            else:
                self.pos = old_pos
        elif x >= self._state.get_map(mx, my).width:
            if mx + 1 < len(self._state.maps[0]):
                self._state.map_pos += Vector(1, 0)
                self._state.pos[0] = 0
            else:
                self._state.pos = old_pos
        if y < 0:
            if my >= 1:
                self._state.map_pos += Vector(0, -1)
                self._state.pos[1] = self._state.get_map(mx, my - 1).height - 1
            else:
                self._state.pos = old_pos
        elif y >= self._state.get_map(mx, my).height:
            if my + 1 < len(self._state.maps):
                self._state.map_pos += Vector(0, 1)
                self._state.pos[1] = 0
            else:
                self._state.pos = old_pos

        if self._state.get_map(*self._state.map_pos).get(
                *self._state.pos) in ('▀', '▌', '▁', '▔', '▄', '█', '▛', '▜',
                                      '▙', '▟', '▐'):
            self._state.pos = old_pos

    def run(self) -> None:
        """Starts the game.
        All requirements must have been registered before calling this method.
        """
        if not hasattr(self._state, 'menu'):
            raise AttributeError("A Menu is required to run the game.")
        if not hasattr(self._state, 'maps'):
            raise AttributeError("Maps are required to run the game.")
        _terminal_resize(135, 35)
        while True:
            try:
                self._state_switch.get(self._state.gameplay_state,
                                       _invalid_gameplay_state)()
            except StopGame:
                break
