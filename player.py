import math
import pyxel
import utils
from utils import collide_map
from constants import GRAV, JUMP_FORCE, PLR_SPD

IDLE = 1
JUMPING = 2
FALLING = 3
DOUBLE_JUMPING = 4


class Player:
    def __init__(self) -> None:
        self.x = 10
        self.y = 20
        self.dx = 0
        self.dy = 0

        self.dir = 1

        self.frame = IDLE

        self.on_ground = False

        self.double_jump = False
        self.jump_pressed = False

    def draw(self, cam):
        if self.on_ground:
            self.frame = IDLE
        elif self.double_jump:
            self.frame = DOUBLE_JUMPING
        else:
            self.frame = JUMPING

        pyxel.blt(self.x - cam.x, self.y - cam.y,
                  0, self.frame * 8, 0, self.dir * 8, 8, 0)

    def update(self):
        self.apply_gravity()
        self.check_input()
        self.handle_collisions()
        self.move()

    def apply_gravity(self):
        self.dy += GRAV

    def check_input(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.jump()
            self.jump_pressed = True

        if pyxel.btnr(pyxel.KEY_SPACE):
            self.jump_pressed = False

        if not self.jump_pressed and self.dy < 0:
            self.dy /= 3

    def handle_collisions(self):
        self.on_ground = False

        if collide_map(self.x, self.y + self.dy, 8, 8):
            if (self.dy > 0):
                self.on_ground = True
                self.y = math.floor((self.y + self.dy) / 8) * 8 - 0.1
                self.double_jump = False
                self.dx = 0
            self.dy = 0

        if collide_map(self.x + self.dx, self.y, 8, 8) and not self.on_ground:
            self.dx = 0
            self.double_jump = False

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def jump(self):
        if self.on_ground:
            self.dy = -JUMP_FORCE
            self.dx = self.dir * PLR_SPD
            pyxel.play(0, 0)
        elif not self.double_jump:
            self.dy = -JUMP_FORCE
            self.double_jump = True
            self.dir = -self.dir
            self.dx = self.dir * PLR_SPD
            pyxel.play(0, 0)
