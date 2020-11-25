from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from checkpoint import Checkpoint
from camera import Camera
import math
import pyxel
import utils
from utils import collide_map
from constants import GRAV, JUMP_FORCE, MAX_FALLING_SPEED, PLR_SPD

IDLE = 1
JUMPING = 2
WALL_JUMPING = 3
DOUBLE_JUMPING = 4
NEXT_ROW_OFFSET = 8

DEATH_PUFF_ROW = 56
JUMP_PUFF_ROW = 64


class Player:
    x = 16
    y = 20
    dx = 0
    dy = 0
    dir = 1
    frame = JUMPING
    on_ground = False
    double_jump = False
    jump_pressed = False
    can_wall_jump = False
    current_checkpoint = None
    puff_frame_timer = 0
    death_puff = {
        "x": 0,
        "y": 0,
        "frame": 0,
        "frame_duration": 3,
        "frame_list": [0, 1, 2, 3, 4, 5, 6]
    }

    jump_puff = {
        "x": 0,
        "y": 0,
        "frame": 5,
        "frame_duration": 3,
        "frame_list": [0, 1, 2, 3, 4]
    }

    def __init__(self) -> None:
        self.update = self.update_normal
        self.draw = self.draw_normal

    def draw_normal(self, cam: Camera):
        if self.on_ground:
            self.frame = IDLE
        elif self.can_wall_jump and not self.jump_pressed:
            self.frame = WALL_JUMPING
        elif self.double_jump:
            self.frame = DOUBLE_JUMPING
        else:
            self.frame = JUMPING

        pyxel.blt(self.x - cam.x, self.y - cam.y + 1,
                  0, self.frame * 8, int(self.double_jump) * NEXT_ROW_OFFSET, self.dir * 8, 8, 0)
        self.draw_jump_puff(cam)

    def draw_jump_puff(self, cam: Camera):
        puff = self.jump_puff
        if puff['frame'] < len(puff['frame_list']):
            frame_number = puff['frame_list'][puff['frame']]
            pyxel.blt(puff['x'] - cam.x, puff['y'] - cam.y, 0,
                      frame_number * 8, JUMP_PUFF_ROW, self.dir * 8, 8, 0)
            puff['frame'] += 1

    def draw_dead(self, cam: Camera):
        self.puff_frame_timer += 1
        puff = self.death_puff

        frame_number = puff['frame_list'][puff['frame']]

        pyxel.blt(puff['x'] - cam.x, puff['y'] - cam.y, 0,
                  frame_number * 8, DEATH_PUFF_ROW, 8, 8, 0)

        if self.puff_frame_timer % 2 == 0:
            puff['frame'] += 1

    def draw_none(self, cam: Camera):
        pass

    def update_normal(self):
        self.apply_gravity()
        self.check_input()
        self.handle_collisions()
        self.move()

    def update_dead(self):
        puff = self.death_puff
        if puff['frame'] >= len(puff['frame_list']):
            puff['frame'] = 0
            self.draw = self.draw_none
            pyxel.play(0, 5)
            self.current_checkpoint.restore()
            self.x, self.y = self.current_checkpoint.x - 1, self.current_checkpoint.y
        pass

    def apply_gravity(self):
        if self.dy < MAX_FALLING_SPEED:
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

        # handle vertical collisions
        collide, harm = collide_map(self.x, self.y + self.dy, 7, 8)

        if harm:
            self.kill()

        if collide:
            if (self.dy > 0):
                self.on_ground = True
                self.y = math.floor((self.y + self.dy) / 8) * 8 - 0.1
                self.double_jump = False
                self.dx = 0
            self.dy = 0

        # handle horizontal collisions
        collide, harm = collide_map(self.x + self.dx, self.y, 7, 8)

        if harm:
            self.kill()

        if collide:
            if self.dx > 0:
                self.x = math.floor((self.x + self.dx) / 8) * 8 + 0.1
            elif self.dx < 0:
                self.x = math.ceil((self.x + self.dx) / 8) * 8

            self.dx = 0

        # handle wall jump
        is_wall_left, harm = collide_map(self.x - 3, self.y, 8, 8)
        is_wall_right, harm = collide_map(self.x + 3, self.y, 8, 8)

        if harm:
            self.kill()
        else:
            self.can_wall_jump = is_wall_left or is_wall_right

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def jump(self):
        if self.on_ground:
            self.dy = -JUMP_FORCE
            self.dx = self.dir * PLR_SPD
            pyxel.play(0, 0)
        elif not self.double_jump and not self.can_wall_jump:
            self.jump_puff['x'] = self.x
            self.jump_puff['y'] = self.y - 8
            self.jump_puff['frame'] = 0
            self.dy = -JUMP_FORCE
            self.double_jump = True
            self.dir = -self.dir
            self.dx = self.dir * PLR_SPD
            pyxel.play(0, 6)
        if not self.on_ground and self.can_wall_jump:
            self.dy = -JUMP_FORCE
            self.dir = -self.dir
            self.dx = self.dir * PLR_SPD
            pyxel.play(0, 0)

    def kill(self, no_anim: bool = False):
        self.draw = self.draw_dead
        self.update = self.update_dead
        self.death_puff["x"] = self.x
        self.death_puff["y"] = self.y
        self.puff_frame_timer = 7 if no_anim else 0
        self.dir = 1
        self.dx = 0
        self.dy = 0
        pyxel.play(0, 4)

    def restore(self):
        self.draw = self.draw_normal
        self.update = self.update_normal

    def set_checkpoint(self, new_check: 'Checkpoint'):
        self.current_checkpoint = new_check
