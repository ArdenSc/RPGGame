from RPGGame.MapSegment import MapSegment
from os import listdir, path
from math import isqrt
from re import search
from typing import List, TypeVar

files = listdir(path.dirname(__file__))


def stripNewlines(x: List[str]):
    return [y.rstrip() for y in x]


def nameToFileLines(x: str):
    with open(path.join(path.dirname(__file__), x)) as file:
        return file.readlines()


def linesToCharLists(x: List[str]) -> List[List[str]]:
    return list(map(lambda y: [z for z in y], x))


T = TypeVar('T')


def rearranageList(list: List[T], columns: int) -> List[List[T]]:
    return [list[i:i + columns] for i in range(0, len(list), columns)]


def uniformLineLengths(list: List[List[str]], columns: int) -> List[List[str]]:
    print(f"ull {list}")
    print(f"ull {columns}")
    return [x + [' '] * (columns - len(x)) for x in list]


# Maps

_maps = list(filter(lambda x: search("^\\d{2}.txt$", x), files))

mapGridSize = isqrt(len(_maps))
if len(_maps) != mapGridSize**2:
    raise Exception("Amount of map files in maps must be a perfect square.")

_maps.sort(key=lambda x: int(x[:2]))
_maps = list(map(nameToFileLines, _maps))
_maps = list(map(stripNewlines, _maps))
_maps = list(map(linesToCharLists, _maps))
_maps = list(
    map(lambda x: uniformLineLengths(x, len(max(x, key=len, default=[]))),
        _maps))
_maps = rearranageList(_maps, mapGridSize)
maps = []
for ir, row in enumerate(_maps):
    maps.append([])
    for ic, column in enumerate(row):
        maps[ir].append(MapSegment(column))

# Hitboxes

# map_hitbox_files = list(
#     filter(lambda x: search("^\\d{2}hitbox.txt$", x), files))
# map_hitbox_files.sort(key=lambda x: int(x[:2]))

# hitboxlist = []

# if len(map_hitbox_files) != isqrt(len(map_hitbox_files))**2:
#     raise Exception("Amount of hitbox files in maps must be a perfect square.")

# for filename in map_hitbox_files:
#     with open(path.join(path.dirname(__file__), filename)) as file:
#         hitboxlist.append(file.read())

# hitboxes = []
# hitboxwidth = isqrt(len(hitboxlist))

# for i in range(hitboxwidth):
#     hitboxes.append(hitboxlist[:hitboxwidth])
#     hitboxlist = hitboxlist[hitboxwidth:]
