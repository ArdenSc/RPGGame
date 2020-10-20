from __future__ import annotations
from RPGGame.abstract.AbstractWidget import *
from RPGGame.util import clear
from RPGGame.GameState import Vector
from RPGGame.MapSegment import MapSegment
from RPGGame.KeyPress import GetKeyPress
from typing import List, Literal, Tuple, Union
from os import get_terminal_size
from copy import deepcopy
"""
Scaffold(
    Text('header'),
    Stack(
        justify='space-around',
        Center(
            mode='vertical',
            Text('info'),
        ),
        Center(
            mode='vertical',
            Border(
                Text('map'),
            ),
        ),
    ),
    Center(
        Text('message'),
    ),
)
"""


class Scaffold(DynamicWidget):
    def __init__(self, children: List[AbstractWidget]):
        self.static: List[Tuple[StaticWidget, int]] = []
        self.dynamic: List[Tuple[DynamicWidget, int]] = []

        for i, child in enumerate(children):
            if isinstance(child, StaticWidget):
                self.static.append((child, i))
            elif isinstance(child, DynamicWidget):
                self.dynamic.append((child, i))

    def build_sized(self, width: int, height: int):
        static_builds = [(child[0].build(), child[1]) for child in self.static]
        dynamic_builders = [(child[0].build(), child[1])
                          for child in self.dynamic]
        return []

    def build(self):
        return (self.build_sized, (0, 0))


class Scaffold(DynamicWidget):
    def __init__(self, children: List[AbstractWidget]) -> None:
        self.children = children

    def build_sized(self, width: int, height: int) -> List[str]:
        build_results = [child.build() for child in self.children]
        static: List[Tuple[StaticWidgetData, int]] = []
        dynamic: List[Tuple[DynamicWidgetData, int]] = []
        for i, x in enumerate(build_results):
            dynamic.append((x, i)) if callable(x) else static.append((x, i))
        remain_height = height - sum(x[0][1][1] for x in static)
        children = [(x[0][0], x[1]) for x in static]
        if len(dynamic):
            dynamic_height = remain_height // len(dynamic)
            children += [(x[0](width, dynamic_height), x[1]) for x in dynamic]

        children.sort(key=lambda x: x[1])
        result: List[str] = []
        for child in children:
            result += child[0]
        return result


class Spacer(StaticWidget):
    def __init__(self, lines: int = 1) -> None:
        self.lines = lines

    def build(self):
        result = [''] * self.lines
        width = 0
        height = self.lines
        return (result, (width, height))


class Text(StaticWidget):
    def __init__(self, text: str, max_length: int = 0) -> None:
        self.text = text.split('\n')
        self.max_length = max_length

    def build(self):
        result: List[str] = []
        for line in self.text:
            if self.max_length != 0:
                while line:
                    result += [line[:self.max_length]]
                    line = line[self.max_length:]
            else:
                result += [line]
        width = len(max(result, key=len))
        height = len(result)
        return (result, (width, height))


class Border(StaticWidget):
    def __init__(self, child: StaticWidget):
        self.child = child

    def build(self):
        child_result = self.child.build()
        result = ['\u250C' + '\u2500' * child_result[1][0] + '\u2510']
        result += ['\u2502' + x + '\u2502' for x in child_result[0]]
        result += ['\u2514' + '\u2500' * child_result[1][0] + '\u2518']
        return (result, (child_result[1][0] + 2, child_result[1][1] + 2))


class Center(DynamicWidget):
    def __init__(self,
                 child: StaticWidget,
                 center: Union[Literal['vertical'], Literal['horizontal'],
                               Literal['both']] = 'both'):
        self.child = child
        self.center = center

    def build_sized(self, width: int, height: int):
        child_result = self.child.build()
        if self.center in ('horizontal', 'both'):
            padding = (width - child_result[1][0]) // 2
            child_result = ([(' ' * padding) + line + (' ' * padding)
                             for line in child_result[0]], child_result[1])

        if self.center in ('vertical', 'both'):
            padding = (height - child_result[1][1]) // 2
            child_result = (([''] * padding) + child_result[0] +
                            ([''] * padding), child_result[1])
        width = len(max(child_result[0], key=len))
        height = len(child_result[0])
        return child_result[0]


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

    def display(self, width: int, height: int, widget: AbstractWidget) -> None:
        clear()
        result = widget.build()
        print('\n'.join(
            result(width, height) if callable(result) else result[0]))

    def navigate(self, game_map: MapSegment, pos: Vector) -> int:
        """Waits for a navigational key to be pressed.

        Returns
            int: one of 0-3 where 0 is North and each successive number is
                 clockwise around a compass. Additionally, 4 may be returned
                 and logic should follow that quits the program.
        """
        size = get_terminal_size()
        width, height = size.columns, size.lines

        map_copy = deepcopy(game_map.map)
        x, y = pos
        map_copy[y][x] = "O"

        # yapf: disable
        self.display(
            width, height - 1,
            Scaffold(
                children=[
                    Center(
                        Border(
                            Text('\n'.join(''.join(x) for x in map_copy)),
                        )
                    ),
                ],
            ),
        )
        # yapf: enable

        while True:
            ch = self.getKeyPress()
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
