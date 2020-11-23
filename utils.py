from constants import BACK_WALL, MAP_HEIGHT, MAP_WIDTH
import pyxel
import math

solid_tiles = [32, 96]


def collide_map(x: float, y: float, w: int, h: int):
    collide = False
    x = math.floor(x)
    y = math.floor(y)
    i = x
    while i < x+w:
        if pyxel.tilemap(0).get(i/8, y/8) in solid_tiles or pyxel.tilemap(0).get(i/8, (y+h)/8) in solid_tiles:
            collide = True
        i += 1

    i = y
    while i < y + h:
        if pyxel.tilemap(0).get(x/8, i/8) in solid_tiles or pyxel.tilemap(0).get((x+w)/8, i/8) in solid_tiles:
            collide = True
        i += 1

    return collide


def place_objects(obj_type: int):
    coords = []
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if pyxel.tilemap(0).get(x, y) == obj_type:
                coords.append({"x": x, "y": y})
                pyxel.tilemap(0).set(x, y, BACK_WALL)
    return coords
