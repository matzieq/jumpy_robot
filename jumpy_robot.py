from camera import Camera
import math
import pyxel

from player import Player
from constants import GRAV


plr = Player()

cam = Camera()


def draw():
    pyxel.cls(0)
    pyxel.bltm(0 - cam.x, 0 - cam.y, 0, 0, 0, 240, 32, 0)
    plr.draw(cam)


def update():
    plr.update()
    cam.update(plr.x, plr.y)

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()


pyxel.init(256, 144, caption="Jump stick robo")
pyxel.load('jumpy_robot.pyxres')
pyxel.run(update, draw)
