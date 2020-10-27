from math import sqrt
from os import listdir, path
from re import search
from typing import List, TypeVar

from RPGGame.MapSegment import MapSegment

files = listdir(path.dirname(__file__))


def strip_newlines(x: List[str]):
    """Removes newlines from the input."""
    return [y.rstrip() for y in x]


def name_to_file(x: str):
    """Returns a list of lines from the specified filename."""
    with open(path.join(path.dirname(__file__), x), encoding='utf-8') as file:
        return file.readlines()


def strings_to_lists(x: List[str]) -> List[List[str]]:
    """Converts a list of strings to a nested list of
    single character strings."""
    return list(map(lambda y: [z for z in y], x))


T = TypeVar('T')


def rearranage_list(list: List[T], columns: int) -> List[List[T]]:
    """Converts a list into a 2D nested list.

    Args:
        list: Any list.
        columns: The width of the requested 2D list.
    """
    return [list[i:i + columns] for i in range(0, len(list), columns)]


def uniform_line_lengths(list: List[List[str]],
                         length: int) -> List[List[str]]:
    """Extends each line in a list of character lists.

    Args:
        list: List of character lists.
        length: The length to be extended to.
    """
    return [x + [' '] * (length - len(x)) for x in list]


# Maps

_maps = list(filter(lambda x: search("^\\d{2}.txt$", x), files))

mapGridSize = int(sqrt(len(_maps)))
if len(_maps) != mapGridSize**2:
    raise Exception("Amount of map files in maps must be a perfect square.")

_maps.sort(key=lambda x: int(x[:2]))
_maps = list(map(name_to_file, _maps))
_maps = list(map(strip_newlines, _maps))
_maps = list(map(strings_to_lists, _maps))
_maps = list(
    map(lambda x: uniform_line_lengths(x, len(max(x, key=len, default=[]))),
        _maps))
_maps = rearranage_list(_maps, mapGridSize)
maps: List[List[MapSegment]] = []
for ir, row in enumerate(_maps):
    maps.append([])
    for ic, column in enumerate(row):
        maps[ir].append(MapSegment(column))

map_names = [
    ['The village', 'The Arena'],
    ['Open Field', 'Rural village'],
]
