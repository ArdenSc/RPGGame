from __future__ import annotations
from RPGGame.Inventory import Inventory
from RPGGame.Vector import Vector
from RPGGame.abstract.AbstractMenu import AbstractMenu
from RPGGame.MapSegment import MapSegment
from typing import List


class GameState:
    maps: List[List[MapSegment]]
    menu: AbstractMenu

    def __init__(self):
        self.map_pos = Vector(0, 0)
        self.pos = Vector(0, 0)
        self.inventory = Inventory()

    def map(self, x: int, y: int) -> MapSegment:
        return self.maps[y][x]

    def move(self, movement: Vector):
        old_pos = self.pos
        self.pos += movement
        x, y = self.pos
        mx, my = self.map_pos
        if x < 0:
            if mx >= 1:
                self.map_pos += Vector(-1, 0)
                self.pos = Vector(
                    len(self.map(mx - 1, my).map[0]) - 1, self.pos[1])
            else:
                self.pos = old_pos
        elif x >= len(self.map(mx, my).map[0]):
            if mx + 1 < len(self.maps[0]):
                self.map_pos += Vector(1, 0)
                self.pos = Vector(0, self.pos[1])
            else:
                self.pos = old_pos
        if y < 0:
            if my >= 1:
                self.map_pos += Vector(0, -1)
                self.pos = Vector(self.pos[0],
                                  len(self.map(mx, my - 1).map) - 1)
            else:
                self.pos = old_pos
        elif y >= len(self.map(mx, my).map):
            if my + 1 < len(self.maps):
                self.map_pos += Vector(0, 1)
                self.pos = Vector(self.pos[0], 0)
            else:
                self.pos = old_pos
