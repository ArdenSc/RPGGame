from __future__ import annotations

from copy import deepcopy
from functools import partial
from itertools import zip_longest
from os import get_terminal_size
from typing import List, Tuple, Union

from typing_extensions import Literal

from RPGGame.abstract.AbstractMenu import AbstractMenu
from RPGGame.abstract.AbstractWidget import *
from RPGGame.KeyPress import GetKeyPress
from RPGGame.MapSegment import MapSegment
from RPGGame.util import clear
from RPGGame.Vector import Vector

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


def uniform_line_lengths(lines: List[str], columns: int) -> List[str]:
    return [x + ' ' * (columns - len(x)) for x in lines]


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


class Stack(DynamicWidget):
    def __init__(self, *children: AbstractWidget):
        self.static: List[Tuple[StaticWidget, int]] = []
        self.dynamic: List[Tuple[DynamicWidget, int]] = []

        for i, child in enumerate(children):
            if isinstance(child, StaticWidget):
                self.static.append((child, i))
            elif isinstance(child, DynamicWidget):
                self.dynamic.append((child, i))

    def build_sized(self, width: int, height: int) -> StaticWidgetData:
        remain_width = width
        remain_width -= sum(build[0][1][0] for build in self.builds)
        remain_width -= sum(builder[0][1][0] for builder in self.builds)

        has_greedy_child = any(builder[0][1][0] == 0
                               for builder in self.dynamic_builders)

        self.dynamic_builders = [((partial(
            builder[0][0],
            height=height if builder[0][1][1] == 0 else builder[0][1][1]),
                                   builder[0][1]), builder[1])
                                 for builder in self.dynamic_builders]

        if has_greedy_child:
            amount_greedy = len(
                [x for x in self.dynamic_builders if x[0][1][0] == 0])
            width_per_greedy = remain_width // amount_greedy
            self.builds += [(builder[0][0](builder[0][1][1]), builder[1])
                            for builder in self.dynamic_builders
                            if builder[0][1][0] != 0]
            self.builds += [(builder[0][0](width_per_greedy), builder[1])
                            for builder in self.dynamic_builders
                            if builder[0][1][0] == 0]
        else:
            width_per_greedy = remain_width // len(self.dynamic_builders)
            self.builds += [
                (builder[0][0](builder[0][1][0] + width_per_greedy),
                 builder[1]) for builder in self.dynamic_builders
            ]

        self.builds.sort(key=lambda x: x[1])
        child_widths = [
            len(max(build[0][0], key=len)) for build in self.builds
        ]
        build_result = [
            ''.join([
                x if x != None else ' ' * child_widths[i]
                for i, x in enumerate(line)
            ]) for line in zip_longest(*[build[0][0] for build in self.builds])
        ]
        build_dimens = (sum(build[0][1][0] for build in self.builds),
                        max(build[0][1][1] for build in self.builds))
        return (build_result, build_dimens)

    def build(self) -> DynamicWidgetData:
        self.builds = [(child[0].build(), child[1]) for child in self.static]
        self.dynamic_builders = [(child[0].build(), child[1])
                                 for child in self.dynamic]
        self.height = max(
            [build[0][1][1] for build in self.builds] +
            [builder[0][1][1] for builder in self.dynamic_builders])
        return (self.build_sized, (0, self.height))


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

    def mainmenu(self) -> int:
        size = get_terminal_size()
        width, height = size.columns, size.lines

        # yapf: disable
        self.display(
            width,
            height,
            Scaffold(
                Center(
                    Text(r"""
 _____  _____   _____
|  __ \|  __ \ / ____|
| |__) | |__) | |  __  __ _ _ __ ___   ___
|  _  /|  ___/| | |_ |/ _` | '_ ` _ \ / _ \
| | \ \| |    | |__| | (_| | | | | | |  __/
|_|  \_\_|     \_____|\__,_|_| |_| |_|\___|

"""),
                ),
                Center(
                    direction="horizontal",
                    child=Text("Press any key to Start. Q to Quit"),
                ),
            ),
        )
        # yapf: enable

        while True:
            ch = self.getKeyPress()
            if ch == 'q':
                return 1
            else:
                return 0

    def navigate(self, game_map: MapSegment, pos: Vector) -> int:
        """Waits for a navigational key to be pressed.

        Returns
            int: one of 0-3 where 0 is North and each successive number is
                 clockwise around a compass. Additionally, 4 may be returned
                 and logic should follow that quits the program.
        """
        size = get_terminal_size()
        width, height = size.columns, size.lines

        map_copy = deepcopy(game_map.get())
        x, y = pos
        map_copy[y][x] = "O"

        # yapf: disable
        self.display(
            width, height,
            Scaffold(
                Spacer(),
                Center(
                    Text('header'),
                ),
                Stack(
                    Text('info\ninfo\ninfo\ninfo'),
                    Center(
                        direction="horizontal",
                        child=Border(
                            Text('\n'.join(''.join(x) for x in map_copy)),
                        ),
                    )
                ),
                Center(
                    Text('message'),
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
