from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from RPGGame.abstract.AbstractGameState import AbstractGameState


class AbstractMenu(ABC):
    """Displays all on-screen elements.

    Must be extended by an actual implementation.
    """
    @abstractmethod
    def navigate(self, state: AbstractGameState) -> int:
        """Menu for navigating the map."""
        ...

    @abstractmethod
    def mainmenu(self) -> int:
        """Title screen."""
        ...

    @abstractmethod
    def fight(self, state: AbstractGameState) -> int:
        """Menu for engaging in a fight."""
        ...

    @abstractmethod
    def winmenu(self) -> int:
        """Win screen."""
        ...

    @abstractmethod
    def losemenu(self) -> int:
        """Loss screen."""
        ...
