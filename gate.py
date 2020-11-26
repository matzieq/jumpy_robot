

import pyxel
from typing import TYPE_CHECKING
from utils import collide_map, is_on_screen

ROW = 32

if TYPE_CHECKING:
    from camera import Camera


class Gate:
    is_open = False

    is_check = False
    is_bad = False
    is_solid = True
    is_switch = False

    def __init__(self, x: int, y: int, id: int) -> None:
        print(x, y)
        print("***")
        self.x = x
        self.y = y
        self.id = id

    def draw(self, cam: 'Camera'):
        if not self.is_open:
            pyxel.blt(self.x - cam.x, self.y - cam.y,
                      0, 0, ROW, 8, 8, 0)

    def update(self):
        pass

    def close(self):
        self.is_open = False

    def open(self):
        self.is_open = True
