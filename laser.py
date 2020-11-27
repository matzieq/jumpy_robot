from shot import Shot
from constants import MAX_FALLING_SPEED
import math
import pyxel
from typing import TYPE_CHECKING
from utils import collide_map, is_on_screen

if TYPE_CHECKING:
    from camera import Camera
    from jumpy_robot import Game


ROW = 80
NORMAL = 0
SHOOTING = 1
FREQ = 30
BACK_SPEED = 1


class Laser:
    anim_frame = NORMAL

    is_check = False
    is_bad = True
    is_solid = False
    is_switch = False

    def __init__(self, x: int, y: int, game_ref: 'Game', cam_ref: 'Camera', spd: int) -> None:
        self.x = x
        self.y = y
        self.update = self.idle
        self.cam_ref = cam_ref
        self.max_timer = spd * FREQ
        self.timer = self.max_timer
        self.shot = Shot(self.x, self.y)
        game_ref.game_objects["shot"].append(self.shot)

    def draw(self, cam: 'Camera'):
        pyxel.blt(self.x - cam.x, self.y - cam.y,
                  0, self.anim_frame * 8, ROW, 8, 8, 0)

    def idle(self):
        self.timer -= 1
        if self.timer <= 0 and not self.shot.is_alive:
            self.anim_frame = SHOOTING
            self.timer = 5
            self.update = self.shooting
            self.shot.fire()

            if is_on_screen(self.x, self.y, self.cam_ref):
                pyxel.play(0, 9)

    def shooting(self):
        self.shot.update()
        self.timer -= 1
        if self.timer <= 0:
            self.timer = self.max_timer
            self.update = self.idle
            self.anim_frame = NORMAL
