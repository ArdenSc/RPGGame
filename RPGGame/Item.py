from __future__ import annotations


class Item:
    @staticmethod
    def Key() -> Item:
        return Item("Key")

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other: Item) -> bool:
        return self.name == other.name


class Armor(Item):
    @staticmethod
    def Chestplate() -> Armor:
        return Armor("Chestplate", 5)

    def __init__(self, name: str, defense: int) -> None:
        super().__init__(name)
        self.defense = defense


class Weapon(Item):
    @staticmethod
    def Broadsword() -> Weapon:
        return Weapon('Broadsword', 20)

    @staticmethod
    def Longsword() -> Weapon:
        return Weapon('Longsword', 30)

    def __init__(self, name: str, damage: int):
        super().__init__(name)
        self.damage = damage


class Heal(Item):
    @staticmethod
    def Bandage() -> Heal:
        return Heal('Bandage', 50)

    @staticmethod
    def Medkit() -> Heal:
        return Heal('Medkit', 100)

    def __init__(self, name: str, health: int):
        super().__init__(name)
        self.health = health
        self.used = False


class WinItem(Item):
    def __init__(self):
        self.name = "Game won, this message should never be displayed."
