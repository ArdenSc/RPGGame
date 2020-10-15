from __future__ import annotations
from typing import List
from RPGGame.MapSegment import MapSegment
from RPGGame.Menu import Menu
from RPGGame.GameState import GameState, Vector
from os import system
from sys import platform


class GameWindow:
    _state: GameState
    _map: List[List[MapSegment]]

    def __init__(self, state: GameState):
        self._state = state

    @staticmethod
    def terminalResize(columns: int, lines: int):
        if platform == 'win32':
            system(f"mode con: cols={columns} lines={lines}")
        else:
            system(f"resize -s {columns} {lines}")

    def addMaps(self, map: List[List[MapSegment]]) -> GameWindow:
        self._map = map
        return self

    def run(self):
        self.terminalResize(135, 35)
        menu = Menu()
        map = self._map[0][0]
        while True:
            direction = menu.navigation(map, self._state.playerPos)
            if direction == 0:
                self._state.playerPos += Vector.North()
            elif direction == 1:
                self._state.playerPos += Vector.East()
            elif direction == 2:
                self._state.playerPos += Vector.South()
            elif direction == 3:
                self._state.playerPos += Vector.West()
            elif direction == 4:
                break

        # while True:
        #     selection = menu.optionSelector(map, [
        #         "Tunnel",
        #         "Cave",
        #         "Hill",
        #         "Quit",
        #     ])
        #     if selection == 0:
        #         selection = menu.optionSelector(map, [
        #             "Left Tunnel",
        #             "Middle Tunnel",
        #             "Right Tunnel",
        #             "Quit",
        #         ])
        #         if selection == 0:
        #             menu.optionSelector(map, ["No further options"])
        #         elif selection == 1:
        #             menu.optionSelector(map, ["No further options"])
        #         elif selection == 2:
        #             menu.optionSelector(map, ["No further options"])
        #         elif selection == 3:
        #             quit()
        #     elif selection == 1:
        #         selection = menu.optionSelector(map, [
        #             "Left Cave",
        #             "Middle Cave",
        #             "Right Cave",
        #             "Quit",
        #         ])
        #         if selection == 0:
        #             menu.optionSelector(map, ["No further options"])
        #         elif selection == 1:
        #             menu.optionSelector(map, ["No further options"])
        #         elif selection == 2:
        #             menu.optionSelector(map, ["No further options"])
        #         elif selection == 3:
        #             quit()
        #     elif selection == 2:
        #         selection = menu.optionSelector(map, [
        #             "Left Hill",
        #             "Middle Hill",
        #             "Right Hill",
        #             "Quit",
        #         ])
        #         if selection == 0:
        #             menu.optionSelector(map, ["No further options"])
        #         elif selection == 1:
        #             menu.optionSelector(map, ["No further options"])
        #         elif selection == 2:
        #             menu.optionSelector(map, ["No further options"])
        #         elif selection == 3:
        #             quit()
        #     elif selection == 3:
        #         quit()
