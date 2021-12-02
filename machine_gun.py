import pygame
import math

from camera import Camera

from tower import Tower
from spritesheet import SpriteSheet


SHEET_PATH = "sprites/machine_gun.png"

class MachineGun(Tower):

    rotation: float

    def __init__(self, position):
        super().__init__(position)
        self.sprite_sheet = SpriteSheet(SHEET_PATH, (3, 1))
        self.rotation = 0

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
