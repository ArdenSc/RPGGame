from __future__ import annotations

from typing import TYPE_CHECKING

from RPGGame.Item import Armor

if TYPE_CHECKING:
    from typing import List

    from RPGGame.Item import Item


class Player():
    inventory: List[Item]

    def __init__(self) -> None:
        self.inventory = []
        self.health = 100

    @property
    def armor(self) -> int:
        return sum(x.defense for x in self.inventory if isinstance(x, Armor))

    def inventory_info(self) -> str:
        return 'Inventory:\n' + '\n'.join(f'- {x}' for x in self.inventory)

    def __str__(self) -> str:
        """
        docstring
        """
        return f"""\
Player:
- Health: {self.health}
- Armor: {self.armor}
"""
