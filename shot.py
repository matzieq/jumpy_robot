from constants import MAX_FALLING_SPEED
import math
import pyxel
from typing import TYPE_CHECKING
from utils import collide_map, is_on_screen

if TYPE_CHECKING:
    from camera import Camera


ROW = 88
NORMAL = 0
SHOOTING = 1
FREQ = 60
BACK_SPEED = 1


class Shot:
    is_check = False
    is_bad = True
    is_solid = False
    is_switch = False

    is_alive = True
    is_narrow = True

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y

    def draw(self, cam: 'Camera'):
        if self.is_alive:
            pyxel.blt(self.x - cam.x, self.y - cam.y,
                      0, 0, ROW, 8, 8, 0)

    def update(self):
        if self.is_alive:
            self.y += 3
            collide, _ = collide_map(self.x, self.y, 8, 8)
            if collide:
                self.kill()

    def kill(self):
        self.reset()
        self.is_alive = False

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y

    def fire(self):
        self.reset()
        self.is_alive = True
