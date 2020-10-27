from __future__ import annotations


class Vector:
    """Represents a 2D position vector."""
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
        """Returns the x-value of the vector."""
        return self.values[0]

    @property
    def y(self) -> int:
        """Returns the y-value of the vector."""
        return self.values[1]

    def __init__(self, x: int, y: int):
        """Initializes a vector with the given values.

        Args:
            x: The x-coordinate of the vector.
            y: The y-coordinate of the vector.
        """
        self.values = [x, y]

    def __str__(self) -> str:
        """Returns a string representation of the vector in format (x, y)."""
        return "(" + ', '.join(map(str, self.values)) + ")"

    def __getitem__(self, index: int) -> int:
        """Gets a value from the vector at the given index."""
        return self.values[index]

    def __setitem__(self, index: int, value: int) -> None:
        """Changes a value in the vector.

        Args:
            index: The index in the vector to be changed.
            value: The new value.
        """
        self.values[index] = value

    def __iter__(self):
        """Starts iteration over the vector."""
        self.n = 0
        return self

    def __next__(self):
        """Returns the next item in the vector.

        __iter__ must be called first.
        """
        n = self.n
        if n < len(self.values):
            self.n += 1
            return self.values[n]
        else:
            raise StopIteration

    def __eq__(self, other: Vector) -> bool:
        """Returns true if the vectors are equal."""
        return self.values == other.values

    def __add__(self, other: Vector) -> Vector:
        """Adds vectors together."""
        self.values = [x + y for x, y in zip(self, other)]
        return self

    def __sub__(self, other: Vector) -> Vector:
        """Subtracts vectors from eachother."""
        self.values = [x - y for x, y in zip(self, other)]
        return self


class RectVector:
    """Represents a rectangular area."""
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Initializes a rectangular vector.

        Args:
            x1: The x-coordinate of the top-left point.
            y1: The y-coordinate of the top-left point.
            x2: The x-coordinate of the bottom-right point.
            y2: The y-coordinate of the bottom-right point.
        """
        self.values = Vector(x1, y1), Vector(x2, y2)

    def contains(self, other: Vector) -> bool:
        """Returns true if a vector point exists
        inside of the rectangle area."""
        return (self.values[0].x <= other.x and self.values[0].y <= other.y
                and self.values[1].x >= other.x
                and self.values[1].y >= other.y)
