from typing import List


class MapSegment:
    map: List[List[str]]

    def __init__(self, map: List[List[str]]):
        self.map = map
