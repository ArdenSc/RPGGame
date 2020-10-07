from os import listdir, path
from math import isqrt
from re import search

files = listdir(path.dirname(__file__))

# Maps

map_files = list(filter(lambda x: search("^\\d{2}.txt$", x), files))
map_files.sort(key=lambda x: int(x[:2]))

maplist = []

if len(map_files) != isqrt(len(map_files))**2:
    raise Exception("Amount of map files in maps must be a perfect square.")

for filename in map_files:
    with open(path.join(path.dirname(__file__), filename)) as file:
        maplist.append(file.read())

maps = []
mapwidth = isqrt(len(maplist))

for i in range(mapwidth):
    maps.append(maplist[:mapwidth])
    maplist = maplist[mapwidth:]

# Hitboxes

map_hitbox_files = list(
    filter(lambda x: search("^\\d{2}hitbox.txt$", x), files))
map_hitbox_files.sort(key=lambda x: int(x[:2]))

hitboxlist = []

if len(map_hitbox_files) != isqrt(len(map_hitbox_files))**2:
    raise Exception("Amount of hitbox files in maps must be a perfect square.")

for filename in map_hitbox_files:
    with open(path.join(path.dirname(__file__), filename)) as file:
        hitboxlist.append(file.read())

hitboxes = []
hitboxwidth = isqrt(len(hitboxlist))

for i in range(hitboxwidth):
    hitboxes.append(hitboxlist[:hitboxwidth])
    hitboxlist = hitboxlist[hitboxwidth:]
