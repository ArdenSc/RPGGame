# Arden Sinclair
# Oct. 06, 2020
# CS30 P1Q1
# An interactive adventure game.
# Currently only example code is implemented.

from RPGGame.BehaviorHandler import BehaviorHandler
from RPGGame.Game import Game
from RPGGame.GameState import GameState
from RPGGame.maps import maps, map_names
from RPGGame.Menu import Menu

if __name__ == "__main__":
    game = Game(GameState())
    game.register('menu', Menu())
    game.register('behaviors', BehaviorHandler())
    game.register('maps', maps, map_names)
    game.run()
