from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable, List

    from RPGGame.Item import Item


class Inventory:
    """Class for holding all inventory data for the player."""
    def __init__(self):
        """Initializes a blank inventory instance."""
        self._data: List[Item] = []

    def __len__(self):
        """Returns the amount of items in the inventory."""
        return len(self._data)

    def __iter__(self):
        """Starts iteration over the inventory."""
        self.n = 0
        return self

    def __next__(self):
        """Returns the next item in the inventory.

        __iter__ must be called first."""
        n = self.n
        if n < len(self):
            self.n += 1
            return self._data[n]
        else:
            raise StopIteration

    def __str__(self) -> str:
        """Returns the inventory items for the player to read."""
        return '\n'.join(['Inventory:'] +
                         [f'- {str(item)}' for item in self._data])

    def append(self, new: Item):
        """Adds an item to the inventory."""
        self._data.append(new)

    def extend(self, new: Iterable[Item]):
        """Adds a list of items to the inventory."""
        self._data.extend(new)
