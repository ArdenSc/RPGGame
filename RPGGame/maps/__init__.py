from RPGGame.MapSegment import MapSegment
from os import listdir, path
from math import isqrt
from re import search
from typing import List, TypeVar

files = listdir(path.dirname(__file__))


def strip_newlines(x: List[str]):
    return [y.rstrip() for y in x]


def name_to_file(x: str):
    with open(path.join(path.dirname(__file__), x)) as file:
        return file.readlines()


def strings_to_lists(x: List[str]) -> List[List[str]]:
    return list(map(lambda y: [z for z in y], x))


T = TypeVar('T')


def rearranage_list(list: List[T], columns: int) -> List[List[T]]:
    return [list[i:i + columns] for i in range(0, len(list), columns)]


def uniform_line_lengths(list: List[List[str]],
                         columns: int) -> List[List[str]]:
    return [x + [' '] * (columns - len(x)) for x in list]


# Maps

_maps = list(filter(lambda x: search("^\\d{2}.txt$", x), files))

mapGridSize = isqrt(len(_maps))
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
