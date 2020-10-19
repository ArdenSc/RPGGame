from __future__ import annotations
from RPGGame.abstract.AbstractMenu import AbstractMenu
from typing import Any, List, Literal, overload
from RPGGame.MapSegment import MapSegment
from RPGGame.GameState import GameState, Vector
from os import system
from sys import platform


def terminal_resize(columns: int, lines: int):
    if platform == 'win32':
        system(f"mode con: cols={columns} lines={lines}")
    else:
        system(f"resize -s {columns} {lines}")


def invalid_register_type():
    raise AttributeError("Invalid type registered to Game object.")


class Game:
    _state: GameState
    _menu: AbstractMenu

    def __init__(self) -> None:
        self._state = GameState()
        self.register_switch = {
            "menu": self.register_menu,
            "maps": self.register_maps,
        }
        self.dir_switch = {
            0: Vector.North(),
            1: Vector.East(),
            2: Vector.South(),
            3: Vector.West(),
        }

    def register_menu(self, menu: AbstractMenu) -> None:
        self._menu = menu

    def register_maps(self, maps: List[List[MapSegment]]) -> None:
        self._state.maps = maps

    @overload
    def register(self, type: Literal['menu'], menu: AbstractMenu) -> None:
        ...

    @overload
    def register(self, type: Literal['maps'],
                 maps: List[List[MapSegment]]) -> None:
        ...

    def register(self, type: str, *args: Any) -> None:
        self.register_switch.get(type, invalid_register_type)(*args)

    def run(self) -> None:
        if not hasattr(self, '_menu'):
            raise AttributeError("A Menu is required to run the game.")
        if not hasattr(self._state, 'maps'):
            raise AttributeError("Maps are required to run the game.")
        terminal_resize(135, 35)
        while 1:
            dir = self._menu.navigate(self._state.map(*self._state.map_pos),
                                      self._state.pos)
            if dir == 4:
                break
            self._state.move(self.dir_switch.get(dir, Vector(0, 0)))
