from utils import place_objects
from checkpoint import Checkpoint
from camera import Camera
import pyxel

from player import Player
from constants import CHECK, GRAV, MAP_HEIGHT, MAP_WIDTH


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
                Checkpoint(item['x'] * 8, item['y'] * 8, self.plr))

        first_check = self.game_objects["check"][0]
        first_check.switch_state("active")
        self.plr.current_checkpoint = first_check
        self.plr.kill()
        self.plr.current_checkpoint.restore()

        pyxel.run(self.update, self.draw)

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0 - self.cam.x, 0 - self.cam.y,
                   0, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0)

        pyxel.text(10, 10, str(self.plr.can_wall_jump), 7)

        for obj_list in self.game_objects.values():
            for obj in obj_list:
                obj.draw(self.cam)

    def update(self):
        # plr.update()
        self.cam.update(self.plr.x, self.plr.y)

        for obj_list in self.game_objects.values():
            for obj in obj_list:
                obj.update()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()


Game()
