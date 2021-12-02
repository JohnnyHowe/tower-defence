from camera import Camera

from spritesheet import SpriteSheet
from tower import Tower

SHEET_PATH = "sprites/walls.png"

class Wall(Tower):

    def __init_subclass__(self):
        self.sprite_sheet = SpriteSheet(SHEET_PATH, (17, 1))

    def draw(self):
        Camera.draw_image(self.sprite_sheet.get_sprite_at((16, 0)), self.position + (1, 1))
    
    def get_icon(self):
        return self.sprite_sheet.get_sprite_at((16, 0))
