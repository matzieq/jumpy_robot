from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from player import Player
import math
import pyxel

INITIAL_ADDRESS = 0
ROW = 40
FPS = 20


class Checkpoint:
    state = "inactive"
    is_active = False

    is_check = True
    is_bad = False
    is_solid = False
    is_switch = False

    def __init__(self, x: int, y: int, plr_ref: 'Player') -> None:
        self.x = x
        self.y = y

        self.anims = {
            "inactive": [11],
            "active": [0],
            "restoring": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        }

        self.current_anim = {
            "frame": 0,
            "frame_timer": 0,
            "frame_duration": math.floor(60 / FPS)
        }

        self.plr_ref = plr_ref

    def update(self):
        if self.current_anim['frame_timer'] <= 0:
            self.current_anim['frame_timer'] = self.current_anim['frame_duration']

            if self.current_anim["frame"] < len(self.anims[self.state]) - 1:
                self.current_anim["frame"] += 1
            else:
                if self.state == "restoring":
                    self.switch_state(
                        "active" if self.is_active else "inactive")
                self.current_anim["frame"] = 0

        self.current_anim['frame_timer'] -= 1

        if self.is_active and self.current_anim["frame"] == 9:
            self.plr_ref.restore()

    def draw(self, cam):
        current_frame = self.anims[self.state][self.current_anim["frame"]] * 8
        pyxel.blt(self.x - cam.x, self.y - cam.y,
                  0, current_frame, ROW, 8, 8, 0)

    def switch_anim(self, new_anim: str):
        self.state = new_anim
        self.current_anim = {
            "frame": 0,
            "frame_timer": 0,
            "frame_duration": math.floor(60 / FPS)
        }

    def activate(self):
        self.switch_state("active")
        self.is_active = True

    def deactivate(self):
        self.switch_state("inactive")
        self.is_active = False

    def restore(self):
        self.switch_state("restoring")

    def switch_state(self, new_state):
        self.current_anim = {
            "frame": 0,
            "frame_timer": 0,
            "frame_duration": math.floor(60 / FPS)
        }

        self.state = new_state

        if new_state == 'active':
            self.is_active = True
