from utils import place_objects
from checkpoint import Checkpoint
from camera import Camera
import math
import pyxel

from player import Player
from constants import CHECK, GRAV


class Game:
    plr = Player()
    checkpoints = []
    cam = Camera()

    def __init__(self) -> None:
        self.game_objects = {
            "plr": [self.plr],
            "check": self.checkpoints
        }

        pyxel.init(256, 144, caption="Jump stick robo")
        pyxel.load('assets/jumpy_robot.pyxres')

        for item in place_objects(CHECK):
            self.game_objects["check"].append(
                Checkpoint(item['x'] * 8, item['y'] * 8))

        pyxel.run(self.update, self.draw)

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0 - self.cam.x, 0 - self.cam.y, 0, 0, 0, 240, 32, 0)
        # for checkpoint in checkpoints:
        #     checkpoint.draw(cam)
        # plr.draw(cam)

        for obj_list in self.game_objects.values():
            for obj in obj_list:
                obj.draw(self.cam)

    def update(self):
        # plr.update()
        self.cam.update(self.plr.x, self.plr.y)

        # for checkpoint in checkpoints:
        #     checkpoint.update()

        for obj_list in self.game_objects.values():
            for obj in obj_list:
                obj.update()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()


Game()
