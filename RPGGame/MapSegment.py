from __future__ import annotations

from typing import TYPE_CHECKING, overload

if TYPE_CHECKING:
    from typing import List, Union


class MapSegment:
    """A 2D map of characters stored as strings."""
    def __init__(self, map: List[List[str]]):
        """Initializes a map segment

        Args:
            map: A 2D list of strings to be used as the map data.
        """
        self._map = map
        self.width = len(max(map, key=len))
        self.height = len(map)

    @overload
    def get(self) -> List[List[str]]:
        """Returns the map data."""
        ...

    @overload
    def get(self, x: int, y: int) -> str:
        """Returns the string at a specific position on the map.

        Args:
            x: The x-coordinate of the location on the map.
            y: The y-coordinate of the location on the map.
        """
        ...

    def get(self, *args: int) -> Union[List[List[str]], str]:
        """Base method for getting data from the map.

        See overloads for specifics.
        """
        arg_length = len(args)
        if arg_length == 0:
            return self._map

        elif arg_length == 2:
            x, y = args
            return self._map[y][x]

        else:
            raise AttributeError("Invalid amount of arguments")

    def set(self, x: int, y: int, value: str) -> None:
        """Sets the value of a specific position on the map.

        Args:
            x: The x-coordinate of the location on the map.
            y: The y-coordinate of the location on the map.
        """
        self._map[y][x] = value
