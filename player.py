from camera import Camera
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
    x = 10
    y = 20
    dx = 0
    dy = 0
    dir = 1
    frame = IDLE
    on_ground = False
    double_jump = False
    jump_pressed = False
    current_checkpoint = (0, 0)

    def __init__(self) -> None:
        self.update = self.update_normal
        self.draw = self.draw_normal

    def draw_normal(self, cam: Camera):
        if self.on_ground:
            self.frame = IDLE
        elif self.double_jump:
            self.frame = DOUBLE_JUMPING
        else:
            self.frame = JUMPING

        pyxel.blt(self.x - cam.x, self.y - cam.y,
                  0, self.frame * 8, 0, self.dir * 8, 8, 0)

    def draw_dead(self, cam: Camera):
        pass

    def update_normal(self):
        self.apply_gravity()
        self.check_input()
        self.handle_collisions()
        self.move()

    def update_dead(self):
        self.x, self.y = self.current_checkpoint

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

        collide, harm = collide_map(self.x, self.y + self.dy, 8, 8)

        if harm:
            self.kill()

        if collide:
            if (self.dy > 0):
                self.on_ground = True
                self.y = math.floor((self.y + self.dy) / 8) * 8 - 0.1
                self.double_jump = False
                self.dx = 0
            self.dy = 0

        collide, harm = collide_map(self.x + self.dx, self.y, 8, 8)

        if collide and not self.on_ground:
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

    def kill(self):
        self.draw = self.draw_dead
        self.update = self.update_dead

    def restore(self):
        self.draw = self.draw_normal
        self.update = self.update_normal
