import pygame
from window import Window
from spritesheet import SpriteSheet

SHEET_PATH = "sprites/walls.png"


class Wall:
    def __init__(self, position):
        self.position = position
        self.sprite_sheet = SpriteSheet(SHEET_PATH, (16, 1))
    
    def get_image(self, connected_top=False, connected_bottom=False, connected_right=False, connected_left=False):
        return self.sprite_sheet.get_sprite_at((0, 0))