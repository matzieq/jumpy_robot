from constants import GRAV, JUMP_FORCE, PLR_SPD
import pyxel
import utils
from utils import hit

IDLE = 1
JUMPING = 2
FALLING = 3
DOUBLE_JUMPING = 4


class Player:
    def __init__(self) -> None:
        self.x = 10
        self.y = 20
        self.vel_x = 0
        self.vel_y = 0
        self.dir = 1
        self.frame = IDLE
        self.on_ground = False
        self.double_jump = False

    def draw(self):
        if self.on_ground:
            self.frame = IDLE
        elif self.double_jump:
            self.frame = DOUBLE_JUMPING
        else:
            self.frame = JUMPING

        pyxel.blt(self.x, self.y, 0, self.frame * 8, 0, self.dir * 8, 8, 0)

    def update(self):
        self.vel_y += GRAV
        self.on_ground = False

        if hit(self.x + self.vel_x, self.y, 8, 8):
            self.vel_x = 0

        if hit(self.x, self.y + self.vel_y, 8, 8):
            if (self.vel_y >= 0):
                self.on_ground = True
                self.double_jump = False
                self.vel_x = 0
            self.vel_y = 0

        self.x += self.vel_x
        self.y += self.vel_y

    def jump(self):
        if self.on_ground:
            self.vel_y = -JUMP_FORCE
            self.vel_x = self.dir * PLR_SPD
            pyxel.play(0, 0)
        elif not self.double_jump:
            self.vel_y = -JUMP_FORCE
            self.double_jump = True
            self.dir = -self.dir
            self.vel_x = self.dir * PLR_SPD
            pyxel.play(0, 0)
