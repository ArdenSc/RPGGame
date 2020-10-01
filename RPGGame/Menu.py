from __future__ import annotations
from typing import List
from os import get_terminal_size, path, system


class Menu:
    def __init__(
        self,
        map: List[str],
        leftPadding: int = 10,
        middlePadding: int = 10,
        rightPadding: int = 10,
    ) -> None:
        """Stores a map/image and has functionality to display
        a menu with the map/image.

        Args:
            map: An array of strings with each line of the map/image.
            leftPadding: Amount of spaces on the left of the menu.
            middlePadding: Amount of spaces between the menu and map/image.
            rightPAdding: Amount of spaces on the right of the map/image.
        """
        self.leftPadding = leftPadding
        self.middlePadding = middlePadding
        self.rightPadding = rightPadding
        self.termSize = get_terminal_size()

        map = [line.rstrip('\n') for line in map]
        self.mapColumns = len(max(map, key=len))
        self.map = [line + ' ' * (self.mapColumns - len(line)) for line in map]

    def waitForInput(self: Menu, options: List[str]) -> int:
        maxOption = len(options) + 1
        out: str = ""
        maxOptionLength = (self.termSize.columns - self.mapColumns -
                           self.leftPadding - self.middlePadding -
                           self.rightPadding - 2)
        out += ' ' * (self.leftPadding + maxOptionLength + self.middlePadding)
        out += '\u250C' + '\u2500' * self.mapColumns + '\u2510'
        out += ' ' * (self.rightPadding)
        for i, line in enumerate(self.map):
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
        out += '\u2514' + '\u2500' * self.mapColumns + '\u2518'
        out += ' ' * (self.rightPadding)
        message = "Choose an option from above"
        while True:
            system('cls')
            print(out)
            print('\033[F' * 3 + ' ' * self.leftPadding + message)
            response = input(' ' * self.leftPadding + "> ")
            if str.isdigit(response) and 0 < int(response) < maxOption:
                system('cls')
                return int(response)
            message = "Sorry, please choose a valid number"


if __name__ == "__main__":
    menu = None
    with open(path.join(path.dirname(__file__), 'assets/worldmap.txt'),
              'r') as mapFile:
        menu = Menu(map=mapFile.readlines())
    menu.waitForInput(["1. North", "2. East", "3. South", "4. West"])
    print("Corrent Answer Entered.")
