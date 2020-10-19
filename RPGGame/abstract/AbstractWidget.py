from abc import ABC, abstractmethod


class AbstractWidget(ABC):
    @abstractmethod
    def build(self, i: int) -> str:
        ...

    @abstractmethod
    def __len__(self) -> int:
        ...
