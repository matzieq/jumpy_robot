from constants import SCREEN_HEIGHT, SCREEN_WIDTH
import math
from random import randint

import pyxel


class Camera:
    x = 0
    y = 0
    shake_x = 0
    shake_y = 0
    shake_magnitude = 0
    shake_duration = 0
    flash_color = -1

    def draw(self):
        if self.flash_color > -1 and self.flash_color <= 15:
            pyxel.rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.flash_color)
            self.flash_color = -1

    def update(self, target_x, target_y):
        self.x = math.floor(target_x / 256) * 256 + self.shake_x
        self.y = math.floor(target_y / 128) * 128 + self.shake_y

        if self.shake_duration:
            self.shake_x = randint(
                0, self.shake_magnitude * 2) - self.shake_magnitude
            self.shake_y = randint(
                0, self.shake_magnitude * 2) - self.shake_magnitude
            self.shake_duration -= 1
        else:
            self.shake_magnitude = 0
            self.shake_x = 0
            self.shake_y = 0

    def shake(self, duration: int, magnitude: int):
        self.shake_duration = duration
        self.shake_magnitude = magnitude

    def flash(self, color: int):
        self.flash_color = color
