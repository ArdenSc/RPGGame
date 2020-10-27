from __future__ import annotations

class Item:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

class Armor(Item):
    defense: int

class Weapon(Item):
    @staticmethod
    def Broadsword() -> Item:
        return Weapon("Broadsword", 20)

    def __init__(self, name: str, damage: int):
        super().__init__(name)
        self.damage = damage
