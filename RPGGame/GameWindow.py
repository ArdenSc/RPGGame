from os import path, system
from .GameState import GameState
from .Menu import Menu
from .strings.consoleAlign import *


class GameWindow:
    def __init__(self, state: GameState):
        self._state = state

    @staticmethod
    def terminalResize(columns: int, lines: int):
        system(f"mode con: cols={columns} lines={lines}")

    def run(self):
        self.terminalResize(135, 35)
        map = open(
            path.join(path.dirname(__file__), 'assets', 'mapplaceholder.txt'))
        menu = Menu(map=map.readlines())
        map.close()
        while True:
            if menu.waitForInput([
                    "Placeholder",
                    "Placeholder",
                    "Placeholder",
                    "Quit",
            ]) == 4:
                break
