from typing import Callable, List
from RPGGame.abstract.AbstractWidget import AbstractWidget
from abc import ABCMeta, abstractmethod

class DynamicWidget(AbstractWidget, metaclass=ABCMeta):
    @abstractmethod
    def build_sized(self, width: int, height: int) -> List[str]:
        ...

    def build(self) -> Callable[[int, int], List[str]]:
        return self.build_sized
