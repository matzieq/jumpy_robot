import math
import pyxel

INITIAL_ADDRESS = 0
ROW = 40
FPS = 20


class Checkpoint:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.state = "restoring"
        self.is_active = False

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

    def update(self):
        if self.current_anim['frame_timer'] <= 0:
            self.current_anim['frame_timer'] = self.current_anim['frame_duration']

            if self.current_anim["frame"] < len(self.anims[self.state]) - 1:
                self.current_anim["frame"] += 1
            else:
                self.current_anim["frame"] = 0

        self.current_anim['frame_timer'] -= 1

    def draw(self, cam):
        pyxel.blt(self.x - cam.x, self.y - cam.y,
                  0, self.current_anim["frame"] * 8, ROW, 8, 8, 0)

    def switch_anim(self, new_anim: str):
        self.state = new_anim
        self.current_anim = {
            "frame": 0,
            "frame_timer": 0,
            "frame_duration": math.floor(60 / FPS)
        }
