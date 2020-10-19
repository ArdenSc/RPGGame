from __future__ import annotations
from functools import partial
from RPGGame.util import clear
from RPGGame.abstract.AbstractWidget import AbstractWidget
from RPGGame.abstract.AbstractMenu import AbstractMenu
from RPGGame.GameState import Vector
from RPGGame.MapSegment import MapSegment
from RPGGame.KeyPress import GetKeyPress
from typing import Callable, List, Tuple, Union
from os import get_terminal_size
from copy import deepcopy


def uniformLineLengths(map: List[List[str]]) -> List[List[str]]:
    columns = len(max(map, key=len))
    return [line + [' '] * (columns - len(line)) for line in map]


def spacer(i: int) -> str:
    return ""


def dist_horizontal(args: List[Union[str, Callable[[int], str]]], width: int,
                    i: int) -> str:
    strings = [arg(i) if callable(arg) else arg for arg in args]
    extra_space = width - sum(len(string) for string in strings)
    spacer = ' ' * (extra_space // (len(args) - 1))
    return spacer.join(strings)


def border(arg: Union[str, Callable[[int], str]], inner_width: int,
           inner_height: int, i: int) -> str:
    if i == 0:
        return '\u250C' + '\u2500' * inner_width + '\u2510'
    elif i == inner_height + 1:
        return '\u2514' + '\u2500' * inner_width + '\u2518'
    else:
        return '\u2502' + (arg(i - 1) if callable(arg) else arg) + '\u2502'


def map(map: List[List[str]], i: int) -> str:
    return ''.join(map[i])


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


class Scaffold(AbstractWidget):
    def __init__(self, children: List[AbstractWidget]) -> None:
        self.children = children
        self.lengths = [len(child) for child in children]

    def __len__(self) -> int:
        return sum(self.lengths)

    def build(self, i: int) -> str:
        for child, length in zip(self.children, self.lengths):
            if i < length:
                return child.build(i)
            else:
                i -= length
        raise AssertionError("Code should never be reached")


class Spacer(AbstractWidget):
    def __init__(self, lines: int = 1) -> None:
        self.lines = lines

    def __len__(self) -> int:
        return self.lines

    def build(self, i: int) -> str:
        return ''

class Text(AbstractWidget):
    def __init__(self, text: str) -> None:
        self.text = text

    def __len__(self) -> int:
        return 1

    def build(self, i: int) -> str:
        return self.text


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

        segments: List[Tuple[int, Callable[[int], str]]] = [
            (5, spacer),
            (len(map_copy) + 2, lambda i: dist_horizontal([
                nav_info,
                border(partial(map, map_copy), len(game_map.map[0]),
                       len(game_map.map), i)
            ], width, i)),
            (1, spacer),
        ]

        for segment in segments:
            for i in range(segment[0]):
                display_lines.append(" " * self.horizontalPad + segment[1](i))

        # yapf: disable
        # display: List[AbstractWidget] = [
        #     Scaffold(
        #         children=[
        #             Spacer(5),
        #             Text("Hello World!"),
        #         ],
        #     ),
        # ]
        # yapf: enable

        # for child in display:
        #     for i in range(len(child)):
        #         display_lines.append(child.build(i))

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
            if i % 2 == 0 or not options:
                out += ' ' * (maxOptionLength)
            else:
                optionString = options.pop(0)[:maxOptionLength]
                out += optionString
                out += ' ' * (maxOptionLength - len(optionString))
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
