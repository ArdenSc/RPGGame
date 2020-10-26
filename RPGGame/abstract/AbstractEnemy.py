from abc import ABC, abstractmethod

class AbstractEnemy(ABC):
    @property
    @abstractmethod
    def damage(self) -> int:
        ...
