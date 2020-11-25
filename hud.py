import pyxel
from typing import TYPE_CHECKING
from functools import reduce

if TYPE_CHECKING:
    from jumpy_robot import Game
    from camera import Camera


class Hud:
    def __init__(self, game_ref: 'Game') -> None:
        self.game_ref = game_ref

    def draw(self, cam: 'Camera'):
        pyxel.text(8, 130, f"Score: {self.game_ref.score}", 7)
        pyxel.text(
            64, 130, f"Total: {len(self.game_ref.game_objects['switch'])}", 7)
        pass

    def update(self):
        pass
