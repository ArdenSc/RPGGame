from typing import List, Tuple
from RPGGame.abstract.AbstractWidget import AbstractWidget
from abc import ABCMeta, abstractmethod


class StaticWidget(AbstractWidget, metaclass=ABCMeta):
    @abstractmethod
    def build(self) -> Tuple[List[str], Tuple[int, int]]:
        ...
