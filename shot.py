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

    alive = True
    is_narrow = True

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def draw(self, cam: 'Camera'):
        if self.alive:
            pyxel.blt(self.x - cam.x, self.y - cam.y,
                      0, self.anim_frame * 8, ROW, 8, 8, 0)

    def update(self):
        if self.alive:
            self.y += 3
            if collide_map(self.x, self.y, 8, 8):
                self.kill()

    def kill(self):
        self.alive = False
