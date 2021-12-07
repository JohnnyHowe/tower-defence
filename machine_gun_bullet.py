import math

from engine.camera import Camera
from engine.clock import Clock

from a_projectile import AProjectile
from spritesheet import SpriteSheet

from engine.vector2 import Vector2
from engine.rect import Rect


SHEET_PATH = "sprites/machine_gun.png"

class MachineGunBullet(AProjectile):

    speed = 20
    damage = 1
    has_hit = False

    def __init__(self, position: Vector2, angle: float):
        self.position = position
        self.angle = angle
        self.gradient = get_gradient(angle)
        self.sprite_sheet = SpriteSheet(SHEET_PATH, (3, 1))

    def draw(self):
        rect = self.get_rect(1) 
        Camera.draw_image(self.sprite_sheet.get_sprite_at((2, 0)), rect, self.angle)

    def update(self):
        self.position.x += self.gradient.x * self.speed * Clock.dt
        self.position.y += self.gradient.y * self.speed * Clock.dt

    def is_expired(self):
        return self.has_hit

    def get_rect(self, size=0.5):
        return Rect(self.position.x, self.position.y, size, size)

    def get_damage(self):
        return self.damage

    def on_hit(self):
        self.has_hit = True


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
