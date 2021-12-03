import math

from camera import Camera
from clock import Clock

from a_projectile import AProjectile
from spritesheet import SpriteSheet

from engine_math import Vector2, Rect


SHEET_PATH = "sprites/machine_gun.png"

class MachineGunBullet(AProjectile):

    speed = 20

    def __init__(self, position: Vector2, angle: float):
        self.position = position
        self.angle = angle
        self.gradient = get_gradient(angle)
        self.sprite_sheet = SpriteSheet(SHEET_PATH, (3, 1))

    def draw(self):
        size = 1
        rect = Rect(self.position.x, self.position.y, size, size)
        Camera.draw_image(self.sprite_sheet.get_sprite_at((2, 0)), rect, self.angle)

    def update(self):
        self.position.x += self.gradient.x * self.speed * Clock.dt
        self.position.y += self.gradient.y * self.speed * Clock.dt

    def is_expired(self):
        return False


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

    return Vector2(-x, y)
