from __future__ import annotations
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
    map_pos: Vector
    pos: Vector

    def __init__(self):
        self.map_pos = Vector(0, 0)
        self.pos = Vector(0, 0)

    def move(self, movement: Vector):
        self.pos += movement
