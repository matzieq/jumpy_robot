from constants import SCREEN_WIDTH
import pyxel
from typing import TYPE_CHECKING
from functools import reduce

if TYPE_CHECKING:
    from jumpy_robot import Game
    from camera import Camera

HIDDEN = 0
VISITED = 1
CURRENT = 2


class Hud:
    is_check = False
    is_bad = False
    is_solid = False
    is_switch = False
    x = 0
    y = 0

    minimap = []

    def __init__(self, game_ref: 'Game') -> None:
        self.game_ref = game_ref

    def draw(self, cam: 'Camera'):
        pyxel.rect(0, 128, SCREEN_WIDTH, 16, 0)
        pyxel.blt(8, 132, 0, 0, 48, 8, 8, 0)
        pyxel.text(
            20, 134, f"{self.game_ref.score} / {len(self.game_ref.game_objects['switch'])}", 7)

    def update(self):
        pass
