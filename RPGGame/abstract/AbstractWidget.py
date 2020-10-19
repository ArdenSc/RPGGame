from abc import ABC, abstractmethod
from typing import Callable, List, Tuple, Union


class AbstractWidget(ABC):
    @abstractmethod
    def build(
        self
    ) -> Union[Tuple[List[str], Tuple[int, int]], Callable[[int, int],
                                                           List[str]]]:
        ...
