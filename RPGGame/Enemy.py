from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

from RPGGame.Item import Heal, Weapon, WinItem

if TYPE_CHECKING:
    from typing import Tuple, List
    from RPGGame.Item import Item


class Enemy():
    @staticmethod
    def Zombie() -> Enemy:
        return Enemy("Zombie", 50, (10, 20), [Heal.Bandage()])

    @staticmethod
    def Skeleton() -> Enemy:
        return Enemy("Skeleton", 50, (10, 20), [Heal.Bandage()])

    @staticmethod
    def Warrior() -> Enemy:
        return Enemy("Warrior", 70, (15, 20), [Weapon.Longsword()])

    @staticmethod
    def Serpent() -> Enemy:
        return Enemy("Serpent", 80, (20, 25), [Heal.Medkit()])

    @staticmethod
    def Werewolf() -> Enemy:
        return Enemy("Werewolf", 100, (25, 30), [Heal.Medkit()])

    @staticmethod
    def Dragon() -> Enemy:
        return Enemy("Dragon", 200, (30, 35), [WinItem()])

    def __init__(self,
                 name: str,
                 health: int,
                 damage_range: Tuple[int, int],
                 drops: List[Item] = []) -> None:
        """
        docstring
        """
        self.name = name
        self.health = health
        self.damage_range = damage_range
        self.drops = drops

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
