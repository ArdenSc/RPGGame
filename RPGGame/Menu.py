from __future__ import annotations
from RPGGame.util import clear
from RPGGame.abstract.AbstractMenu import AbstractMenu
from RPGGame.GameState import Vector
from RPGGame.MapSegment import MapSegment
from RPGGame.KeyPress import GetKeyPress
from typing import Callable, List, Union
from os import get_terminal_size
from copy import deepcopy
from functools import partial


def uniformLineLengths(map: List[List[str]]) -> List[List[str]]:
    columns = len(max(map, key=len))
    return [line + [' '] * (columns - len(line)) for line in map]


class Menu(AbstractMenu):
    def __init__(
        self,
        horizontalPad: int = 10,
        middlePadding: int = 10,
    ) -> None:
        """Displays a well-formatted menu.
        See method docstrings for more details.

        Args:
            horizontalPad: Amount of spaces on the left and right of the menu.
            middlePadding: Amount of spaces between the menu and map/image.
        """
        self.horizontalPad = horizontalPad
        self.middlePadding = middlePadding
        self.getKeyPress = GetKeyPress()

    def navigate(self, game_map: MapSegment, pos: Vector) -> int:
        """Waits for a navigational key to be pressed.

        Returns
            int: one of 0-3 where 0 is North and each successive number is
                 clockwise around a compass. Additionally, 4 may be returned
                 and logic should follow that quits the program.
        """
        width = get_terminal_size().columns - self.horizontalPad * 2

        display_lines = []

        map_copy = deepcopy(game_map.map)
        x, y = pos
        map_copy[y][x] = "O"

        def spacer(i: int) -> str:
            return ""

        def dist_horizontal(args: List[Union[str, Callable[[int], str]]],
                            i: int) -> str:
            extra_space = width
            strings = [arg(i) if callable(arg) else arg for arg in args]
            for string in strings:
                extra_space -= len(string)
            spacer = ' ' * (extra_space // (len(args) - 1))
            return spacer.join(strings)

        def map(i: int) -> str:
            return ''.join(map_copy[i])

        def nav_info(i: int) -> str:
            menu = [
                r"              ",
                r"              ",
                r"              ",
                r"              ",
                r"              ",
                r"              ",
                r"              ",
                r"  W ---- Up   ",
                r"A S D -- Right",
                r" \ \---- Down ",
                r"  \----- Left ",
                r"  Q ---- Quit ",
            ]
            try:
                return menu[i]
            except IndexError:
                return menu[0]

        segments = [
            (5, spacer),
            (len(map_copy), partial(dist_horizontal, [nav_info, map])),
            (1, spacer),
        ]

        for segment in segments:
            for i in range(segment[0]):
                display_lines.append(" " * self.horizontalPad + segment[1](i))

        clear()
        print('\n'.join(display_lines), end="")

        while True:
            ch = self.getKeyPress()
            if ch:
                if ch == 'w':
                    return 0
                elif ch == 'd':
                    return 1
                elif ch == 's':
                    return 2
                elif ch == 'a':
                    return 3
                elif ch == 'q':
                    return 4

    def select(self, game_map: List[List[str]], options: List[str]) -> int:
        termSize = get_terminal_size()
        game_map = uniformLineLengths(game_map)
        mapColumns = len(game_map[0])
        options = [f"{i+1}. {v}" for i, v in enumerate(options)]
        maxOption = len(options) + 1
        out: str = ""
        maxOptionLength = (termSize.columns - mapColumns - self.horizontalPad -
                           self.middlePadding - self.horizontalPad - 2)
        out += ' ' * (self.horizontalPad + maxOptionLength +
                      self.middlePadding)
        out += '\u250C' + '\u2500' * mapColumns + '\u2510'
        out += ' ' * (self.horizontalPad)
        for i, line in enumerate(game_map):
            out += ' ' * (self.horizontalPad)
            if i % 2 != 0 and len(options) != 0:
                optionString = options.pop(0)[:maxOptionLength]
                out += optionString
                out += ' ' * (maxOptionLength - len(optionString))
            else:
                out += ' ' * (maxOptionLength)
            out += ' ' * (self.middlePadding)
            out += '\u2502' + ''.join(line) + '\u2502'
            out += ' ' * (self.horizontalPad)
        out += ' ' * (self.horizontalPad + maxOptionLength +
                      self.middlePadding)
        out += '\u2514' + '\u2500' * mapColumns + '\u2518'
        out += ' ' * (self.horizontalPad)
        message = "Choose an option from above"
        while True:
            clear()
            print(out)
            print('\033[F' * 3 + ' ' * self.horizontalPad + message)
            response = input(' ' * self.horizontalPad + "> ")
            if str.isdigit(response) and 0 < int(response) < maxOption:
                clear()
                return int(response) - 1
            message = "Sorry, please choose a valid number"
