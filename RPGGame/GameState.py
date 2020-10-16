from __future__ import annotations
from typing import Callable, Dict, List
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
    # Bindings to all menu and behavior functions
    _call: Dict[str, Callable[[], None]]
    _mapSegment: Vector
    playerPos: Vector

    def __init__(self):
        self._call = {}
        self._mapSegment = Vector(0, 0)
        self.playerPos = Vector(0, 0)
        # TODO: Add needed parameters to GameState constructor

    def __call__(self, key: str) -> None:
        return self._call[key]()

    def registerItem(self, behavior: Behavior) -> GameState:
        """Registers a menu or behavior to the game to be used in the map.

        Args:
            behavior: Dictionary with the key for the function to be stored
                      under and function for the actual function.
        Returns:
            The class instance the method was called on.
        """
        self._call[behavior["key"]] = behavior["function"]
        return self

    def registerItems(self, behaviors: List[Behavior]) -> GameState:
        """Registers multiple menus and/or behaviors for use in the game.

        Args:
            behaviors: A list of behavior dictionaries.
        Returns:
            The class instance the method was called on.
        """
        for behavior in behaviors:
            self.registerItem(behavior)
        return self

    def movePlayer(self, movement: Vector):
        self.playerPos = self.playerPos + movement
