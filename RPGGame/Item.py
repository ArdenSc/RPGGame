from __future__ import annotations


class Item:
    """Represents a base item."""
    @staticmethod
    def Key() -> Item:
        return Item("Key")

    def __init__(self, name: str):
        """Initializes an item.

        Args:
            name: The name of the item.
        """
        self.name = name

    def __str__(self):
        """Returns the name of the item."""
        return self.name

    def __eq__(self, other: Item) -> bool:
        """Returns true if two items have the same name
        and are assumed to be equal."""
        return self.name == other.name


class Armor(Item):
    """Represents an armor item."""
    @staticmethod
    def Chestplate() -> Armor:
        return Armor("Chestplate", 5)

    def __init__(self, name: str, defense: int) -> None:
        """Initializes an armor item.

        Args:
            name: The name of the item.
            defense: The amount of defense points the armor provides.
        """
        super().__init__(name)
        self.defense = defense


class Weapon(Item):
    """Represents a weapon item."""
    @staticmethod
    def Broadsword() -> Weapon:
        return Weapon('Broadsword', 20)

    @staticmethod
    def Longsword() -> Weapon:
        return Weapon('Longsword', 30)

    def __init__(self, name: str, damage: int):
        """Initializes a weapon item.

        Args:
            name: The name of the item.
            damage: The amount of damage the item does.
        """
        super().__init__(name)
        self.damage = damage


class Heal(Item):
    """Represents a healing item."""
    @staticmethod
    def Bandage() -> Heal:
        return Heal('Bandage', 50)

    @staticmethod
    def Medkit() -> Heal:
        return Heal('Medkit', 100)

    def __init__(self, name: str, health: int):
        """Initializes a healing item.

        Args:
            name: The name of the item.
            health: The amount of health points the item heals.
        """
        super().__init__(name)
        self.health = health
        self.used = False


class WinItem(Item):
    """Item that causes a win condition if it is in the player's inventory."""
    def __init__(self):
        self.name = "Game won, this message should never be displayed."
