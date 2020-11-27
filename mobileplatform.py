import math
import pyxel
from constants import TILE_SIZE
from typing import TYPE_CHECKING
from utils import collide_map, is_on_screen

if TYPE_CHECKING:
    from camera import Camera

ROW = 96


class MobilePlatform:
    is_check = False
    is_bad = False
    is_solid = True
    is_switch = False

    spd = 1

    def __init__(self, x: int, y: int, start_moving_up: bool = False) -> None:
        self.x = x
        self.y = y
        self.top_level = y if not start_moving_up else y - (5 * TILE_SIZE)
        self.bottom_level = y if start_moving_up else y + (5 * TILE_SIZE)
        self.dir = -1 if start_moving_up else 1

    def draw(self, cam: 'Camera'):
        pyxel.blt(self.x - cam.x, self.y - cam.y + 1,
                  0, 0, ROW, 8, 8, 0)

    def update(self):
        if self.dir > 0 and self.y >= self.bottom_level:
            self.dir = -1
        elif self.dir < 0 and self.y <= self.top_level:
            self.dir = 1
        self.y += self.spd * self.dir
