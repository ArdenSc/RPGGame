from __future__ import annotations
from RPGGame.GameState import Vector
from RPGGame.MapSegment import MapSegment
from RPGGame.KeyPress import GetKeyPress
from typing import Callable, List
from os import get_terminal_size, system
from typing_extensions import TypedDict
from copy import deepcopy


class ScreenSegment(TypedDict):
    lines: int
    getLine: Callable[[int], str]


class Menu:
    def __init__(
        self,
        leftPadding: int = 10,
        middlePadding: int = 10,
        rightPadding: int = 10,
    ) -> None:
        """Displays a well-formatted menu.
        See method docstrings for more details.

        Args:
            leftPadding: Amount of spaces on the left of the menu.
            middlePadding: Amount of spaces between the menu and map/image.
            rightPadding: Amount of spaces on the right of the map/image.
        """
        self.leftPadding = leftPadding
        self.middlePadding = middlePadding
        self.rightPadding = rightPadding
        self.getKeyPress = GetKeyPress()

    @staticmethod
    def uniformLineLengths(map: List[List[str]]) -> List[List[str]]:
        columns = len(max(map, key=len))
        return [line + [' '] * (columns - len(line)) for line in map]

    def navigation(self, map: MapSegment, player_position: Vector[int]) -> int:
        """Waits for a navigational key to be pressed.

        Returns
            int: one of 0-3 where 0 is North and each successive number is
                 clockwise around a compass. Additionally, 4 may be returned
                 and logic should follow that quits the program.
        """
        # termSize = get_terminal_size()
        # t_width, t_height = termSize.columns, termSize.lines

        display_lines = []

        map_copy = deepcopy(map.map)
        map_copy[player_position[1]][player_position[0]] = "O"

        def spacer(i: int) -> str:
            return ""

        def right_map(i: int) -> str:
            return ''.join(map_copy[i])

        segments: List[ScreenSegment] = [
            {
                "lines": 5,
                "getLine": spacer,
            },
            {
                "lines": len(map_copy),
                "getLine": right_map,
            },
            {
                "lines": 1,
                "getLine": spacer,
            },
        ]

        for segment in segments:
            for i in range(segment["lines"]):
                display_lines.append(segment["getLine"](i))

        system('cls')
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

    def optionSelector(self, map: List[List[str]], options: List[str]) -> int:
        termSize = get_terminal_size()
        map = self.uniformLineLengths(map)
        mapColumns = len(map[0])
        options = [f"{i+1}. {v}" for i, v in enumerate(options)]
        maxOption = len(options) + 1
        out: str = ""
        maxOptionLength = (termSize.columns - mapColumns - self.leftPadding -
                           self.middlePadding - self.rightPadding - 2)
        out += ' ' * (self.leftPadding + maxOptionLength + self.middlePadding)
        out += '\u250C' + '\u2500' * mapColumns + '\u2510'
        out += ' ' * (self.rightPadding)
        for i, line in enumerate(map):
            out += ' ' * (self.leftPadding)
            if i % 2 != 0 and len(options) != 0:
                optionString = options.pop(0)[:maxOptionLength]
                out += optionString
                out += ' ' * (maxOptionLength - len(optionString))
            else:
                out += ' ' * (maxOptionLength)
            out += ' ' * (self.middlePadding)
            out += '\u2502' + ''.join(line) + '\u2502'
            out += ' ' * (self.rightPadding)
        out += ' ' * (self.leftPadding + maxOptionLength + self.middlePadding)
        out += '\u2514' + '\u2500' * mapColumns + '\u2518'
        out += ' ' * (self.rightPadding)
        message = "Choose an option from above"
        while True:
            system('cls')
            print(out)
            print('\033[F' * 3 + ' ' * self.leftPadding + message)
            response = input(' ' * self.leftPadding + "> ")
            if str.isdigit(response) and 0 < int(response) < maxOption:
                system('cls')
                return int(response) - 1
            message = "Sorry, please choose a valid number"
