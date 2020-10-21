from typing import List
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

    def append(self, new: Item):
        self._data.append(new)
