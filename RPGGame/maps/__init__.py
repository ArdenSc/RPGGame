from os import listdir, path
from math import isqrt
import numpy as np

files = listdir(path.dirname(__file__))
files = list(filter(lambda x: x.endswith('.txt'), files))
files.sort(key=lambda x: int(x[:2]))

maplist = []

if len(files) != isqrt(len(files))**2:
    raise Exception("Amount of text files in maps must be a perfect square.")

for filename in files:
    with open(path.join(path.dirname(__file__), filename)) as file:
        maplist.append(file.read())

maplist = np.reshape(np.array(maplist), (isqrt(len(maplist)), -1))
print(maplist)
