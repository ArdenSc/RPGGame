from RPGGame.maps import maps

for ir, r in enumerate(maps):
    for ic, c in enumerate(r):
        print(f"Map: (x={ir}, y={ic}) (w={len(c.map[0])}, h={len(c.map)})")
        print('\n'.join([''.join(x) for x in c.map]))
