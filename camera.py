import math


class Camera:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0

    def update(self, target_x, target_y):
        self.x = math.floor(target_x / 256) * 256
        self.y = math.floor(target_y / 128) * 128
