from constants import GRAV
import pyxel

from player import Player


plr = Player()
is_pressed = "YES"


def draw():
    pyxel.cls(0)
    pyxel.bltm(0, 0, 0, 0, 0, 32, 32, 0)
    plr.draw()
    pyxel.text(8, 8, is_pressed, 8)


def update():
    global is_pressed
    plr.update()
    if pyxel.btnp(pyxel.KEY_SPACE, 30, 30):
        is_pressed = "YES"
        plr.jump()
    else:
        is_pressed = "NO"
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()


pyxel.init(256, 144, caption="Jumpy robot")
pyxel.load('jumpy_robot.pyxres')
pyxel.run(update, draw)
