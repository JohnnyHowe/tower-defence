import pygame
import math

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
        self.time_to_fire = 1 / self.fire_rate

    def get_icon(self):
        surf = pygame.Surface(self.sprite_sheet.sprite_size, pygame.SRCALPHA)
        surf.blit(self.sprite_sheet.get_sprite_at((0, 0)), (0, 0))
        surf.blit(self.sprite_sheet.get_sprite_at((1, 0)), (0, 0))
        return surf

    def draw(self):
        Camera.draw_image(self.sprite_sheet.get_sprite_at((0, 0)), self.position + (1, 1))
        Camera.draw_image(self.sprite_sheet.get_sprite_at((1, 0)), self.position + (1, 1), self.rotation)

    def update(self, first_enemy):
        enemy_position = first_enemy.get_game_position()
        dp = self.position[0] - enemy_position[0], self.position[1] - enemy_position[1] 
        self.rotation = math.atan2(dp[1], dp[0]) + math.pi / 2

        self.time_to_fire -= Clock.dt
        if self.time_to_fire < 0:
            self.shoot()
            self.time_to_fire += 1 / self.fire_rate

    def shoot(self):
        self.projectile_list.append(MachineGunBullet(self.position, self.rotation))
