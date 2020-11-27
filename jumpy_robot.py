from mobileplatform import MobilePlatform
from gate import Gate
from bad_robot import BadRobot
import json
from hud import Hud
from switch import Switch
from utils import collide_object, overlap_map_area, place_objects
from checkpoint import Checkpoint
from camera import Camera
import pyxel
from operator import itemgetter
import os
import sys

from player import Player
from constants import BADDER_ROBOT, BAD_ROBOT, CHECK, GATE_IDS, GATE_START_ADDRESS, MAP_HEIGHT, MAP_WIDTH, MOVING_PLATFORM, MOVING_PLATFORM_OPPOSITE, SCREEN_HEIGHT, SCREEN_WIDTH, SWITCH, TILE_SIZE

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

DEBUG_MODE = True


class Game:
    plr = Player()
    cam = Camera()
    flash_white = False
    score = 0

    def __init__(self) -> None:
        self.game_objects = {
            "check": [],
            "switch": [],
            "robot": [],
            "platform": [],
            "gate": [],
            "plr": [self.plr],
            "hud": [Hud(self)]
        }
        self.game_data = {}

        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Jump stick robo")
        pyxel.load(os.path.join(os.path.dirname(__file__),
                                'assets', 'jumpy_robot.pyxres'),)

        self.load_objects()

        first_check = self.game_objects["check"][0]
        first_check.activate()
        self.plr.current_checkpoint = first_check
        self.plr.kill(True)
        self.plr.current_checkpoint.restore()

        with open(os.path.join(os.path.dirname(__file__), 'assets', 'data.json'), 'r') as j:
            self.game_data = json.load(j)

        self.update_gate_status()
        pyxel.run(self.update, self.draw)

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0 - self.cam.x, 0 - self.cam.y,
                   0, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0)

        for obj_list in self.game_objects.values():
            for obj in obj_list:
                obj.draw(self.cam)
        self.cam.draw()

    def update(self):
        self.cam.update(self.plr.x, self.plr.y)
        self.update_objects()
        self.handle_collisions()
        self.check_trigger_areas()
        self.check_quit()

    def update_objects(self):
        for obj_list in self.game_objects.values():
            for obj in obj_list:
                obj.update()

    def handle_collisions(self):
        for obj_list in self.game_objects.values():
            for obj in obj_list:
                if collide_object(self.plr, obj):
                    if obj.is_check:
                        self.handle_checkpoint_collisions(obj)
                    if obj.is_bad:
                        self.handle_harmful_collisions()
                    if obj.is_switch:
                        self.handle_switch_collisions(obj)
                    if obj.is_solid:
                        self.handle_solid_collisions(obj)

    def handle_checkpoint_collisions(self, checkpoint):
        if not checkpoint.is_active:
            for check in self.game_objects['check']:
                check.deactivate()
            checkpoint.activate()
            pyxel.play(0, 7)
            self.cam.shake(5, 1)
            self.plr.current_checkpoint = checkpoint

    def handle_switch_collisions(self, game_switch):
        if not game_switch.is_on:
            game_switch.turn_on()
            self.cam.shake(10, 3)
            self.cam.flash(7)
            self.recalculate_score()
            pyxel.play(0, 8)

    def handle_harmful_collisions(self):
        self.plr.kill()

    def handle_solid_collisions(self, obj):
        self.plr.handle_solid_object_collision(obj)

    def recalculate_score(self):
        score = 0
        for switch in self.game_objects["switch"]:
            if switch.is_on:
                score += 1

        self.score = score

    def load_objects(self):
        for x, y in place_objects(CHECK):
            self.game_objects["check"].append(
                Checkpoint(x * 8, y * 8, self.plr))

        for x, y in place_objects(SWITCH):
            self.game_objects["switch"].append(
                Switch(x * 8, y * 8))

        for x, y in place_objects(BAD_ROBOT):
            self.game_objects["robot"].append(
                BadRobot(x * 8, y * 8, self.cam))

        for x, y in place_objects(BADDER_ROBOT):
            self.game_objects["robot"].append(
                BadRobot(x * 8, y * 8, self.cam, True))

        for x, y in place_objects(MOVING_PLATFORM):
            self.game_objects["platform"].append(
                MobilePlatform(x * 8, y * 8))

        for x, y in place_objects(MOVING_PLATFORM_OPPOSITE):
            self.game_objects["platform"].append(
                MobilePlatform(x * 8, y * 8, True))

        for id in range(1, GATE_IDS + 1):
            for x, y in place_objects(GATE_START_ADDRESS + id):
                self.game_objects["gate"].append(Gate(x * 8, y * 8, id))

    def update_gate_status(self):
        for gate_status in self.game_data["gate_starting_state"]:
            for gate in self.game_objects["gate"]:
                if gate.id == gate_status["id"] and gate_status["open"]:
                    gate.open()

    def check_trigger_areas(self):
        for area in self.game_data["gate_trigger_areas"]:
            for gate in self.game_objects["gate"]:
                if gate.id == area["id"]:
                    rect = area["rect"]
                    x, y, w, h = itemgetter('x', 'y', 'w', 'h')(rect)

                    if overlap_map_area(self.plr, x, y, w, h) and gate.is_open != area["target_open_state"]:
                        if area["target_open_state"]:
                            gate.open()
                        else:
                            gate.close()
                        check_x, check_y = itemgetter("x", "y")(
                            area["checkpoint_activate"])
                        checkpoint_to_toggle = next(
                            (check for check in self.game_objects["check"] if check.x == check_x * TILE_SIZE and check.y == check_y * TILE_SIZE), None)
                        if checkpoint_to_toggle != None:
                            self.handle_checkpoint_collisions(
                                checkpoint_to_toggle)

    def check_quit(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if DEBUG_MODE:
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.plr.x -= 100
            if pyxel.btnp(pyxel.KEY_RIGHT):
                self.plr.x += 100
            if pyxel.btnp(pyxel.KEY_UP):
                self.plr.y -= 100
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.plr.y += 100


Game()
