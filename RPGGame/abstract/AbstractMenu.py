from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from RPGGame.abstract.AbstractGameState import AbstractGameState


class AbstractMenu(ABC):
    @abstractmethod
    def navigate(self, state: AbstractGameState) -> int:
        ...

    @abstractmethod
    def mainmenu(self) -> int:
        ...

    @abstractmethod
    def fight(self, state: AbstractGameState) -> int:
        ...

    @abstractmethod
    def winmenu(self) -> int:
        ...

    @abstractmethod
    def losemenu(self) -> int:
        ...
