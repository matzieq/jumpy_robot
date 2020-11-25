from constants import BACK_WALL, MAP_HEIGHT, MAP_WIDTH
import pyxel
import math

solid_tiles = [32, 96]
harmful_tiles = [96, 97, 98, 99]


def collide_map(x: float, y: float, w: int, h: int):
    collide = False
    harm = False
    x = math.floor(x)
    y = math.floor(y)
    i = x
    while i < x+w:
        current_tiles = [pyxel.tilemap(0).get(
            i/8, y/8), pyxel.tilemap(0).get(i/8, (y+h)/8)]
        for tile in current_tiles:
            if tile in solid_tiles:
                collide = True
            if tile in harmful_tiles:
                harm = True
        i += 1

    i = y
    while i < y + h:
        current_tiles = [pyxel.tilemap(0).get(
            x/8, i/8), pyxel.tilemap(0).get((x+w)/8, i/8)]
        for tile in current_tiles:
            if tile in solid_tiles:
                collide = True
            if tile in harmful_tiles:
                harm = True
        i += 1

    return collide, harm


def collide_object(self, other):
    return self.x < other.x + 8 and self.x + 8 > other.x and self.y < other.y + 8 and self.y + 8 > other.y


def place_objects(obj_type: int):
    coords = []
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if pyxel.tilemap(0).get(x, y) == obj_type:
                coords.append((x, y))
                pyxel.tilemap(0).set(x, y, BACK_WALL)
    return coords
