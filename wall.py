import pygame

from engine.camera import Camera
from engine.vector2 import Vector2
from engine.rect import Rect

from spritesheet import SpriteSheet
from tower import Tower


SHEET_PATH = "sprites/walls.png"

class Wall(Tower):

    sprite_sheet: SpriteSheet

    def __init_subclass__(self) -> None:
        self.sprite_sheet = SpriteSheet(SHEET_PATH, (17, 1))

    def draw(self) -> None:
        Camera.draw_image(self.sprite_sheet.get_sprite_at((16, 0)), Rect(self.position.x + 0.5, self.position.y + 0.5, 1, 1))
    
    def draw_icon(self, rect, surface) -> None:
        surface.blit(pygame.transform.scale(self.sprite_sheet.get_sprite_at((16, 0)), rect.get_size().get_rounded_tuple()), rect.get_bottom_left().get_rounded_tuple())

