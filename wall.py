import pygame
from window import Window


class Wall:
    def __init__(self, position):
        self.position = position

    def draw(self):
        pygame.draw.rect(Window.surface, (255, 0, 0), (0, 0, 10, 10))