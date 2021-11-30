from spritesheet import SpriteSheet
from tower import Tower

SHEET_PATH = "sprites/walls.png"

class Wall(Tower):
    def __init__(self, position):
        super().__init__(position)
        self.sprite_sheet = SpriteSheet(SHEET_PATH, (17, 1))
    
    def get_image(self, board):
        return self.sprite_sheet.get_sprite_at((16, 0))