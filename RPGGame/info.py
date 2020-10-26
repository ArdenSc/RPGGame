from RPGGame.maps import maps

for ir, r in enumerate(maps):
    for ic, c in enumerate(r):
        print(f"Map: (x={ir}, y={ic}) (w={c.width}, h={c.height})")
        print('\n'.join([''.join(x) for x in c.get()]))
