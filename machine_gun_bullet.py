import math

from camera import Camera
from clock import Clock

from a_projectile import AProjectile
from spritesheet import SpriteSheet


SHEET_PATH = "sprites/machine_gun.png"

class MachineGunBullet(AProjectile):

    speed = 20

    def __init__(self, position: tuple, angle: float):
        self.position = list(position)
        self.angle = angle
        self.gradient = get_gradient(angle)
        self.sprite_sheet = SpriteSheet(SHEET_PATH, (3, 1))

    def draw(self):
        # Camera.draw_rect((0, 0, 0), self.position + [0.1, 0.1])
        Camera.draw_image(self.sprite_sheet.get_sprite_at((2, 0)), self.position + [1, 1], self.angle)

    def update(self):
        self.position[0] += self.gradient[0] * self.speed * Clock.dt
        self.position[1] += self.gradient[1] * self.speed * Clock.dt


def get_gradient(angle):
    # don't judge me too bad, i took this from old code
    angle = angle * 180 / math.pi
    while angle > 360:
        angle -= 360
    while angle < 0:
        angle += 360

    if angle > 270:
        c = 3
        angle -= 270
    elif angle > 180:
        c = 2
        angle -= 180
    elif angle > 90:
        c = 1
        angle -= 90
    else:
        c = 0

    x = angle / 90
    y = 1 - x

    if c == 1:
        y, x = -x, y
    if c == 2:
        x = -x
        y = -y
    if c == 3:
        y, x = x, -y

    return -x, y
