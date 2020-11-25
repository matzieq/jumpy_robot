from switch import Switch
from utils import collide_object, place_objects
from checkpoint import Checkpoint
from camera import Camera
import pyxel

from player import Player
from constants import CHECK, GRAV, MAP_HEIGHT, MAP_WIDTH, SWITCH


class Game:

    plr = Player()
    cam = Camera()

    def __init__(self) -> None:
        self.game_objects = {
            "check": [],
            "switch": [],
            "plr": [self.plr]
        }

        pyxel.init(256, 144, caption="Jump stick robo")
        pyxel.load('assets/jumpy_robot.pyxres')

        for x, y in place_objects(CHECK):
            self.game_objects["check"].append(
                Checkpoint(x * 8, y * 8, self.plr))

        for x, y in place_objects(SWITCH):
            self.game_objects["switch"].append(
                Switch(x * 8, y * 8))

        first_check = self.game_objects["check"][0]
        first_check.activate()
        self.plr.current_checkpoint = first_check
        self.plr.kill(True)
        self.plr.current_checkpoint.restore()

        pyxel.run(self.update, self.draw)

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0 - self.cam.x, 0 - self.cam.y,
                   0, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0)

        for obj_list in self.game_objects.values():
            for obj in obj_list:
                obj.draw(self.cam)

    def update(self):
        self.cam.update(self.plr.x, self.plr.y)

        for obj_list in self.game_objects.values():
            for obj in obj_list:
                obj.update()

        for checkpoint in self.game_objects['check']:
            if collide_object(self.plr, checkpoint) and not checkpoint.is_active:
                for check in self.game_objects['check']:
                    check.deactivate()
                checkpoint.activate()
                self.plr.current_checkpoint = checkpoint

        for game_switch in self.game_objects['switch']:
            if collide_object(self.plr, game_switch):
                game_switch.turn_on()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()


Game()
