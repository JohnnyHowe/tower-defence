import pygame


class _Window:
    def __init__(self):
        self.size = (500, 500)
        self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)

    def update_size(self, new_size):
        self.size = new_size
        self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)


Window = _Window()