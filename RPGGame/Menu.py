from __future__ import annotations
from typing import List
from os import get_terminal_size, system
from .KeyPress import GetKeyPress


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
    def fixmaplol(map: List[str]) -> List[str]:
        map = [line.rstrip('\n') for line in map]
        columns = len(max(map, key=len))
        return [line + ' ' * (columns - len(line)) for line in map]

    def navigation(self) -> int:
        """Waits for a navigational key to be pressed.

        Returns
            int: one of 0-3 where 0 is North and each successive number is
                 clockwise around a compass. Additionally, 4 may be returned
                 and the program should quit.
        """
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
        # if platform != "win32":
        #     raise Exception("Following code unimplemented for non-win32 OSes.")
        # while True:
        #     if kbhit():
        #         key = getch()
        #         if key == b'\xe0':
        #             key = getch()
        #             if key == b'H':
        #                 return 0
        #             elif key == b'M':
        #                 return 1
        #             elif key == b'P':
        #                 return 2
        #             elif key == b'K':
        #                 return 3
        #         elif key in [b'w', b'a', b's', b'd', b'q']:
        #             if key == b'w':
        #                 return 0
        #             elif key == b'd':
        #                 return 1
        #             elif key == b's':
        #                 return 2
        #             elif key == b'a':
        #                 return 3
        #             elif key == b'q':
        #                 return 4

    def optionSelector(self, map: List[str], options: List[str]) -> int:
        termSize = get_terminal_size()
        map = self.fixmaplol(map)
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
            out += '\u2502' + line + '\u2502'
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
