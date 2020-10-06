# Arden Sinclair
# Oct. 06, 2020
# CS30 P1Q1
# An interactive adventure game.
# Currently only example code is implemented.

from .GameState import GameState
from .GameWindow import GameWindow


if __name__ == "__main__":
    window = GameWindow(GameState())
    window.run()
