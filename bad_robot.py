import math
import pyxel
from typing import TYPE_CHECKING
from utils import collide_map

if TYPE_CHECKING:
    from camera import Camera


ROW = 72
NORMAL = 0
BAD = 1
MOVE_SPEED = 3
BACK_SPEED = 0.5


class BadRobot:
    anim_frame = NORMAL
    timer = 60

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.update = self.idle

    def draw(self, cam: 'Camera'):
        pyxel.blt(self.x - cam.x, self.y - cam.y,
                  0, self.anim_frame * 8, ROW, 8, 8, 0)

    def idle(self):
        self.timer -= 1
        if self.timer <= 0:
            self.anim_frame = BAD
            self.timer = 60
            self.update = self.preparing

    def preparing(self):
        self.timer -= 1
        if self.timer <= 0:
            self.timer = 60
            self.update = self.attacking

    def attacking(self):
        self.y += MOVE_SPEED
        collide, _ = collide_map(self.x, self.y, 8, 8)
        print(self.y)
        if collide:
            self.anim_frame = NORMAL
            while collide_map(self.x, self.y, 8, 8)[0]:
                print(collide_map(self.x, self.y, 8, 8)[0])
                self.y -= 1
            self.update = self.retracting

    def retracting(self):
        self.y -= BACK_SPEED
        collide, _ = collide_map(self.x, self.y, 8, 8)

        if collide:
            self.update = self.idle
            self.y = math.floor(self.y + 1)
