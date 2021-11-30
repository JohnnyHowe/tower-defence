import pygame
from tower import Tower
from spritesheet import SpriteSheet


SHEET_PATH = "sprites/machine_gun.png"

class MachineGun(Tower):
    def __init__(self, position):
        super().__init__(position)
        self.sprite_sheet = SpriteSheet(SHEET_PATH, (3, 1))

    def get_image(self, board):
        surf = pygame.Surface(self.sprite_sheet.sprite_size, pygame.SRCALPHA)
        surf.blit(self.sprite_sheet.get_sprite_at((0, 0)), (0, 0))
        surf.blit(self.sprite_sheet.get_sprite_at((1, 0)), (0, 0))
        return surf
