from os import path, system
from sys import platform
from .GameState import GameState
from .Menu import Menu


class GameWindow:
    def __init__(self, state: GameState):
        self._state = state

    @staticmethod
    def terminalResize(columns: int, lines: int):
        if platform == 'win32':
            system(f"mode con: cols={columns} lines={lines}")
        else:
            system(f"resize -s {columns} {lines}")

    def run(self):
        self.terminalResize(135, 35)
        menu = Menu()
        handler = open(
            path.join(path.dirname(__file__), 'assets', 'mapplaceholder.txt'))
        map = handler.readlines()
        handler.close()
        while True:
            selection = menu.optionSelector(map, [
                "Tunnel",
                "Cave",
                "Hill",
                "Quit",
            ])
            if selection == 0:
                selection = menu.optionSelector(map, [
                    "Left Tunnel",
                    "Middle Tunnel",
                    "Right Tunnel",
                    "Quit",
                ])
                if selection == 0:
                    menu.optionSelector(map, ["No further options"])
                elif selection == 1:
                    menu.optionSelector(map, ["No further options"])
                elif selection == 2:
                    menu.optionSelector(map, ["No further options"])
                elif selection == 3:
                    quit()
            elif selection == 1:
                selection = menu.optionSelector(map, [
                    "Left Cave",
                    "Middle Cave",
                    "Right Cave",
                    "Quit",
                ])
                if selection == 0:
                    menu.optionSelector(map, ["No further options"])
                elif selection == 1:
                    menu.optionSelector(map, ["No further options"])
                elif selection == 2:
                    menu.optionSelector(map, ["No further options"])
                elif selection == 3:
                    quit()
            elif selection == 2:
                selection = menu.optionSelector(map, [
                    "Left Hill",
                    "Middle Hill",
                    "Right Hill",
                    "Quit",
                ])
                if selection == 0:
                    menu.optionSelector(map, ["No further options"])
                elif selection == 1:
                    menu.optionSelector(map, ["No further options"])
                elif selection == 2:
                    menu.optionSelector(map, ["No further options"])
                elif selection == 3:
                    quit()
            elif selection == 3:
                quit()
