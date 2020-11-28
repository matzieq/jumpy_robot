from mobileplatform import MobilePlatform
from gate import Gate
from bad_robot import BadRobot
import json
from hud import Hud
from switch import Switch
from utils import button_pressed, button_released, collide_object, overlap_map_area, place_objects
from checkpoint import Checkpoint
from camera import Camera
import pyxel
from operator import itemgetter
import os
import sys
from laser import Laser

from player import Player
from constants import BADDER_ROBOT, BAD_ROBOT, CHECK, FAST_LASER, GATE_IDS, GATE_START_ADDRESS, LASER, MAP_HEIGHT, MAP_WIDTH, MOVING_PLATFORM, MOVING_PLATFORM_OPPOSITE, SCREEN_HEIGHT, SCREEN_WIDTH, SWITCH, TILE_SIZE, VERY_FAST_LASER

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

DEBUG_MODE = True

# for instrucitons: tuples with x, y, w, h of images

game_buttons = (0, 144, 16, 16)
arrow = (32, 144, 8, 8)
guy = (16, 0, 8, 8)
wall_jump_guy = (24, 0, 8, 8)
double_jump_guy = (32, 8, 8, 8)
floor = (16, 144, 8, 8)
wall = (24, 144, 8, 8)
hand = (40, 144, 8, 8)
hand_clock = (48, 144, 16, 16)


class Game:
    plr = Player()
    cam = Camera()
    flash_white = False
    score = 0
    key_used = None
    key_timer = 0
    menu_option = 0
    is_instructions = False

    def __init__(self) -> None:
        self.game_objects = {
            "check": [],
            "switch": [],
            "robot": [],
            "platform": [],
            "laser": [],
            "shot": [],
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
        self.draw_state = self.draw_title

        self.update_state = self.update_title

        pyxel.run(self.update, self.draw)

    def update(self):
        self.update_state()

    def draw(self):
        self.draw_state()

    def draw_game(self):
        pyxel.cls(0)
        pyxel.bltm(0 - self.cam.x, 0 - self.cam.y,
                   0, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0)

        for obj_list in self.game_objects.values():
            for obj in obj_list:
                obj.draw(self.cam)
        self.cam.draw()

    def update_game(self):

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

        for x, y in place_objects(LASER):
            self.game_objects["laser"].append(
                Laser(x * 8, y * 8, self, self.cam, 3))

        for x, y in place_objects(FAST_LASER):
            self.game_objects["laser"].append(
                Laser(x * 8, y * 8, self, self.cam, 2))

        for x, y in place_objects(VERY_FAST_LASER):
            self.game_objects["laser"].append(
                Laser(x * 8, y * 8, self, self.cam, 1))

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

    def draw_title(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 128, 32, 19)
        pyxel.blt(100, 20,
                  0, 0, 104, 48, 24)
        if self.is_instructions:
            self.draw_instructions()
        else:

            pyxel.blt(120, 60,
                      0, 16, 128, 16, 9)
            pyxel.blt(120, 72,
                      0, 32, 128, 16, 9)
            pyxel.rectb(120, 60 + self.menu_option * 12, 16, 9, 7)
            pyxel.rectb(120, 60 + self.menu_option *
                        12, self.key_timer / 2, 9, 6)
            self.draw_sprite_tuple(120, 90, game_buttons)
            self.draw_sprite_tuple(138, 94, hand)
            pyxel.text(150, 94, "/", 7)
            self.draw_sprite_tuple(158, 90, hand_clock)

        pyxel.text(71, 121, "A GAME BY PRESIDENT OF SPACE", 5)
        pyxel.text(70, 120, "A GAME BY PRESIDENT OF SPACE", 6)

    def update_title(self):
        key = button_pressed()
        if self.is_instructions and key != None:
            self.is_instructions = False
            return

        if key != None:
            self.key_used = key

        if self.key_used != None and not self.is_instructions:
            self.key_timer += 1

            if self.key_timer > 30:
                if self.menu_option == 0:
                    self.update_state = self.update_game
                    self.draw_state = self.draw_game
                    pyxel.playm(0, loop=True)

                elif self.menu_option == 1:
                    self.is_instructions = True
                self.key_timer = 0
                pyxel.play(0, 7)

            if button_released(self.key_used):
                self.key_used = None
                if self.key_timer <= 30:
                    self.menu_option = (self.menu_option + 1) % 2
                    pyxel.play(0, 10)
                    self.key_timer = 0

    def draw_instructions(self):
        start_x = 20
        self.draw_sprite_tuple(start_x + 30, 100, game_buttons)
        self.draw_sprite_tuple(start_x + 48, 106, hand)
        self.draw_sprite_tuple(start_x + 36, 90, floor)
        self.draw_sprite_tuple(start_x + 40, 80, arrow)
        self.draw_sprite_tuple(start_x + 48, 70, guy)

        self.draw_sprite_tuple(start_x + 80, 100, game_buttons)
        self.draw_sprite_tuple(start_x + 98, 106, hand)
        self.draw_sprite_tuple(start_x + 108, 106, hand)
        self.draw_sprite_tuple(start_x + 86, 90, floor)
        self.draw_sprite_tuple(start_x + 90, 80, arrow, False)
        self.draw_sprite_tuple(start_x + 90, 70, arrow, True)
        self.draw_sprite_tuple(start_x + 80, 60, double_jump_guy, True)

        self.draw_sprite_tuple(start_x + 130, 100, game_buttons)
        self.draw_sprite_tuple(start_x + 148, 106, hand)
        self.draw_sprite_tuple(start_x + 158, 106, hand)
        self.draw_sprite_tuple(start_x + 168, 106, hand)
        pyxel.text(start_x + 178, 108, "...", 7)
        self.draw_sprite_tuple(start_x + 136, 90, floor)
        self.draw_sprite_tuple(start_x + 150, 50, wall, True)
        self.draw_sprite_tuple(start_x + 150, 70, wall, True)
        self.draw_sprite_tuple(start_x + 130, 60, wall, False)
        self.draw_sprite_tuple(start_x + 140, 80, arrow, False)
        self.draw_sprite_tuple(start_x + 140, 70, arrow, True)
        self.draw_sprite_tuple(start_x + 140, 60, arrow, False)
        self.draw_sprite_tuple(start_x + 146, 50, wall_jump_guy)

    def draw_sprite_tuple(self, coord_x: int, coord_y: int, sprite_tuple: tuple[int], flipped: bool = False):
        x, y, w, h = sprite_tuple
        pyxel.blt(coord_x, coord_y, 0, x, y, w if not flipped else -w, h, 0)


Game()
