from __future__ import annotations


class Vector:
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

    @property
    def x(self) -> int:
        return self.values[0]

    @property
    def y(self) -> int:
        return self.values[1]

    def __init__(self, x: int, y: int):
        self.values = [x, y]

    def __str__(self) -> str:
        return "(" + ', '.join(map(str, self.values)) + ")"

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, index: int) -> int:
        return self.values[index]

    def __setitem__(self, index: int, value: int) -> None:
        self.values[index] = value

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

    def __eq__(self, other: Vector) -> bool:
        return self.values == other.values

    def __add__(self, other: Vector) -> Vector:
        if len(self) != len(other):
            raise ValueError("Vectors are not the same length.")
        self.values = [x + y for x, y in zip(self, other)]
        return self

    def __sub__(self, other: Vector) -> Vector:
        if len(self) != len(other):
            raise ValueError("Vectors are not the same length.")
        self.values = [x - y for x, y in zip(self, other)]
        return self


class RectVector:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.values = Vector(x1, y1), Vector(x2, y2)

    def contains(self, other: Vector) -> bool:
        return (self.values[0].x <= other.x and self.values[0].y <= other.y
                and self.values[1].x >= other.x
                and self.values[1].y >= other.y)
