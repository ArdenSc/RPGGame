# Arden Sinclair
# Oct. 06, 2020
# CS30 P1Q1
# An interactive adventure game.
# Currently only example code is implemented.

from RPGGame.maps import maps
from RPGGame.GameState import GameState
from RPGGame.GameWindow import GameWindow

if __name__ == "__main__":
    window = GameWindow(GameState())
    window.addMaps(maps)
    window.run()
