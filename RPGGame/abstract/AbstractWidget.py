from abc import ABC, ABCMeta, abstractmethod
from typing import Callable, List, Tuple, Union

SizeData = Tuple[int, int]
StaticWidgetData = Tuple[List[str], SizeData]
DynamicWidgetData = Tuple[Callable[[int, int], List[str]], SizeData]


class AbstractWidget(ABC):
    @abstractmethod
    def build(self) -> Union[StaticWidgetData, DynamicWidgetData]:
        ...


class DynamicWidget(AbstractWidget, metaclass=ABCMeta):
    @abstractmethod
    def build_sized(self, width: int, height: int) -> List[str]:
        ...

    def build(self) -> DynamicWidgetData:
        ...


class StaticWidget(AbstractWidget, metaclass=ABCMeta):
    @abstractmethod
    def build(self) -> StaticWidgetData:
        ...
