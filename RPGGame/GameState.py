from __future__ import annotations
from RPGGame.MapSegment import MapSegment
from typing import Callable, List
from typing_extensions import TypedDict


class Behavior(TypedDict):
    key: str
    function: Callable[[], None]


class Vector:
    values: List[int]

    @staticmethod
    def North():
        return Vector(0, -1)

    @staticmethod
    def East():
        return Vector(1, 0)

    @staticmethod
    def South():
        return Vector(0, 1)

    @staticmethod
    def West():
        return Vector(-1, 0)

    def __init__(self, *args: int):
        self.values = list(args)

    def __str__(self) -> str:
        return "(" + ', '.join(map(str, self.values)) + ")"

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, index: int) -> int:
        return self.values[index]

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        n = self.n
        if n < len(self.values):
            self.n += 1
            return self.values[n]
        else:
            raise StopIteration

    def __add__(self, other: Vector) -> Vector:
        if len(self) != len(other):
            raise ValueError("Vectors are not the same length.")
        return Vector(*[self[i] + other[i] for i in range(len(self))])

    def __sub__(self, other: Vector) -> Vector:
        if len(self) != len(other):
            raise ValueError("Vectors are not the same length.")
        return Vector(*[self[i] - other[i] for i in range(len(self))])


class GameState:
    maps: List[List[MapSegment]]
    map_pos: Vector
    pos: Vector

    def __init__(self):
        self.map_pos = Vector(0, 0)
        self.pos = Vector(0, 0)

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
