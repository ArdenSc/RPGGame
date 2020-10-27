from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable, List

    from RPGGame.Item import Item


class Inventory:
    def __init__(self):
        self._data: List[Item] = []

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        n = self.n
        if n < len(self):
            self.n += 1
            return self._data[n]
        else:
            raise StopIteration

    def __str__(self) -> str:
        return '\n'.join(['Inventory:'] +
                         [f'- {str(item)}' for item in self._data])

    def append(self, new: Item):
        self._data.append(new)

    def extend(self, new: Iterable[Item]):
        self._data.extend(new)
