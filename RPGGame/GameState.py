from __future__ import annotations
from typing import Callable, Dict, List, TypedDict


class Behavior(TypedDict):
    key: str
    function: Callable[[], None]


class GameState:
    # Bindings to all menu and behavior functions
    _call: Dict[str, Callable[[], None]] = {}

    def __init__(self):
        # TODO: Add needed parameters to GameState constructor
        pass

    def __call__(self, key: str) -> None:
        return self._call[key]()

    def registerBehavior(self, behavior: Behavior) -> GameState:
        """Registers a menu or behavior to the game to be used in the map.

        Args:
            behavior: Dictionary with the key for the function to be stored
                      under and function for the actual function.
        Returns:
            The class instance the method was called on.
        """
        self._call[behavior["key"]] = behavior["function"]
        return self

    def registerBehaviors(self, behaviors: List[Behavior]) -> GameState:
        """Registers multiple menus and/or behaviors for use in the game.

        Args:
            behaviors: A list of behavior dictionaries.
        Returns:
            The class instance the method was called on.
        """
        for behavior in behaviors:
            self.registerBehavior(behavior)
        return self
