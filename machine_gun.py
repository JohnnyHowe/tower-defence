import pygame
import math

from engine_math import Vector2, Rect

from camera import Camera
from clock import Clock

from tower import Tower
from machine_gun_bullet import MachineGunBullet
from spritesheet import SpriteSheet


SHEET_PATH = "sprites/machine_gun.png"

class MachineGun(Tower):

    rotation: float
    fire_rate = 10

    def __init__(self, position, projectile_list):
        super().__init__(position, projectile_list)
        self.sprite_sheet = SpriteSheet(SHEET_PATH, (3, 1))
        self.rotation = 0
        self.time_to_fire = 0 

    def draw_icon(self, rect, surface):
        surface.blit(pygame.transform.scale(self.sprite_sheet.get_sprite_at((0, 0)), rect.get_size().get_rounded_tuple()), rect.get_bottom_left().get_rounded_tuple())
        surface.blit(pygame.transform.scale(self.sprite_sheet.get_sprite_at((1, 0)), rect.get_size().get_rounded_tuple()), rect.get_bottom_left().get_rounded_tuple())

    def draw(self):
        Camera.draw_image(self.sprite_sheet.get_sprite_at((0, 0)), Rect(self.position.x + 0.5, self.position.y + 0.5, 1, 1))
        Camera.draw_image(self.sprite_sheet.get_sprite_at((1, 0)), Rect(self.position.x + 0.5, self.position.y + 0.5, 1, 1), self.rotation)

    def update(self, first_enemy):
        enemy_position = first_enemy.get_position()
        dp = (self.position + Vector2(0.5, 0.5)) - enemy_position
        self.rotation = math.atan2(dp.y, dp.x) + math.pi / 2

        self.time_to_fire -= Clock.dt
        if self.time_to_fire < 0:
            self.shoot()
            self.time_to_fire += 1 / self.fire_rate

    def shoot(self):
        self.projectile_list.append(MachineGunBullet(self.position + Vector2(0.5, 0.5), self.rotation))
