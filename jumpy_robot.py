import functools
from hud import Hud
from switch import Switch
from utils import collide_object, place_objects
from checkpoint import Checkpoint
from camera import Camera
import pyxel

from player import Player
from constants import CHECK, MAP_HEIGHT, MAP_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, SWITCH


class Game:
    plr = Player()
    cam = Camera()
    flash_white = False
    score = 0

    def __init__(self) -> None:
        self.game_objects = {
            "check": [],
            "switch": [],
            "plr": [self.plr],
            "hud": [Hud(self)]
        }

        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Jump stick robo")
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

        if self.flash_white:
            pyxel.rect(0, 0, SCREEN_WIDTH, SCREEN_WIDTH, 15)
            self.flash_white = False

    def update(self):
        self.cam.update(self.plr.x, self.plr.y)
        self.update_objects()
        self.handle_checkpoint_collisions()
        self.handle_switch_collisions()
        self.check_quit()

    def update_objects(self):
        for obj_list in self.game_objects.values():
            for obj in obj_list:
                obj.update()

    def handle_checkpoint_collisions(self):
        for checkpoint in self.game_objects['check']:
            if collide_object(self.plr, checkpoint) and not checkpoint.is_active:
                for check in self.game_objects['check']:
                    check.deactivate()
                checkpoint.activate()
                pyxel.play(0, 7)
                self.cam.shake(5, 1)
                self.plr.current_checkpoint = checkpoint

    def check_quit(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def handle_switch_collisions(self):
        for game_switch in self.game_objects['switch']:
            if collide_object(self.plr, game_switch) and not game_switch.is_on:
                game_switch.turn_on()
                self.cam.shake(10, 3)
                self.flash_white = True
                self.recalculate_score()
                pyxel.play(0, 8)

    def recalculate_score(self):
        self.score = functools.reduce(
            lambda a, b: a.is_on + b.is_on, self.game_objects['switch'])


Game()
