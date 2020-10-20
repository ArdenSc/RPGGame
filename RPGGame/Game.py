from __future__ import annotations
from RPGGame.abstract.AbstractMenu import AbstractMenu
from typing import Any, List, Literal, overload
from RPGGame.MapSegment import MapSegment
from RPGGame.GameState import GameState, Vector
from os import system
from sys import platform


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


class Game:
    """A semi-modular framework for a terminal rpg game.

    Requires at least maps and a menu, add them using the register method.
    """
    _state: GameState
    _menu: AbstractMenu

    def __init__(self) -> None:
        """Creates an instance of the game framework"""
        self._state = GameState()
        self._register_switch = {
            "menu": self._register_menu,
            "maps": self._register_maps,
        }
        self._dir_switch = {
            0: Vector.North(),
            1: Vector.East(),
            2: Vector.South(),
            3: Vector.West(),
        }

    def _register_menu(self, menu: AbstractMenu) -> None:
        """Internal method for registering a menu"""
        self._menu = menu

    def _register_maps(self, maps: List[List[MapSegment]]) -> None:
        """Internal method for registering maps"""
        self._state.maps = maps

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

    def register(self, type: str, *args: Any) -> None:
        """Base method for registering maps or a handler.
        See overloads for details specific to each registerable item.
        """
        self._register_switch.get(type, _invalid_register_type)(*args)

    def run(self) -> None:
        """Starts the game.
        All requirements must have been registered before calling this method.
        """
        if not hasattr(self, '_menu'):
            raise AttributeError("A Menu is required to run the game.")
        if not hasattr(self._state, 'maps'):
            raise AttributeError("Maps are required to run the game.")
        _terminal_resize(135, 35)
        while 1:
            dir = self._menu.navigate(self._state.map(*self._state.map_pos),
                                      self._state.pos)
            if dir == 4:
                break
            self._state.move(self._dir_switch.get(dir, Vector(0, 0)))
