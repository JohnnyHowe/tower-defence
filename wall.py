import pygame
from window import Window
from spritesheet import SpriteSheet

SHEET_PATH = "sprites/walls.png"

SPRITE_POSITIONS = [
    # Dot
    (0, 0, 0, 0),
    # Ends
    (1, 0, 0, 0),
    (0, 0, 0, 1),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    # Pipes
    (1, 1, 0, 0),
    (0, 0, 1, 1),
    # T
    (0, 1, 1, 1),
    (1, 1, 1, 0),
    (1, 0, 1, 1),
    (1, 1, 0, 1),
    # All
    (1, 1, 1, 1),
    # Corners
    (1, 0, 1, 0),
    (1, 0, 0, 1),
    (0, 1, 0, 1),
    (0, 1, 1, 0)
]


class Wall:
    def __init__(self, position):
        self.position = position
        self.sprite_sheet = SpriteSheet(SHEET_PATH, (16, 1))
    
    def get_image(self, board):
        left = not board.is_empty((self.position[0] - 1, self.position[1]))
        right = not board.is_empty((self.position[0] + 1, self.position[1]))
        up = not board.is_empty((self.position[0], self.position[1] - 1))
        down = not board.is_empty((self.position[0], self.position[1] + 1))
        key = (int(up), int(down), int(left), int(right))

        return self.sprite_sheet.get_sprite_at((SPRITE_POSITIONS.index(key), 0))