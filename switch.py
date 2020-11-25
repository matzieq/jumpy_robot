import pyxel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from camera import Camera

ROW = 48


class Switch:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.is_on = 0

    def draw(self, cam: 'Camera'):
        pyxel.blt(self.x - cam.x, self.y - cam.y,
                  0, self.is_on * 8, ROW, 8, 8, 0)

    def turn_on(self):
        self.is_on = 1

    def update(self):
        pass
