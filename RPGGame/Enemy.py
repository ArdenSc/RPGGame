from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple


class Enemy():
    @staticmethod
    def Zombie() -> Enemy:
        return Enemy("Zombie", 50, (10, 20))

    def __init__(self, name: str, health: int,
                 damage_range: Tuple[int, int]) -> None:
        """
        docstring
        """
        self.name = name
        self.health = health
        self.damage_range = damage_range

    @property
    def damage(self) -> int:
        return randint(*self.damage_range)

    def __str__(self) -> str:
        """
        docstring
        """
        return f"""\
{self.name}:
- Health: {self.health}
- Damage per hit: {'-'.join(map(str, self.damage_range))}
"""
