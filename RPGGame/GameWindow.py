from msvcrt import getch, kbhit
from os import get_terminal_size, path, system
from time import sleep, time

from .GameState import GameState
from .Menu import Menu
from .strings.consoleAlign import *


class GameWindow:
    def __init__(self, state: GameState):
        self._state = state

    @staticmethod
    def terminalAlign():
        if get_terminal_size().columns != 140 or get_terminal_size(
        ).lines != 35:
            system("cls")
            print(STRING_RESIZE_NEEDED)
            sleep(2)

        if get_terminal_size().columns != 140:
            old_width_state = width_state = ""
            while not width_state == "done":
                while get_terminal_size().columns != 140:
                    old_width_state = width_state
                    width_state = "Increase" if get_terminal_size(
                    ).columns < 140 else "Decrease"
                    if old_width_state != width_state:
                        system("cls")
                        print(STRING_WIDTH_INCORRECT.format(width_state))
                time_end = time() + 2
                system("cls")
                print(STRING_WIDTH_CORRECT)
                while time() < time_end:
                    if get_terminal_size().columns != 140:
                        old_width_state = width_state = ""
                        break
                else:
                    width_state = "done"
                    system("cls")
                    print(STRING_WIDTH_DONE)
                    sleep(3)

        if get_terminal_size().lines != 35:
            old_height_state = height_state = ""
            while not height_state == "done":
                while get_terminal_size().lines != 35:
                    old_height_state = height_state
                    height_state = "Increase" if get_terminal_size(
                    ).lines < 35 else "Decrease"
                    if old_height_state != height_state:
                        system("cls")
                        print(STRING_HEIGHT_INCORRECT if height_state ==
                              "Increase" else STRING_HEIGHT_SKIPPABLE)
                    if height_state == "Decrease" and kbhit() and getch(
                    ) == b's':
                        height_state = "done"
                        break
                if height_state == "done":
                    system("cls")
                    print(STRING_HEIGHT_DONE)
                    sleep(3)
                else:
                    system("cls")
                    print(STRING_HEIGHT_CORRECT)
                    time_end = time() + 2
                    while time() < time_end:
                        if get_terminal_size().lines != 35:
                            old_height_state = height_state = ""
                            break
                    else:
                        height_state = "done"
                        system("cls")
                        print(STRING_HEIGHT_DONE)
                        sleep(3)

    def run(self):
        # Guided console window alignment
        self.terminalAlign()
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
