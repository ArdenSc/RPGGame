from __future__ import annotations
from RPGGame.abstract.AbstractWidget import *
from RPGGame.abstract.AbstractMenu import AbstractMenu
from RPGGame.util import clear
from RPGGame.GameState import Vector
from RPGGame.MapSegment import MapSegment
from RPGGame.KeyPress import GetKeyPress
from typing import List, Literal, Tuple, Union
from os import get_terminal_size
from copy import deepcopy
from functools import partial
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
    def __init__(self, *children: AbstractWidget):
        self.static: List[Tuple[StaticWidget, int]] = []
        self.dynamic: List[Tuple[DynamicWidget, int]] = []

        for i, child in enumerate(children):
            if isinstance(child, StaticWidget):
                self.static.append((child, i))
            elif isinstance(child, DynamicWidget):
                self.dynamic.append((child, i))

    def build_sized(self, width: int, height: int):
        builds = [(child[0].build(), child[1]) for child in self.static]
        dynamic_builders = [(child[0].build(), child[1])
                            for child in self.dynamic]

        remain_height = height
        remain_height -= sum(build[0][1][1] for build in builds)
        remain_height -= sum(builder[0][1][1] for builder in dynamic_builders)

        has_greedy_child = any(builder[0][1][1] == 0
                               for builder in dynamic_builders)

        dynamic_builders = [
            ((partial(builder[0][0],
                      width if builder[0][1][0] == 0 else builder[0][1][0]),
              builder[0][1]), builder[1]) for builder in dynamic_builders
        ]

        if has_greedy_child:
            amount_greedy = len(
                [x for x in dynamic_builders if x[0][1][1] == 0])
            height_per_greedy = remain_height // amount_greedy
            builds += [(builder[0][0](builder[0][1][1]), builder[1])
                       for builder in dynamic_builders
                       if builder[0][1][1] != 0]
            builds += [(builder[0][0](height_per_greedy), builder[1])
                       for builder in dynamic_builders
                       if builder[0][1][1] == 0]
        else:
            height_per_greedy = remain_height // len(dynamic_builders)
            builds += [(builder[0][0](builder[0][1][1] + height_per_greedy),
                        builder[1]) for builder in dynamic_builders]

        builds.sort(key=lambda x: x[1])
        build_result = ['\n'.join(build[0][0]) for build in builds]
        build_dimens = (sum(build[0][1][0] for build in builds),
                        sum(build[0][1][1] for build in builds))

        return (build_result, build_dimens)

    def build(self):
        return (self.build_sized, (0, 0))


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
                 direction: Union[Literal['vertical'], Literal['horizontal'],
                                  Literal['both']] = 'both'):
        self.child = child
        self.direction = direction
        self.child_dimens = self.child.build()[1]

    def build_sized(self, width: int, height: int):
        build = self.child.build()
        if self.direction in ('horizontal', 'both'):
            padding = (width - self.child_dimens[0]) // 2
            build = ([(' ' * padding) + line + (' ') * padding
                      for line in build[0]], build[1])
        if self.direction in ('vertical', 'both'):
            padding = (height - self.child_dimens[1]) // 2
            build = ([''] * padding + build[0] + [''] * padding, build[1])

        build_result = build[0]
        build_dimens = (len(max(build_result, key=len)), len(build_result))
        return (build_result, build_dimens)

    def build(self):
        width = 0 if self.direction in ('horizontal',
                                        'both') else self.child_dimens[0]
        height = 0 if self.direction in ('vertical',
                                         'both') else self.child_dimens[1]
        return (self.build_sized, (width, height))


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
        if isinstance(widget, DynamicWidget):
            builder = widget.build()
            build = builder[0](width, height)
        elif isinstance(widget, StaticWidget):
            build = widget.build()
        else:
            raise AttributeError
        print('\n'.join(build[0]))

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
            width, height,
            Scaffold(
                Spacer(1),
                Center(
                    Text('header'),
                ),
                Center(
                    direction='horizontal',
                    child=Border(
                        Text('\n'.join(''.join(x) for x in map_copy)),
                    ),
                ),
                Center(
                    Text('footer'),
                ),
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
