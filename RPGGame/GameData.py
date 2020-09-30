# Arden Sinclair
# CS30 - P1Q1
# Sept. 29th 2020
# Stores data about the game's inventories, characters, and locations,
# as well as a function to display them in a formatted way.

# Data about the inventory of the game's characters.
inventories = {
    "Player": {
        "Sword": {
            "description": "A longsword, great for any engagement.",
            "damage": 5,
        },
        "Shield": {
            "description": "A wooden shield, not very strong",
            "defense": 2,
        },
        "Dagger": {
            "description":
            "A stealty dagger, perfect for sneaking up on enemies.",
            "damage": 4,
        },
    },
    "Giant": {
        "Club": {
            "description": "A heavy club. It takes a lot of effort to swing, \
but deals nasty damage.",
            "damage": 10,
        },
        "Potion": {
            "description": "A magical elixer that makes your skin harden.",
            "effect": "Doubles your attack resistance for 5 turns.",
        },
    },
}

# Information about locations in the game.
locations = {
    "Home": {
        "Description": "A small shack made of wood. You are safe here",
        "Location": "In a little green valley near a mountain",
    },
    "Giant's Dungeon": {
        "Description": "A big, dark cave. You can't make out many details",
        "Location": "Somewhere inside of the mountain",
    },
    "Dragon's Lair": {
        "Description": "A massive cave filled with loot and riches",
        "Location": "Deep, deep inside of the mountain",
    },
}

# Information about the game's characters.
characters = {
    "Player": {
        "Name": "Arden",
        "Age": 17,
        "Height": "6'",
    },
    "Giant": {
        "Name": "Russellrek",
        "Age": 252,
        "Height": "9'10\"",
    },
}


def printAllData():
    """Prints all of the formatted game data."""
    # Pretty prints the inventory data.
    for name, inventory in inventories.items():
        print(f"{name}'s Inventory:")
        for item, data in inventory.items():
            print(f"  * {item}")
            for key, value in data.items():
                print(f"      {key}: {value}")

    # Newline for readability
    print()

    # Pretty prints the location data.
    for location, data in locations.items():
        for key, value in data.items():
            print(f"{location}'s {key} is {value}.")

    # Newline for readability
    print()

    # Pretty prints the character data.
    for character, data in characters.items():
        for key, value in data.items():
            print(f"{character}'s {key} is {value}.")
