from __future__ import annotations

from typing import TYPE_CHECKING

from RPGGame.Exceptions import WinGame
from RPGGame.Item import Armor, Heal, WinItem

if TYPE_CHECKING:
    from typing import List

    from RPGGame.Item import Item


class Player():
    """Represents a player."""
    _inventory: List[Item]

    def __init__(self) -> None:
        """Initializes a player with an empty inventory and 100 max health."""
        self._inventory = []
        self.health = 100

    @property
    def armor(self) -> int:
        """Returns the amount of armor the player has."""
        return sum(x.defense for x in self.inventory if isinstance(x, Armor))

    @property
    def inventory(self) -> List[Item]:
        """Returns the player's inventory.

        Runs clean_inventory before returning to perform needed operations on
        the inventory.
        """
        self.clean_inventory()
        return self._inventory

    def inventory_info(self) -> str:
        """Returns information about the inventory for the player."""
        return 'Inventory:\n' + '\n'.join(f'- {x}' for x in self.inventory)

    def clean_inventory(self) -> None:
        """Scans the inventory for used heal items and for the win item and
        does neccesary actions."""
        for item in reversed(self._inventory):
            if isinstance(item, Heal) and item.used:
                self._inventory.remove(item)
            if isinstance(item, WinItem):
                raise WinGame

    def __str__(self) -> str:
        """Returns information about the player's status
        for the human player to read."""
        return f"""\
Player:
- Health: {self.health}
- Armor: {self.armor}
"""
