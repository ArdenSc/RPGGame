from __future__ import annotations

from typing import TYPE_CHECKING, overload

if TYPE_CHECKING:
    from typing import List, Union


class MapSegment:
    def __init__(self, map: List[List[str]]):
        self._map = map
        self.width = len(max(map, key=len))
        self.height = len(map)

    @overload
    def get(self) -> List[List[str]]:
        ...

    @overload
    def get(self, x: int, y: int) -> str:
        ...

    def get(self, *args: int) -> Union[List[List[str]], str]:
        arg_length = len(args)
        if arg_length == 0:
            return self._map

        elif arg_length == 2:
            x, y = args
            return self._map[y][x]

        else:
            raise AttributeError("Invalid amount of arguments")

    def set(self, x: int, y: int, value: str) -> None:
        self._map[y][x] = value
