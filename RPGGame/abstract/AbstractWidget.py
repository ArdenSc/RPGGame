from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, List, Tuple, Union
    SizeData = Tuple[int, int]
    StaticWidgetData = Tuple[List[str], SizeData]
    DynamicWidgetData = Tuple[Callable[[int, int], StaticWidgetData], SizeData]



class AbstractWidget(ABC):
    """Represents any displayable widget."""
    @abstractmethod
    def build(self) -> Union[StaticWidgetData, DynamicWidgetData]:
        """Builds the widget by converting it into a list of strings."""
        ...


class DynamicWidget(AbstractWidget, metaclass=ABCMeta):
    """Represents any displayable widget that can expand into unused space."""
    @abstractmethod
    def build_sized(self, width: int, height: int) -> StaticWidgetData:
        """Builds the widget by converting it into a list of strings.

        Args:
            width: The width that the widget may expand into.
            height: The height that the widget may expand into.
        """
        ...

    def build(self) -> DynamicWidgetData:
        """Provides a function for building the widget
        alongside the minimum size."""
        ...


class StaticWidget(AbstractWidget, metaclass=ABCMeta):
    """Represents any displayable widget that has a static size."""
    @abstractmethod
    def build(self) -> StaticWidgetData:
        """Builds the widget by converting it into a list of strings."""
        ...
