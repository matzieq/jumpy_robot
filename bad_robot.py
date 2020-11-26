import math
import pyxel
from typing import TYPE_CHECKING
from utils import collide_map, is_on_screen

if TYPE_CHECKING:
    from camera import Camera


ROW = 72
NORMAL = 0
BAD = 1
MOVE_SPEED = 3
BACK_SPEED = 0.5


class BadRobot:
    anim_frame = NORMAL

    is_check = False
    is_bad = True
    is_solid = False
    is_switch = False

    def __init__(self, x: int, y: int, cam_ref: 'Camera', is_badder: bool = False) -> None:
        self.x = x
        self.y = y
        self.update = self.idle
        self.cam_ref = cam_ref
        self.max_timer = 30 if is_badder else 60
        self.timer = self.max_timer

    def draw(self, cam: 'Camera'):
        pyxel.blt(self.x - cam.x, self.y - cam.y,
                  0, self.anim_frame * 8, ROW, 8, 8, 0)

    def idle(self):
        self.timer -= 1
        if self.timer <= 0:
            self.anim_frame = BAD
            self.timer = self.max_timer
            self.update = self.preparing

    def preparing(self):
        self.timer -= 1
        if self.timer <= 0:
            self.timer = self.max_timer
            self.update = self.attacking

    def attacking(self):
        self.y += MOVE_SPEED
        collide, _ = collide_map(self.x, self.y, 8, 8)

        if collide:
            self.anim_frame = NORMAL

            while collide_map(self.x, self.y, 8, 8)[0]:
                self.y -= 1

            self.update = self.retracting
            if is_on_screen(self.x, self.y, self.cam_ref):
                self.cam_ref.shake(3, 1)
                pyxel.play(0, 9)

    def retracting(self):
        self.y -= BACK_SPEED
        collide, _ = collide_map(self.x, self.y, 8, 8)

        if collide:
            self.update = self.idle
            self.y = math.floor(self.y + 1)
