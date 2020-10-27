from __future__ import annotations

from typing import TYPE_CHECKING

from RPGGame.Exceptions import WinGame
from RPGGame.Item import Armor, Heal, WinItem

if TYPE_CHECKING:
    from typing import List

    from RPGGame.Item import Item


class Player():
    _inventory: List[Item]

    def __init__(self) -> None:
        self._inventory = []
        self.health = 100

    @property
    def armor(self) -> int:
        return sum(x.defense for x in self.inventory if isinstance(x, Armor))

    @property
    def inventory(self) -> List[Item]:
        self.clean_inventory()
        return self._inventory

    def inventory_info(self) -> str:
        return 'Inventory:\n' + '\n'.join(f'- {x}' for x in self.inventory)

    def clean_inventory(self) -> None:
        for item in reversed(self._inventory):
            if isinstance(item, Heal) and item.used:
                self._inventory.remove(item)
            if isinstance(item, WinItem):
                raise WinGame

    def __str__(self) -> str:
        """
        docstring
        """
        return f"""\
Player:
- Health: {self.health}
- Armor: {self.armor}
"""
